from __future__ import annotations

import argparse
from deckgen_common import ensure_case_dirs, write_report


def suggest(case: str, device_type: str, goal: str) -> str:
    paths = ensure_case_dirs(case)
    device = device_type.lower()
    goal_l = goal.lower()
    lines = [
        f"Device type: `{device_type}`",
        f"Simulation goal: `{goal}`",
        "",
        "## Recommended models",
        "",
    ]
    if "pn" in device or "diode" in device:
        lines.extend([
            "- `srh`: Shockley-Read-Hall recombination for diode current behavior.",
            "- `conmob`: concentration-dependent mobility for doped silicon regions.",
            "- `fldmob`: high-field mobility for biased junction sweeps.",
            "- `fermi`: Fermi statistics for heavily doped contact regions.",
            "",
            "Reference pattern: local diode-like ATLAS examples and manually verified PN control baseline.",
            "User confirmation required before final deck generation.",
        ])
    elif "photo" in goal_l or "optical" in goal_l or "luminous" in goal_l:
        lines.extend([
            "- Luminous/optoelectronic models require wavelength, source, optical constants, incidence geometry, and output targets.",
            "- No final model set is recommended without those confirmations.",
            "",
            "No explicit complete case basis was found for the requested optical setup; user confirmation or Silvaco manual review is required.",
        ])
    else:
        lines.append("No explicit basis was found in the local knowledge summary; user confirmation or Silvaco manual review is required.")
    path = paths["reports"] / "model_recommendations.md"
    write_report(path, "Model Recommendations", lines)
    return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest ATLAS models from local knowledge without running Silvaco.")
    parser.add_argument("--case", required=True)
    parser.add_argument("--device-type", required=True)
    parser.add_argument("--goal", required=True)
    args = parser.parse_args()
    print(f"Wrote model recommendations: {suggest(args.case, args.device_type, args.goal)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
