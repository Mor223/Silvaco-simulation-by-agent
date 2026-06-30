from __future__ import annotations

import argparse
import re
from pathlib import Path

RUNTIME_SUFFIXES = {".str", ".log", ".out", ".plt", ".set", ".history", ".dat", ".csv", ".png"}
PY_CACHE_SUFFIXES = {".pyc", ".pyo"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "dist", "build"}
FORBIDDEN_DIRS = {"archive", "runs", "results", "raw_examples", "external_examples", "local_examples"}
FORBIDDEN_FILES = {"run_silvaco.py", "prepare_manual_run.py", "collect_results.py", "parse_iv.py", "plot_iv.py", "probe_deckbuild_batch.py"}
BINARY_SUFFIXES = {".zip", ".pyd", ".dll", ".exe", ".obj", ".lib", ".bin", ".pack", ".idx"}
SKIP_NAMES = {"audit_sanitization.py", "audit_portability.py"}


def should_skip_path(path: Path) -> bool:
    return bool(set(path.parts) & SKIP_DIRS)


def is_pyc_like(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() in PY_CACHE_SUFFIXES or ".pyc." in name or name.endswith(".pyc")


def is_binary_like(path: Path) -> bool:
    return path.suffix.lower() in BINARY_SUFFIXES or is_pyc_like(path)


def portability_text_issues(path: Path, text: str) -> list[str]:
    if path.name in SKIP_NAMES:
        return []
    issues: list[str] = []
    if re.search(r"\b[A-Za-z]:[\\/][^\s`'\"<>)]*", text):
        issues.append("absolute local path")
    lowered = text.lower()
    for token in ["deckbuild.exe", "atlas.exe", "devedit.exe", "tonyplot.exe", "guiappstarter.exe"]:
        if token in lowered:
            issues.append(f"direct simulator executable reference: {token}")
    if "subprocess" in lowered and any(token in lowered for token in ["deckbuild", "atlas", "devedit", "athena"]):
        issues.append("subprocess-based simulator launch reference")
    if "run_silvaco" in lowered or "prepare_manual_run" in lowered:
        issues.append("legacy runtime workflow reference")
    for token in ["_".join(["LM", "LICENSE", "FILE"]), "_".join(["SFLM", "SERVERS"]), "license server"]:
        if token.lower() in lowered:
            issues.append(f"license reference: {token}")
    return issues


def audit(root: Path) -> list[tuple[Path, str]]:
    findings: list[tuple[Path, str]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if should_skip_path(rel):
            continue
        if path.is_dir():
            continue
        if set(rel.parts) & FORBIDDEN_DIRS:
            findings.append((rel, "forbidden runtime/local directory"))
            continue
        if path.name in FORBIDDEN_FILES:
            findings.append((rel, "forbidden legacy runtime script"))
            continue
        if is_pyc_like(path):
            findings.append((rel, "Python bytecode/cache file"))
            continue
        if path.suffix.lower() in RUNTIME_SUFFIXES:
            findings.append((rel, f"runtime output suffix: {path.suffix}"))
            continue
        if is_binary_like(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError) as exc:
            findings.append((rel, f"cannot read as text: {exc}"))
            continue
        for issue in portability_text_issues(path, text):
            findings.append((rel, issue))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit exported package portability.")
    parser.add_argument("root", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    findings = audit(args.root)
    if findings:
        lines = ["# Portability Issues", ""]
        lines.extend(f"- `{path}`: {issue}" for path, issue in findings)
        report = args.report or args.root.parent / "portability_issues.md"
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"FAIL: {len(findings)} portability issue(s). Report: {report}")
        return 2
    print("PASS: portability audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
