# 硬件学习生态 · 架构设计与 Monorepo 重构方案（ARCHITECTURE v3）

> 状态：**v3 品牌重命名与多 app 门户拓扑已落地（2026-10-21，ADR-0006 Accepted）**
> 版本：v3（在 v2 Monorepo 基础上完成「路书 Lubook」品牌重命名 + 门户占根/分册居子路径拓扑；v2 由内部方案与外部 Codex R1 评审融合，用户已"全部同意"）
> 决策：1A 2A 3A 4A 5A 6A；并采纳 Codex R1 的路由快照/内容 manifest/统一 verify/学习数据仓储/包边界/发布可追溯；**不采纳** Python→Node 全量重写与 140 章强回填（详见第 14 节"本版明确不做"）。
> v3 命名与拓扑以 [`docs/NAMING.md`](docs/NAMING.md) 与 [`ADR-0006`](docs/adr/ADR-0006.md) 为准：scope `@lubook/*`、根包 `lubook-monorepo`、门户 `apps/portal` 占根、硬件分册 `apps/hardware`、学习键 `lubook.v1.<slug>.learning`。
> 被推迟/待评审的建议见 `REQUIREMENTS.md` 附录 A（Backlog，由用户日后逐项评审）。

---

## 0. 设计立场与不变量

立场：**先在单站冻结可验证基线（路由快照 + 内容 manifest），再搭建 Monorepo 并搬迁，搬迁结果用快照/对账证明零变化；重写类大投入一律推迟。**

不变量（写入 CI，而非仅文档）：

1. 已发布章节的 URL 永久稳定；删除/改名必须经路由快照门禁人工批准并提供 redirect。
2. Markdown、SVG、来源记录是事实源；sidebar、manifest、搜索索引、离线目录均为生成物。
3. 在线站与离线包使用**同一份 `content-manifest.json`** 对账（章节数、标题、图片、资源）。
4. 一次发布对应一个 commit、一个 manifest revision、一份可追溯 release.json。
5. 学习数据按 appId 隔离，可迁移、导出、导入（不误污染）、回滚不丢。
6. 架构/构建/部署/共享包变更必须在同一改动更新文档或补 ADR。
7. 安全、版权、数据迁移、URL 破坏性变更必须先写 ADR。
8. 本阶段内容文件只 `git mv`，不修改内容。

---

## 1. 现状盘点（已核对磁盘，2026-10-14）

- 内容：140 章正文（basics14/components13/opamp33/digital12/mcu13/power12/pcb13/practice12/quizbank9/appendix9）+ 首页 + SUMMARY；411 张 SVG；93 个 ECharts 块；996 处五类容器；542 个折叠题；153 组块公式、约 3400 处行内公式；418 处图片引用。
- 在线：`vitepress build docs`，base 默认 `/hardware-handbook/`，`VP_BASE=/` 覆盖（Cloudflare）。
- 离线：`tools/build_single_html.py`（Python 纯标准库，内联 `tools/vendor`，零依赖）。
- 质检：`validate.py / scan_math.py / scan_grounds.py / scan_svg_order.py`（+ `fix_*`）。
- 主题：`docs/.vitepress/theme/`（index.ts、style.css、EChart、brand、learning 5 个组件）；config.mts 约 440 行，通用规则与手册内容（PART_NAMES/nav/title/base）混杂。
- 学习数据：`store.ts` 硬编码 `STORAGE_KEY='hh.v1.learning'`；catalog 相对路径 import 站点 sidebar。
- CI：`.github/workflows/deploy-docs.yml`（push main 自动）、`deploy-cloudflare.yml`（手动）。
- 包：VitePress 1.6.x、KaTeX 0.16.11、ECharts 5.5.1、markdown-it-container、@vscode/markdown-it-katex。

---

## 2. 目标架构（pnpm Monorepo）

```
lubook-monorepo/                    # 根包（原 hardware-handbook-monorepo）
├─ apps/
│  ├─ portal/                      # 极简门户（占根 base，品牌「路书」首页）
│  │  ├─ docs/
│  │  │  ├─ index.md               # 渲染 PortalHome（品牌 + 分册卡片）
│  │  │  └─ .vitepress/{config.mts,theme/index.ts}
│  │  ├─ content.config.ts         # 集中声明 PORTAL_CARDS（internal/external）
│  │  └─ package.json              # @lubook/portal
│  └─ hardware/                    # 硬件分册（原 apps/handbook，内容零改动）
│     ├─ docs/                     # 140 章 md + 411 SVG + assets + SUMMARY + index
│     ├─ .vitepress/{config.mts,theme/index.ts}
│     ├─ content.config.ts         # appId=hardware、part registry、legacyKeys
│     └─ package.json              # @lubook/hardware
├─ packages/
│  ├─ theme/            (@lubook/theme)        # 布局/品牌/学习 UI/EChart/图片查看器；只依赖接口
│  ├─ shared-config/    (@lubook/shared-config) # defineBookConfig：通用 markdown/搜索/插件工厂
│  ├─ content-core/     (@lubook/content-core)  # manifest/路由快照/校验；CLI bin book-manifest
│  ├─ learning/         (@lubook/learning)      # LearningRepository、legacyKeys 迁移、导入导出
│  ├─ tooling/          (Python，非 npm 包)       # bundle 组装/离线/质检/快照（参数化，读 manifest）
│  ├─ components/                            # 占位：P5 交互组件（仿真/题库/计算器）
│  └─ svg-kit/                               # 占位：原理图元件/接地标准（后期从 tooling 拆）
├─ templates/site-template/                   # 新专项脚手架（空内容也能过 verify）
├─ tests/
│  ├─ fixtures/                     # frontmatter/公式/图表/学习迁移样本
│  ├─ hardware.routes.snapshot.json # 各分册独立 URL 快照（入库，CI 比对基准）
│  └─ hardware.manifest.snapshot.json # 各分册内容指纹（章节数/标题/图片数/checksum）
├─ .generated/                     # 生成物：<app>-content-manifest、sidebar、catalog（不入库）
├─ docs/
│  ├─ NAMING.md  PLAYBOOK.md
│  └─ adr/ADR-0001…0006.md（含 README 索引）
├─ .github/workflows/
│  ├─ quality.yml                   # 多 app 矩阵 + pnpm verify:all 门禁
│  ├─ deploy-docs.yml               # bundle（VP_BASE=/lubook/）+ 部署后 HTTP smoke
│  └─ deploy-cloudflare.yml         # bundle（VP_BASE=/）+ wrangler --project-name=lubook
├─ package.json  pnpm-workspace.yaml  pnpm-lock.yaml  .npmrc  .node-version
├─ ARCHITECTURE.md  REQUIREMENTS.md  CHANGELOG.md  CONTRIBUTING.md  AGENTS.md  README.md
├─ THIRD_PARTY_LICENSES.md         # KaTeX/ECharts/字体等许可证清单
├─ .bundle/  .bundle_test/         # 可整体部署站点目录（不入库）
└─ dist/                           # 离线单文件 <app>.html（不入库）
```

> 本地下划线：门户 `apps/portal` 占根 base；硬件分册 `apps/hardware`。
> 未来：`apps/embedded`（P4 试点 5 章，嵌入式软件开发手册）、`apps/embedded-linux`（P4 试点 4 章，另立第三 app，见 EMBEDDED_PLAN）；更远候选 fpca/power-electronics/pcb-emc/test-measurement/signal-integrity/algorithms-control。

---

## 3. 内容内核（采纳 Codex，做轻量版）

### 3.1 content-manifest.json（两形态共同的单一事实清单）

由 `@lubook/content-core`（CLI bin `book-manifest`）从 `SUMMARY.md` + 各章 frontmatter + 磁盘扫描生成（写入 `.generated/<app>-content-manifest.json`）：

```ts
interface ContentManifest {
  appId: string
  revision: string               // 由内容 checksum 派生
  docs: ContentDoc[]
}
interface ContentDoc {
  id: string                     // 本版 = 相对路径（如 opamp/inverting-amplifier.md）；预留未来独立 id
  path: string
  url: string                    // clean URL
  title: string
  part: string                   # 来自 app content.config 的 part registry（不再写死数字）
  order: number
  tags: string[]
  difficulty?: 1 | 2 | 3
  status?: 'draft' | 'published' | 'deprecated'  // 可选，缺省 published
  images: string[]
  checksum: string               // 自动计算，无需手填
}
```

**本版关键取舍**：
- `id` 直接用相对路径（与现状等价），**不回填 140 章独立 id**；独立 id 与路径解耦列入 Backlog（B2）。
- `status / sources` 为**必填**（与 `validate.py` 一致，见 ADR-0008）；`review` 字段暂不要求。状态机/来源模型列 Backlog（B3/B4/B5）。
- checksum、统计、图片清单由生成器自动计算，**零手工内容改动**。

构建时强校验（立即失败）：id/URL 重复；SUMMARY 有但磁盘无、磁盘有但未登记；文件名-id-URL 不一致；order/part 冲突；`draft` 出现在生产构建。

### 3.2 路由快照（URL 不变的硬门禁）

- `tests/<app>.routes.snapshot.json`：现有全部干净 URL 的排序列表，**P0 冻结入库**（现 `tests/hardware.routes.snapshot.json`）。
- `tests/<app>.manifest.snapshot.json`：章节数、标题序列、图片总数、SVG 数等指纹（现 `tests/hardware.manifest.snapshot.json`）。
- CI / verify：重新生成后与快照 diff，出现删除或变更即失败，需人工更新快照并在 PR 说明（URL 破坏性变更须 ADR）。

### 3.3 生成器演进

- **P0（零依赖、先冻结）**：用 Python 标准库 `freeze_manifest.py` 生成 manifest + 两张快照，立刻拿到回归基线。
- **P1 后**：`@lubook/content-core`（TS）成为 manifest 生成主体，纳入 VitePress 构建；Python 离线/质检**只读 manifest JSON 对账**，不重写 Markdown。

---

## 4. 共享包设计与边界

- `@lubook/shared-config`：`defineBookConfig(options)` 封装五类容器、KaTeX、CJK 加粗、details 折叠、ECharts 围栏、figure 化、frontmatter 修复、本地搜索中文、难度默认名；`options` 含 `appId/title/description/base/sidebar/nav/partRegistry/socialLinks/logo?`。base 由 `deriveBase(appId, VP_BASE)` 派生（门户=VP_BASE，分册=VP_BASE+slug+'/'）。统一设置 `vite.ssr.noExternal=[/@lubook\//]`。
- `@lubook/theme`：布局/品牌/学习 UI/EChart/图片查看器；**只依赖 `CatalogProvider` 与 `LearningRepository` 接口**，不 import 任何 app 的 sidebar；门户用 `createPortalTheme`（`PortalLayout`），分册用 `createBookTheme`（`LayoutBrand`，含「路书」角标回链）。
- `@lubook/content-core`：见第 3 节。
- `@lubook/learning`：见第 5 节。
- `packages/tooling`（Python）：`build_pages_bundle.py`（bundle 组装）、`verify_all.py`（遍历 apps）、`freeze_manifest.py`、`build_single_html.py`、`run_quality.py` 等均按 `--app/--src/--out` 参数化；读 manifest 对账。
- 边界铁律：共享包**不得**读取 `apps/<app>` 私有路径；app 只能通过包 API 使用，不改包内部文件。
- 生成物统一在 `.generated/`（`<app>-content-manifest`、sidebar、catalog），不入库；缓存按 `内容 checksum + lockfile + toolchain 版本` 失效（B12 完整化在 Backlog）。

---

## 5. 学习数据（仓储化 + 迁移加固，本版仍用 localStorage）

- `@lubook/learning` 定义 `LearningRepository` 接口（getChapter/putChapter/export/import），UI 只依赖接口，不直接操作 localStorage。
- 存储 key 按 appId：`lubook.v1.<appId>.learning`（hardware=`lubook.v1.hardware.learning`、portal 无学习数据）。
- 多源迁移（per-app `legacyKeys`，从旧到新）：新键不存在时依次读取旧键、归一化后合并并写新键，**所有旧键保留不删**。
  - hardware 迁移链：`hh.v1.learning`（最早全局键，OldShape，notes 为字符串、无时间戳）→ `hb.v1.handbook.learning`（旧 app 键，PersistedShape）→ `lubook.v1.hardware.learning`。
  - 合并：progress/favorites 后者覆盖前者；notes 按 `updatedAt` 取最新；无时间戳的旧全局笔记标记为最早纪元（`1970-01-01`），不覆盖新来源。
  - 新 app 默认无 `legacyKeys`。
- 导出：
  ```ts
  interface LearningExport {
    schemaVersion: 1; appId: string; contentRevision: string; exportedAt: string;
    progress: Record<string,'learning'|'done'>;
    favorites: Record<string,boolean>;
    notes: Record<string,{ text:string; updatedAt:string }>;
  }
  ```
- 导入：校验 appId/schema/字段类型/笔记长度/文件大小；支持 `merge` 与 `replace` 两种模式；未知章节进入 tombstone，不计入完成率，不产生坏链接。
- 为云同步预留 `updatedAt` 字段。
- **本版不换 IndexedDB**（当前数据量小，localStorage 足够）；IndexedDB 与云同步列 Backlog（B6/B7），届时只换 Repository 实现、不动 UI。

---

## 6. 离线形态

- 保留 Python 标准库零依赖单文件构建（已验证 140 章、0 错误），纳入 `packages/tooling` 参数化：`build_single_html.py --app <app> --manifest .generated/<app>-content-manifest.json`，输出 `dist/<app>.html`（如 `dist/hardware.html`）。
- 离线构建按 `content-manifest.json` 与在线结果对账（章节/标题/图片/资源数量一致）。
- 离线品牌按 app 化（书名/英文标题/系列/存储前缀）；hardware 沿用 storePrefix `hh` 以保留旧离线笔记。
- **不做** Python→Node 全量重写。"离线打包改为消费 VitePress 已渲染产物（而非自解析 Markdown）"列为 Backlog B1，仅允许做一个**不阻塞的 POC**，失败即维持现状。

---

## 7. 统一 verify 与质量门禁

`pnpm verify:all`（`packages/tooling/src/verify_all.py` 遍历 `apps/*`；非内容 app 自动跳过内容检查）每个 app 固定顺序：

1. 工具链/lockfile 版本检查；
2. 构建（`build:<app>`，含 gen sidebar/catalog）；
3. 内容 app：manifest 快照门禁（SUMMARY↔磁盘、id/URL、part、draft 拦截）；
4. 内容 app：本地链接/锚点/资源检查（validate）；
5. 内容 app：SVG XML 与接地规范（scan_grounds、scan_svg_order）；
6. 内容 app：数学/容器/details/ECharts 扫描（scan_math）+ 离线单文件并按 manifest 对账；
7. **路由快照比对（删除/变更必须人工批准）**；
8. 最后跑学习模块单测（`test:learning`）；代表页截图（门户/首页/代表章，桌面/移动，0 console error、无横向溢出）。

本版**不强制** Playwright/axe/CSP（列 Backlog B9/B10，预留挂点）；**低成本先做**：依赖审计（pnpm audit）、第三方许可证清单 `THIRD_PARTY_LICENSES.md`、保持资源本地化（已满足）。

---

## 8. 构建与部署

- 本地：`pnpm install`、`pnpm dev:<app>`、`pnpm build:<app>`、`pnpm verify:all`、`pnpm offline:<app>`。
- **base 由 `VP_BASE` 派生**：门户 base=`VP_BASE`，分册 base=`VP_BASE<slug>/`。
- **bundle 组装**：`build_pages_bundle.py` 按 `VP_BASE` 构建门户与各分册，门户 dist 放输出根、分册 dist 放 `<slug>/`，产出一个可整体上传的站点目录（`.bundle`）。
- GitHub Pages（`deploy-docs.yml`）：`pnpm install --frozen-lockfile` → `pnpm bundle:pages`（`VP_BASE='/lubook/'`）→ 统一 `upload-pages-artifact` 该 bundle；部署后 smoke job 对门户 `/lubook/`、硬件 `/lubook/hardware/`、代表章做 HTTP 200。
- Cloudflare（`deploy-cloudflare.yml`）：`pnpm bundle:cloudflare`（`VP_BASE='/'`）→ `wrangler pages deploy .bundle --project-name=lubook`。
- 中期目标（Backlog B8）：**构建一次、多处发布**——同一 artifact 配 `release.json`（commit SHA、manifest revision、构建时间、Node/pnpm 版本、锁哈希、资源清单）发 Pages 与 Cloudflare（需 Cloudflare API token，届时请用户授权）；部署后跑 HTTP/资源/搜索/旧 URL smoke。

---

## 9. 门户、新专项脚手架与嵌入式手册

`templates/site-template/`：最小可构建 app（index、SUMMARY、示例章、薄 config、content.config、package.json），空内容也能过 `verify:all`。

**门户 `apps/portal`（v3，占根）**：极简首页，品牌「路书」+ 副标题「路先生知识手册」+ 分册卡片网格。卡片在门户 `content.config.ts` 的 `PORTAL_CARDS` 集中声明：
- `internal`：链接到 `<VP_BASE><slug>/`（如 hardware）；`available:false` 渲染非链接占位 +「即将上线」徽章（embedded/embedded-linux）。
- `external`：新标签页外链（本期不实际接外部站）。
- 图标统一内联 SVG 线性图标（`BookIcon`），无 emoji。

**新专项（P4）**：`cp -r templates/site-template apps/<slug>` → 设 `appId`、title、part registry → 写 md+SUMMARY；先做 3–5 章验证 schema、搜索、学习数据隔离（`lubook.v1.<slug>.learning`）、离线包，再在门户卡片置为可用。
- `apps/embedded`（嵌入式软件开发手册，MCU/RTOS，试点 5 章）与 `apps/embedded-linux`（嵌入式 Linux，独立技术栈，试点 4 章）——大纲与边界见 `EMBEDDED_PLAN.md`。

---

## 10. 活文档（6A）

- `docs/PLAYBOOK.md`（现状操作手册，随代码改）、`docs/adr/`（只追加，MADR）、根 `CHANGELOG.md`（Keep a Changelog）。
- CONTRIBUTING/AGENTS 写死：**改架构/构建/共享组件/部署必须同步文档或补 ADR**；不可逆依赖/数据格式/URL/部署拓扑/第三方服务必须 ADR。
- 初始 ADR：0001 采用 pnpm Monorepo；0002 内容 manifest 与"路径即 id"；0003 学习数据仓储与 appId 隔离；0004 双形态共用 manifest 对账；0005 发布制品与 release.json（目标）。
- 豆包 Skill 待 PLAYBOOK 在两个专项验证稳定后派生。

---

## 11. 现状 → 目标 映射（git mv，保留历史）

- `docs/<各篇>`、`docs/quizbank`、`docs/appendix`、`docs/assets`、`SUMMARY.md`、`index.md` → `apps/handbook/docs/…`（P2，内容零改动），v3 再 `git mv` 到 `apps/hardware/docs/…`。
- `docs/.vitepress/theme/**` → `packages/theme/src/**`（通用化）。
- `config.mts` 通用规则 → `packages/shared-config`；手册特有项 → app 的 `config.mts` + `content.config.ts`。
- `tools/*.py` → `packages/tooling/src/`（参数化）；`tools/vendor` → `packages/tooling/vendor`。
- 根 `package.json` 拆为 workspace 根 + app 的 `package.json`。
- 根 `docs/`（内容移走后）→ 活文档。
- 内容文件 Git 只记录 rename，不记录内容增删。

---

## 12. 分阶段执行

### P0 · 冻结基线（在分支，保持现单站结构，不移动目录）
1. main 打 tag `pre-monorepo`，切 `refactor/monorepo`。
2. 新增 `tools/freeze_manifest.py`（纯标准库），生成 `content-manifest.json`、`tests/routes.snapshot.json`、`tests/manifest.snapshot.json`，快照入库。
3. 新增 `run_quality.py` 聚合现有 validate/scan + manifest 一致性。
4. 生成 `THIRD_PARTY_LICENSES.md`；跑一次依赖审计（记录到 ADR）。
- 出口：干净克隆可安装/质检/在线与离线构建；URL 快照已冻结。

### P1 · Monorepo 骨架与共享包
1. 启用 pnpm（corepack 优先；受限再 npm i -g pnpm；仍失败停下反馈）；建 workspace 根、`.npmrc`、`.node-version`。
2. 建 `@hw/shared-config`、`@hw/theme`、`@hw/content-core`、`@hw/learning`、`packages/tooling`（参数化）；`@hw/content-core` 接管 manifest 生成。
3. 先用最小 hello app（templates）验证 SSR/HMR/dev/build/preview。
- 出口：空 app 可构建，包接口可用。

### P2 · 迁移 handbook（只 rename）
1. git mv 内容到 `apps/handbook/docs/`；写薄 config/content.config/app package。
2. 生成 manifest/sidebar，**路由快照与 P0 必须零差异**，否则停下排查。
3. 在线构建 0 错误，产物与重构前按 manifest 对账。
4. 离线单文件 140 章，读 manifest 对账。
5. learning 仓储化 + 旧 key 迁移 + merge/replace/tombstone，注入旧 key 实测。
6. 首页/代表章桌面+移动截图（0 console error、无横向溢出）。
7. CI 改 pnpm/apps/handbook，新增 quality.yml；推分支先让 CI 跑绿（**不合并、不 push main**）。
- 出口：URL 不变、双形态全绿、数据不丢、分支 CI 绿。

### P3 · 活文档与模板
- PLAYBOOK 初版（含建站全过程与故障）、ADR-0001~0005、CHANGELOG、CONTRIBUTING、更新 AGENTS/README；完善 site-template（空 app 过 verify）。

### P4 · 嵌入式软件开发手册（apps/embedded，3–5 章验证）；P5 · 平台能力（按 Backlog/想法 3 逐项立项 ADR）。

---

## 12.5 v3 品牌重命名与门户拓扑（ADR-0006，2026-10-21，已完成）

- 回滚点：main(`ff8da96`) 打 tag `pre-brand`；切 `refactor/brand-lubook`。
- **A 本地改名**：根包/scope `@hw→@lubook`、工厂 `defineBookConfig/createBookTheme`、bin `book-manifest`；`apps/handbook→apps/hardware`（558 rename 全 R100）。
- **B 多 app 地基**：`VP_BASE` 派生、`build_pages_bundle.py`、run_quality/离线/快照按 app 参数化、根脚本与 CI。
- **C 门户**：`apps/portal` 与分册卡片（hardware 可用，embedded/embedded-linux 占位）。
- **D 学习数据**：迁移到 `lubook.v1.<slug>.learning`，per-app `legacyKeys` 多源合并 + 43 单测。
- **E 验证**：`verify:all` 全绿、门户/硬件/代表章桌面+移动截图、浏览器注入旧键实测、离线对账、grep 无残留。
- **F 文档**：NAMING/ARCHITECTURE/PLAYBOOK/README/CHANGELOG/AGENTS/CONTRIBUTING 更新；ADR-0006 转 Accepted。
- 停在 `refactor/brand-lubook` 待用户核实，未 push；GitHub 侧（仓库改名/Pages/Cloudflare）核实后另行操作。

---

## 13. 回滚预案

- v2 全程在 `refactor/monorepo`；v3 全程在 `refactor/brand-lubook`；main 与线上始终可部署，未合并可随时放弃。
- tag `pre-monorepo`（v2 基线）、`pre-brand`（v3 基线）；合并后异常可 revert 合并提交或回到对应 tag 重部署。
- 内容仅 rename，回退可完整还原；学习数据迁移保留旧 key，回退不丢用户数据。

---

## 14. 本版明确不做（避免过度工程，均入 Backlog 待评审）

1. **不**把 Python 离线/质检全量重写为 Node（保留零依赖；B1 仅做非阻塞 POC）。
2. **不**为重构而回填已有章节；但新章必须写全 `id/status/sources`（ADR-0008）。`review` 与新稳定 id 列 Backlog（B2–B5）。
3. **不**引入 IndexedDB，保持 localStorage + 仓储接口（B6）。
4. **不**建正式技术/编辑审核状态机、不建 CODEOWNERS（B5）。
5. **不**做 embedded/embedded-linux 实际内容、不做仿真/题库/计算器/Giscus/PWA/云同步/后端/英文版/门户增强（P4/P5）；门户仅极简卡片。
6. **不**强制 Playwright/axe/CSP（B9/B10），仅预留 verify 挂点。
7. **不**部署、不合并、不 push main；全部完成并自审后请用户核实，核实通过再操作。
8. pnpm 若无法在本机启用，**停下反馈**，不擅自改用其他方案或降级。

---

## 15. 验收标准（P2 完成判据）

1. 140 章 md 与 411 SVG 内容零改动（Git 仅 rename）。
2. 路由快照与 P0 零差异；线上全部章节 URL 不变（合并部署后主站/镜像 200）。
3. 在线构建 0 错误；离线 140 章、0 硬错误、0 图片缺失；manifest 在线/离线对账一致。
4. validate 0 硬错误（index 孤儿告警除外）、scan_math 0、scan_grounds 247 合规、scan_svg_order 411 OK。
5. 首页与代表章桌面/移动截图 0 console error、无横向溢出；容器/KaTeX/ECharts/折叠题/学习面板正常。
6. 旧 `hh.v1.learning` 平滑迁移到 `hb.v1.handbook.learning`，merge/replace 导入与 tombstone 行为正确。
7. PLAYBOOK + ADR-0001~0005 + CHANGELOG + CONTRIBUTING 落地；site-template 空 app 过 verify。
8. 分支 CI 绿；release.json 字段就绪（单 artifact 双发列为 B8）。

### 15.5 v3 品牌重命名验收（ADR-0006，已达成）

1. 558 个 rename 全 R100（143 md / 411 svg / 4 配置）；归一化 LF 后 md/svg 与 pre-brand(`ff8da96`) 逐字一致。
2. 内容 revision 改名前后均为 `sha256-361225735a3a67f4`（140/418/411，grounds 247，routes 141）。
3. `pnpm install --frozen-lockfile` 成功；`pnpm verify:all` 全绿（portal + hardware 构建、质检、离线、learning 43 单测）。
4. 门户 `/lubook/`、硬件 `/lubook/hardware/`、代表章均 200；桌面/移动截图 0 console error（仅 favicon 外链 warning）、无横向溢出、无 emoji、图标全 SVG。
5. 浏览器注入 `hh.v1.learning` + `hb.v1.handbook.learning`，刷新后写入 `lubook.v1.hardware.learning`，进度/收藏/笔记完整、textarea 16px、收藏星 SVG。
6. 代码/配置/CI 无 `@hw`/`defineHwConfig`/`createHwTheme`/`hw-manifest`/`hardware-handbook` 残留；`hb.v1` 仅作为 legacyKeys 声明与历史文档存在。
