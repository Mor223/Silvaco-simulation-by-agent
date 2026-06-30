# Natural Language to Silvaco TCAD Deck Generator

This project turns natural-language semiconductor simulation requests into confirmed parameters and generated Silvaco DevEdit/ATHENA + ATLAS `.in` deck files. It performs text processing, template rendering, compact case-pattern lookup, model suggestions, and static checks only.

## What This Project Does Not Do

- It does not run Silvaco or launch DeckBuild.
- It does not provide Silvaco software, official examples, or license material.
- It does not redistribute proprietary Silvaco example decks.
- It does not guarantee physical correctness; users must review and validate every deck with their own licensed tools.

## Supported Routes

- DevEdit + ATLAS
- ATHENA + ATLAS
- ATLAS direct control baseline
- Luminous / optical deck generation after optical parameters are confirmed

## Install

```bash
python -m pip install -r requirements.txt
```

## Basic Usage

```bash
python scripts/start_case.py --case pn_demo --request "Generate a 2D silicon PN diode IV deck"
python scripts/search_silvaco_examples.py --query "PN diode IV"
python scripts/render_structure_deck.py --case pn_demo
python scripts/render_atlas_deck.py --case pn_demo
python scripts/check_deck_static.py --case pn_demo
```

Outputs are written under `cases/<case_name>/decks/`.

## Workflows

Generate Deck Workflow, Error Analysis Workflow, New Example Learning Workflow, and Knowledge Update Workflow are documented under `docs/` and in the bundled Codex skill.

## Local Scan Safety

`scripts/scan_silvaco_examples.py` writes sanitized public summaries by default. Do not commit raw local scan outputs, local example roots, private decks, or generated runtime results.

## Copyright And Security

This project contains original templates, scripts, documentation, and compact syntax-pattern summaries. Users must hold their own valid Silvaco license and must not publish private decks, license files, local paths, or sensitive runtime outputs.
