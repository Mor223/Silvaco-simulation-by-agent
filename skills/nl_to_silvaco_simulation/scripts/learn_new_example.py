from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from scan_silvaco_examples import command_snippets, summarize, tags_from_map, MODULE_TAGS, DEVICE_TAGS, SIM_TAGS

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "silvaco_examples_index.public.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_index() -> dict:
    if INDEX_PATH.is_file():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {"schema": "silvaco_examples_index.public.v1", "records": [], "statistics": {}}


def safe_source_path(case_id: str, filename: str) -> str:
    return f"<USER_LEARNED_EXAMPLE>/{case_id}/{filename}"


def is_verified(value: str) -> bool | None:
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def record_for(path: Path, case_id: str, verified: str, purpose: str) -> dict:
    text = read_text(path)
    lower = text.lower()
    source_path = safe_source_path(case_id, path.name)
    module_tags = tags_from_map(text, source_path, MODULE_TAGS)
    if "go devedit" in lower and "go atlas" in lower:
        module_tags.append("devedit_atlas_flow")
    if "go athena" in lower and "go atlas" in lower:
        module_tags.append("athena_atlas_flow")
    if "go athena" in lower and "structure" in lower:
        module_tags.append("process_device_flow")
    if "go atlas" in lower and "mesh infile" not in lower and any(k in lower for k in ["x.mesh", "region", "doping"]):
        module_tags.append("atlas_direct")
    module_tags = sorted(set(module_tags))
    device_tags = tags_from_map(text, source_path + " " + purpose, DEVICE_TAGS) or ["generic"]
    sim_tags = tags_from_map(text, source_path + " " + purpose, SIM_TAGS)
    syntax_tags, snippets = command_snippets(text)
    keywords = sorted(set(module_tags + device_tags + sim_tags + syntax_tags))
    return {
        "case_id": case_id,
        "source_path": source_path,
        "source": "User-provided learned pattern summary; original deck not redistributed",
        "source_type": "user_learned_example_summary",
        "module_tags": module_tags,
        "device_tags": sorted(set(device_tags)),
        "simulation_tags": sorted(set(sim_tags)),
        "syntax_tags": syntax_tags,
        "keywords": keywords,
        "short_summary": summarize(text, module_tags, sorted(set(device_tags)), sim_tags),
        "key_commands": snippets,
        "reusable_patterns": [],
        "risk_notes": ["User must confirm all numeric values, syntax applicability, material assumptions, and model choices before reuse."],
        "whether_user_verified": is_verified(verified),
        "user_verified": is_verified(verified),
        "verified_status": verified,
        "purpose": purpose,
        "learned_case_id": case_id,
    }


def update_stats(index: dict) -> None:
    stats = {"module": {}, "device": {}, "simulation": {}, "syntax": {}}
    for rec in index.get("records", []):
        for key, field in [("module", "module_tags"), ("device", "device_tags"), ("simulation", "simulation_tags"), ("syntax", "syntax_tags")]:
            for tag in rec.get(field, []):
                stats[key][tag] = stats[key].get(tag, 0) + 1
    index["statistics"] = stats
    index["indexed_text_files"] = len(index.get("records", []))


def commands(rec: dict) -> list[str]:
    return rec.get("key_commands") or rec.get("command_snippets") or []


def write_index_md(index: dict) -> None:
    lines = ["# Silvaco Examples Index", "", f"Indexed text files: {index.get('indexed_text_files', 0)}", "", "## Learned Examples"]
    for rec in [r for r in index.get("records", []) if r.get("learned_case_id")]:
        lines.extend([
            f"### `{rec['learned_case_id']}`",
            f"- Source path: `{rec.get('source_path', '<USER_LEARNED_EXAMPLE>')}`",
            f"- Verified: `{rec.get('verified_status')}`",
            f"- Purpose: {rec.get('purpose')}",
            f"- Tags: {', '.join(rec.get('keywords', [])[:20])}",
            f"- Commands: {'; '.join(commands(rec)[:8])}",
            "",
        ])
    base = ROOT / "docs" / "silvaco_examples_index.md"
    base.write_text("\n".join(lines), encoding="utf-8")


def append_docs(rec: dict) -> None:
    verified_note = "user verified" if rec.get("whether_user_verified") is True else "not user verified or unknown; syntax is reference only"
    note = f"\n\n## Learned example: {rec['learned_case_id']}\n\n- Source path: `{rec['source_path']}`\n- Verification: {verified_note}\n- Purpose: {rec['purpose']}\n- Tags: {', '.join(rec.get('keywords', [])[:20])}\n- Reusable command forms: {'; '.join(commands(rec)[:8])}\n"
    for doc in ["docs/silvaco_case_knowledge.md", "docs/syntax_rules.md", "docs/model_recommendation_rules.md", "docs/nl_request_to_examples.md"]:
        p = ROOT / doc
        p.write_text(p.read_text(encoding="utf-8", errors="ignore") + note, encoding="utf-8")


def write_template_draft(rec: dict, case_id: str) -> Path | None:
    category = "atlas" if "atlas" in rec.get("module_tags", []) else (rec.get("module_tags") or ["generic"])[0]
    out_dir = ROOT / "templates" / "learned"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{case_id}_{category}.in.j2"
    lines = [
        f"# Learned template draft for {case_id}",
        "# This is parameterized from command forms only; it is not a copy of the original example.",
        "# User must fill and confirm all parameters before rendering a final deck.",
        "",
    ]
    for snippet in commands(rec)[:20]:
        sanitized = re.sub(r"[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?", "{{ value }}", snippet, flags=re.IGNORECASE)
        lines.append("# pattern: " + sanitized)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def rel_or_placeholder(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return "<USER_PROVIDED_EXTERNAL_PATH>"


def write_report(rec: dict, template: Path | None) -> Path:
    report_dir = ROOT / "docs" / "learning_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = report_dir / f"{rec['learned_case_id']}_learning_report.md"
    lines = [
        f"# Learning Report: {rec['learned_case_id']}",
        "",
        f"- Example source path: `{rec['source_path']}`",
        f"- User verified: `{rec.get('verified_status')}`",
        f"- Purpose: {rec.get('purpose')}",
        f"- Module tags: {', '.join(rec.get('module_tags', []))}",
        f"- Device tags: {', '.join(rec.get('device_tags', []))}",
        f"- Simulation tags: {', '.join(rec.get('simulation_tags', []))}",
        f"- Syntax tags: {', '.join(rec.get('syntax_tags', []))}",
        "",
        "## Reusable command forms",
    ]
    lines.extend(f"- `{s}`" for s in commands(rec)[:20])
    lines.extend(["", "## Updated files", "- `data/silvaco_examples_index.public.json`", "- `docs/silvaco_examples_index.md`", "- `docs/syntax_rules.md`", "- `docs/silvaco_case_knowledge.md`", "- `docs/model_recommendation_rules.md`", "- `docs/nl_request_to_examples.md`"])
    if template:
        lines.append(f"- `{rel_or_placeholder(template)}`")
    lines.extend(["", "## Remaining user confirmations", "Example numeric values, geometry, material assumptions, models, optical settings, and sweep settings must still be confirmed by the user before final deck generation."])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def sync_skill_refs() -> None:
    refs = ROOT / "skills" / "nl_to_silvaco_simulation" / "references"
    refs.mkdir(parents=True, exist_ok=True)
    for name in ["syntax_rules.md", "silvaco_case_knowledge.md", "user_questionnaire.md"]:
        src = ROOT / "docs" / name
        if src.is_file():
            (refs / name).write_text(src.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Learn compact syntax patterns from a user-provided Silvaco example without running Silvaco.")
    parser.add_argument("--example", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--verified", choices=["true", "false", "unknown"], required=True)
    parser.add_argument("--purpose", required=True)
    args = parser.parse_args()
    path = Path(args.example)
    if not path.is_file():
        raise SystemExit(f"Example file not found: <USER_PROVIDED_EXTERNAL_PATH>")
    index = load_index()
    rec = record_for(path, args.case_id, args.verified, args.purpose)
    index.setdefault("records", []).append(rec)
    update_stats(index)
    INDEX_PATH.parent.mkdir(exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    write_index_md(index)
    append_docs(rec)
    template = write_template_draft(rec, args.case_id)
    report = write_report(rec, template)
    sync_skill_refs()
    print(f"Wrote public index: {INDEX_PATH}")
    print(f"Wrote learning report: {report}")
    if template:
        print(f"Wrote template draft: {template}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
