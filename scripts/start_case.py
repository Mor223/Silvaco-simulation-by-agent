from __future__ import annotations

import argparse
from pathlib import Path

from deckgen_common import ensure_case_dirs, slug_text, write_report

SIGE_MISSING = [
    "Structure dimensions",
    "Si/Ge/SiGe layer stack",
    "Ge fraction and material parameter source",
    "Doping species, concentrations, and ranges",
    "Electrode names and locations",
    "Mesh strategy and optical absorption refinement regions",
    "Wavelength",
    "Optical source type",
    "Incidence direction and location",
    "Optical power or intensity",
    "Bias sweep electrode, start, stop, and step",
    "Output target: photocurrent, responsivity, QE, absorption, or optical generation",
    "Whether to use Luminous",
    "Whether to use built-in material parameters or external optical constants",
]

COMMON_ROUTE_QUESTIONS = [
    "Do you want DevEdit direct geometry building or ATHENA process simulation?",
    "Should ATLAS perform electrical, optical, or Luminous optoelectronic simulation?",
    "What physical outputs or curves are required?",
    "Is a full DevEdit/ATHENA -> .str -> ATLAS flow required?",
    "Is an ATLAS direct control baseline explicitly requested?",
]

PN_MISSING = [
    "Geometry dimensions: length, thickness, coordinate convention, and surface location",
    "P-region and N-region doping species, concentrations, and spatial ranges",
    "Electrode names, positions, materials, and ohmic/Schottky assumptions",
    "Mesh strategy near the PN junction and contact regions",
    "Structure output file name `<case_name>_device.str`",
    "ATLAS log file name and final structure output file name",
    "Voltage sweep electrode, grounded electrode, start, stop, and step",
    "Confirmed ATLAS model set and method",
]


def classify_request(text: str) -> dict[str, object]:
    lower = text.lower()
    is_sige = "sige" in lower or "ge" in lower and "pd" in lower
    is_pn = "pn" in lower or "p-n" in lower or "diode" in lower or "二极" in lower or "结" in lower
    is_optical = any(k in lower for k in ["光", "optical", "luminous", "photo", "photocurrent", "pd"])
    wants_athena = "athena" in lower or "工艺" in lower or "process" in lower
    wants_devedit = "devedit" in lower or "建结构" in lower or "geometry" in lower
    control = "control" in lower or "baseline" in lower or "对照" in lower or "direct" in lower
    route = "undetermined"
    if wants_athena:
        route = "athena_atlas"
    elif wants_devedit or is_sige or is_optical:
        route = "devedit_atlas"
    elif control:
        route = "atlas_direct_control"
    return {"route": route, "is_sige": is_sige, "is_pn": is_pn, "is_optical": is_optical, "control_baseline": control}


def start_case(case: str, request: str) -> Path:
    paths = ensure_case_dirs(case)
    normalized = slug_text(request)
    (paths["specs"] / "user_request.md").write_text(normalized + "\n", encoding="utf-8")
    classification = classify_request(normalized)
    missing = list(COMMON_ROUTE_QUESTIONS)
    if classification["is_pn"]:
        missing.extend(PN_MISSING)
    if classification["is_sige"] or classification["is_optical"]:
        missing.extend(SIGE_MISSING)
    lines = [
        f"Case: `{case}`",
        f"Initial route guess: `{classification['route']}`",
        f"SiGe detected: `{classification['is_sige']}`",
        f"PN/diode detected: `{classification['is_pn']}`",
        f"Optical/optoelectronic detected: `{classification['is_optical']}`",
        "",
        "## Missing or confirmation-required parameters",
        "",
    ]
    lines.extend(f"- {item}" for item in missing)
    lines.extend([
        "",
        "No final deck was generated because required parameters are missing or unconfirmed.",
    ])
    missing_path = paths["specs"] / "missing_parameters.md"
    missing_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_report(paths["reports"] / "generation_summary.md", "Draft Case Summary", [
        "Natural-language request was saved.",
        "Missing-parameter report was generated.",
        "No Silvaco deck was rendered.",
    ])
    return missing_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Start a natural-language Silvaco deck-generation case without running Silvaco.")
    parser.add_argument("--case", required=True)
    parser.add_argument("--request", default=None)
    parser.add_argument("--request-file", default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.request_file:
        request = Path(args.request_file).read_text(encoding="utf-8")
    elif args.request:
        request = args.request
    else:
        raise SystemExit("Provide --request or --request-file")
    path = start_case(args.case, request)
    print(f"Wrote missing parameters: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

