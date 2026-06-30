from __future__ import annotations

import argparse
from deckgen_common import ensure_case_dirs, read_yaml, render_template, require_confirmed, unwrap


def render_structure(case: str) -> str:
    paths = ensure_case_dirs(case)
    spec_path = paths["specs"] / "completed_device_spec.yaml"
    spec = read_yaml(spec_path)
    require_confirmed(spec, "completed_device_spec.yaml")
    data = unwrap(spec)
    route = data.get("route")
    if route != "devedit_atlas":
        raise ValueError(f"Device spec route is {route}; expected devedit_atlas")
    context = data["devedit"]
    text = render_template(data.get("template", "devedit_structure/lateral_pn_devedit.in.j2"), context)
    out = paths["decks"] / "01_structure_devedit.in"
    out.write_text(text, encoding="utf-8")
    print(f"Wrote DevEdit deck: {out}")
    return str(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a DevEdit structure deck after all parameters are confirmed.")
    parser.add_argument("--case", required=True)
    args = parser.parse_args()
    render_structure(args.case)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
