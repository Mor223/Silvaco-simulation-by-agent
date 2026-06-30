from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]


def ensure_case_dirs(case: str) -> dict[str, Path]:
    base = ROOT / "cases" / case
    paths = {
        "base": base,
        "specs": base / "specs",
        "decks": base / "decks",
        "reports": base / "reports",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def render_template(template: str, context: dict[str, Any]) -> str:
    env = Environment(loader=FileSystemLoader(str(ROOT / "templates")), undefined=StrictUndefined, trim_blocks=False, lstrip_blocks=False)
    return env.get_template(template).render(**context)


def confirmed(value: Any) -> bool:
    if isinstance(value, dict):
        if "value" in value:
            return value.get("confirmed_by_user") is True
        return all(confirmed(v) for v in value.values())
    if isinstance(value, list):
        return all(confirmed(v) for v in value)
    return True


def unwrap(value: Any) -> Any:
    if isinstance(value, dict):
        if "value" in value:
            return value["value"]
        return {k: unwrap(v) for k, v in value.items() if k not in {"source", "confirmed_by_user", "reason"}}
    if isinstance(value, list):
        return [unwrap(v) for v in value]
    return value


def require_confirmed(spec: dict[str, Any], label: str) -> None:
    if not confirmed(spec):
        raise ValueError(f"{label} contains unconfirmed parameters; final deck generation is blocked")


def write_report(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def slug_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())
