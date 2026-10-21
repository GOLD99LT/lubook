# 硬件工程师手册 · 需求整理与现状功能（REQUIREMENTS）

> 版本：v1（2026-10-13）
> 用途：一份文档看清"你要什么（需求）"与"现在已经有什么（功能）"，作为后续 Monorepo 重构与功能扩展的需求基线。
> 配套文档：`ARCHITECTURE.md`（怎么演进）、`docs/PLAYBOOK.md`（重构后落地，怎么操作）。
> 状态标签：【已完成】【已规划·待执行】【待启动】【待办】

---

## 一、项目定位

一个**开源、可交互、可持续更新**的硬件工程师学习体系：以 Markdown 为唯一事实源，体系化覆盖电路基础 → 元器件 → 模拟/运放 → 数字 → 单片机 → 电源 → PCB/EMC → 工程实践 → 面试题库；以静态站点交付，配套离线单文件；未来在同一仓库内**聚合多个专项**（首个为《嵌入式软件开发手册》）。

- 仓库：https://github.com/GOLD99LT/hardware-handbook
- 主站：https://gold99lt.github.io/hardware-handbook/
- 国内镜像：https://hardware-handbook.pages.dev/
- 许可：代码 MIT，文档 CC BY-SA 4.0

---

## 二、需求整理（按主题，含状态）

### 1. 内容与质量（长期）

| 需求 | 状态 | 说明 |
| --- | --- | --- |
| 体系化硬件手册（8 篇 + 题库 + 附录，140 章） | 【已完成】 | 原理图、公式推导、设计示例、面试题库成体系 |
| 教学化内容方言（动机/类比/示例/坑/进阶） | 【已完成】 | 五类容器 996 处，统一视觉与阅读节奏 |
| 重点电路扩展与变种 | 【已完成】 | 运放篇 33 章新增 105 个扩展电路、105 张 SVG |
| 原理图统一绘制规范（接地三线标准等） | 【已完成】 | 247 处接地符合 (28/18/10)、间距 7、线宽 2.4 |
| 章节可持续追加 | 【已完成】 | 新增章 = 写 md + SUMMARY 加一行，构建零硬编码 |
| 题库深度再挖掘、附录开源作品赏析扩充 | 【待启动】 | 站点稳定后的内容侧待办 |

### 2. 成品网站与交付形态

| 需求 | 状态 | 说明 |
| --- | --- | --- |
| 可在线访问的成品文档站 | 【已完成】 | VitePress 构建，GitHub Pages + Cloudflare 双线上 |
| 国内访问顺畅 | 【已完成】 | Cloudflare Pages 镜像，实测 200 |
| 离线可分发单文件 | 【已完成】 | 纯标准库 Python 构建，内联 KaTeX/ECharts/字体，零依赖 140 章 |
| 自动化部署 | 【已完成】 | push main 自动构建 GitHub Pages |
| 学习进度/收藏/笔记与跨设备迁移 | 【已完成】 | localStorage 存储，JSON 导出/导入 |
| 交互功能扩展（仿真、题库、计算器、评论等） | 【已规划】 | 想法 3，排在重构与活文档之后（阶段 5），见第六节 |

### 3. Git / 多机协作（想法 1）

| 需求 | 状态 | 说明 |
| --- | --- | --- |
| 不再依赖令牌（PAT） | 【已完成】 | GCM 浏览器 OAuth，主力机首次 push 已授权，凭据缓存 |
| 多机同步顺畅 | 【已完成】 | 工程已从旧机 BOOM 克隆到主力机 LBH 并验证可构建 |
| 跨平台换行统一 | 【已完成】 | `.gitattributes` 入库，仓库内统一 LF、二进制受保护 |
| 协作默认项 | 【已完成】 | pull.rebase、默认 main、自动建立上游 |
| 撤销旧 PAT | 【待办】 | 你手动到 https://github.com/settings/tokens 检查并撤销 |

### 4. 多专项生态与聚合（想法 2 · 核心）

| 需求 | 状态 | 说明 |
| --- | --- | --- |
| 支持长期持续更新、可升级的架构 | 【已规划·待执行】 | Monorepo 方案 `ARCHITECTURE.md` 已出，待你核对 |
| 主题/组件/工具/质检跨专项复用 | 【已实现】 | 抽为 `@lubook/theme`、`@lubook/shared-config`、`packages/tooling` |
| 新专项低成本落地 | 【已规划】 | 复制 `templates/site-template` + 写 Markdown |
| 第一个新专项：**嵌入式软件开发手册** | 【已规划·阶段 4】 | 目录 `apps/embedded`，固件/驱动/RTOS/构建/嵌入式 Linux |
| 软硬件一体专项 | 【已规划·更后】 | 目录 `apps/hwsw`，硬件 + 软件联调方向 |
| 顶层学习门户聚合各专项 | 【已规划·2 个专项后】 | 目录 `apps/portal`，原则：手册现有 URL 永不变 |
| 异构外部网站嵌入 | 【已规划】 | 门户卡片 / iframe 仅展示，不做深度集成 |
| 全站聚合搜索、学习进度云同步 | 【待启动】 | 云同步需评估是否引入后端；聚合搜索阶段 6 |
| 英文版 | 【待启动】 | 后期 |

### 5. 工作流与知识沉淀（想法 2）

| 需求 | 状态 | 说明 |
| --- | --- | --- |
| 把建站全过程/操作/故障沉淀为可复用工作流 | 【已规划·阶段 3】 | 三层活文档，随重构落地 |
| 文档随项目持续同步更新 | 【已规划】 | PLAYBOOK（现状）+ ADR（决策只追加）+ CHANGELOG（变更） |
| 强制文档与代码同步 | 【已规划】 | CONTRIBUTING/AGENTS 规则 + CI 门禁 + 多智能体收尾动作 |
| 下次类似需求可一句话调用 | 【已规划】 | 两个专项验证稳定后，由 PLAYBOOK 派生豆包 Skill |
| 建站方案文档 | 【已完成】 | `WEBSITE_PLAN.md`；`AGENTS.md` 协作约定 |

---

## 三、现状功能清单（已上线、实测可用）

### 3.1 内容资产规模（截至 2026-10-13 实测）

| 篇目 | 章节数 |
| --- | --- |
| 第一篇 电路基础 basics | 14 |
| 第二篇 元器件详解 components | 13 |
| 第三篇 模拟电路与运放 opamp | 33 |
| 第四篇 数字电路与逻辑 digital | 12 |
| 第五篇 单片机与嵌入式硬件 mcu | 13 |
| 第六篇 电源设计 power | 12 |
| 第七篇 PCB 设计与 EMC pcb | 13 |
| 第八篇 测量、调试与工程实践 practice | 12 |
| 第九篇 硬件测试与面试题库 quizbank | 9 |
| 附录 appendix | 9 |
| **正文合计** | **140 章** |

- 原理图 SVG：**411 张**（`docs/assets/schematics`）
- 交互图表：**93 个** ECharts 围栏块
- 五类教学容器：**996 处**
- 原生折叠题：**542 个**（答案折叠、点击即看）
- 数学公式：**153 组**块公式 + 约 **3400 处**行内公式
- 文中图片引用：**418 处**

### 3.2 阅读与交互功能

- **导航**：顶部 nav（开始学习 / 工程速查 / 面试刷题 / 附录）、GitHub 链接、上一章/下一章、本页大纲、clean URLs。
- **全文搜索**：VitePress 本地搜索（minisearch），中文界面翻译，可按知识点/公式/元器件名检索。
- **暗色主题**：亮/暗模式切换（代码高亮 github-light/dark）。
- **首页**：Hero 三入口（开始学习/工程速查/面试刷题）、6 张学习路径卡片（内联 SVG 线性图标：零基础、电源/PCB、数电/MCU、工程实战、面试题库、工程速查）、我的学习面板、全书导航（八篇+题库+附录）、许可说明。
- **学习系统**（localStorage，本地持久化）：
  - 章节进度（未学 / 学习中 / 已学）、完成度百分比统计；
  - 章节收藏、章节笔记；
  - 侧边栏进度指示、首页学习面板；
  - 学习数据 JSON 导出 / 导入（换机/备份）。
- **面包屑与徽章**：每页顶部"篇 / 章"面包屑，难度徽章（入门/进阶/深入）与标签。
- **数学公式**：KaTeX 块/行内渲染、本地字体离线可用；针对中文紧贴单位（如 `μs`、`V`）放宽行内规则。
- **五类容器**：设计动机、直觉类比、设计示例、常见坑、进阶内容（可跳过，折叠呈现）。
- **折叠题**：`<details>` 内的公式、加粗、列表等 Markdown 正常渲染。
- **ECharts 交互图表**：用 ```` ```echarts ```` JSON 围栏直接在 Markdown 中声明。
- **图片**：段落单图自动 figure 化、带图注；点击图片全屏放大（Esc/点击关闭）。
- **响应式**：桌面/移动适配，移动端抽屉菜单、无横向溢出。

### 3.3 工程与交付能力

- **双形态构建**：
  - 在线：`vitepress build docs`（多页静态站，0 错误）；
  - 离线：`tools/build_single_html.py`（Python 纯标准库，内联 vendor，零第三方依赖产 140 章单文件）。
- **侧边栏自动装配**：`build_vp_sidebar.py` 从 `SUMMARY.md` 生成侧边栏并同步品牌资源，零硬编码。
- **质检脚本**（Python 标准库）：
  - `validate.py` 结构/引用校验（硬错误 0，仅首页孤儿告警）；
  - `scan_math.py` 公式裸串扫描（0）；
  - `scan_grounds.py` 接地符号规范（247 处合规）；
  - `scan_svg_order.py` SVG 根节点顺序（411 张 OK，0 坏）；
  - 配套 `fix_grounds.py`、`fix_math.py` 自动修复。
- **CI/CD**：`.github/workflows/deploy-docs.yml`（push main 自动部署 Pages）；Cloudflare 镜像经 `VP_BASE=/` 构建。
- **内容工程约定**：Markdown 唯一事实源；文件路径 = 稳定 id；SUMMARY 装配；frontmatter 宽松修复；CJK 加粗/折叠/figure 等中文排版修复。

### 3.4 技术栈

- 构建：VitePress 1.6.x（Vue 3）、Vite。
- 渲染：KaTeX 0.16.11、ECharts 5.5.1、@vscode/markdown-it-katex、markdown-it-container。
- 离线/质检：Python 3（标准库，仅 sources 合并用 PyYAML）。
- 托管：GitHub Pages（项目子路径 `/hardware-handbook/`）+ Cloudflare Pages（根域镜像）。

---

## 四、需求 ↔ 现状 覆盖矩阵

| 需求 | 当前状态 | 由谁满足 |
| --- | --- | --- |
| 体系化硬件内容、原理图、公式、题库 | 已满足 | 140 章内容 + 411 SVG + 容器/题库 |
| 在线 + 离线双形态阅读 | 已满足 | VitePress + build_single_html |
| 学习进度/收藏/笔记/迁移 | 已满足 | 学习组件 + 导入导出 |
| 免令牌多机协作 | 已满足 | GCM + .gitattributes |
| 多专项复用与聚合 | 未满足 | **阶段 2 Monorepo 重构**（ARCHITECTURE） |
| 工作流活文档 | 部分满足 | 阶段 3 PLAYBOOK + ADR + CHANGELOG |
| 嵌入式等新专项 | 未满足 | 阶段 4 模板起 apps/embedded |
| 仿真/题库组卷/计算器/评论/PWA | 未满足 | 阶段 5 共享组件 packages/components |
| 门户/聚合搜索/云同步/英文版 | 未满足 | 阶段 6 |

---

## 五、明确边界（当前不做什么）

- 重构阶段内容文件**只移动、不改动**；不牺牲现有章节 URL。
- 阶段 5 之前不实现电路仿真/题库组卷等交互功能（只做方案规划）。
- 不做后端、不做账号体系（学习进度仍为本地存储，云同步到阶段 6 再评估）。
- 门户在有 2 个专项之后再做。
- 异构外部站点只做卡片/iframe 展示，不做深度数据集成。

---

## 六、想法 3（功能扩展）已调研清单——仅规划，待阶段 5

- **硬件杀手锏**：CircuitJS/Falstad（浏览器内电路仿真，可 iframe、电流动画，适合模电/运放/电源）；Wokwi（Arduino/ESP32/STM32/Pico 浏览器仿真，适合单片机/嵌入式）。
- **学习闭环**：题库随机组卷/计分/错题本、间隔重复（SRS）、Anki 导出、在线计算器（运放增益/分压/RC/Buck/色环/E 系列/单位换算）。
- **呈现与社区**：Mermaid + Markmap（流程图/脑图）、Giscus（基于 GitHub Discussions 的评论/勘误）、PWA（离线安装）、打印/PDF、CHANGELOG/RSS、"在 GitHub 编辑本页"、隐私统计、多语言、Pagefind 强搜索（当前内置 minisearch 够用，列后期）。
- 建议落地批次：第一批 CircuitJS + 题库错题本 + Giscus + Mermaid/脑图；第二批 计算器 + Wokwi + PWA + PDF；第三批 SRS + Anki 及其他。

---

## 七、待办与待决策

1. 【已完成】Monorepo v2（P0–P3）已合并并部署上线（GitHub Pages + Cloudflare），main 与 origin 同步；后续在其上迭代。
2. 【待办】你手动检查并撤销旧 PAT。
3. 【已定】新专项：《嵌入式软件开发手册》（MCU，`embedded`）与《嵌入式 Linux 开发手册》（`embedded-linux`），先做共享地基再并行（见 EMBEDDED_PLAN）。
4. 【已定·待核实执行】品牌定为「路书 Lubook」，命名规范见 [docs/NAMING.md](docs/NAMING.md)；品牌重命名 + 多 app 门户拓扑方案见 [ADR-0006](docs/adr/ADR-0006.md)，待你核实后执行。
5. 【后续任务】注册/配置自定义域名（首选 `lubook.dev`），见附录 A B16。
6. 【后期再议】学习进度上云、英文版范围。

---

## 附录 A：外部评审（Codex R1）建议处置台账（Backlog · 由你日后逐项评审）

> 说明：本台账记录 Codex R1《平台级架构重设计》中**未在 v2 本版实施**、但有价值的建议。每条标注价值、暂缓理由、建议评估时机与初步规模；你评审为"做"时，按流程立项并补 ADR。**本版已采纳**的建议（路由快照、内容 manifest、统一 verify、part registry、学习仓储接口、迁移加固、merge/replace、tombstone、导出 contentRevision、包边界、.generated、release.json、部署 smoke、ADR 触发、依赖审计、许可证清单、资源本地化）已写入 `ARCHITECTURE.md` v2，不再列入 Backlog。

| ID | 建议 | 价值 | 暂缓理由 | 建议评估时机 | 初步规模 |
| --- | --- | --- | --- | --- | --- |
| B1 | 离线包改为**消费 VitePress 已渲染产物**，不再用 Python 自解析 Markdown | 彻底消除在线/离线两套 Markdown 解析分叉 | 多页 SPA 合并为单文件有技术难点，Python 零依赖已稳定且经质检对账 | P4 前后做一次**非阻塞 POC**，验证 KaTeX/ECharts/学习组件合并后可用再决定 | 中（需 POC） |
| B2 | 独立稳定 `id` 与文件路径解耦 | 章节改名/移动时学习数据与外链不断、可重定向 | 需回填或生成 140 章 id，本版要求内容零改动；路径即 id 已能满足现状 | 出现首次大规模改章/移动，或做云同步前 | 中 |
| B3 | 文档状态 `draft/technical-review/editorial-review/published/deprecated` 全状态机 + 草稿不进生产 + 墓碑页/重定向 | 多人协作、灰度发布、废弃内容治理 | 个人 + AI 维护，正式流程过重；本版仅保留可选 status 字段 | 开始多人协作或频繁先写草稿再发布时 | 中 |
| B4 | 结构化来源/版权模型（type/license/retrievedAt/usedFor/本地摘要）+ 第三方素材独立许可证清单 | 避免 CC BY-SA 内容与代码/字体/素材许可证混淆 | 现有 sources.list.yaml 与 THIRD_PARTY_LICENSES.md 已覆盖基础；结构化需改 frontmatter | 引入新的第三方素材（仿真器/字体/图库）或对外分发前 | 小–中 |
| B5 | 机器可读 review 索引（章节/严重度/修复提交/复核提交/最终状态）+ CODEOWNERS | 把多篇"PASS 报告"聚合为发布条件 | 单人项目无多 reviewer，CODEOWNERS 意义不大 | 出现稳定协作团队或对外正式发布质量要求时 | 中 |
| B6 | 学习存储从 localStorage 迁到 **IndexedDB** | 承载长笔记、题库作答记录、仿真数据等大数据 | 当前进度/收藏/短笔记数据量小；IndexedDB 带来异步/SSR 复杂度 | 阶段 5 题库/仿真上线、数据量明显增大时 | 中（仓储接口已就绪，仅换实现） |
| B7 | 学习数据**云同步**（provider 接口、冲突策略、updatedAt/deviceId/revision、多端合并） | 多设备进度/笔记一致 | 需引入账号与后端，违背本阶段"无后端"边界 | 明确多端刚需且愿意维护后端时（评估 BaaS/自建） | 大 |
| B8 | **构建一次、多处发布**：同一 artifact + release.json 发 GitHub Pages 与 Cloudflare（wrangler/pages deploy） | 消除两平台各自构建导致的漂移 | 需 Cloudflare API token 与 CI 改造；短期已用 release.json/快照对账 | P4 前或你方便提供 Cloudflare API token 时 | 中 |
| B9 | Playwright 端到端冒烟 + **axe 无障碍**（alt、焦点陷阱、Logo aria、键盘关闭） | 关键路径与无障碍回归自动化 | 本版已用截图人工/脚本复核；自动化 e2e 需持续维护 | 功能增多（交互组件上线）后再建自动化基线 | 中 |
| B10 | 安全基线：CSP 白名单、Markdown 危险 HTML 清理、ECharts option 字段白名单 | 引入外部内容（Giscus/仿真器）时防注入 | 当前资源全本地化、ECharts 为作者自写，无外部输入风险 | 阶段 5 接入 Giscus/统计/仿真器等外部来源时 | 小–中 |
| B11 | 依赖漏洞 high/critical 阻断 + 自动更新（dependabot/renovate） | 持续安全基线 | 本版先做一次依赖审计与记录；自动 PR 需投入跟进 | 依赖变多或接入 Dependabot 后 | 小 |
| B12 | 构建缓存按 `内容 checksum + lockfile + toolchain 版本` 失效 | 多站/多包构建提速与稳定 | 单站阶段构建仅约 30s，收益不明显 | 多专项导致构建变慢时 | 中（可配 Turborepo） |
| B13 | PR 预览环境（每个 PR 一个可点链接）+ 部署 OIDC/最小权限 | 合并前可视化评审、收敛凭据 | 个人项目当前直接 push main 自动部署；需改 CI 流程 | 多人协作或改动频繁需要预览时 | 中 |
| B14 | frontmatter/学习导出/图表 option 用 **Zod/JSON Schema 强校验** | 数据结构错误在构建期即暴露 | 本版 content-core 先用最小手写校验；引入 Zod 增加依赖 | 字段增多、多专项复用导致结构出错时 | 小 |
| B15 | "五类资产"（知识/编译/产品/工程/信任）模型与发布门禁全面落地 | 每次变更可回答"改了什么/谁审核/如何构建发布回滚" | 平台公司级目标，当前以 manifest + verify + ADR 覆盖关键部分 | 项目从"作品"走向长期产品/团队协作时 | 大（持续） |
| B16 | 注册并配置**自定义域名**（首选 `lubook.dev`，备选 `lubook.io`；2026-10-21 核实可注册）：域名购买、DNS、GitHub Pages CNAME / Cloudflare Pages 自定义域、HTTPS | 域名与仓库名解耦，对外链接稳定、好记、利于长期品牌化；门户占根后再改仓库名也不影响 URL | 免费的 `github.io`/`pages.dev` 已可用；域名购买与 DNS 需你本人操作 | 品牌重命名（ADR-0006）上线后，或希望对外分享稳定链接时 | 小（注册 + 配置） |

> 评审方式：你可逐条回复"B1 做 / B8 暂缓"等；确定做的条目，我会先写 ADR、给出执行方案，再纳入对应阶段。未评审前不实施。
