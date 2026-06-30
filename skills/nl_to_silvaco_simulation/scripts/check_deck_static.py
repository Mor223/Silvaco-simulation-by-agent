from __future__ import annotations

import argparse
import re
from pathlib import Path
from deckgen_common import ROOT, ensure_case_dirs

FORBIDDEN = ["-ascii", "dbascii", "tonyplot"]
COMPLEX_UNCONFIRMED = ["luminous", "beam", "wavelength", "impact", "bbt", "tunnel", "trap"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def has_solve_after_log(text: str) -> bool:
    lower = text.lower()
    idx = lower.find("log outf")
    return idx >= 0 and "solve" in lower[idx:]


def check_devedit(text: str) -> tuple[list[str], list[str]]:
    lower = text.lower()
    errors: list[str] = []
    warnings: list[str] = []
    for token in ["go devedit", "region", "struct outf", "quit"]:
        if token not in lower:
            errors.append(f"missing DevEdit token: {token}")
    if "mesh" not in lower and "constr.mesh" not in lower:
        errors.append("missing DevEdit mesh command")
    if "imp.refine" in lower and "x=" in lower:
        errors.append("forbidden unverified DevEdit syntax: imp.refine x=")
    if "elec.id" in lower or "electrode" in lower:
        warnings.append("DevEdit electrode inheritance into ATLAS cannot be fully verified statically; check electrode names in DeckBuild logs")
    if re.search(r"region\b.*\b(mat=aluminum|material=aluminum|mat=gold|material=gold)", lower) and "elec.id" not in lower:
        warnings.append("metal/contact-like DevEdit region lacks elec.id; ATLAS electrode inheritance may be uncertain")
    return errors, warnings


def check_athena(text: str) -> tuple[list[str], list[str]]:
    lower = text.lower()
    errors: list[str] = []
    warnings: list[str] = []
    for token in ["go athena", "line x", "line y", "init", "structure outfile", "quit"]:
        if token not in lower:
            errors.append(f"missing ATHENA token: {token}")
    if not any(cmd in lower for cmd in ["implant", "diffuse", "etch", "deposit", "oxidize"]):
        warnings.append("no explicit ATHENA process command found")
    return errors, warnings


def check_atlas(text: str, expected_structure: str | None = None, sweep_electrode: str | None = None, allow_direct: bool = False) -> tuple[list[str], list[str]]:
    lower = text.lower()
    errors: list[str] = []
    warnings: list[str] = []
    has_direct_geometry = any(token in lower for token in ["x.mesh", "y.mesh", "region num", "doping uniform"])
    has_mesh_infile = "mesh infile" in lower
    for token in ["go atlas", "models", "method", "solve init", "log outf", "log off", "save outf", "quit"]:
        if token not in lower:
            errors.append(f"missing ATLAS token: {token}")
    if not has_mesh_infile:
        if allow_direct:
            warnings.append("ATLAS direct control baseline detected; this must not replace full DevEdit/ATHENA flow")
        else:
            errors.append("ATLAS full-flow deck must contain mesh infile=<first-step structure>.str")
    if has_direct_geometry and not allow_direct:
        errors.append("ATLAS direct geometry commands appear in a full-flow ATLAS deck; use only for explicit control baseline")
    if not has_solve_after_log(text):
        errors.append("log outf is not followed by a solve command")
    if expected_structure and expected_structure.lower() not in lower:
        errors.append(f"mesh infile does not reference expected structure: {expected_structure}")
    match = re.search(r"solve\s+name\s*=\s*([a-zA-Z0-9_]+)", lower)
    if not match:
        warnings.append("solve name=<electrode> not found or cannot be statically matched to inherited .str electrode")
    else:
        found = match.group(1)
        warnings.append(f"solve electrode `{found}` must be checked against inherited .str electrodes in DeckBuild")
        if sweep_electrode and found.lower() != sweep_electrode.lower():
            errors.append(f"solve name `{found}` does not match confirmed sweep electrode `{sweep_electrode}`")
    if "workfunction" in lower or "work.func" in lower:
        warnings.append("contact workfunction present; ensure user explicitly confirmed Schottky/metal assumptions")
    if any(model in lower for model in COMPLEX_UNCONFIRMED):
        warnings.append("complex/Luminous/impact/tunneling/interface-trap token present; ensure it was explicitly confirmed by user")
    return errors, warnings


def check_file(deck: Path, deck_type: str, expected_structure: str | None = None, sweep_electrode: str | None = None, allow_direct: bool = False) -> tuple[list[str], list[str]]:
    text = read(deck)
    lower = text.lower()
    errors: list[str] = []
    warnings: list[str] = []
    for token in FORBIDDEN:
        if token in lower:
            errors.append(f"forbidden token present: {token}")
    if deck_type == "devedit":
        e, w = check_devedit(text)
    elif deck_type == "athena":
        e, w = check_athena(text)
    elif deck_type == "atlas":
        e, w = check_atlas(text, expected_structure, sweep_electrode, allow_direct)
    else:
        raise ValueError(f"unknown deck type: {deck_type}")
    errors.extend(e)
    warnings.extend(w)
    return errors, warnings


def infer_type(path: Path) -> str:
    name = path.name.lower()
    if "devedit" in name or "structure" in name:
        return "devedit"
    if "athena" in name or "process" in name:
        return "athena"
    return "atlas"


def write_static_report(case: str, results: list[tuple[Path, list[str], list[str]]]) -> Path:
    paths = ensure_case_dirs(case)
    lines = ["# Static Check Report", ""]
    error_count = 0
    warning_count = 0
    for deck, errors, warnings in results:
        error_count += len(errors)
        warning_count += len(warnings)
        lines.append(f"## {deck.name}")
        lines.append("")
        if errors:
            lines.append("### ERROR")
            lines.extend(f"- {e}" for e in errors)
        if warnings:
            lines.append("### WARNING")
            lines.extend(f"- {w}" for w in warnings)
        if not errors and not warnings:
            lines.append("PASS")
        lines.append("")
    lines.append(f"Total errors: {error_count}")
    lines.append(f"Total warnings: {warning_count}")
    report = paths["reports"] / "static_check_report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Static-check generated Silvaco decks without running Silvaco.")
    parser.add_argument("--case", required=True)
    parser.add_argument("--deck", action="append", default=[])
    parser.add_argument("--expected-structure", default=None)
    parser.add_argument("--sweep-electrode", default=None)
    parser.add_argument("--allow-atlas-direct", action="store_true")
    args = parser.parse_args()
    paths = ensure_case_dirs(args.case)
    decks = [Path(d) for d in args.deck] if args.deck else sorted((paths["decks"]).glob("*.in"))
    results = []
    for deck in decks:
        if not deck.is_absolute():
            deck = ROOT / deck
        deck_type = infer_type(deck)
        allow_direct = args.allow_atlas_direct or deck.name.startswith("00_atlas_direct_control")
        results.append((deck, *check_file(deck, deck_type, args.expected_structure, args.sweep_electrode, allow_direct)))
    report = write_static_report(args.case, results)
    total_errors = sum(len(r[1]) for r in results)
    print(f"Wrote static check report: {report}")
    print(f"Errors: {total_errors}")
    return 0 if total_errors == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
