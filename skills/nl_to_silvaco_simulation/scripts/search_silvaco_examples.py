from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_records(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")).get("records", [])


def record_path(rec: dict) -> str:
    return rec.get("source_path") or rec.get("relative_path") or rec.get("path") or "<unknown>"


def record_summary(rec: dict) -> str:
    return rec.get("short_summary") or rec.get("summary") or ""


def record_commands(rec: dict) -> list[str]:
    return rec.get("key_commands") or rec.get("command_snippets") or []


def score_record(rec: dict, terms: list[str], tags: list[str]) -> int:
    hay = " ".join([
        record_path(rec),
        record_summary(rec),
        " ".join(record_commands(rec)),
        " ".join(rec.get("keywords", [])),
    ]).lower()
    score = 0
    for term in terms:
        if term and term.lower() in hay:
            score += 3
    rec_tags = set(rec.get("keywords", [])) | set(rec.get("module_tags", [])) | set(rec.get("device_tags", [])) | set(rec.get("simulation_tags", [])) | set(rec.get("syntax_tags", []))
    for tag in tags:
        if tag in rec_tags:
            score += 5
    return score


def index_path() -> Path:
    public = Path("data/silvaco_examples_index.public.json")
    return public if public.is_file() else Path("data/silvaco_examples_index.json")


def search(query: str | None, tags: str | None, limit: int) -> list[tuple[int, dict]]:
    terms = query.split() if query else []
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    scored = []
    for rec in load_records(index_path()):
        score = score_record(rec, terms, tag_list)
        if score > 0:
            scored.append((score, rec))
    return sorted(scored, key=lambda x: (-x[0], record_path(x[1])))[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Search compact Silvaco example index without printing full examples.")
    parser.add_argument("--query", default=None)
    parser.add_argument("--tags", default=None)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    results = search(args.query, args.tags, args.limit)
    for score, rec in results:
        print(f"score={score} path={record_path(rec)}")
        print(f"  tags={', '.join(rec.get('keywords', [])[:18])}")
        print(f"  summary={record_summary(rec)}")
        print(f"  commands={'; '.join(record_commands(rec)[:5])}")
    print(f"results={len(results)}")
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
