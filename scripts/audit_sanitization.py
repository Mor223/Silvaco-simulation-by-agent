from __future__ import annotations

import argparse
import re
from pathlib import Path

RUNTIME_SUFFIXES = {".str", ".log", ".out", ".plt", ".set", ".history", ".dat", ".csv", ".png"}
PY_CACHE_SUFFIXES = {".pyc", ".pyo"}
BINARY_SUFFIXES = {".zip", ".pyd", ".dll", ".exe", ".obj", ".lib", ".bin", ".pack", ".idx"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "dist", "build"}
SKIP_NAMES = {"audit_sanitization.py", "audit_portability.py"}


def should_skip_path(path: Path) -> bool:
    return bool(set(path.parts) & SKIP_DIRS)


def is_pyc_like(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() in PY_CACHE_SUFFIXES or ".pyc." in name or name.endswith(".pyc")


def is_binary_like(path: Path) -> bool:
    return path.suffix.lower() in BINARY_SUFFIXES or is_pyc_like(path)


def text_issues(path: Path, text: str) -> list[str]:
    if path.name in SKIP_NAMES:
        return []
    issues: list[str] = []
    if re.search(r"\b[A-Za-z]:[\\/][^\s`'\"<>)]*", text):
        issues.append("drive-letter absolute path")
    sensitive_tokens = [
        "".join(["D", ":", "\\", "silvaco"]),
        "".join(["E", ":", "\\", "Software", "\\", "sedatools"]),
        "".join(["C", ":", "\\", "Temp"]),
        "".join(["C", ":", "\\", "Users"]),
        "_".join(["LM", "LICENSE", "FILE"]),
        "_".join(["SFLM", "SERVERS"]),
        "license server",
    ]
    lowered = text.lower()
    for token in sensitive_tokens:
        if token.lower() in lowered:
            issues.append(f"sensitive token: {token}")
    if re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text):
        issues.append("possible IP address")
    if re.search(r"\b[0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5}\b", text):
        issues.append("possible MAC address")
    return issues


def audit(root: Path) -> list[tuple[Path, str]]:
    findings: list[tuple[Path, str]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if should_skip_path(rel):
            continue
        if path.is_dir():
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
        for issue in text_issues(path, text):
            findings.append((rel, issue))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an exported tree for local paths, license hints, caches, and runtime outputs.")
    parser.add_argument("root", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    findings = audit(args.root)
    if findings:
        lines = ["# Sanitization Issues", ""]
        lines.extend(f"- `{path}`: {issue}" for path, issue in findings)
        report = args.report or args.root.parent / "sanitization_issues.md"
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"FAIL: {len(findings)} sanitization issue(s). Report: {report}")
        return 2
    print("PASS: sanitization audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
