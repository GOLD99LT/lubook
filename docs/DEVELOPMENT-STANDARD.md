# DEVELOPMENT-STANDARD — 分册开发、审查与成型规范

> 状态：Active（2026-10-24 立）
> 适用范围：本仓所有分册（`apps/*`）与其共享包（`packages/*`）。
> 来源：把 `apps/hardware`（140 章，18 个内容批次，3 轮全量技术审查，38 处确认错误修正）的
> 实际流程提炼成可复用条款。**本文的每一条都对应一次真实事故或一次真实修正**，不是凭空写的理想流程。
>
> 相关文档：架构 [`../ARCHITECTURE.md`](../ARCHITECTURE.md)、内容标准
> [`CONTENT-STANDARD.md`](CONTENT-STANDARD.md)、命名 [`NAMING.md`](NAMING.md)、
> 操作手册 [`PLAYBOOK.md`](PLAYBOOK.md)、ADR [`adr/`](adr/)。

---

## 0. 一句话原则

**门禁绿 ≠ 内容对。** 门禁只能证明"能构建、链接不坏、公式能编译"，
证明不了"这个公式推对了、这个数字算对了、这个电路画对了"。
所以本规范把"机械门禁"和"复算审查"当成两条**都必须过**的独立防线。

---

## 1. 不变量（违反即返工，不接受"下批再改"）

| # | 不变量 | 判定方式 |
|---|---|---|
| I1 | Markdown 是唯一事实源；内容文件只允许 `git mv`，不改写既有正文来"顺手重构" | `git log --follow`、diff 只含 rename |
| I2 | 已发布 URL 永不变；路由快照（`tests/<app>.routes.snapshot.json`）必须零差异 | `git diff tests/*routes.snapshot.json` 为空 |
| I3 | 离线单文件构建保持**零第三方依赖**（Python 标准库） | `build_single_html.py` 的 import 白名单 |
| I4 | 共享包边界：app 不 import 别的 app；theme 只依赖接口，不读 localStorage/sidebar | 代码评审 + `grep` 依赖方向 |
| I5 | 每章 frontmatter 必备 `title/part/chapter/order/tags/difficulty/id/status/sources` | `validate.py` |
| I6 | 正文禁止手写章号（"第 N 章"由构建期按 SUMMARY 生成） | `check-content.py` |
| I7 | 新增生成物必须被 `.gitignore` 覆盖，不得提交构建产物 | `git status` 干净 |
| I8 | 未立项不做（P4/P5 之类） | ADR + 用户授权 |

---

## 2. 生命周期总览

```
S0 立项(ADR) → S1 脚手架 → S2 章节规划(SUMMARY+篇/章) → S3 分批生产
                                   ↑                          ↓
                        S6 上线(用户确认) ← S5 双站部署 ← S4 审查+门禁
```

| 阶段 | 产出 | 退出条件（Gate） |
|---|---|---|
| S0 立项 | ADR：目的、范围、不变量影响、不做清单 | ADR 合入；用户明确授权 |
| S1 脚手架 | `apps/<app>/`（config/package/SUMMARY/首页）、根 `package.json` 脚本、CI 矩阵自动发现 | `pnpm build:<app>` 退出 0；门户卡片可配 |
| S2 规划 | SUMMARY 分层（篇 → 章）、每章一句话定位、档位（主干/支撑/速查）、依赖排序 | 章节清单评审通过；无重复主题 |
| S3 生产 | 每批 3~6 章，含图与自测题 | 单章自检表全绿（见 §5） |
| S4 审查 | 审查报告（确认错误清单 + 存疑清单） | §6 审查协议走完；错误已修或明确记录 |
| S5 部署 | 双站构建 | §7 门禁矩阵全绿 + 线上体检 0 失败 |
| S6 交付 | 用户确认 | 用户签字；写入 `CURRENT-STATE.md` |

---

## 3. 内容生产规范（S3）

### 3.1 分批

- **一批 3~6 章**，同篇、同难度档，便于一次审查闭环。历史上 4 章/批的节奏最稳。
- 每批必须先出**章纲**（模块标题 + 关键公式 + 计划配图），再写正文。
- 批量并行时，每个智能体负责 ≤6 章；超过则拆。

### 3.2 写作要求（摘要，细则见 CONTENT-STANDARD）

- 主干章 ≥4,500 CJK，支撑章 ≥3,200，速查档不设限。
- **导读/总览章也算正文**：它是读者进入分册的第一屏，必须按正文标准写全（8 模块 + 图 + 来源），
  不允许用 `--quick-dirs` 绕过。速查口径只适用于真正的速查表与题库。
- 模块顺序固定：概念章 8 模块（动机/定义与直观/定量关系/典型计算/工程含义/常见坑/自测题/参考资料），电路章 11 模块。
- 每个数字**可复算**、每条结论**有来源**；公式给结论 + 符号解释，推导放 `::: advanced`。
- 图：SVG 放 `docs/assets/schematics/`，必须是合法 XML（见 F5）；波形用 `echarts` 围栏。
- 自测题用 `<details>`，每题答案里**带计算过程**。
- 交叉引用用相对路径 `[x](../<篇>/<章>.md)`，链接文字要说明"为什么相关"。

### 3.3 单章自检表（写完自己过一遍）

- [ ] 字数达标（`check-content.py`）
- [ ] 11/8 模块齐全且顺序正确
- [ ] 至少 1 张原理图；电路章 ≥2 张；SVG XML 合法
- [ ] 所有算例已用 Python 复算，单位与量级正确
- [ ] 至少 2 条"现象→原因→解决"的坑
- [ ] 至少 2 道自测题，答案含推导
- [ ] 来源 ≥3 条，编号/URL 可核（见 §6.4）
- [ ] 无绝对化表述（"绝对安全""一定不会"）
- [ ] 无手写章号，无 emoji 图标

---

## 4. 质量门禁矩阵（S4 机械部分）

| 门禁 | 工具 | 拦什么 | 入口 | 历史战果 |
|---|---|---|---|---|
| frontmatter/SUMMARY/图片/死链/id 唯一 | `validate.py` | 结构错、图片缺失、站内死链 | 自动 | — |
| 内容档位与模块 | `check-content.py --profile all --by-dir --strict` | 字数、模块、配图、坑、来源 | 自动 | 速查档恒红已修，现 140/140 |
| KaTeX 编译 | `scan_math.py` | 公式语法 | 自动 | 102 处公式错误 |
| 来源编号 | `scan_grounds.py` | 来源缺失/编号对不上 | 自动 | — |
| SVG 顺序与合法性 | `scan_svg_order.py` | 图层顺序、XML 非法、BOM | 自动 | 2 张线上破图 |
| 产物契约 | `scan_math_render.py` | 构建期/运行期公式契约被破坏 | 自动 | 运行期改造后的回归保护 |
| 旧错回归 | `scan_legacy_errors.py --strict` | 已纠正的错误说法被写回 | 自动 | 命中 0（纠错语境已排除） |
| manifest/指纹 | `run_quality.py` + `freeze_manifest.py` | 内容变更未登记、跨形态不一致 | 自动 | — |
| 路由快照 | `run_quality.py` | URL 变更（不变量 I2） | 自动 | — |
| 构建内存 | `build_memory_budget.py` | 预计 OOM（模型见 ADR-0012） | 自动 | 从"偶发 OOM"变"可预测" |
| 线上体检 | `check_live_site.py` | 部署后 404/空壳/缺资源 | **人工**（需网络） | 1238 个资源全绿 |
| 外链复核 | `verify_sources.py` / `check_sources_online.py` | 正文外链与来源注册表失效 | **人工**（需网络） | 9 条死链、2 条错 ISBN |

**统一入口**：`pnpm verify:all`（内存预算 → 构建 → 产物契约 → 内容档位 → 旧错回归 →
质量/对账 → 离线单文件 → 学习单测）。非零退出即阻断，**不看单条日志**，看退出码。

**为什么不把联网检查放进 `verify:all`**：外部站点的 403/改版/超时会制造"门禁红但工程没毛病"的假告警
（本机还有透明代理，404 甚至不可信）。联网检查是**人工/定时体检**，红了开 issue，不拦提交。

---

## 5. 内容审查协议（S4 人工/智能体部分）

这一节是整套流程里**唯一能发现"40 个公式里第 17 个推导错了"**的环节，必须按协议执行。

### 5.1 编组

- 每个审查智能体负责 **6 章左右**，同篇分片，避免跨领域。
- 提示词必须包含：文件清单、重点风险清单（该领域历史上易错的点）、**复算要求**、输出格式、禁止项。

### 5.2 复算要求（硬性）

- 所有带数字的例子、表格、公式必须**自己算一遍**（用 Python 脚本，允许临时脚本但用完删除）。
- 判定标准：**能证明是错的**才报错误；有疑问但无法证明的，单列"存疑"并说明缺什么证据。
- 禁止项：文风、排版、公式写法偏好、"可以更详细"。

### 5.3 置信分级与处置

| 级别 | 定义 | 处置 |
|---|---|---|
| 确认错误 | 可由文中自身公式/数值反推矛盾 | 直接修 |
| 与权威冲突 | 与同册其他章节或公认标准冲突 | 修，并在提交信息写明依据 |
| 存疑 | 依赖标准原文/口径，本机无法证实 | **不改**，记入报告与 `CURRENT-STATE.md` |
| 误报 | 语境是"在纠正错误说法" | 不改；优化工具的模式/豁免规则 |

### 5.4 假阳性治理（血泪）

工具与审查都会误报，**误报会摧毁信任**，必须收敛：

1. **纠错语境豁免**：正文在说"这个说法是错的"时必须排除（`scan_legacy_errors.py` 用引号 + 否定词窗口实现）。
2. **反向自测**：每条规则都要用"故意插入的错误"验证能抓到（见该脚本 `--strict` 用法）。
3. **代理/DNS 陷阱**：本机 DNS 可能被透明代理接管（全部解析到 `198.18.0.0/15`），此时 404 不可作为失效证据。`verify_sources.py` 会自检并声明"只有 200 可确认"。
4. **反爬不等于失效**：403/429 记 `blocked`，不记 `dead`。

### 5.5 审查后必须做的三件事

1. 逐条复算**不是自己权威领域**的修正（别信"看起来对"）。
2. 修改后重跑 `pnpm verify:all`。
3. 把"确认错误 / 存疑 / 误报"三类写进提交信息与 `CURRENT-STATE.md`。

---

## 6. 构建与部署（S5）

### 6.1 双站拓扑（ADR-0013）

| 站点 | base | 触发 |
|---|---|---|
| GitHub Pages 主站 | `/lubook/` | push main |
| Cloudflare Pages 镜像 | `/` | push main（自动） |

- 两条流水线**都跑完整门禁**（镜像不是低保证副本）。
- 可复用工作流的并发组必须带调用方：`quality-${{ github.workflow }}-${{ github.ref }}`，
  否则两条流水线会互相取消（踩过两次）。

### 6.2 构建内存（ADR-0011 / ADR-0012）

- 模型：`峰值 ≈ 0.80 GB + 10.4 MB × 页面数`（运行期公式渲染）。
- 坑：`.npmrc` 的 `node-options` 对本仓无效（实测 `NODE_OPTIONS=UNSET`）；
  真正生效的是包装器 `packages/tooling/bin/vitepress-with-heap.mjs` 与 workflow 级 env。
- 新分册接入后先跑 `build_memory_budget.py` 估预算。

### 6.3 上线后体检

```bash
python packages/tooling/src/check_live_site.py --base https://gold99lt.github.io/lubook/<slug> --app <app> --check-assets
python packages/tooling/src/check_live_site.py --base https://lubook.pages.dev/<slug> --app <app> --check-assets
```

判据：路由全 200、有 `<title>`、同源资源全 200。**必须两边都跑**。

---

## 7. 常见失败模式（照单核对，别再踩）

| # | 现象 | 根因 | 对策 |
|---|---|---|---|
| F1 | 门禁全绿但线上公式全乱 | 旧门禁不编译公式 | 把 `scan_math.py` 纳入 `verify:all` |
| F2 | 线上两张图裂开 | SVG 里有裸 `&`/`<`，或带 BOM | `scan_svg_order.py` + `ET.parse` 校验 |
| F3 | 修完公式，正文结论还是错的 | 只修了语法没复算 | §5 复算协议 |
| F4 | "加了 `.npmrc` 就好了" | 实测没生效，只是内容还小 | 用包装器 + workflow env，见 §6.2 |
| F5 | 构建神秘 OOM | 构建期渲染 4 万公式 | ADR-0012 运行期渲染 |
| F6 | 两条流水线互相取消 | 并发组只按 ref | 组名带 `github.workflow` |
| F7 | 跑完审查仓库多出 `verify*.py` | 智能体的临时复算脚本 | 审查后 `git status` 检查；只 `git add` 明确文件，少用 `git add -A` |
| F8 | 把死链改得更糟 | 代理导致 404 不可信 | 只替换"能复现 200"的地址；否则留编号 |
| F9 | 归档链接指向错文档 | 只看标识符不看 metadata | 改指前必须查 title/access 字段 |
| F10 | 替换后出现"纠正一处一些资料写法"病句 | 批量替换叠加 | 替换表按长串优先排序；替换后扫叠加痕迹 |
| F11 | 智能体互相取消/超时 | 一次派太多或任务过大 | 每批 ≤6 章，失败就重派 |
| F12 | 内容改了但 manifest 不过 | 未更新基线 | `freeze_manifest.py --accept`（先确认 diff 是有意的） |

---

## 8. 交付定义（DoD）

一个分册"可交付"必须同时满足：

- [ ] `pnpm verify:all` 退出 0（含构建、产物契约、质量、离线、学习单测）
- [ ] 路由快照零差异；manifest 对账一致
- [ ] `check-content.py` 全部分册通过（速查档用 `--profile quick`）
- [ ] 审查报告存在，确认错误已修、存疑已记录
- [ ] 双站部署成功；`check_live_site.py` 两边 0 失败
- [ ] `CURRENT-STATE.md` 与 `docs/adr/` 已更新
- [ ] 用户确认（涉及上线/拓扑/新分册）

---

## 9. 命令速查

```bash
# 开发
pnpm dev:<app>                 build:<app>            preview:<app>

# 门禁
pnpm verify:all                # 全量（构建+质量+离线+单测）
pnpm quality:<app>             # 仅质量
python scripts/check-content.py --app <app> --profile all --dir <篇>
python packages/tooling/src/build_memory_budget.py --src apps/<app>/docs --heap-mb 8192

# 内容维护
python packages/tooling/src/scan_math.py --src apps/<app>/docs
python packages/tooling/src/scan_legacy_errors.py --app <app>
python packages/tooling/src/scan_orphan_assets.py --app <app>
python packages/tooling/src/check_sources_online.py --app <app>

# 台账
python packages/tooling/src/freeze_manifest.py --app <app> --accept   # 内容变更后
python packages/tooling/src/build_single_html.py --app <app> --manifest .generated/<app>-content-manifest.json

# 上线后
python packages/tooling/src/check_live_site.py --base <url> --app <app> --check-assets
```

---

## 10. 新分册接入清单（S1 检查表）

1. `cp -r templates/site-template apps/<app>`，改 `package.json` 的 name 为 `@lubook/<app>`。
2. `content.config.ts` 填 `appId`、篇注册表、标题；`docs/.vitepress/config.mts` 用 `defineBookConfig`。
3. 根 `package.json` 增加 `dev/build/preview/quality/freeze/offline:<app>` 六个脚本。
4. `docs/SUMMARY.md` 定篇与章；`build_vp_sidebar.py` 生成 sidebar。
5. 门户卡片（`apps/portal` 的 content.config）填 `slug/title/desc/icon`，**未上线先 `available: false`**。
6. 加入 `tests/<app>.routes.snapshot.json` 基线；`verify_all.py` 会自动遍历 `apps/*`。
7. 跑 `pnpm build:<app>` 与 `pnpm verify:all`，再进入 S2。
