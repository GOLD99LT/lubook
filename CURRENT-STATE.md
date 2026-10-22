# CURRENT-STATE — 路书 Lubook 当前状态

> 这是**唯一**的"现在到哪了"入口。历史方案（`EMBEDDED_PLAN.md`、`WEBSITE_PLAN.md`、`REQUIREMENTS.md` 的旧状态列）只作背景，不再当操作依据。
> 状态定义：**规划**（只有文档）｜**实现**（代码存在）｜**本地验证**（本机跑过并有证据）｜**线上验证**（真实站点确认）。
> 更新规则：每次合并进 `main` 的改动，都必须同步更新本表；证据写命令或提交号，不写"看起来正常"。

- 最后更新：2026-10-22
- 代码基线：`main` @ `5931963`（**比 `origin/main` (`c6f0002`) 领先 6 个提交，尚未 push**）

---

## 1. 交付物状态

| 分册 | 状态 | 证据 |
|---|---|---|
| 门户 `apps/portal` | 本地验证 | 构建通过；产物 `href="/lubook/hardware/" target="_self"`（两种 base 均正确） |
| 硬件分册 `apps/hardware` | 本地验证，**线上仍是旧版** | 140 章 / 411 SVG / 418 图 / 231,273 中文字；`revision=sha256-f199c10b304f5a89`（内容勘误后重新冻结） |
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

1. **批次 1**：规范二选一（`id/status/sources`），模板修好，`build:<app>` 脚本契约。
2. **批次 2**：渲染级验证脚手架（KaTeX 错误数、破图数、跨 app 点击、学习往返），这是"门禁绿≠页面对"的唯一解。
3. **批次 3**：内容勘误（上表 10 处）+ 主干章深挖。
4. **发布**：本地 6 个提交含安全勘误，至今未上线；push 需用户明确授权。
