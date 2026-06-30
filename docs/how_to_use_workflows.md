# How To Use Project Workflows

This project supports four Codex workflows. None of them launches Silvaco.

## 1. Generate Deck Workflow

Use when you want a new Silvaco deck generated from a device/simulation request.

Example prompt:

> 我想做一个 SiGe PD 1310 nm 光电仿真，请按生成 deck 工作流处理。

Codex will:

- identify the device and route;
- search local example indexes;
- ask missing parameters;
- wait for confirmation;
- generate DevEdit/ATHENA + ATLAS `.in` files;
- run static text checks only.

## 2. Analyze Error Workflow

Use when you manually ran Silvaco and got an error.

Example prompt:

> 这个 case 报错了，请按错误分析工作流处理。case 路径是 cases/pn_test，deck 是 cases/pn_test/decks/02_atlas_simulation.in，日志是 cases/pn_test/logs/manual_run.out，目标是 PN I-V。

Please provide:

1. case path;
2. deck path;
3. log path or pasted error text;
4. intended simulation goal;
5. whether Codex may generate a `proposed_fix` deck.

Codex will not overwrite the original deck. Proposed fixes go under `cases/<case>/decks/proposed_fix/`.

## 3. Learn New Example Workflow

Use when you have a new official/example/user-verified deck that should inform future generation.

Example prompt:


Please provide:

1. example file path;
2. whether it was user-verified: true, false, or unknown;
3. short purpose;
4. permission to extract syntax patterns into the knowledge base.

Codex extracts tags and reusable command forms only; it does not copy full commercial examples.

## 4. Update Knowledge Base Workflow

Use when you want to rescan examples or refresh skill/docs.

Example prompt:

> 请重新扫描案例库并更新 skill。

Codex will update docs/data/skills only and will not run Silvaco.
