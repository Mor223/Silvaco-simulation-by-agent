from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

TEXT_EXTS = {".in", ".cmd", ".deck"}
SKIP_EXTS = {".str", ".plt", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".dll", ".exe", ".lib", ".obj", ".zip", ".gz", ".tar"}
MAX_SIZE = 2_000_000

MODULE_TAGS = {
    "devedit": ["go devedit", "devedit>"],
    "athena": ["go athena", "line x", "line y", "implant", "diffuse", "oxidize"],
    "atlas": ["go atlas", "models", "solve", "mesh infile"],
    "luminous": ["luminous", "beam", "wavelength", "photo"],
    "tonyplot": ["tonyplot"],
    "victory": ["victory", "go victory"],
}
DEVICE_TAGS = {
    "pn_diode": ["pn", "diode", "p-n"],
    "pin_diode": ["pin", "intrinsic"],
    "schottky": ["schottky"],
    "mos": ["mos", "oxide"],
    "mosfet": ["mosfet", "nmos", "pmos"],
    "bjt": ["bjt", "bipolar"],
    "jfet": ["jfet"],
    "photodiode": ["photodiode", "photo diode", "photocurrent"],
    "solar_cell": ["solar", "cell"],
    "led": ["led"],
    "laser": ["laser", "vcsel"],
    "sige": ["sige", "si_ge"],
    "ge": ["germanium", " ge ", "ge."],
    "iii_v": ["gaas", "inp", "ingaas", "algaas", "iii-v"],
    "gan": ["gan", "algan"],
    "sic": ["sic", "silicon carbide"],
    "oxide": ["oxide", "sio2"],
}
SIM_TAGS = {
    "iv": [" i-v", "iv", "vstep", "vfinal", "solve v"],
    "cv": [" cv", "ac", "capacitance"],
    "transient": ["transient", "ramptime", "tstep"],
    "breakdown": ["breakdown", "impact", "avalanche"],
    "leakage": ["leakage"],
    "optical": ["optical", "beam", "wavelength"],
    "luminous": ["luminous"],
    "responsivity": ["responsivity"],
    "photocurrent": ["photocurrent", "photo current"],
    "mobility": ["mobility", "conmob", "fldmob", "cvt"],
    "process": ["implant", "diffuse", "oxidize", "deposit", "etch"],
    "implantation": ["implant"],
    "oxidation": ["oxidize", "oxidation"],
    "diffusion": ["diffuse", "diffusion"],
    "etch": ["etch"],
    "deposition": ["deposit", "depo"],
}
SYNTAX_TAGS = ["mesh", "region", "line", "init", "implant", "diffuse", "electrode", "contact", "material", "doping", "impurity", "models", "method", "solve", "log", "extract", "save", "struct_out", "mesh_infile"]
COMMAND_PATTERNS = {
    "mesh": r"^\s*(mesh|x\.mesh|y\.mesh)\b.*",
    "region": r"^\s*region\b.*",
    "line": r"^\s*line\s+[xy]\b.*",
    "init": r"^\s*init\b.*",
    "implant": r"^\s*implant\b.*",
    "diffuse": r"^\s*diffuse\b.*",
    "electrode": r"^\s*electrode\b.*",
    "contact": r"^\s*contact\b.*",
    "material": r"^\s*material\b.*",
    "doping": r"^\s*doping\b.*",
    "impurity": r"^\s*impurity\b.*",
    "models": r"^\s*models\b.*",
    "method": r"^\s*method\b.*",
    "solve": r"^\s*solve\b.*",
    "log": r"^\s*log\b.*",
    "extract": r"^\s*extract\b.*",
    "save": r"^\s*save\b.*",
    "struct_out": r"^\s*(struct\s+outf|structure\s+outfile|structure\s+outf)\b.*",
    "mesh_infile": r"^\s*mesh\s+infile\b.*",
}


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        try:
            return path.read_text(encoding="latin-1", errors="ignore")
        except Exception:
            return None


def tags_from_map(text: str, rel: str, mapping: dict[str, list[str]]) -> list[str]:
    hay = f" {rel.lower()} {text.lower()} "
    return sorted(tag for tag, keys in mapping.items() if any(k in hay for k in keys))


def command_snippets(text: str) -> tuple[list[str], list[str]]:
    snippets: list[str] = []
    syntax_tags: list[str] = []
    lines = text.splitlines()
    for tag, pattern in COMMAND_PATTERNS.items():
        rx = re.compile(pattern, re.IGNORECASE)
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("!"):
                continue
            if rx.match(stripped):
                syntax_tags.append(tag)
                if len(snippets) < 18:
                    snippets.append(stripped[:160])
                break
    return sorted(set(syntax_tags)), snippets


def summarize(text: str, module_tags: list[str], device_tags: list[str], sim_tags: list[str]) -> str:
    parts = []
    if module_tags:
        parts.append("modules=" + ",".join(module_tags[:4]))
    if device_tags:
        parts.append("devices=" + ",".join(device_tags[:4]))
    if sim_tags:
        parts.append("sim=" + ",".join(sim_tags[:4]))
    return "; ".join(parts) if parts else "text file with no primary Silvaco module tag"


def scan(root: Path) -> dict[str, Any]:
    records = []
    counters = {"module": Counter(), "device": Counter(), "simulation": Counter(), "syntax": Counter()}
    all_files = 0
    text_files = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        all_files += 1
        ext = path.suffix.lower()
        if ext in SKIP_EXTS or ext not in TEXT_EXTS:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > MAX_SIZE:
            continue
        text = read_text(path)
        if text is None:
            continue
        text_files += 1
        rel = str(path.relative_to(root))
        lower = text.lower()
        module_tags = tags_from_map(text, rel, MODULE_TAGS)
        if "go devedit" in lower and "go atlas" in lower:
            module_tags.append("devedit_atlas_flow")
        if "go athena" in lower and "go atlas" in lower:
            module_tags.append("athena_atlas_flow")
        if "go athena" in lower and "structure" in lower and "go atlas" not in lower:
            module_tags.append("process_device_flow")
        if "go atlas" in lower and "mesh infile" not in lower and any(k in lower for k in ["x.mesh", "region", "doping"]):
            module_tags.append("atlas_direct")
        module_tags = sorted(set(module_tags))
        device_tags = tags_from_map(text, rel, DEVICE_TAGS) or ["generic"]
        sim_tags = tags_from_map(text, rel, SIM_TAGS)
        syntax_tags, snippets = command_snippets(text)
        for group, tags in [("module", module_tags), ("device", device_tags), ("simulation", sim_tags), ("syntax", syntax_tags)]:
            counters[group].update(tags)
        records.append({
            "case_id": path.stem,
            "source_path": "<SILVACO_EXAMPLES_ROOT>/" + rel.replace("\\", "/"),
            "source": "Silvaco example pattern summary; original example not redistributed",
            "source_type": "official_example_summary",
            "module_tags": module_tags,
            "device_tags": sorted(set(device_tags)),
            "simulation_tags": sorted(set(sim_tags)),
            "syntax_tags": syntax_tags,
            "keywords": sorted(set(module_tags + device_tags + sim_tags + syntax_tags)),
            "short_summary": summarize(text, module_tags, device_tags, sim_tags),
            "key_commands": snippets,
            "reusable_patterns": [],
            "risk_notes": ["Summary only; confirm syntax against the local installed version before final use."],
            "whether_user_verified": False,
        })
    return {
        "examples_root": str(root),
        "scanned_at": datetime.now().isoformat(timespec="seconds"),
        "total_files_seen": all_files,
        "indexed_text_files": text_files,
        "records": records,
        "statistics": {k: dict(v.most_common()) for k, v in counters.items()},
    }


def write_outputs(index: dict[str, Any]) -> None:
    data_dir = Path("data")
    docs_dir = Path("docs")
    data_dir.mkdir(exist_ok=True)
    docs_dir.mkdir(exist_ok=True)
    public_index = {
        "schema": "silvaco_examples_index.public.v1",
        "copyright_note": "Compact syntax and case-pattern summaries only. Original commercial examples are not redistributed.",
        "source_root": "<SILVACO_EXAMPLES_ROOT>",
        "scanned_at": index.get("scanned_at"),
        "total_files_seen": index.get("total_files_seen", 0),
        "indexed_text_files": index.get("indexed_text_files", 0),
        "records": index.get("records", []),
        "statistics": index.get("statistics", {}),
    }
    (data_dir / "silvaco_examples_index.public.json").write_text(json.dumps(public_index, indent=2, ensure_ascii=False), encoding="utf-8")
    records = public_index["records"]
    lines = [
        "# Silvaco Examples Index",
        "",
        "This is a sanitized public summary. Original examples and local paths are not redistributed.",
        f"Total files seen: {public_index['total_files_seen']}",
        f"Indexed deck files: {public_index['indexed_text_files']}",
        "",
        "## Statistics",
        "",
    ]
    for group, stats in public_index["statistics"].items():
        lines.append(f"### {group}")
        for tag, count in sorted(stats.items(), key=lambda x: (-x[1], x[0]))[:40]:
            lines.append(f"- {tag}: {count}")
        lines.append("")
    lines.append("## Representative Indexed Files")
    for rec in records[:300]:
        lines.extend([
            f"### `{rec.get('source_path', '<SILVACO_EXAMPLES_ROOT>/unknown')}`",
            f"- Tags: {', '.join(rec.get('keywords', [])[:20])}",
            f"- Summary: {rec.get('short_summary', '')}",
            f"- Commands: {', '.join(rec.get('key_commands', [])[:6])}",
            "",
        ])
    (docs_dir / "silvaco_examples_index.md").write_text("\n".join(lines), encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="Scan local Silvaco examples into compact indexes without running Silvaco.")
    parser.add_argument("--examples-root", required=True)
    args = parser.parse_args()
    root = Path(args.examples_root)
    if not root.is_dir():
        raise SystemExit(f"Examples root not found: {root}")
    index = scan(root)
    write_outputs(index)
    print("Examples root: <SILVACO_EXAMPLES_ROOT>")
    print(f"Total files seen: {index['total_files_seen']}")
    print(f"Indexed deck files: {index['indexed_text_files']}")
    print("Wrote data/silvaco_examples_index.public.json")
    print("Wrote docs/silvaco_examples_index.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
