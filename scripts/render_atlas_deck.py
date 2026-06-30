from __future__ import annotations

import argparse
from deckgen_common import ensure_case_dirs, read_yaml, render_template, require_confirmed, unwrap


def render_atlas(case: str) -> list[str]:
    paths = ensure_case_dirs(case)
    spec_path = paths["specs"] / "completed_simulation_spec.yaml"
    spec = read_yaml(spec_path)
    require_confirmed(spec, "completed_simulation_spec.yaml")
    data = unwrap(spec)
    outputs: list[str] = []
    if data.get("route") in {"devedit_atlas", "athena_atlas"}:
        text = render_template(data.get("template", "atlas_simulation/electrical_iv_atlas.in.j2"), data["atlas"])
        out = paths["decks"] / "02_atlas_simulation.in"
        out.write_text(text, encoding="utf-8")
        outputs.append(str(out))
        print(f"Wrote ATLAS deck: {out}")
    if data.get("control_baseline") is True:
        control = data.get("control")
        if not control:
            raise ValueError("control_baseline=true requires a control spec")
        text = render_template(data.get("control_template", "control_baseline/atlas_direct_pn_control.in.j2"), control)
        out = paths["decks"] / "00_atlas_direct_control.in"
        out.write_text(text, encoding="utf-8")
        outputs.append(str(out))
        print(f"Wrote control baseline deck: {out}")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Render ATLAS simulation decks after all parameters are confirmed.")
    parser.add_argument("--case", required=True)
    args = parser.parse_args()
    render_atlas(args.case)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
