from __future__ import annotations

import argparse
from deckgen_common import ensure_case_dirs


def main() -> int:
    parser = argparse.ArgumentParser(description="Print the missing-parameter report for a case.")
    parser.add_argument("--case", required=True)
    args = parser.parse_args()
    path = ensure_case_dirs(args.case)["specs"] / "missing_parameters.md"
    if not path.is_file():
        print(f"No missing parameter report found: {path}")
        return 2
    print(path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
