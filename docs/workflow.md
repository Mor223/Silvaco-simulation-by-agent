# Workflow

This project converts natural-language semiconductor simulation requests into Silvaco input decks. It does not run Silvaco.

Main workflow:

1. User describes the device and simulation goal in natural language.
2. Codex identifies the route: DevEdit + ATLAS, ATHENA + ATLAS, or optional ATLAS direct control baseline.
3. Codex lists missing parameters and recommended options with sources.
4. User confirms all required parameters.
5. Codex writes completed YAML specs under `cases/<case_name>/specs/`.
6. Codex renders one of these full-flow deck sets:
   - `01_structure_devedit.in` + `02_atlas_simulation.in`
   - `01_process_athena.in` + `02_atlas_simulation.in`
7. Optional control baseline is written only when explicitly requested as `00_atlas_direct_control.in`.
8. Codex runs static text checks only and writes `static_check_report.md`.
9. User runs Silvaco manually outside this project.

Forbidden in this project:

- Do not launch DeckBuild, DevEdit, ATHENA, ATLAS, or TonyPlot.
- Do not use `-ascii` or `dbascii`.
- Do not generate manual run scripts.
- Do not collect runtime outputs, parse logs, or plot results.
- Do not generate final decks when required parameters are missing or unconfirmed.

Final deck locations:

- DevEdit route: `cases/<case_name>/decks/01_structure_devedit.in` and `cases/<case_name>/decks/02_atlas_simulation.in`
- ATHENA route: `cases/<case_name>/decks/01_process_athena.in` and `cases/<case_name>/decks/02_atlas_simulation.in`
- Optional control route: `cases/<case_name>/decks/00_atlas_direct_control.in`

## Workflow Router

Codex chooses one of four workflows from the user request. When intent is ambiguous, ask which workflow the user wants.

### 1. Generate Deck Workflow

Trigger phrases include: generate Silvaco code, build a device, make a simulation, write an `.in`, modeling, DevEdit, ATHENA, ATLAS, Luminous, PN, PIN, SiGe PD, waveguide PD, optoelectronic simulation.

Required user information:

- device type and route preference;
- geometry/process/material/doping/electrode/mesh parameters;
- simulation type, models, method, sweep, outputs;
- confirmation for all recommended parameters.

Outputs:

- completed YAML specs;
- `01_structure_devedit.in` or `01_process_athena.in`;
- `02_atlas_simulation.in`;
- static check and generation reports.

Forbidden: do not run Silvaco or generate final decks with unconfirmed parameters.

### 2. Analyze Error Workflow

Trigger phrases include: error, warning, failed, cannot, convergence, file not found, no such electrode, empty log, empty `pn_iv.log`, `manual_run.out`, `mesh infile`, DeckBuild error, ATLAS error, DevEdit error, Luminous error.

Before analysis, ask for:

- case path;
- deck file path;
- log file path or pasted error text;
- intended simulation goal;
- permission to generate a proposed fix deck.

Outputs:

- `cases/<case_name>/reports/error_analysis.md`;
- optional `cases/<case_name>/decks/proposed_fix/*_fixed.in`;
- `cases/<case_name>/reports/proposed_fix_summary.md`;
- reusable updates to troubleshooting, syntax rules, static checker, and skill when applicable.

Forbidden: do not run Silvaco and do not overwrite the original deck.

### 3. Learn New Example Workflow

Trigger phrases include: new example, learn this deck, add to example library, update example library, official example, I ran this deck successfully, use this as future reference, add to skill.

Before learning, ask for:

- example file path;
- whether the user manually verified it: true, false, or unknown;
- purpose/application;
- permission to add syntax patterns to the project knowledge base.

Outputs:

- updated compact examples index;
- updated syntax/model/NL mapping docs;
- optional parameterized learned template draft;
- `docs/learning_reports/<case_id>_learning_report.md`.

Forbidden: do not copy full commercial examples, do not mark unverified examples as verified, do not run Silvaco.

### 4. Update Knowledge Base Workflow

Trigger phrases include: update skill, update knowledge base, rescan examples, rebuild index, relearn examples, update syntax_rules.

Outputs:

- refreshed docs/data/skills/templates/scripts as requested;
- update report.

Forbidden: do not run Silvaco or modify the Silvaco installation.
