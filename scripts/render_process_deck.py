from __future__ import annotations

import argparse
from deckgen_common import ensure_case_dirs, read_yaml, render_template, require_confirmed, unwrap


def render_process(case: str) -> str:
    paths = ensure_case_dirs(case)
    spec_path = paths["specs"] / "completed_process_spec.yaml"
    spec = read_yaml(spec_path)
    require_confirmed(spec, "completed_process_spec.yaml")
    data = unwrap(spec)
    route = data.get("route")
    if route != "athena_atlas":
        raise ValueError(f"Process spec route is {route}; expected athena_atlas")
    text = render_template(data.get("template", "athena_process/generic_diode_process_athena.in.j2"), data["athena"])
    out = paths["decks"] / "01_process_athena.in"
    out.write_text(text, encoding="utf-8")
    print(f"Wrote ATHENA deck: {out}")
    return str(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an ATHENA process deck after all parameters are confirmed.")
    parser.add_argument("--case", required=True)
    args = parser.parse_args()
    render_process(args.case)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
