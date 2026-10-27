# CURRENT-STATE — 路书 Lubook 当前状态

> 这是**唯一**的"现在到哪了"入口。历史方案（`EMBEDDED_PLAN.md`、`WEBSITE_PLAN.md`、`REQUIREMENTS.md` 的旧状态列）只作背景，不再当操作依据。
> 状态定义：**规划**（只有文档）｜**实现**（代码存在）｜**本地验证**（本机跑过并有证据）｜**线上验证**（真实站点确认）。
> 更新规则：每次合并进 `main` 的改动，都必须同步更新本表；证据写命令或提交号，不写"看起来正常"。

- 最后更新：2026-10-22（已上线）
- 代码基线：`main` @ `14d3517`（已 push、已部署；内容批次 1 上线）

---

## 1. 交付物状态

| 分册 | 状态 | 证据 |
|---|---|---|
| 门户 `apps/portal` | 本地验证 | 构建通过；产物 `href="/lubook/hardware/" target="_self"`（两种 base 均正确） |
| 硬件分册 `apps/hardware` | **已上线（双站）** 2026-10-24 03:04 | 140 章 / 491 SVG / 375 处图片引用 / 322 条来源；`revision=sha256-4fb67d571370933b`；线上体检 141 路由 + 1238 资源 **0 失败** |
| 嵌入式软件 `apps/embedded` | 规划 | 无目录；门户卡片 `available:false` |
| 嵌入式 Linux `apps/embedded-linux` | 规划 | 无目录；门户卡片 `available:false` |

## 2. 工程能力状态

| 能力 | 状态 | 说明 |
|---|---|---|
| 在线 VitePress 构建 | 本地验证 | `pnpm build:<app>`；CI 用 Node 22 |
| 离线单文件 | 本地验证 | `dist/hardware.html` 6,116,251 B；公式双重转义 0、`.md` 死链 0、140 内部锚点全命中 |
| 多 app bundle 组装 | 本地验证 | `--out` 已有安全边界（见 §4） |
| 质量门禁 `run_quality` | 本地验证 | manifest/validate/scan_grounds/scan_svg_order/scan_math 五项 |
| 学习数据仓储 | 本地验证 | 单测 93 passed（`node packages/learning/test/learning.test.ts`） |
| 部署链路 | 实现，**未验证** | Pages 已加 `needs: quality`；尚未在 CI 实跑 |
| 自动化测试覆盖 | 仅 learning | 构建/渲染/导航/主题 **零自动化测试** |
| 内容技术准确性 | **高风险** | 抽样 35 章发现 10 章有实质错误（见 §5） |

## 3. 上一轮审查 F01–F15 处置

| 编号 | 问题 | 状态 | 证据 |
|---|---|---|---|
| F01 | 门户跨 app 404 | ✅ 已修（本地验证） | `PortalHome.vue` `target="_self"` + `withBase`；VitePress `router.js:134` 对带 `target` 的链接跳过 SPA |
| F02 | 安全用电误导 | ✅ 已修 | `basics/electrical-safety.md` 重写相关段落 |
| F03 | 示波器接地缺前提 | ✅ 已修 | `practice/oscilloscope.md` |
| F04 | 存储失败仍报成功 | ✅ 已修（本地验证） | `saveState` + 重试 + 导出兜底；单测覆盖配额失败 |
| F05 | 门禁不阻止发布 | ✅ 已修（本轮） | `deploy-docs.yml` 增 `quality` job（`uses: quality.yml`）+ `needs`；smoke 改为断言正文特征串 |
| F06 | 离线公式双重转义 | ✅ 已修 | 产物 `data-t` 二次转义 0 处 |
| F07 | 离线死链 | ✅ 已修 | `.md` 链接 0 处 |
| F08 | 离线备份协议分裂 | ✅ 已修 | 产物含 `schemaVersion`/`appId`/文件导入；旧三键迁移保留 |
| F09 | 新册串入硬件数据 | ✅ 已修 | `legacyKeys` 显式声明 + `knownIds` 由 catalog 注入 |
| F10 | 模板契约不成立 | ✅ 已修 | 去掉写死 base、注入 knownIds、模板章节补齐字段；模板 docs:build + validate 均通过 |
| F11 | manifest 对账造假 | ✅ 已修 | 逐章重算 checksum + 复算 revision；清单缺失即失败；TS/Python 双解析器逐字段对账已真实跑通（[PARITY PASS]） |
| F12 | 源目录错仍退出 0 | ✅ 已修（本轮） | 源目录缺失/内容 app 缺 SUMMARY 均 exit 2 |
| F13 | LTspice 算例错 | ✅ 已修（待实跑） | 阈值改 3.1606V；作者自注"待 LTspice 实跑验证" |
| F14 | 状态文档矛盾 | 🟡 部分（本轮） | 新增本文件；`REQUIREMENTS.md`/`CHANGELOG.md`/`ARCHITECTURE.md` 的过期表述未清理 |
| F15 | bundle 无边界检查 | ✅ 已修（本轮） | `guard_out()`：拒绝仓库根/源码目录/非 marker 非空目录；先校验 dist 再删除 |

## 4. 本轮（批次 0）已落地的改动

| 改动 | 文件 | 回归证据 |
|---|---|---|
| bundle 输出安全边界 | `packages/tooling/src/build_pages_bundle.py` | `--out apps/. /packages/docs/reviews` 全部拒绝，`apps/` 1227 个文件未变；正常 `.bundle` 可重复组装 |
| 门禁必须能失败 | `run_quality.py` | `--src 不存在` exit 2；`--app hardwar` exit 2；`--app portal` exit 0 |
| manifest 真对账 | `packages/tooling/src/build_single_html.py` | 篡改 revision+checksum → exit 1；路径不存在 → exit 1；正常 → 逐章 checksum 通过 |
| 解析器不再挂死 | 同上 `parse_blocks` | 5 类曾无限循环的 Markdown（```` ```c++ ````、`::::`、裸 `:::`、无前导竖线表头、含括号图片路径）现均正常结束 |
| 部署先验后发 | `.github/workflows/deploy-docs.yml`、`quality.yml` | 静态检查（未在 CI 实跑） |
| Windows 脚本修复 | `package.json` | `offline:hardware` 的 `;` 改 `&&` |
| 2 张坏 SVG | `assets/schematics/*.svg` | 411 张 SVG 全部 XML 可解析 |
| 仓库卫生 | `.gitignore` | 补 `.bundle-root/`、`.bundle*/`、`.pnpm-store/`、`.wrangler/`、`*.log` |

## 5. 已知未修问题（按严重度）

| 严重度 | 问题 | 位置 |
|---|---|---|
| **P1** | 安规章自相矛盾：加强绝缘要求 6/8mm，示例 3.5/5mm 却判"满足" | `practice/safety-certification.md:49 vs :64` |
| **P1** | 模板不注入 `knownIds` → 照模板建的新册，学习数据每次刷新被清空 | `templates/site-template/content.config.ts:32-37` |
| **P1** | 学习仓储 boot 解析失败时静默清空，`saveState.ok` 仍为 true，下次写入覆盖原数据 | `packages/learning/src/index.ts:280-317` |
| **P1** | 首页"我的收藏"链接绕过 base，子路径部署下 404/回首页 | `HomePanel.vue:102`、`store.ts:109` |
| P2 | 另 9 处内容技术错误（555 二极管接反、T 网络 1.2M 写成 310k、反激 RCD 权衡写反、EMI 辐射幂次、ADC 分压超 VREF…） | 见审查报告 §7.3 |
| P2 | 模板 `base:'/'` 写死，覆盖 `VP_BASE` 派生（F10） | `templates/site-template/docs/.vitepress/config.mts:20` |
| P2 | 内容规范与校验器互斥：文档说不要 `id/status/sources`，`validate.py` 强制要求 | `AGENTS.md:14` vs `validate.py:43-47` |
| P2 | 内容指纹不含 SVG 字节，改图不报警 | `freeze_manifest.py:154-172` |
| P2 | TS/Python 写同一个 manifest 互相覆盖；`parity.ts` 是死代码且指纹过期 | `apps/hardware/package.json:8`、`freeze_manifest.py:185`、`parity.ts:20` |
| P2 | 新册首跑 `verify:all` 会 FileNotFoundError（先 quality 后 freeze） | `verify_all.py:62,67`、`run_quality.py:63-66` |
| P2 | CI 矩阵与 content-gate 写死 portal/hardware | `quality.yml:22,80-84` |
| P3 | `gen:portal` 指向不存在的脚本；`.node-version` 未被 workflow 使用 | `package.json:12`、三个 workflow |

## 6. 环境约定（踩过的坑）

- `python` 在本机是微软商店的坏别名（退出码 9009）；跑项目脚本请用真实解释器全路径，或把可用的 `python` 放到 PATH 前面。
- 本机 Node 24 / Python 3.14；CI 锁 Node 22 / Python 3.11。跨版本差异要分别记录。
- pnpm 必须走 `corepack pnpm`（`packageManager` 锁 12.11.2）；**本机没有 `pnpm` 命令、也没有跑过 `corepack enable`**，所以 `package.json` 里 `pnpm -F ...` 这类嵌套脚本会报"不是内部或外部命令"。解决办法二选一：`corepack enable`（可能需要管理员），或准备一个 `pnpm.cmd` 垫片（内容 `corepack pnpm %*`）并放到 PATH。
- 本机沙箱内 `pnpm install` 会因 store 锁失败；需要在普通权限终端里手工跑一次。

## 7. 下一步（按批次）

1. **P4 / P5 立项**（需用户决策）：嵌入式软件手册（`apps/embedded`）与平台能力（搜索/计算器/题库扩展等）。
   按 AGENTS.md §2.5，未立项前不做实际内容。
2. **标准原文核对**：`pcb/routing.md` 的 IPC-2221 间距表——审校认为与 B1 列差 5~10 倍，
   但本机代理取不到标准原文，未擅自改。
3. **反爬站点来源链接人工确认**：JEDEC / onsemi / ST / Murata（403 或超时，本机不可验证）。
4. **可选优化**：搜索索引 7 MB 的加载策略、portal 端与分册的一致性抽查。

## 8. 本轮整改总览（2026-10-22，分支 `fix/batch0-hardening`）

| 批次 | 内容 | 状态 |
|---|---|---|
| 0 止血 | F15 路径守卫、F12 严格失败、F11 真对账、解析器无限循环、F05 部署前置门禁、2 张坏 SVG、`;`→`&&`、.gitignore | ✅ 完成并实测 |
| 1 规范与模板 | F10 模板 base/knownIds/字段、ADR-0008 内容 schema、validate 与 freeze 口径对齐、boot 失败不再静默覆盖、收藏链接补 base | ✅ 完成并实测 |
| 2 门禁 | CI 自动枚举 apps、content-gate 按矩阵展开、scaffold job、TS/Python parser parity 真正跑通、快照基线不被静默覆盖、指纹覆盖 SVG 字节（ADR-0009）、pnpm 可移植性 | ✅ 完成并实测 |
| 3 内容 | 13 处技术勘误（含 2 处安全类）+ 安全表述去绝对化 | ✅ 完成，指纹重新冻结 |
| 4 体验 | 学习面板无障碍（label/aria-live/aria-pressed）、对比度、死脚本 gen:portal、CI 跟随 .node-version | ✅ 完成 |

### 上线前已做的产物级验证

- `pnpm verify:all` 退出 0：portal/hardware 构建、质检 0 失败、离线对账、parser parity、learning 102 passed。
- `pnpm bundle:pages`（VP_BASE=/lubook/）产物路径核对：门户卡片 `/lubook/hardware/` + `target="_self"`；
  门户资源 `/lubook/assets/…`；分册资源 `/lubook/hardware/assets/…`；分册回门户 `/lubook/` + `target="_self"`。
- 本地静态服务 + 无头浏览器实测：`/lubook/` 与 `/lubook/hardware/` 正常渲染、非 404；
  章节页 `/lubook/hardware/basics/voltage-current-power.html` 标题/h1 正确、23 个公式 0 错误、186 项侧边栏。
- 离线单文件真实浏览器：3599 个公式 0 错误、93 个 ECharts canvas、0 破图。

### 仍未处理（下一轮）

| 优先级 | 问题 | 位置 |
|---|---|---|
| ✅ 已修 | ~~ECharts 全量打进 theme chunk~~ → 按需加载，theme 1.15MB→113KB（ADR-0010） | `EChart.vue` |
| P2 | 导入固定 replace、无 merge 选项与二次确认；多标签页后写覆盖先写 | `store.ts`、`learning/index.ts` |
| P2 | 存储不可用时静默降级内存 Storage，`saveState.ok` 仍为 true（界面显示"已保存"但刷新即丢） | `learning/index.ts` resolveStorage |
| P3 | 离线单文件不生成标题 id，章内 `#锚点` 无效（当前正文 0 处使用） | `build_single_html.py` render |
| P3 | 140 章平均 1,652 中文字，深度不足；本轮只修错，未加深 | 内容 |
| ✅ 已处理 | 来源链：删除跑不起来的 `merge_sources.py`，`sources.list.yaml` 改为手工维护的唯一来源索引 | `sources.list.yaml` 头部 |
---

## 9. 上线记录（2026-10-22）

| 项 | 值 |
|---|---|
| 合并方式 | `fix/batch0-hardening` → `main` 快进合并（14 个提交） |
| 部署提交 | `d33b556` |
| Pages 部署 run | https://github.com/GOLD99LT/lubook/actions/runs/39746343362（success） |
| 线上入口 | https://gold99lt.github.io/lubook/ ｜ https://gold99lt.github.io/lubook/hardware/ |
| Cloudflare 镜像 | **未更新**（deploy-cloudflare.yml 仅 workflow_dispatch，需手动触发） |

### 上线时踩到并修掉的坑

首次 push（`fb69742`）后 **Deploy run 显示 cancelled**：同一个 commit 起了两个 run——独立的 Quality Gate
与被 deploy-docs 通过 `workflow_call` 调用的 quality job——两者落在同一个 concurrency 组
`quality-<ref>` 里，`cancel-in-progress` 让它们互相取消。
修法：`quality.yml` 的 push 触发排除 `main`（`branches-ignore`），main 的门禁统一由部署 run 内的
quality job 承担。修复后重新 push（`d33b556`），部署成功。

### 线上实测（发布后，真实浏览器 + HTTP）

- `/lubook/` → 200，标题「路书」，卡片 `<a class="card" href="/lubook/hardware/" target="_self">`，非 404 页。
- `/lubook/hardware/` → 200，标题「硬件工程师手册」。
- `/lubook/hardware/basics/voltage-current-power`（无扩展名）→ **200**（GitHub Pages 支持该写法；本地静态服务器不支持，之前本地测试的 404 是服务器差异，不是产物问题）。
- 章节页 `/lubook/hardware/opamp/inverting-amplifier` 真实浏览器：61 个公式 **0 错误**、1 个 ECharts canvas、186 项侧边栏、学习面板存在。
- 内容勘误已上线：T 型网络改为 1.2MΩ（旧 310k 已消失）、`GB 4943.1-2022`、加强绝缘判定文案均在线上页面中。
---

## 10. 内容批次进度（CONTENT-STANDARD 执行中）

标准：docs/CONTENT-STANDARD.md（概念章 8 模块 / 电路章 11 模块，H1 字数 ≥4,000，配图/自测题/坑/来源硬门槛）。
机械检查：python scripts/check-content.py --app hardware --profile all --min 4000。
审核：主审核逐章复算数值 + 官方门禁 + 真实浏览器渲染，整批通过才合入。

| 批次 | 章节 | 状态 | 字数 | 审核 |
|---|---|---|---|---|
| 批次 1 | basics/voltage-current-power、ohms-law、series-parallel、kcl-kvl | ✅ 已合入并上线（c89ec5） | 7,974 / 7,842 / 5,905 / 5,951 | 数值逐条复算通过；0 公式错误；0 破图 |
| 批次 2 | basics/dc-ac、capacitor-rc、inductor-rl、impedance | ✅ 已合入（`06adc7d`） | 7,102 / 7,763 / 7,299 / 5,705 | 数值复算通过；42 处 `°` 已改成 `^{\circ}` |
| 批次 3 | basics/math-basics、transformer、nodal-mesh-analysis、rlc-resonance | ✅ 已合入并上线（`aab4f66`） | 9,041 / 8,472 / 8,115 / 6,638 | 复算通过；顺带修正旧图 transformer.svg 写反的匝比公式 |
| 批次 4 | basics/mains-three-phase、electrical-safety | ✅ 已合入并上线（`ae4edc1`） | 10,725 / 11,553 | 安规章带 13 条文末《复核清单》+ 顶部提示；接地符号已统一为标准尺寸 |
| 批次 5 | components/resistors、diodes、mosfet、capacitors | ✅ 已合入并上线（`828c869`） | 9,086 / 8,740 / 8,037 / 7,658 | 主干章标准；复算通过 |
| 批次 6 | components 其余 9 章 | ✅ 已合入并上线（`0ac5728`） | 5,506–8,421 | 支撑章标准；components 篇 13/13 达标 |
| 批次 7 | opamp 地基 5 章（opamp-overview、ideal-opamp、open-loop-feedback、small-signal-model、bjt-amplifiers） | ✅ 已合入并上线（`7d1bb0b`） | 6,264–7,366 | 主干章标准；术语约定统一后派工 |
| 批次 8 | opamp 反馈四拓扑、稳定性、供电轨、CMRR/PSRR、失调（5 章） | ✅ 已合入并上线（`8821b54`） | 6,071–7,915 | 主干章标准 |
| 批次 9 | opamp 跟随器 / 反相 / 同相 / 差分 / 仪表放大 | ✅ 已合入并上线（`370fa7b`） | 5,853–8,283 | 智能体两次纠正任务书（INA 的 CMRR 机理、噪声增益方向） |
| 批次 10 | opamp 加法 / 微积分 / 一阶滤波 / Sallen-Key / 带通带阻 | ✅ 已合入并上线（`be0b500`） | 5,415–8,472 | 写作者纠正 7 处技术错误（含前作者的 MFB 拓扑错误） |
| 批次 11 | opamp 噪声 / GBW 与压摆率 / 比较器 / 振荡器 / 555 | ✅ 已合入并上线（`5c4c4fe`） | 5,511–8,190 | 累计纠正 20 处技术错误，纠错密度最高的一批 |
| 批次 12 | opamp 最后 8 章（二极管电路 / 线性稳压 / 功放 / 信号链 / 精密整流 / V-I 变换 / 单电源偏置 / 模拟开关） | ✅ 已合入并上线（`4a1e298`） | 5,010–8,331 | **opamp 篇 33/33 收官** |
| 批次 13 | power 全部 12 章 | ✅ 已合入并上线（`75b1851`） | 5,025–8,568 | 一轮收官；三路智能体共纠正 49 处技术错误 |
| 批次 14 | digital 全部 12 章 | ✅ 已合入并上线（`7cae2f8`） | 5,036–9,404 | 一轮收官；约 40 处纠错 |
| 批次 15 | mcu 全部 13 章 | ✅ 已合入并上线（`90070ad`） | 4,978–7,518 | 一轮收官；约 40 处纠错 + 主审补修 2 处残留错误 |
| 批次 16 | pcb 全部 13 章 | ✅ 已合入并上线（`b62c646`） | 4,522–7,178 | 一轮收官；约 60 处纠错 + 主审补齐 10 条互链 |
| 批次 17 | practice 全部 12 章 + 修复构建 OOM（ADR-0011） | ✅ 已合入并上线（`d6a1d9a`） | 4,989–7,428 | **全书正文 122/140 收官**；约 35 处纠错 |
| 批次 18 | appendix 9 + quizbank 9 校订 + 修复构建内存（ADR-0011 重写） | ✅ 已合入并上线（`faa75ea`） | 附录 1,225–4,531 / 题库 3,218–4,414 | **全书 140/140 覆盖**；附录 41 处 + 题库 37 处纠错 |
| 批次 19 | 构建内存整改（ADR-0012：公式改运行期渲染）+ 工具闸门 | ✅ 已合入并上线（`26026d7`） | — | 内存 −61%、HTML −71%、容量 ×4.3 |
| 待办 | 来源编号联网复核（web_search 仍 401）；孤儿图清点后决定不删（129 张/363 KB，0 张进产物） | ⬜ 待排 | — | — |
| 不排期 | appendix 9 / quizbank 9 | 按"速查/附录"档，不设字数门槛 | — | — |

现状：**全书 140/140 覆盖**——正文 122 章全部达主干章标准（basics 14 + components 13 + opamp 33 + power 12 + digital 12 + mcu 13 + pcb 13 + practice 12），附录 9 章与题库 9 章按速查/题库档完成校订。
基线：
evision=sha256-b0bfc73e3ba0bc48，routes 仍 141（URL 未变）。

### 待专业复核（写作智能体无法联网核实，已在正文标注"以数据手册为准"）

- Vishay CRCW 降额曲线 70°C/155°C 的具体数值；GB/T 156-2017 的 220/380V 表述；
  Kuphaldt 与 Practical Electronics 的章节/小节名；Sedra & Smith Ch2 章名。
- AWG 电阻按标称直径几何计算，未计绞线系数（与标准表差约 3%，正文已注明）。

## 11. 并行处理的遗留问题

| 项 | 状态 | 说明 |
|---|---|---|
| ECharts 全量进 theme chunk | ✅ 已修 | 改为按需加载：theme chunk 1.15MB → 113KB，门户 58.7KB 且不再产出图表 chunk（ADR-0010） |
| 导入 merge/确认 | ✅ 已修 | 见 c704cfa，130 单测覆盖 |
| 存储降级假成功 | ✅ 已修 | 见 c704cfa，persistent 标志 + 会话级提示 |
| 离线标题锚点 | ✅ 已修 | 1,755 个标题 id；#章锚点!标题 路由 |
| 内容深度 | ✅ 已修 | 18 个批次完成：正文 122 章全部达主干章标准、附录 9 + 题库 9 完成校订，**全书 140/140**；累计纠正 300+ 处技术错误（其中约 230 处为前作者遗留） |
| 来源链 | ✅ 已处理 | 删除 merge_sources.py，sources.list.yaml 改手工维护 |

## 12. 构建内存（ADR-0011 / ADR-0012）

实测模型：**峰值 ≈ 0.80 GB + 10.4 MB × 页面数**（数学改为运行期渲染后）。
8 GB 堆可支撑约 615 页；当前 144 页，占用 29%。

```bash
python packages/tooling/src/build_memory_budget.py --src apps/hardware/docs --heap-mb 8192
```

历史上两次 OOM 的处置与教训见 ADR-0011（含"`.npmrc` 的 node-options 实测无效"这一条），
渲染策略的取舍见 ADR-0012。任何回归由 `scan_math_render.py` 在构建后拦截（CI 已接）。

## 13. 上线体检与旧错回归（批次 20）

三个新增工具，把"部署之后"和"别把错话写回来"也纳入常规：

```bash
# 按路由快照逐页体检线上站点（状态码、标题、同源资源 200）
python packages/tooling/src/check_live_site.py --base https://gold99lt.github.io/lubook/hardware --app hardware --check-assets
python packages/tooling/src/check_live_site.py --base https://lubook.pages.dev/hardware --app hardware --check-assets

# 旧错误说法回归扫描（报告用；--strict 才非零退出）
python packages/tooling/src/scan_legacy_errors.py --app hardware

# 孤儿图清点
python packages/tooling/src/scan_orphan_assets.py --app hardware
```

2026-10-23 实测：GitHub Pages 与 Cloudflare 镜像各 **141 路由 + 1238 资源，0 失败**；
旧错扫描命中 0（另有 5 处是正文在纠正这些说法，已按引号/否定语境排除）。

Cloudflare 镜像已改为随 main 自动部署（Secrets 与 Pages 项目已配置）。

### 13.1 双站部署（ADR-0013）

| 站点 | 地址 | base | 触发 |
|---|---|---|---|
| 主站 | https://gold99lt.github.io/lubook/ | `/lubook/` | push main（deploy-docs） |
| 镜像 | https://lubook.pages.dev/ | `/` | push main（deploy-cloudflare，2026-10-23 起自动） |

两条流水线都跑完整质量门禁。**并发组必须带调用方**（`quality-${{ github.workflow }}-${{ github.ref }}`），
否则两条流水线的门禁会互相取消——2026-10-22 与 2026-10-23 各踩过一次，详见 ADR-0013。

## 14. 阶段定位（对照 ARCHITECTURE v3 §12）

| 阶段 | 内容 | 状态 |
|---|---|---|
| P0 | 冻结基线（保持单站结构） | ✅ 完成 |
| P1 | Monorepo 骨架与共享包（shared-config / theme / content-core / learning / tooling） | ✅ 完成 |
| P2 | 迁移 140 章（只 rename，URL 零变更） | ✅ 完成（路由快照 141 条零差异） |
| P3 | 活文档与模板（CONTENT-STANDARD / PLAYBOOK / ADR-0001~0013 / 新分册脚手架） | ✅ 完成 |
| — | **内容生产 18 批 / 140 章** | ✅ 完成并上线 |
| — | **质量审查（本轮 6 智能体、约 1200 条断言、38 处修正）** | ✅ 完成并上线 |
| — | **双站部署（Pages 主站 + Cloudflare 镜像，随 main 自动）** | ✅ 完成 |
| P4 | 嵌入式软件手册（3–5 章验证） | ⬜ 未立项 |
| P5 | 平台能力（按 Backlog 逐项立项） | ⬜ 未立项 |

上线方式：合并到 `main` 即自动发布两条流水线（deploy-docs → GitHub Pages；deploy-cloudflare → 镜像），
无需人工触发。最近一次：commit `f5b061e`，2026-10-24 03:01:51 触发、03:04 双侧完成。

## 15. P4 进展（2026-10-24）

| 分册 | 章节 | 中文字 | 自绘图 | 路由 | 构建 | 质量门禁 |
|---|---|---|---|---|---|---|
| apps/embedded | 24 章（六篇齐备） | 156,360 | 24 | 25 | ✅ | ✅ 0 项失败 |
| apps/embedded-linux | 17 章（六篇齐备） | 114,145 | 17 | 18 | ✅ | ✅ 0 项失败 |

- pnpm verify:all 退出 0，四个 app（portal/embedded/embedded-linux/hardware）全部通过。
- 内容审查：6 组审查覆盖 27 章、1,069 条量化断言，确认并修复 **45 条错误**（全部复算验证）；
  另有若干存疑因证据不足未改，已在当轮记录。
- 浏览器抽验：6 页 KaTeX 149~484 个、0 错误、图正常。
- **已上线（仅代码，门户卡片仍关闭）** 2026-10-24：
  - GitHub Pages：https://gold99lt.github.io/lubook/embedded/、.../embedded-linux/
  - Cloudflare：https://lubook.pages.dev/embedded/、.../embedded-linux/
  - 双站全路由体检与资源检查均「全部通过」；线上浏览器抽验 KaTeX 484/261、0 错误。
- **门户入口已全量开启**（2026-10-27）：vailable: true，双站门户均显示三个分册卡片，
  链接为 /lubook/embedded/、/lubook/embedded-linux/（镜像站同构），无即将上线标记。

### 第 2 批内容（已完成并上线）

12 章全部完成，四组审查共 31 条确认错误，全部复算修复：

| 分册 | 篇 | 新增章 | 审查 |
|---|---|---|---|
| embedded | 第三篇 通信接口与协议 | CAN/CAN FD、USB 设备、以太网 | 8 条 |
| embedded | 第二篇 Cortex-M 与 MCU 外设 | MPU 与 Cache、FPU 与 DSP、硬件加速 | 7 条 |
| embedded-linux | 第二篇 内核与驱动 | 中断与并发、DMA 与内存、电源管理 | 8 条 |
| embedded-linux | 第四/五篇 | eMMC/UFS/SD、Camera 与 ISP、安全启动 | 8 条 |

规模：embedded 30 章 / 193,961 字 / 30 图 / 31 路由；embedded-linux 23 章 / 152,703 字 / 23 图 / 24 路由。
erify:all 退出 0（四个 app 全绿）；两册构建 18.9 s / 18.6 s。

典型修订（都以复算为准）：
- MPU 的 SRD 子区域禁用不是禁止访问，而是该区域不再覆盖该段 → 保护带改用独立 AP=000 区域；
- CAN FD 的 BRS=1 才切高速率；64 字节 FD 帧 CRC 字段含 7 个固定填充位 → 总帧 579 位、T=342 µs；
- Linux DMA 的 map/sync/unmap 方向必须一致（统一 DMA_BIDIRECTIONAL）；
- suspend 阶段顺序：late→noirq→关非启动 CPU；prepare 正序、suspend 逆序。
