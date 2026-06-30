from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERROR_PATTERNS = [
    "command error", "error", "warning", "cannot", "can't", "file not found", "no such", "unknown", "failed", "convergence", "singular", "license", "sflm"
]



def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return "<USER_PROVIDED_EXTERNAL_PATH>"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def classify_stage(context: str) -> str:
    lower = context.lower()
    if "devedit" in lower:
        return "DevEdit"
    if "athena" in lower:
        return "ATHENA"
    if "mesh infile" in lower:
        return "ATLAS mesh infile"
    if "contact" in lower or "electrode" in lower or "no such electrode" in lower:
        return "ATLAS contact/electrode"
    if "models" in lower:
        return "ATLAS models"
    if "solve init" in lower:
        return "ATLAS solve init"
    if "log outf" in lower or "vstep" in lower or "vfinal" in lower:
        return "ATLAS log/scan"
    if "luminous" in lower or "beam" in lower or "wavelength" in lower:
        return "Luminous/optical"
    if "file not found" in lower or "error on open" in lower:
        return "file path / temporary file"
    if "convergence" in lower or "singular" in lower:
        return "convergence"
    if "license" in lower or "sflm" in lower:
        return "license"
    return "unknown"


def first_error(log_text: str) -> tuple[int, str, str]:
    lines = log_text.splitlines()
    for idx, line in enumerate(lines):
        lower = line.lower()
        if any(p in lower for p in ERROR_PATTERNS):
            start = max(0, idx - 12)
            end = min(len(lines), idx + 13)
            context = "\n".join(lines[start:end])
            return idx + 1, line.strip(), context
    return 0, "No explicit error/warning keyword found", "\n".join(lines[:40])


def trigger_command(deck_text: str, error_line: str, context: str) -> str:
    lower_context = context.lower()
    deck_lines = [l.strip() for l in deck_text.splitlines() if l.strip()]
    candidates = []
    for line in deck_lines:
        low = line.lower()
        if any(k in lower_context for k in ["mesh infile", "file not found", "error on open"]) and "mesh infile" in low:
            candidates.append(line)
        if "no such electrode" in lower_context and "solve" in low:
            candidates.append(line)
        if "unknown" in lower_context or "command error" in lower_context:
            token = error_line.split()[0].lower() if error_line.split() else ""
            if token and token in low:
                candidates.append(line)
        if "log" in lower_context and "log outf" in low:
            candidates.append(line)
    return candidates[0] if candidates else "Could not statically identify trigger command"


def example_hints(stage: str, deck_text: str) -> list[str]:
    query = []
    low = deck_text.lower()
    if "pn" in low or "diode" in low:
        query.append("pn_diode")
    if stage.startswith("DevEdit"):
        query.extend(["devedit", "devedit_atlas_flow"])
    if stage.startswith("ATHENA"):
        query.extend(["athena", "process_device_flow"])
    if stage.startswith("ATLAS"):
        query.extend(["atlas", "mesh_infile", "solve", "log"])
    if "luminous" in stage.lower():
        query.extend(["luminous", "optical"])
    return query or ["atlas", "generic"]


def propose_fix(deck_path: Path, deck_text: str, stage: str, error_line: str, case: str) -> tuple[Path | None, str]:
    proposed_dir = ROOT / "cases" / case / "decks" / "proposed_fix"
    proposed_dir.mkdir(parents=True, exist_ok=True)
    fixed = deck_text
    summary = "No automatic text fix was generated; review the analysis report."
    lower = (error_line + "\n" + deck_text).lower()
    if "imp.refine" in lower and "x=" in lower:
        fixed = re.sub(r"^.*imp\.refine.*x=.*$", "# removed: unsupported imp.refine x= form; confirm local refinement syntax before re-adding", fixed, flags=re.IGNORECASE | re.MULTILINE)
        summary = "Removed unsupported `imp.refine ... x=...` form."
    elif "log outf" in deck_text.lower() and not re.search(r"log\s+outf[\s\S]*?solve\b", deck_text, flags=re.IGNORECASE):
        fixed = re.sub(r"(log\s+outf\s*=\s*[^\n]+)", r"\1\n# TODO: add a user-confirmed solve sweep after log outf", fixed, flags=re.IGNORECASE)
        summary = "Inserted a TODO after `log outf` because no solve follows the log command."
    elif "mesh infile" in lower and ("file not found" in lower or "error on open" in lower):
        summary = "Mesh infile/file-open errors require confirming the first-step `.str` filename and working directory; no safe automatic filename rewrite was made."
    else:
        summary = "No safe automatic rewrite rule matched this error."
    if fixed != deck_text:
        suffix = "02_atlas_simulation_fixed.in" if "go atlas" in deck_text.lower() else ("01_process_athena_fixed.in" if "go athena" in deck_text.lower() else "01_structure_devedit_fixed.in")
        out = proposed_dir / suffix
        out.write_text(fixed, encoding="utf-8")
        return out, summary
    return None, summary


def append_reusable_knowledge(stage: str, error_line: str, fix_summary: str) -> None:
    topic = re.sub(r"[^A-Za-z0-9]+", " ", error_line).strip()[:80] or "Silvaco error pattern"
    block = f"\n\n## {topic}\n\n- Trigger scenario: user-provided Silvaco runtime log.\n- Typical error: `{error_line}`\n- Error stage: {stage}\n- Common cause: inspect deck/log consistency, first-step structure output, electrode names, log/solve ordering, and confirmed syntax.\n- Recommended fix form: {fix_summary}\n- Requires user confirmation: yes, before final deck replacement.\n- Static check rule: add or keep checks when the error is detectable from text.\n"
    for doc in ["docs/troubleshooting.md", "docs/syntax_rules.md", "docs/silvaco_case_knowledge.md"]:
        p = ROOT / doc
        p.write_text(p.read_text(encoding="utf-8", errors="ignore") + block, encoding="utf-8")
    skill = ROOT / "skills" / "nl_to_silvaco_simulation" / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8", errors="ignore") + f"\n\n## Error Pattern: {topic}\n\n- Stage: {stage}\n- Typical error: `{error_line}`\n- Future behavior: use Analyze Error Workflow and do not overwrite original decks.\n", encoding="utf-8")

def sync_skill_refs() -> None:
    refs = ROOT / "skills" / "nl_to_silvaco_simulation" / "references"
    refs.mkdir(parents=True, exist_ok=True)
    for name in ["syntax_rules.md", "silvaco_case_knowledge.md", "user_questionnaire.md"]:
        src = ROOT / "docs" / name
        if src.is_file():
            (refs / name).write_text(src.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze user-provided Silvaco deck/log errors without running Silvaco.")
    parser.add_argument("--case", required=True)
    parser.add_argument("--deck", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--proposed-fix", action="store_true")
    args = parser.parse_args()
    deck_path = Path(args.deck)
    log_path = Path(args.log)
    if not deck_path.is_absolute():
        deck_path = ROOT / deck_path
    if not log_path.is_absolute():
        log_path = ROOT / log_path
    deck_text = read(deck_path)
    log_text = read(log_path)
    line_no, err, context = first_error(log_text)
    stage = classify_stage(context + "\n" + deck_text)
    trigger = trigger_command(deck_text, err, context)
    hints = example_hints(stage, deck_text)
    fix_path = None
    fix_summary = "Proposed fix not requested."
    if args.proposed_fix:
        fix_path, fix_summary = propose_fix(deck_path, deck_text, stage, err, args.case)
    paths = ROOT / "cases" / args.case / "reports"
    paths.mkdir(parents=True, exist_ok=True)
    report = paths / "error_analysis.md"
    lines = [
        f"# Error Analysis: {args.case}", "",
        f"- Deck: `{display_path(deck_path)}`",
        f"- Log: `{display_path(log_path)}`",
        f"- Goal: {args.goal}",
        f"- Error stage: {stage}",
        f"- First explicit error line: {line_no}",
        f"- First explicit error: `{err}`",
        f"- Suspected trigger command: `{trigger}`",
        f"- Example search tags: {', '.join(hints)}",
        "", "## Error Context", "", "```text", context[:4000], "```", "",
        "## Possible Root Cause", "",
        "Review deck/log consistency, command syntax, structure-file names, electrode inheritance, log/solve ordering, and model confirmation.", "",
        "## Recommended Fix", "", fix_summary,
    ]
    if fix_path:
        lines.append(f"\nProposed fix deck: `{display_path(fix_path)}`")
    lines.extend(["", "## User Confirmation Needed", "", "Confirm any changed syntax, filenames, electrode names, model set, and sweep target before replacing the original deck."])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if args.proposed_fix:
        summary = paths / "proposed_fix_summary.md"
        summary.write_text(f"# Proposed Fix Summary\n\n- Change summary: {fix_summary}\n- Proposed file: `{display_path(fix_path) if fix_path else None}`\n- Original deck was not overwritten.\n- User must manually validate with their own tools.\n", encoding="utf-8")
    append_reusable_knowledge(stage, err, fix_summary)
    sync_skill_refs()
    print(f"Wrote error analysis: {report}")
    if fix_path:
        print(f"Wrote proposed fix: {fix_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


