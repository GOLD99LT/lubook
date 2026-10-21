# 命名规范（NAMING · 路书 Lubook）

> 状态：**Accepted（2026-10-21 品牌决策已拍板）**
> 本文件是整个项目（仓库、站点、pnpm 包、分册、学习数据键、URL、离线包、域名）的**命名宪法**。新增站点、新建分册/包、改名或部署前，先读本文。
>
> 配套：重命名与多 app 门户拓扑见 [ADR-0006](adr/ADR-0006.md)；多 app 架构见 [ARCHITECTURE.md](../ARCHITECTURE.md)；嵌入式两本分册大纲见 [EMBEDDED_PLAN.md](../EMBEDDED_PLAN.md)。

---

## 1. 品牌

- **中文品牌名：路书**　英文/技术标识：**`lubook`**（全小写、无连字符）。
- **全称/副标题：路先生知识手册**（作者：路先生）。
- 定位：作者个人可持续使用的**多领域知识手册合集**——每个领域是一本"分册"，由一个统一品牌（路书）聚合。
- 为什么是"路书"：①含姓氏"路"；②"路书"本意为指引路线的手册；③暗合电路、工程师成长之路、思路。英文 `lubook` = Lu's book + "路书"。

---

## 2. 命名分层（唯一事实表）

| 层 | 规则 | 当前值 / 示例 |
|---|---|---|
| GitHub 仓库 | `GOLD99LT/lubook`（由 `hardware-handbook` 改名，见 ADR-0006） | `https://github.com/GOLD99LT/lubook` |
| 本地工程根目录 | `<工作区>/lubook` | `E:\001_work\010-Doubao\lubook` |
| 根 pnpm 包名 | `lubook-monorepo` | `package.json` 的 `name` |
| GitHub Pages 主站 | `https://gold99lt.github.io/lubook/` | 门户占根 |
| Cloudflare 镜像项目 | 项目名 `lubook` | `https://lubook.pages.dev/`（根路径） |
| 自定义域名（后续） | 首选 `lubook.dev`（已核实可注册，见 §7） | backlog B16 |
| pnpm scope | `@lubook/*` | `@lubook/theme`、`@lubook/hardware` |
| 站点（分册/门户） | 目录 `apps/<slug>`、包 `@lubook/<slug>`、`appId=<slug>` | `apps/hardware` |
| 门户 | `apps/portal`（路书总入口，**占根**） | base `/lubook/` |
| 分册 URL 子路径 | `/lubook/<slug>/` | `/lubook/hardware/` |
| 中文标题 | 分册保留专业书名 + 页头/页脚"路书"系列角标（见 §5） | 《硬件工程师手册》 |
| 学习数据键 | `lubook.v1.<slug>.learning`（localStorage） | `lubook.v1.hardware.learning` |
| 离线单文件 | `dist/<slug>.html` | `dist/hardware.html` |
| 内容 manifest | `.generated/<slug>-content-manifest.json` | `.generated/hardware-content-manifest.json` |
| 路由/指纹快照 | `tests/<slug>.routes.snapshot.json`、`tests/<slug>.manifest.snapshot.json` | `tests/hardware.routes.snapshot.json` |
| 框架共享包 | 用通用"book"词，不绑品牌：`@lubook/shared-config`、`@lubook/theme`、`@lubook/content-core`、`@lubook/learning`、`@lubook/components`、`@lubook/svg-kit` | 见 §6 |
| 框架工厂/CLI | `defineBookConfig`、`createBookTheme`、CLI bin `book-manifest` | 原 `defineHwConfig`/`createHwTheme`/`hw-manifest` |
| 内容章 slug | 英文 kebab-case，"路径即 id"（沿用，见 ADR-0002） | `opamp/inverting-amplifier` |

---

## 3. slug 规则（新分册 / 新包）

1. 全小写、只含 `[a-z0-9-]`、kebab-case；用**领域词**，不带 `-handbook`/`-book` 后缀（book/lubook 是整个产品名，不属于某个分册）。
2. 尽量短、含义清晰、可长期使用；**一经发布即冻结**——改 slug 等于同时改 URL、目录、包名、学习键、离线名、快照名，必须补 ADR、做数据迁移与重定向。
3. 一个分册的 6 个标识必须**同一名 slug**：目录、pnpm 包、`appId`、URL 子路径、学习键、离线文件名；manifest 与快照文件名也以它派生。
4. 历史例外：硬件分册前身 `appId='handbook'`、占根 `/hardware-handbook/`，重命名时一次性对称化为 `hardware`（见 ADR-0006），此后不再保留历史特例。

---

## 4. 分册目录（规划）

| slug | 中文分册 | 状态 | URL |
|---|---|---|---|
| `portal` | 路书（门户 / 总入口） | 重命名时建**极简版**（品牌 + 分册卡片），后续增强 | `/lubook/` |
| `hardware` | 硬件工程师手册（硬件篇） | 已上线（原 `handbook` 改名，内容零改动） | `/lubook/hardware/` |
| `embedded` | 嵌入式软件开发手册（MCU / Cortex-M） | P4 试点（5 章） | `/lubook/embedded/` |
| `embedded-linux` | 嵌入式 Linux 开发手册（Cortex-A） | P4 与 MCU 并行试点（4 章） | `/lubook/embedded-linux/` |
| 未来候选 | `fpga`、`power-electronics`、`pcb-emc`、`test-measurement`、`signal-integrity`、`algorithms-control` … | 按需立项，走 §6 checklist | `/lubook/<slug>/` |
| 外部独立站点 | 不建 app，在门户以**外链卡片**（必要时 iframe）聚合 | 门户增强阶段 | 外链 |

> 门户卡片分两类：**内部分册**（同 monorepo，共享主题与学习数据）与**外部站点**（外链 / 嵌入）。你以后做出的其他网站可直接挂进门户。

---

## 5. 中文呈现规范

- 门户：`<h1>` 用「路书」，副标题「路先生知识手册」。
- 各分册：保留**专业书名**（如《硬件工程师手册》《嵌入式软件开发手册》），在导航栏 / 页头 / 页脚显示统一的「路书」系列角标并回链门户（角标链接到 `/lubook/`）。
- 浏览器 tab 标题：`分册书名 · 路书`（如 `硬件工程师手册 · 路书`）。
- 若日后想改为强系列化（如「路书 · 硬件篇」），只改各分册 `content.config.ts` 的 title/角标，**不影响 slug/URL**。

---

## 6. 共享包（packages/）命名

| 包 | 职责 | 命名 |
|---|---|---|
| `@lubook/shared-config` | VitePress 通用 markdown/搜索/插件工厂，导出 `defineBookConfig` | 原 `@hw/shared-config` |
| `@lubook/theme` | 布局、品牌、学习 UI、ECharts、图片查看器，导出 `createBookTheme` | 原 `@hw/theme` |
| `@lubook/content-core` | 内容 manifest / 路由 / 校验，CLI bin `book-manifest` | 原 `@hw/content-core` |
| `@lubook/learning` | LearningRepository：appId 隔离、迁移、导入导出、tombstone | 原 `@hw/learning` |
| `@lubook/components` | Vue 交互组件（题库、计算器、仿真容器等，P5 起） | 占位 |
| `@lubook/svg-kit` | 原理图 SVG 元件 / 图标库（后期从 tooling 拆） | 占位 |
| `@lubook/tooling` | Python 质检 / 离线 / 脚手架（无 npm 包，目录名） | 目录 `packages/tooling` |
| 新增 | 命名 `@lubook/<能力>`（如 Mermaid 封装 `@lubook/diagram`），能力名用通用词 | 按需 |

新增包规则：能力名小写、kebab-case、通用词（不绑某一分册、不绑个人品牌）；只有分册本身才用领域 slug。

---

## 7. 域名规划

- **本期（零成本）**：GitHub Pages `gold99lt.github.io/lubook/` + Cloudflare `lubook.pages.dev`（国内镜像）。
- **后续（已登记 backlog B16）**：注册自定义域名，首选 **`lubook.dev`**（2026-10-21 RDAP 核实可注册；备选 `lubook.io`，亦可注册）。挂上自定义域后，门户 `lubook.dev/`、分册 `lubook.dev/<slug>/`，**此后再改仓库名也不影响对外链接**。
- `lubook.com` 已被 GoDaddy 停放（2021-01 注册、2028-01 到期、HTTP 200 但无实际内容），**不建议溢价收购**。
- 域名相关任务（注册、DNS、Pages/Cloudflare 自定义域、HTTPS 证书）统一在 B16 触发时单独立项并补 ADR。

---

## 8. 命名冲突核查记录（2026-10-21）

| 检查项 | 结果 |
|---|---|
| 商标 / 知名产品 | 无知名商业产品或商标。仅一个越南开发者已停服的同名个人练手项目（Lubook，2024）；近似拼写 LiBook 为 iOS 阅读器，不构成撞名。 |
| `lubook.com` | 已注册（GoDaddy 停放空页，无实际业务）。 |
| 其他后缀 | `.io/.dev/.app/.net/.me/.tech/.co/.org/.xyz/.fun` 经 RDAP 核实**均可注册**。 |
| GitHub 用户名 `lubook` | 被一个空账号占用（0 仓库、0 星，弃号）；不影响在 `GOLD99LT/lubook` 建仓。 |
| npm scope `@lubook` | 下挂 0 个已发布包，干净；私有 workspace 本就无需注册 npm。 |
| GitHub Pages / Cloudflare | `gold99lt.github.io/lubook/` 可用；`lubook.pages.dev` 部署时分配，若被占退 `lubook-hub`。 |

---

## 9. 变更规则

- 本表中**对外可感知**的命名（URL、localStorage 键、仓库名、包名、域名、内容 id）一旦发布即冻结；任何变更必须：补 ADR → 提供数据迁移/重定向 → 更新本文与 PLAYBOOK/ARCHITECTURE。
- 纯内部、用户不可见的命名（如某个工具函数名）可按正常重构调整，但需同步更新引用与文档。
- 每个分册的 `content.config.ts` 是其 slug/title 的唯一声明处；脚本与 CI 不硬编码分册列表，统一以 appId 派生。
