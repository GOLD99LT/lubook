# 变更日志（Changelog）

遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式；本项目遵循语义化版本。

## [Unreleased] — 品牌重命名为「路书 Lubook」与多 app 门户拓扑（ADR-0006，2026-10-21，分支 `refactor/brand-lubook`，基线 tag `pre-brand`；待用户核实，未 push）

> 内容（140 章 md / 411 SVG）**零改动**，仅 `git mv`；内容 revision 改名前后均为 `sha256-361225735a3a67f4`。

### 新增（Added）

- 极简门户 `apps/portal`（`@lubook/portal`，占根 base）：品牌「路书」+ 副标题「路先生知识手册」+ 分册卡片网格；卡片在门户 `content.config.ts` 的 `PORTAL_CARDS` 集中声明（internal/external；hardware 可用，embedded/embedded-linux 显示「即将上线」占位）。
- 品牌资产：`BrandMark`（路书 mark）、`BookIcon`（分册线性图标）、`PortalLayout`/`PortalHome`、分册「路书」角标回链 `BackToPortal`；favicon/logo 更新为路书品牌。
- 工具链：`build_pages_bundle.py`（按 `VP_BASE` 组装门户+各分册为一个可整体部署目录）、`verify_all.py`（遍历 apps）、`sync_public.py`（门户品牌资产同步）。
- 学习数据 per-app `legacyKeys` 多源迁移；新键 `lubook.v1.<slug>.learning`。

### 变更（Changed）

- pnpm scope `@hw/*` → `@lubook/*`；根包 `hardware-handbook-monorepo` → `lubook-monorepo`。
- 框架工厂/CLI：`defineHwConfig`→`defineBookConfig`、`createHwTheme`→`createBookTheme`、bin `hw-manifest`→`book-manifest`。
- `apps/handbook` → `apps/hardware`（558 rename 全 R100）；包 `@lubook/hardware`、`appId` `handbook`→`hardware`；中文书名《硬件工程师手册》保留。
- base 由 `VP_BASE` 派生（门户=`VP_BASE`，分册=`VP_BASE<slug>/`）；run_quality/离线/快照均按 app 参数化（`tests/<app>.*.snapshot.json`、`dist/<app>.html`）。
- 社交链接改 `GOLD99LT/lubook`；离线导出文件名按 app 化（`<appId>-learning-…`）。
- CI：`quality.yml` 多 app 矩阵；`deploy-docs.yml` 用 bundle（`VP_BASE=/lubook/`）+ 部署后 HTTP smoke；`deploy-cloudflare.yml` 用 bundle（`VP_BASE=/`）+ `--project-name=lubook`。

### 修复（Fixed）

- 窄屏（≤640px）多列表格被挤压逐字折行：表格改为横向滚动容器、每列保底 108px（完成既有「表格移动端横向滚动」意图；纯主题 CSS，内容指纹不变）。

### 不变（Preserved）

- 140 章 md 与 411 SVG 归一化 LF 后与 pre-brand(`ff8da96`) 逐字一致；revision `sha256-361225735a3a67f4`（140/418/411，grounds 247，routes 141）。
- 旧学习键 `hh.v1.learning`、`hb.v1.handbook.learning` 迁移后保留不删；learning 单测 43 passed。

## [0.2.0] — Monorepo 重构 v2（已合并 `main` 并部署上线，2026-10-14，main `9cbeb4a`；开发分支 `refactor/monorepo`，基线 tag `pre-monorepo`）

> 内容（140 章 md / 411 SVG）**零改动**，仅 `git mv`；已发布 URL 全部保持不变。

### 新增（Added）

- pnpm workspace 骨架：`apps/*`、`packages/*`、`templates/*`，根 `package.json`/`pnpm-workspace.yaml`/`.npmrc`/`.node-version`/`tsconfig.base.json`。
- 共享包：
  - `@hw/shared-config`：`defineHwConfig` 工厂（五类容器、KaTeX、CJK 强调、折叠题、ECharts、图片 figure、面包屑、中文本地搜索等通用规则）。
  - `@hw/theme`：`createHwTheme({catalog, repository, logo?})`；布局/品牌/学习 UI/EChart/图片查看器，解耦为注入 `CatalogProvider` 与 `LearningRepository`。
  - `@hw/content-core`：TS 版内容 manifest 生成器（与 Python 逐字一致，含 parity），CLI 另输出纯数据 `catalog.generated.mjs`。
  - `@hw/learning`：`LearningRepository`，按 appId 隔离、一次性迁移旧键、导入导出（merge/replace）、未知章 tombstone（40 项单测）。
  - `packages/tooling`（Python，非 npm 包）：参数化的离线构建/质检/vendor，`build_single_html.py` 支持 `--manifest` 对账。
- `templates/site-template`：与正式 app 同形态的最小可构建脚手架（空 app 可过构建）。
- 冻结基线：`tools/freeze_manifest.py`（P0，后随 tooling 平移）、`tests/routes.snapshot.json`（141 URL）、`tests/manifest.snapshot.json`（内容指纹）。
- 仓库根 `run_quality.py` 统一质量门禁；`THIRD_PARTY_LICENSES.md` 与依赖审计结论。
- CI：新增 `.github/workflows/quality.yml`（分支/PR 全量门禁，含空 app 构建）。
- 活文档：`docs/PLAYBOOK.md`、`docs/adr/ADR-0001~0005`、`CONTRIBUTING.md`、根 `AGENTS.md`。

### 变更（Changed）

- 内容从根 `docs/` 经 `git mv` 迁至 `apps/handbook/docs/`（554 个文件，仅 rename）；主题迁至 `packages/theme`；脚本迁至 `packages/tooling`。
- 手册 app 改为薄 `config.mts` + `content.config.ts`（part registry、站点元数据、学习仓储装配）。
- 部署工作流（Pages / Cloudflare）改为 pnpm + `pnpm --filter @hw/handbook docs:build`，dist 路径改为 `apps/handbook/docs/.vitepress/dist`。
- 学习数据键从全局 `hh.v1.learning` 迁移为按 app 的 `hb.v1.handbook.learning`（旧键保留）。

### 修复（Fixed）

- 修复内容指纹跨平台不一致导致的 Linux 质量门禁失败：`.gitattributes` 为 `* text=auto`，Windows 工作区检出为 CRLF、GitHub Actions（Linux）检出为 LF，而 content-core(TS) 与 freeze_manifest(Python) 此前对文件**原始字节**做 sha256，使同一份逻辑内容在两平台算出不同 revision。修复为在哈希前统一把 CRLF/CR 归一为 LF（与仓库 blob 一致）；修复后 Windows TS、Windows Python、Linux CI 三端指纹一致为 `sha256-361225735a3a67f4`，`tests/manifest.snapshot.json` 已据此重新冻结（routes 不变）。

### 不变（Preserved）

- 全部已发布 URL（路由快照 141=141，零差异）；140 章正文与 411 张 SVG 逐字节零改动（100% rename）。跨平台稳定指纹 revision `sha256-361225735a3a67f4`（重构过程中的 `sha256-4c8521761e575941` 仅为 Windows CRLF 工作区值，已由换行归一化取代，逻辑内容相同）。
- 在线 VitePress 与离线单文件双形态；离线构建零第三方 Python 依赖。
- 在线构建 0 错误；离线 140 章、0 图片缺失、manifest 对账一致。

## [0.1.0] — 2026-10（已上线基线，main `3205604` / tag `pre-monorepo`）

- 单目录 VitePress 文档站上线：140 章（10 篇 + 附录）、411 张 SVG、93 个 ECharts 围栏、996 个五类容器、618 个折叠题。
- 在线站（GitHub Pages，Cloudflare 镜像）与离线单文件 HTML（`dist/hardware-handbook.html`）共用同一批 Markdown。
- 学习功能：在学/已学、收藏、章末笔记、导入导出（localStorage `hh.v1.learning`）。
- 四类质检脚本：validate / scan_math / scan_grounds / scan_svg_order。
- 代码 MIT、文档 CC BY-SA 4.0。
