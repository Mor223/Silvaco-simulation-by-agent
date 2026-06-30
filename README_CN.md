# Natural Language to Silvaco TCAD Deck Generator（中文说明）

本项目用于把**自然语言半导体器件仿真需求**转化为可供 Silvaco TCAD 使用的 `.in` 输入文件。它面向 DevEdit、ATHENA、ATLAS 与 Luminous/光学仿真场景，重点解决“需求描述不完整、模型选择不确定、语法容易写错、案例经验难以复用”的问题。

项目的定位很明确：**生成和检查 Silvaco deck，不负责运行 Silvaco**。用户仍然需要在自己的合法 Silvaco 环境中打开 DeckBuild 或用自己的方式运行生成的 `.in` 文件。

---

## 1. 项目能做什么

本项目提供一套可迁移的工作流：

```text
自然语言器件仿真需求
  → 识别建模路线
  → 追问缺失参数
  → 基于案例知识推荐模型和语法模式
  → 用户确认参数
  → 生成结构/工艺 .in
  → 生成 ATLAS 仿真 .in
  → 静态检查
  → 用户自行用 Silvaco 运行
```

支持的主要路线：

1. **DevEdit + ATLAS**：适合几何结构明确、希望直接建立二维/三维器件模型的场景。
2. **ATHENA + ATLAS**：适合需要描述氧化、沉积、刻蚀、离子注入、扩散/退火等工艺流程的场景。
3. **ATLAS direct control baseline**：只作为对照基准，用于快速验证 ATLAS 求解和扫描语法，不替代完整的 DevEdit/ATHENA → `.str` → ATLAS 流程。
4. **Luminous / optical deck generation**：适合光电探测器、光照响应、波长扫描、光电流或响应度等需求，但必须先补齐光学参数。

---

## 2. 项目不做什么

本项目不包含也不替代 Silvaco 软件本身。

默认工作流中，项目不会：

- 启动 DeckBuild；
- 运行 DevEdit / ATHENA / ATLAS / TonyPlot；
- 使用 `-ascii` 或 `dbascii`；
- 自动收集仿真输出；
- 自动解析 `.log`；
- 自动绘图；
- 自动修改本地 license 或软件安装目录；
- 复制或分发 Silvaco 官方完整案例源码；
- 在参数不完整时强行生成最终 deck。

如果用户需要仿真后结果分析，应作为单独任务处理，而不是本项目的默认主流程。

---

## 3. 目录结构

```text
nl-silvaco-simulation-workflow/
├─ README.md                         # 英文说明
├─ README_CN.md                      # 中文说明
├─ AGENTS.md                         # 给 Codex/Claude/其他 agent 的工作流规则
├─ SECURITY.md                       # 敏感信息和发布安全说明
├─ CONTRIBUTING.md                   # 贡献指南
├─ requirements.txt                  # Python 依赖
│
├─ configs/                          # 示例配置，不应写入本机真实路径
│  ├─ project.example.yaml
│  ├─ device_spec.example.yaml
│  ├─ process_spec.example.yaml
│  ├─ simulation_spec.example.yaml
│  └─ silvaco_paths.example.yaml
│
├─ scripts/                          # 文本处理、模板渲染、静态检查脚本
│  ├─ start_case.py
│  ├─ ask_missing_parameters.py
│  ├─ search_silvaco_examples.py
│  ├─ suggest_models_from_examples.py
│  ├─ render_structure_deck.py
│  ├─ render_process_deck.py
│  ├─ render_atlas_deck.py
│  ├─ check_deck_static.py
│  ├─ learn_new_example.py
│  ├─ analyze_silvaco_error.py
│  ├─ scan_silvaco_examples.py
│  ├─ audit_sanitization.py
│  └─ audit_portability.py
│
├─ templates/                        # Jinja2 模板，用于生成 Silvaco .in
│  ├─ devedit_structure/
│  ├─ athena_process/
│  ├─ atlas_simulation/
│  └─ control_baseline/
│
├─ data/                             # 脱敏后的案例知识索引
│  ├─ silvaco_examples_index.public.json
│  └─ silvaco_syntax_patterns.public.json
│
├─ docs/                             # 工作流、语法规则、模型推荐、排错知识
│  ├─ workflow.md
│  ├─ user_questionnaire.md
│  ├─ silvaco_case_knowledge.md
│  ├─ syntax_rules.md
│  ├─ model_recommendation_rules.md
│  ├─ nl_request_to_examples.md
│  ├─ troubleshooting.md
│  └─ how_to_use_workflows.md
│
├─ skills/                           # 可迁移的 agent skill
│  └─ nl_to_silvaco_simulation/
│     ├─ SKILL.md
│     ├─ references/
│     ├─ scripts/
│     ├─ templates/
│     └─ data/
│
├─ examples/                         # 项目自带的最小示例，不是官方案例原文
│  ├─ pn_devedit_atlas_minimal/
│  ├─ pn_athena_atlas_minimal/
│  ├─ atlas_direct_control_baseline/
│  └─ sige_pd_luminous_questionnaire/
│
└─ tests/                            # 纯 Python 测试，不运行 Silvaco
```

---

## 4. 本地环境搭建

### 4.1 Python 环境

建议使用 Python 3.10 或更新版本。

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# Windows 用户可使用自己的虚拟环境激活方式
pip install -r requirements.txt
```

如果只是让 AI agent 阅读和生成 `.in` 文件，也可以不安装 Silvaco；但用户要实际仿真，必须自己拥有合法的 Silvaco 安装和 license。

### 4.2 Silvaco 环境

本项目不要求在仓库中写入 Silvaco 安装路径。需要运行 deck 时，用户自行在本机 DeckBuild / Silvaco GUI 中运行生成的 `.in` 文件。

不要把以下内容提交到 Git：

- 本机 Silvaco 安装路径；
- license 文件；
- 许可证服务地址；
- 用户名、邮箱、机器名；
- 私有工艺 deck；
- `.str`、`.log`、`.out`、`.csv`、`.png` 等运行结果。

---

## 5. 基本建模流程

### 5.1 新建自然语言 case

示例：

```bash
python scripts/start_case.py \
  --case pn_demo \
  --request "建立一个二维硅 PN 结，使用 DevEdit 建结构，ATLAS 做 I-V。"
```

该命令不会生成最终 deck，而是保存用户请求并列出缺失参数。

输出位置：

```text
cases/pn_demo/specs/user_request.md
cases/pn_demo/specs/missing_parameters.md
cases/pn_demo/reports/generation_summary.md
```

### 5.2 补齐参数

用户需要根据 `missing_parameters.md` 补充：

- 器件尺寸；
- 材料层；
- 掺杂浓度和范围；
- 电极名称和位置；
- 网格策略；
- ATLAS 物理模型；
- 扫描电极、起止电压、步长；
- 输出文件名；
- 是否需要 Luminous 或光学参数。

当参数完整且确认后，生成：

```text
cases/<case_name>/specs/completed_device_spec.yaml
cases/<case_name>/specs/completed_process_spec.yaml
cases/<case_name>/specs/completed_simulation_spec.yaml
```

所有推荐参数都应明确标记是否由用户确认。未确认参数不得进入最终 deck。

### 5.3 生成 DevEdit 结构 deck

DevEdit 路线：

```bash
python scripts/render_structure_deck.py --case <case_name>
```

输出：

```text
cases/<case_name>/decks/01_structure_devedit.in
```

该文件负责：

- `go devedit`；
- region / material；
- impurity / doping；
- electrode / contact；
- mesh；
- `struct outf=<case_name>_device.str`；
- `quit`。

### 5.4 生成 ATHENA 工艺 deck

ATHENA 路线：

```bash
python scripts/render_process_deck.py --case <case_name>
```

输出：

```text
cases/<case_name>/decks/01_process_athena.in
```

该文件负责：

- `go athena`；
- `line x` / `line y`；
- `init`；
- implant / diffuse / etch / deposit / oxidize；
- electrode；
- `structure outfile=<case_name>_device.str`；
- `quit`。

### 5.5 生成 ATLAS 仿真 deck

```bash
python scripts/render_atlas_deck.py --case <case_name>
```

输出：

```text
cases/<case_name>/decks/02_atlas_simulation.in
```

ATLAS 文件必须读取第一步生成的结构：

```text
mesh infile="<case_name>_device.str"
```

ATLAS 文件负责：

- `go atlas`；
- `mesh infile=...`；
- `models ...`；
- `method ...`；
- `solve init`；
- `log outf=...`；
- `solve ...`；
- `log off`；
- `save outf=...`；
- `quit`。

---

## 6. 静态检查

生成 `.in` 后，应先做静态检查：

```bash
python scripts/check_deck_static.py --case <case_name>
```

也可以指定预期结构文件和扫描电极：

```bash
python scripts/check_deck_static.py \
  --case <case_name> \
  --expected-structure <case_name>_device.str \
  --sweep-electrode anode
```

静态检查不会运行 Silvaco，只检查：

- 是否包含必要模块命令；
- DevEdit / ATHENA 输出结构名是否与 ATLAS `mesh infile` 一致；
- `log outf` 后是否有有效 `solve`；
- `solve name` 是否与用户确认的扫描电极一致；
- 是否存在 `-ascii`、`dbascii`、自动 TonyPlot 等禁止项；
- 是否存在未确认的 Luminous、隧穿、impact、interface trap 等复杂模型；
- 是否存在已知高风险语法。

如果有 ERROR，不应把 deck 视为完成。WARNING 需要用户人工检查。

---

## 7. 案例库检索和模型推荐

本项目包含脱敏后的案例知识索引，不包含 Silvaco 官方完整案例源码。

搜索相似案例：

```bash
python scripts/search_silvaco_examples.py --query "PN diode IV"
python scripts/search_silvaco_examples.py --tags atlas,pn_diode,iv
```

推荐模型：

```bash
python scripts/suggest_models_from_examples.py \
  --case pn_demo \
  --device-type pn_diode \
  --goal iv
```

示例推荐：普通 Si PN / PIN I-V 可考虑：

```text
models srh conmob fldmob fermi
```

但模型推荐不是自动写入最终 deck。用户必须确认模型选择、材料参数、接触假设和扫描条件。

---

## 8. 新案例学习流程

当用户有新的 deck 或案例想加入知识库时，使用：

```bash
python scripts/learn_new_example.py \
  --example <path_to_deck> \
  --case-id <case_id> \
  --verified true \
  --purpose "short description"
```

注意：

- 脚本只做文本分析；
- 不运行 Silvaco；
- 不修改原案例；
- 不复制完整案例源码；
- 会将路径脱敏后写入 public index；
- 会更新语法规则、模型推荐、自然语言映射和 skill references。

如果案例未手动跑通，应使用：

```text
--verified false
```

未验证案例只能作为语法参考，不能当作已验证模板。

---

## 9. 错误分析流程

如果用户手动运行 Silvaco 后出现错误，可以用：

```bash
python scripts/analyze_silvaco_error.py \
  --case <case_name> \
  --deck cases/<case_name>/decks/02_atlas_simulation.in \
  --log <path_to_user_log> \
  --goal "simulation goal" \
  --proposed-fix
```

该脚本会：

- 读取 deck 和日志；
- 找第一处明确错误；
- 判断错误阶段；
- 生成 `error_analysis.md`；
- 可选生成 proposed fix；
- 更新 troubleshooting、syntax rules 和 skill。

它不会运行 Silvaco，也不会覆盖原始 deck。

---

## 10. 给 Codex / Claude / 其他 AI agent 的使用说明

如果把本项目交给本地 Codex CLI、Claude Code、Cursor agent 或其他 AI agent，建议先让 agent 阅读以下文件：

1. `AGENTS.md`
2. `README_CN.md`
3. `docs/workflow.md`
4. `docs/user_questionnaire.md`
5. `docs/syntax_rules.md`
6. `docs/model_recommendation_rules.md`
7. `docs/troubleshooting.md`
8. `skills/nl_to_silvaco_simulation/SKILL.md`

建议给 agent 的启动提示词：

```text
请先阅读本仓库的 AGENTS.md、README_CN.md、docs/workflow.md 和 skills/nl_to_silvaco_simulation/SKILL.md。
本项目的任务是根据用户确认后的半导体器件仿真需求生成 Silvaco DevEdit/ATHENA + ATLAS .in 文件。
不要运行 Silvaco，不要启动 DeckBuild，不要调用 ATLAS/DevEdit/ATHENA/TonyPlot，不要解析仿真结果。
遇到缺失参数必须先询问用户。
生成 deck 前必须查阅案例知识和语法规则，并进行静态检查。
```

### Agent 工作流路由

Agent 应根据用户意图选择工作流：

1. **Generate Deck Workflow**：用户要生成新的器件仿真 `.in` 文件。
2. **Analyze Error Workflow**：用户提供运行日志或错误输出。
3. **Learn New Example Workflow**：用户提供新的 deck 或案例。
4. **Knowledge Update Workflow**：用户要求重新扫描或更新知识库。

不得在用户只是说“做一个仿真”时直接生成最终 deck。必须先列出缺失参数并等待确认。

---

## 11. 发布和安全注意事项

上传 GitHub 前建议运行：

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
python scripts/audit_sanitization.py .
python scripts/audit_portability.py .
```

如果运行测试后生成了缓存，提交前删除：

```bash
find . -type d -name __pycache__ -prune -exec rm -rf {} +
rm -rf .pytest_cache
```

不要提交：

- `__pycache__/`；
- `.pytest_cache/`；
- 本机路径配置；
- license；
- Silvaco 原始官方案例源码；
- 用户私有工艺 deck；
- 仿真运行结果。

---

## 12. 局限性

1. 本项目只能辅助生成 Silvaco deck，不能保证物理模型完全正确。
2. 复杂器件仍需要用户具备 TCAD、半导体器件物理和 Silvaco 语法知识。
3. DevEdit 电极继承到 ATLAS 的行为可能依版本而异，静态检查只能给出 warning，最终仍需用户运行验证。
4. Luminous、SiGe、异质结、隧穿、击穿等复杂模型必须由用户确认参数，不能直接套默认值。
5. 本项目不包含 Silvaco 软件、手册、license 或官方案例源码。

---

## 13. 推荐贡献方式

欢迎贡献：

- 新的参数化模板；
- 新的语法模式摘要；
- 新的静态检查规则；
- 新的错误模式；
- 新的用户问询清单；
- 新的脱敏案例索引记录。

不要贡献：

- 商业软件官方完整案例源码；
- license；
- 私有项目路径；
- 未脱敏日志；
- 未经确认的仿真结果。

---

## 14. 一句话总结

本项目不是 Silvaco 自动运行器，而是一个面向 AI agent 的 **自然语言到 Silvaco TCAD `.in` 文件生成与静态检查工作流**。

它的核心价值是：

```text
把用户的器件仿真想法，经过参数补全、案例知识检索、模型推荐和静态检查，转化成可由用户自行运行的 Silvaco DevEdit/ATHENA + ATLAS deck。
```
