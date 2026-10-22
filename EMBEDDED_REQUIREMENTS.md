# 嵌入式两册 · 可评审需求与落地方案（EMBEDDED_REQUIREMENTS）

> 版本：R1（P4 评审稿）
> 日期：2026-10-21（Asia/Shanghai）
> 性质：**只调研、只构思、只写文档**。本轮不创建 `apps/embedded`、不写正文/代码、不改 CI/脚本/主题、不提交。
> 配套文档：`EMBEDDED_PLAN.md`（调研底稿，7 个决策已拍板 1A2A3A4A5A6A7B）、`EMBEDDED_OUTLINE.md`（知识地图细化与试点章大纲，详细底稿）。本文为"可评审需求 + 落地方案"，知识地图与大纲只引用、不整段复制。

---

## 结论先行

1. **值得做，且应做两册**：嵌入式软件（MCU）与嵌入式 Linux 是两条独立、可就业、可长期复盘的技术栈，与现有《硬件工程师手册》边界清晰（硬件原理只链接、不重复，软件实现重点写）。本轮调研确认中文市场存在结构性空白（见 §4）。
2. **共享地基已就绪，加册的"真正工程项"很少且已参数化**：`paths_util.list_apps()`、`verify_all.py`、`build_pages_bundle.py`、`freeze_manifest.py`、`run_quality.py`、`build_single_html.py` 均已支持 `--app` 并自动遍历 `apps/*`。落地每个新 app 只需：复制模板 + 改元数据 + 根脚本补 3 条 + CI 改 1 处 + 首次 freeze 快照 + 门户卡片改状态（精确清单见 §1）。
3. **差异化空白明确**：核实到 2026-10-21，**不存在"VitePress + 中文 + 代码密集 + 嵌入式"的成熟手册**；中文嵌入式内容高度绑定开发板/商业课程（野火、正点原子、韦东山、RT-Thread 文档），缺"中立、跨厂商、在线+离线双形态、裸机→RTOS→Linux 全链路"的开源手册。
4. **C 是主线，Rust 进进阶附录**：34 条 2026 在招 JD 中 MCU 岗无一条要求 Rust；Rust 已过"能不能用"但未到"必须学"。建议设 1 章以内"Rust on MCU"进阶视野，不与 C 并列。
5. **AI 辅助开发收录"方法论与边界"，不做厂商测评**；**功能安全**收录"概念 + MISRA C:2025 核心规则速查"，标准全文与认证流程仅外链。
6. **Mermaid 需新接入**（全仓当前为 0），建议在 `shared-config/theme` 以共享能力接入，落地时单独评估并写 ADR（方案对比见 §6）。
7. **建议节奏**：先 MCU 试点 5 章跑通"新 app 全链路"，再两线并行；Linux 试点 4 章随后。规模估算 MCU 90–115 章、Linux 40–60 章（见 §7）。

---

## ① 现状基线与剩余接入清单

### 1.1 已就绪的共享地基（直接采信，无需重复核对）

| 能力 | 现状 | 对新册的意义 |
|---|---|---|
| app 发现 | `paths_util.list_apps()` 自动扫描 `apps/*` 下含 `package.json` 的目录 | 新 app 落目录即被识别 |
| 全量验证 | `verify_all.py` 遍历 apps，对内容 app（有 `SUMMARY.md`）执行 build→quality→freeze→offline，最后跑学习单测 | 新册自动纳入 `verify:all` |
| 部署 bundle | `build_pages_bundle.py` 按 `VP_BASE` 构建并组装：portal dist→bundle 根；内容分册 dist→`bundle/<slug>/` | 新册自动并入可部署目录 |
| 内容清单 | `freeze_manifest.py --app` 生成 `.generated/<app>-content-manifest.json` 与 `tests/<app>.{routes,manifest}.snapshot.json` | 新册可独立对账 |
| 质检 | `run_quality.py --app/--src/--out/--snapshot-prefix` | 新册独立质检 |
| 离线单文件 | `build_single_html.py --app --manifest` 输出 `dist/<app>.html`；`brand_for()` 对未登记 app 有默认品牌（storePrefix=app） | 新册可直接出离线 |
| 学习数据 | `@lubook/learning` 按 appId 隔离，键 `lubook.v1.<slug>.learning`；支持 `legacyKeys`、导入导出、tombstone | 新册默认空、互不串 |
| 空 app 模板 | `templates/site-template` 与正式 app 同形态、可构建 | 直接复制派生 |

### 1.2 每个新 app 的精确接入清单（落地时执行，本轮不做）

**A. 复制与改元数据（以 `embedded` 为例，`embedded-linux` 同理）**
1. `cp -r templates/site-template apps/embedded`（去掉 `docs/.vitepress/cache`、`docs/example` 等模板残留）。
2. `apps/embedded/package.json`：
   - `name` → `@lubook/embedded`；
   - `gen:catalog` 脚本 `--appId embedded`、`--out ../../.generated/embedded-manifest.json`；
   - `gen:sidebar` 已按 `--src docs` 无需改。
3. `apps/embedded/content.config.ts`：
   - `APP_ID='embedded'`、`TITLE='嵌入式软件手册'`、`DESCRIPTION=...`、`FAVICON`；
   - `PART_REGISTRY`（篇号→篇名，与 `SUMMARY.md` 一致）、`NAV`、`SOCIAL_LINKS`（GitHub 指向 `GOLD99LT/lubook`）；
   - 新 app **不传** `legacyKeys`（默认空）；hardware 已传 `['hh.v1.learning','hb.v1.handbook.learning']`。
4. `apps/embedded/docs/SUMMARY.md` 与 `index.md`：写篇/章结构与首页；中文书名 + 「路书」角标回链门户。
5. `apps/embedded/docs/.vitepress/config.mts`：薄配置（模板已就绪，确认 import 路径）。
6. 品牌资产（可选，为统一离线品牌）：`build_single_html.py` 的 `OFFLINE_BRANDS` 补 `embedded`/`embedded-linux` 条目（book/title/storePrefix；新册无离线历史，storePrefix 用 slug）；不补也能跑（默认品牌）。

**B. 根 `package.json` 补脚本（bundle/verify 调 `pnpm run build:<app>`，脚本必须存在）**
- `gen:embedded`、`dev:embedded`、`build:embedded`、`preview:embedded`；
- `quality:embedded`（`python run_quality.py --app embedded`）、`freeze:embedded`、`offline:embedded`；
- `embedded-linux` 同 7 条（可按需精简 dev/preview）。

**C. CI 改 1 处（`.github/workflows/quality.yml`）**
- 当前 build 矩阵写死 `app:['portal','hardware']`；content-gate 写死 `quality:hardware`/`offline:hardware`。
- 建议：**改为自动枚举 `apps/*`**（用一步 `python -c "import ...paths_util"` 生成矩阵 JSON），或暂时在矩阵补 `'embedded','embedded-linux'`、content-gate 改为循环遍历。推荐自动枚举，避免以后每加一册都改 CI。
- 部署流水线 `deploy-docs.yml`（`bundle:pages`）、`deploy-cloudflare.yml`（`bundle:cloudflare`）**无需改**——bundle 自动遍历并合并。

**D. 首次快照与对账**
- 内容落地后 `pnpm freeze:embedded` 生成 `tests/embedded.routes.snapshot.json`、`tests/embedded.manifest.snapshot.json`（Linux 册同）；首次入库即基准，后续 CI 逐字比对。

**E. 门户卡片改状态**
- `apps/portal/content.config.ts` 的 `PORTAL_CARDS`：对应册上线后把 `available:false` 改 `true`（internal 链接 `VP_BASE + '<slug>/'` 已就绪）。

**F. 无需做的事**
- 部署拓扑已被 ADR-0006 覆盖、bundle 已自动合并，**无需再写部署 ADR**；
- 无需改学习数据模型（已隔离）；无需改 bundle 规则。

### 1.3 本轮未执行声明
以上清单为落地方案，本轮**未**复制模板、未改任何文件、未写脚本、未提交；工作区新增项仅为文档（`EMBEDDED_REQUIREMENTS.md`、`EMBEDDED_OUTLINE.md`）。

---

## ② 两册定位、受众与知识大纲

> 完整知识地图（逐块三级小节、必讲/对比/外链/附录分级、交叉引用）见 `EMBEDDED_PLAN.md §2` 与 `EMBEDDED_OUTLINE.md` 第一部分；此处只给定位、受众与篇级骨架。

### 2.1 两册定位与受众

| 维度 | 嵌入式软件手册（`embedded`） | 嵌入式 Linux 手册（`embedded-linux`） |
|---|---|---|
| 一句话定位 | 从 C 到 Cortex-M 裸机/RTOS 的 MCU 固件开发手册 | 从 Cortex-A 启动链到 rootfs/构建/OTA 的 Linux 系统手册 |
| 目标读者 | 做 MCU 固件、传感器/电机控制、低功耗 IoT 的工程师与求职者 | 做嵌入式 Linux BSP/驱动/系统集成、网关/边缘设备的工程师与求职者 |
| 读完能做 | 独立交付一个 MCU 工程：配时钟/外设、写中断与 DMA、上 RTOS、做 IAP/OTA | 交叉编译、改设备树、写/调驱动、用 Buildroot/Yocto 出镜像、做 OTA |
| 主例 | 通用 Cortex-M/CMSIS 打底，STM32 为主例，ESP32/RISC-V 关键差异专栏 | QEMU virt aarch64 免硬件主例，真实板卡（RPi4/STM32MP1）对照 |
| 与硬件册关系 | 硬件原理链 `hardware/5.x`，软件配置/代码/现象重点写 | 硬件底座链 `hardware/5.x` 与 MCU 册，Linux 机制重点写 |
| 离线形态 | `dist/embedded.html`，manifest 对账 | `dist/embedded-linux.html`，manifest 对账 |

### 2.2 知识大纲（篇级骨架）

**MCU 9 篇（+ 建议补 3 个结构件）**
1. 嵌入式 C 深度：内存模型/指针/对齐/位域/`volatile`/宏/可重入/混汇编（建议补 `stdint`/大小端、错误码、固件数据结构）
2. 编译工具链：`arm-none-eabi-gcc`、链接脚本/启动文件/CMSIS/newlib-nano（补 picolibc 选型）
3. Cortex-M 架构与编程模型：寄存器/异常/NVIC/双栈/SysTick/MPU/系列差异（补 RISC-V 软件视角小节）
4. 裸机开发：RCC/时钟/GPIO/EXTI/TIM/ADC/UART/I2C/SPI/CAN/USB + DMA
5. 三种开发方式与软件架构：寄存器/LL/HAL、DMA、FSM/事件驱动/前后台
6. RTOS：FreeRTOS/RT-Thread/Zephyr，任务/同步/IPC/内存/典型问题
7. 系统工程：Bootloader/IAP/OTA/A-B/安全启动/日志断言/低功耗/看门狗（补参数持久化、HardFault 转储、IoT 安全基线、功能安全概念）
8. 工程效能：Make/CMake/Kconfig、GDB/OpenOCD/RTT、Unity/Ceedling、cppcheck/MISRA、**Git**、**AI 辅助**
9. 通信协议栈：Modbus/CANopen/LwIP/MQTT/AT/环形缓冲（补本地文件系统 FatFS/LittleFS/FlashDB）
- 建议补：⑩ 综合项目实战 + 选型决策（含"何时升级 Linux"）、⑪ 题库、附录 A–G

**Linux 9 模块（建议补 1 个应用基础模块）**
1. Cortex-A/SoC vs Cortex-M：MMU/页表/cache/EL0–EL3/TrustZone/GIC/通用定时器/SMP
2. 交叉编译：sysroot/`ARCH`/`CROSS_COMPILE`/QEMU user-mode/pkg-config
3. 启动链：ROM→SPL→TF-A(BL1/2/31/32/33)→U-Boot→内核+DTB；映像格式/cmdline/init
4. 设备树：DTS/DTB/compatible/reg/interrupts/pinctrl/clocks/Overlay/binding
5. 内核与驱动：menuconfig/ko/cdev/platform/`request_irq`/file_operations/并发/顶底半部；用户态 libgpiod/i2c-dev/spidev
- 建议在模块 5 前补：**Linux 应用基础**（进程/线程/IPC/Socket/epoll/内存模型）
6. rootfs：BusyBox/PID1/init/ext4/SquashFS+overlayfs/UBIFS/initramfs/devtmpfs
7. 构建系统：Buildroot vs Yocto（BitBake/recipe/layer/SDK/wic/复现构建）
8. OTA + 网络 + 调试：RAUC/SWUpdate/Mender、NetworkManager、ftrace/perf/strace/core dump/PREEMPT_RT
9. MCU vs Linux 选型与异构 SoC（rpmsg/共享内存、量化决策表）

### 2.3 边界原则（Q2=A）
- 硬件原理（电路、电平、时序电气参数）**只放链接、不重复**；软件侧写配置序列、代码、现象与排查。
- 跨册引用具体到篇/章（`EMBEDDED_OUTLINE.md` 已核对 25 个硬件册章节，无悬空引用）。

---

## ③ 行业与岗位能力调研（含 Rust / AI / 安全取舍）

> 详细证据、34 条 JD 样本表、来源 URL 与核实日期见行业调研子线回报；本节为结论与取舍。

### 3.1 岗位能力项（2026，按频次三档）

- **A 档·高频共同门槛（手册主线必覆盖）**：C 精通（指针/位操作/内存布局/`volatile`）；UART/I2C/SPI 原理与驱动；硬件协同（读原理图/datasheet、示波器/逻辑分析仪/JTAG）；Git + Linux 命令 + 工程文档；中断/时钟/DMA/看门狗；严谨/独立排查/沟通等软素质。
- **B 档·MCU 固件核心**：RTOS（任务/同步/IPC/优先级翻转/栈）；CAN/RS-485/USB/ADC+DMA；固件架构（状态机/前后台/事件驱动）；低功耗；Modbus/MQTT/LwIP；Make/CMake/Shell/Python；Bootloader/OTA。
- **C 档·Linux 专项**：启动链（U-Boot/内核裁剪/设备树/rootfs）；内核与驱动模型；Yocto/Buildroot；系统级调试（ftrace/perf/kprobe/kgdb）；应用层（多线程/IPC/Socket/epoll）；平台量产经验。
- **D 档·垂直专项（仅外链/附录导航）**：汽车 AUTOSAR/CANoe/UDS/ASPICE；端侧 AI（TFLite Micro/NPU 部署）；安全关键认证。

### 3.2 关键缺口补录（相对原大纲）

| 缺口 | 取舍 | 位置 | 优先级 |
|---|---|---|---|
| Git 工程实践（分支/评审/冲突/规范） | 收录（新增章） | MCU 第 8 篇 | 高 |
| 固件数据结构（环形缓冲/队列/CRC/边界） | 收录 | MCU 第 1/5 篇 | 高 |
| 仪器实操（示波器/逻辑分析仪/电流/接线） | 收录 | MCU 第 4/8 篇 | 高 |
| 中断与并发正确性（临界区/ISR 禁止项/可重入） | 强化 | MCU 第 4/6 篇 | 高 |
| Linux 应用基础（进程/线程/IPC/Socket/epoll） | 收录（新增模块） | Linux 模块 5 前 | 高 |
| 系统级调试与 Yocto 工程深度 | 强化 | Linux 模块 7/8 | 高 |
| 量产可靠性（错误码/标定/复位记录/老化） | 收录（小节） | MCU 第 7 篇 | 中 |

### 3.3 Rust 嵌入式：进阶附录，不与 C 并列

- **成熟度（2026）**：`embedded-hal` 1.0 稳定、`embedded-hal-async`、Embassy 为新项目事实默认、probe-rs/defmt 已成主流工具链；Ferrocene 取得 ISO 26262 ASIL D / IEC 61508 SIL 3 / IEC 62304 资格；Linux 7.0 内核把 Rust 转为永久特性。
- **缺口**：无线栈（BLE/Thread/Matter）成熟度与认证仍落后；版本演进快、迁移成本真实；编译慢。
- **就业信号**：34 条 JD 中 **MCU 岗无一条要求 Rust**，仅 Linux/系统方向作加分。
- **取舍**：MCU 册设 **1 章以内「进阶：Rust on MCU」**（生态地图、与 C 对照、适用边界、学习路径外链，不讲语言入门）；Linux 册模块 9 用一小段提趋势；**优先级低**，每 6 个月复查。

### 3.4 AI 辅助开发：收录方法论与边界，不做厂商测评

- **现状**：出现专用固件 AI（Embedder）、厂商助手（Microchip/ARM/Infineon）、通用工具（Copilot/CLion+Junie/Cursor/Claude Code）与国产（Trae/灵码）。
- **风险**：通用模型在固件层有三类幻觉——幻影 HAL 函数、DMA/中断映射错配、RTOS 时序错误；安全研究显示 LLM 生成代码漏洞率高，安全关键代码必须人工复核；涉密固件需本地/私有部署。
- **取舍**：MCU 第 8 篇新增 1 章「AI 辅助嵌入式开发」（适用边界、上下文注入工作法、三类幻觉复核清单、工具快照附录 + 隐私合规）；**优先级中高**；不做价格对比正文与工具广告。

### 3.5 安全与功能安全：概念 + 规则速查，全文仅外链

| 标准 | 适用 | 2026 版本 | 取舍 |
|---|---|---|---|
| MISRA C | 安全关键 C 编码事实标准 | **MISRA C:2025（201 rules + 22 directives）** | 收录 30–50 条日常核心规则速查 + 正反例 + 静态工具入门；**不再以 2012 为现行版** |
| IEC 61508 | 通用 E/E/PE 安全（SIL 1–4） | 2010 版 + 修订 | 概念科普，全文外链 |
| ISO 26262 | 汽车功能安全（ASIL A–D/QM） | 2018 版，第三版 DIS 征询中 | 概念科普，全文外链 |
| IEC 62304 | 医疗器械软件（Class A/B/C） | 2006+A1，Ed.2 制定中 | 仅外链 |
| IEC 60730/60335 | 家电/控制器自检（Class A/B/C） | 现行 | 外链 + 自检模式概念 |
- **取舍**：MCU 第 7/8 篇收「功能安全与可靠性入门」一章（V 模型、SIL/ASIL/Class 映射、防御式编程、覆盖度概念、可追溯）；标准全文、认证流程、ASPICE/DO-178C/SOTIF 仅外链。另：IoT 信息安全基线（RoT/安全启动/PSA 分级）并入第 7 篇；EU CRA 背景半页。

### 3.6 其他趋势
- **RISC-V**：MCU 第 3 篇加"软件视角差异"小节（不做指令集教学），RP2350 作为 RISC-V 专栏硬件依据；中优先级。
- **端侧 AI/TinyML**：趋势一节 + 外链，不收录模型训练；低优先级。
- **无线协议族**：概念地图 + 外链；低优先级。

---

## ④ 对标项目更新表（核实日 2026-10-21）

> 数字均来自本轮 GitHub REST API（`api.github.com/repos/...`）实时返回，非 GitHub 平台标注"未取到"。活跃度：当日–7 日=高；30 日=活跃；3 月=中；>1 年=停滞。

### 4.1 主表（11 个）

| # | 名称 | 形态/技术栈 | License | star（10-21） | 活跃度 | 可借鉴 / 我们的差异 |
|---|---|---|---|---|---|---|
| 1 | [Awesome-Embedded](https://github.com/nhivp/Awesome-Embedded) | Markdown 链接索引 | Unlicense | 9,238 / 1,226 fork | 活跃 | 分类目录可作附录骨架；纯链接无正文，我们做体系化讲解 |
| 2 | [FreeRTOS](https://github.com/FreeRTOS/FreeRTOS)（[内核](https://github.com/FreeRTOS/FreeRTOS-Kernel) 4,597） | C 源码发行 | MIT | 7,917 / 2,110 | 中（内核 10-16 提交） | 源码与文档版本对应；我们做调度原理与选型，不替代 API |
| 3 | [Zephyr](https://github.com/zephyrproject-rtos/zephyr) | C RTOS + Sphinx 文档 | Apache-2.0 | 16,850 / 10,229 | 高（当日） | 多架构/设备模型分层；我们做中立多 RTOS 对比 |
| 4 | [RT-Thread](https://github.com/RT-Thread/rt-thread) | C RTOS（中文 docsify 文档） | Apache-2.0 | 12,293 / 5,483 | 高（10-19） | 中文术语/PR 协作；我们做中立对比 |
| 5 | [ESP-IDF](https://github.com/espressif/esp-idf) | C/Python SDK + 厂商文档 | Apache-2.0 | 19,300 / 8,555 | 高（10-20） | 环境→外设→协议栈递进；单厂商 SDK，我们跨厂商 |
| 6 | [arduino-esp32](https://github.com/espressif/arduino-esp32) | C/C++ Arduino 核心 | LGPL-2.1 | 17,590 / 7,927 | 高（当日） | 低门槛示例；**LGPL 传染，引用须隔离注明** |
| 7 | [Compiler Explorer](https://github.com/compiler-explorer/compiler-explorer) | TS/Node（godbolt.org） | BSD-2 | 19,145 / 2,141 | 高（当日） | 代码-汇编对照；作外链实验，不内嵌 |
| 8 | [Renode](https://github.com/renode/renode) | C#/Python 仿真 | MIT | 3,050 / 547 | 高（当日） | 可复现仿真；作外链，不实现仿真器 |
| 9 | [Wokwi](https://wokwi.com/)（[docs](https://github.com/wokwi/wokwi-docs) 206） | 核心闭源 Web 仿真，周边开源 | 闭源/MIT | 核心未取到 | 高 | 无硬件跑通入门；闭源单形态，我们开源 + 双形态 |
| 10 | [Awesome C](https://github.com/inputsh/awesome-c) | Markdown 链接索引（**已归档**） | NOASSERTION | 3,855 / 366 | 停滞（约 4 年） | 反面教材：链接需巡检、内容化 |
| 11 | [awesome-embedded-software](https://github.com/iDoka/awesome-embedded-software) | Markdown 清单 | CC0 | 1,136 / 110 | 中 | 按资源约束分级选型；无原理讲解 |

### 4.2 新增同类（摘要）

- **中文大手册（非嵌入式）**：[JavaGuide](https://github.com/Snailclimb/JavaGuide)（VuePress2，159,181★，高）、[doocs/leetcode](https://github.com/doocs/leetcode)（36,706★，高）——借鉴中文大手册分层与"知识点-代码-题解"密度；领域不同。
- **嵌入式中文站**：[100ask ELinuxCourse-Docs](https://github.com/100askTeam/ELinuxCourse-Docs)（Docusaurus，12★）、[Staok/ARM-Linux-Study](https://github.com/Staok/ARM-Linux-Study)（博客，353★，CC BY-NC-SA）、[wujique/stm32f407](https://github.com/wujique/stm32f407)（RTD 文档，208★，代码停滞）、[zhengnianli/EmbedSummary](https://github.com/zhengnianli/EmbedSummary)（5,898★，GitHub 停滞）。
- **Rust embedded**：[awesome-embedded-rust](https://github.com/rust-embedded/awesome-embedded-rust)（8,149★）、[Embedded Rust Book](https://github.com/rust-embedded/book)（1,355★）、[Discovery](https://github.com/rust-embedded/discovery)（1,606★）、[RPi OS tutorials](https://github.com/rust-embedded/rust-raspberrypi-OS-tutorials)（14,740★，停滞）。
- **浏览器交互教学**：[CircuitVerse](https://github.com/CircuitVerse/CircuitVerse)（1,282★）、[pxt-microbit](https://github.com/microsoft/pxt-microbit)（809★）、[logisim-evolution](https://github.com/logisim-evolution/logisim-evolution)（7,807★，**GPL-3.0**）、CPUlator（闭源，未取到）。
- 厂商参照（非开源）：野火、正点原子、RT-Thread 文档、韦东山、RYMCU。

### 4.3 结论

1. 三类对标（源码仓库 / 链接索引 / 在线工具）均非"体系化中文手册"，不直接构成竞品。
2. 中文嵌入式内容高度绑定开发板/课程，框架分散（docsify/Docusaurus/Sphinx/博客），缺中立、跨厂商、双形态、全链路开源手册。
3. **核心结论：未发现"VitePress + 中文 + 代码密集 + 嵌入式"成熟手册，该象限为空**（成熟中文大手册 JavaGuide 用 VuePress；嵌入式中文站无一用 VitePress）。
4. 差异化：中立跨厂商、全链路（裸机→RTOS→Linux 衔接）、在线+离线双形态、内容化代码密集、可补中文 Rust/中文 Linux 手册空白。
5. 风险：LGPL/GPL 代码须隔离；链接需定期巡检；建立持续维护机制（个人仓库停滞 2.7–7 年是共同教训）。

---

## ⑤ 试点章写作大纲（MCU 5 + Linux 4）

> 每章"目标 / 小节 / 最小代码与现象 / 图示 / 交叉引用 / 验收"六字段完整版见 `EMBEDDED_OUTLINE.md` 第二部分；此处给每章的目标、关键小节与现象。

### 5.1 MCU 试点（建议落在 `apps/embedded/docs/`）

**M1 · 开发环境与点亮 LED**（`getting-started/toolchain-blink.md`）
- 目标：装 Arm GNU Toolchain + 烧录工具，Makefile/CMake 构建最小工程，烧录或 Wokwi 仿真，LED 闪烁；说清每个文件职责。
- 小节：范围与平台约定 → 主机安装（Toolchain 15.x/CubeCLT/OpenOCD）→ 工程目录 → 第一个 main（HAL 初始化+GPIO 翻转）→ 构建产物（`size` 读段）→ 烧录验证（无硬件 Wokwi）→ 报错对照。
- 现象：LED 1s 周期闪烁；`size` 三段可读。图示：构建-烧录-运行链路（Mermaid flowchart）。

**M2 · 从复位到 main**（`boot/reset-to-main.md`）
- 目标：对照启动文件与链接脚本，说清复位到 `main()` 间 CPU 动作；看懂 map 段地址；指出 `.data/.bss` 初始化错误现象。
- 小节：复位取指（SP/PC/VTOR）→ `Reset_Handler` 逐行（搬 `.data`、清 `.bss`、`SystemInit`、`__libc_init_array`、`main`）→ linker script（`MEMORY/SECTIONS/段符号`）→ 内存布局 → map 解读 → 三类故障定位。
- 现象：注释 data 搬运后全局变量初值异常（故障演示）。图示：上电→main（Mermaid TD）、内存布局（SVG）。

**M3 · GPIO 与外部中断（三方式）**（`peripherals/gpio-exti-three-ways.md`）
- 目标：同一 GPIO 输出+按键中断，用寄存器/LL/HAL 分别实现并对比；说清 EXTI 序列与标志清除时机。
- 小节：GPIO 回顾 → 寄存器方式 → LL 方式 → HAL 方式 → EXTI（线映射/触发沿/NVIC/ISR 清标志/消抖）→ 三方式对照表（实测行数/体积）。
- 现象：按键翻转 LED；不消抖计数抖动。图示：EXTI 路径（Mermaid）、三方式对照表。

**M4 · 串口收发与 printf 重定向**（`peripherals/uart-ringbuffer-dma.md`）
- 目标：UART 轮询→中断→DMA 三级演进；`printf` 重定向；环形缓冲组织接收；解释帧错误与缓冲满策略。
- 小节：接线与波特率（KaTeX）→ 轮询 → 中断+环形缓冲（ISR 入队、主循环解析）→ printf（`_write`/newlib-nano 浮点体积）→ DMA+IDLE 双缓冲/零拷贝 → 帧协议状态机 → 故障排查。
- 现象：回显+定时打印；DMA 下 CPU 占用下降。图示：DMA+IDLE 时序（Mermaid sequence）、环形缓冲（SVG）。

**M5 · RTOS 入门**（`rtos/first-task-scheduler.md`）
- 目标：FreeRTOS 建两任务+一队列，演示抢占/延时/通知；理解任务状态、优先级、临界区；识别栈溢出与优先级反转。
- 小节：为何上 RTOS → 移植与 `FreeRTOSConfig.h` → 第一个任务（`xTaskCreate/vTaskDelay`）→ 调度与任务状态 → 队列/任务通知 → 临界区与 FromISR → 栈高水位调试 → 三内核对照。
- 现象：两任务按优先级交替打印、无冲突。图示：任务状态迁移（Mermaid state）、抢占时序（Mermaid sequence）。

### 5.2 Linux 试点（建议落在 `apps/embedded-linux/docs/`）

**L1 · 开发环境与交叉编译（QEMU）**（`getting-started/cross-compile-qemu.md`）
- 目标：WSL2/Ubuntu 装 aarch64 工具链，交叉编译 Hello，QEMU user-mode 运行；理解 sysroot 与前缀；与 MCU 工具链对照。
- 小节：实验基线（QEMU virt）→ 主机准备 → 工具链（前缀拆解/ABI）→ 交叉程序（`file/readelf`）→ sysroot/第三方库 → MCU vs Linux 工具链对照 → 报错。
- 现象：`qemu-aarch64 hello` 打印，`file` 确认 ARM64。图示：主机→交叉→QEMU（Mermaid）。

**L2 · 启动链全景**（`boot/boot-chain-panorama.md`）
- 目标：画出 ROM→用户空间全链路，说清各阶段职责/镜像/内存传递；QEMU 一条命令启动并从串口定位各阶段。
- 小节：为何链路长 → 全景（ROM/SPL/TF-A BL/U-Boot/内核+DTB+rootfs）→ 各阶段职责 → U-Boot 变量与命令（`bootcmd/bootargs/bootm/bootz/booti`）→ cmdline 参数 → QEMU virt 实战（`-M virt,gic-version=3`）→ 无 TF-A 简化路径 → MCU 对照。
- 现象：串口依次打印引导→解压→内核日志→login。图示：启动链全景（Mermaid TD，标 EL）。

**L3 · 设备树入门**（`devicetree/first-dts.md`）
- 目标：看懂节点与 compatible/reg/interrupts；编译自定义 DTB 用 QEMU 传入；`/proc/device-tree` 验证；理解 `of_match_table`。
- 小节：为何用设备树 → DTS/DTSI 与 `dtc`（aliases/chosen）→ compatible 匹配 → reg 与 `#cells/ranges` → interrupts/GIC → GPIO/pinctrl/clocks → 实战（`dumpdtb` 提取+加 led 节点）→ 验证 → Overlay 概念。
- 现象：新节点出现在 `/proc/device-tree`。图示：DTS→DTB→解析、节点-驱动匹配（Mermaid）。

**L4 · 用户态硬件访问**（`userspace/gpio-i2c-access.md`）
- 目标：libgpiod v2 控制 GPIO 点灯，i2c-dev ioctl 读传感器；理解字符设备/权限/节点由来；与 MCU 寄存器对照。
- 小节：三条官方路径（sysfs 废弃、`/dev/mem` 禁忌）→ GPIO chardev v2（libgpiod 2.x）→ libgpiod 点灯 → i2c-dev（`I2C_SLAVE`/字节序）→ 读传感器 → spidev 边界 → udev 权限 → MCU 对照。
- 现象：`gpioset` 翻转、`i2cdetect` 列器件、读数可解释。图示：用户态→字符设备→驱动→硬件（Mermaid）。

### 5.3 试点验收通用标准
每章：命令可从零复现、最小代码为骨架占位、现象可观察、图示标注 Mermaid/SVG、交叉引用具体到篇章、章末自测 ≥5 题；试点 9 章先跑通"新 app 的 schema/搜索/学习隔离/离线包"，再决定是否继续。

---

## ⑥ 内容形态与 Mermaid 接入评估

### 6.1 内容形态（沿用 Q4=A / Q5=A）
- 每 app 双形态：在线 VitePress + 离线单文件 `dist/<slug>.html`，起步即做，manifest 对账。
- 代码运行/仿真：**本期只外链**（Godbolt/Compiler Explorer、Wokwi、Renode），不内嵌、不自建仿真器。
- 图标：内联 SVG 线性图标，无 emoji；公式 KaTeX；图表 ECharts。

### 6.2 Mermaid 接入方案对比（当前全仓 grep=0，需新接入）

| 方案 | 说明 | 优点 | 缺点 | 离线影响 |
|---|---|---|---|---|
| A. `@vitepress-plugin/mermaid` | Vite 插件 + `:::mermaid` 容器，客户端渲染 | 接入简单、与现有容器风格一致、支持主题/look | 单作者、周下载约 3、仅 1 版本、维护风险 | 离线需内联 mermaid（体积大） |
| B. `@discretetom/vitepress-plugin-mermaid` / `vitepress-mermaid` | `withMermaid` 配置包装 | 配置式、文档较多 | 同样客户端渲染、维护参差 | 同上 |
| C. **自封装共享组件**（`@mermaid-js/mermaid`，在 theme/shared-config 提供 `<Mermaid>` 组件，`setup/onMounted` 渲染） | 自控版本、主题变量、确定性 ID | 完全可控、统一风格、可设 `securityLevel`、对接深浅色 | 需自维护薄封装 | 可控制内联范围 |
| D. **构建期渲染为静态 SVG**（构建时用 headless/Playwright 或 mermaid SSR 出 SVG） | 图在构建期定型 | 零运行时 JS、体积小、天然离线、确定性最强 | 需构建期 DOM、流程复杂、无交互 | 离线最友好 |

- **建议**：v1 采用 **方案 C（自封装共享组件，客户端渲染、确定性 ID、`securityLevel:'strict'`）**，一条代码路径同时服务在线与离线；把 **方案 D（构建期 SVG）** 列为离线体积超预算后的演进。方案 A 因维护风险不首选。
- **落地要求**：作为共享能力放在 `shared-config`/`theme`，新 app 零配置可用；接入时**单独写 ADR**（依赖、渲染时机、离线内联策略、主题变量）；与现有 `markdown-it-container` 风格统一。
- 边界：Mermaid 只用于时序/状态/流程；内存布局、时序波形走 SVG（与硬件册风格统一）。

---

## ⑦ 分阶段路线与规模估算

### 7.1 规模估算（以硬件册 140 章为参照）

| 分册 | 章节规模 | 图示规模 | 说明 |
|---|---|---|---|
| embedded（MCU） | 90–115 章 | 中（代码密集，图多为时序/流程/寄存器表） | 9 篇 + 实战/题库/附录 |
| embedded-linux | 40–60 章 | 中（启动链/内存布局/流程图） | 9 模块 + 应用基础 |

### 7.2 建议阶段（每阶段可独立回滚/验收）

- **P4-1 接入与试点（先串行）**：接 Mermaid（写 ADR）；建 `apps/embedded`，落地 M1–M5 试点，跑通新 app 全链路（构建/质检/快照/离线/学习隔离/搜索/截图）。
- **P4-2 两线并行**：MCU 按篇批次推进（C 深度→工具链→架构→裸机→架构模式→RTOS→系统工程→工程效能→协议栈）；Linux 建 `apps/embedded-linux`，落地 L1–L4 试点。
- **P4-3 分册成型**：完成各篇/模块主体 + 综合实战 + 题库；门户卡片改 `available:true`。
- **P4-4 收尾**：离线对账、全量 `verify:all`、截图自检、文档（ARCHITECTURE/PLAYBOOK/CHANGELOG）、ADR 状态更新。

### 7.3 验收硬指标（沿用硬件册口径）
- 章节/图片/SVG 数与 manifest 快照一致；离线 `dist/<slug>.html` 章节对账；
- 0 console error、无横向溢出、无 emoji、图标全 SVG；
- 学习键正确隔离（`lubook.v1.embedded.learning` / `.embedded-linux.learning`），新册不串硬件历史；
- 全仓 grep 无旧品牌残留；两线均给出命令可复现清单。

---

## ⑧ Codex 建议需求候选 Backlog（可勾选，不替用户决定）

> 依据工程外 Codex《平台级架构重设计》，对照当前 monorepo 实际状态逐条标注。状态：✅已实现 / 🟡部分实现 / ⬜未实现；关联：P4 必需 / 平台增强 / 暂缓。勾选框供用户决定。

### 8.1 内容模型与治理

| 勾选 | Codex 建议 | 状态 | 关联 | 优先级 | 所需 ADR |
|---|---|---|---|---|---|
| ☐ | 稳定 `id`/URL，重命名提供 redirect | 🟡（快照能捕获删除/变化，无自动 redirect 机制） | 平台增强 | 中 | 是（URL 破坏） |
| ☐ | 文档状态机 draft→technical-review→editorial-review→published→deprecated | 🟡（frontmatter 有 `status`，但全为 published，无状态机） | 暂缓 | 低 | 是 |
| ☐ | 机器可读审核索引（章节/严重度/修复/复核/状态） | ⬜ | 暂缓 | 低 | 否 |
| ☐ | **SourceRef 结构化版权模型**（type/license/retrievedAt/usedFor） | 🟡（`sources` 为纯字符串列表） | 平台增强 | 中 | 是（版权） |
| ☐ | 第三方素材独立许可证清单（SVG/字体/KaTeX/ECharts/仿真器） | 🟡（有 `THIRD_PARTY_LICENSES.md`，未与 SourceRef 打通） | 平台增强 | 中 | 否 |

### 8.2 编译与包边界

| 勾选 | Codex 建议 | 状态 | 关联 | 优先级 | 所需 ADR |
|---|---|---|---|---|---|
| ☐ | 单一 TS 内容管线（在线/离线共用同一 AST） | 🟡（content-core 为 TS，但离线/质检为 Python 自行解析，存在分叉） | 平台增强 | 中 | 否 |
| ☐ | 独立包 content-schema / site-config / offline / quality | 🟡（有 content-core/shared-config/theme/learning；离线/质检在 Python tooling） | 暂缓 | 低 | 否 |
| ☐ | 生成物统一 `.generated/`（不入库） | 🟡（manifest 在 `.generated`；sidebar/catalog 在 docs/.vitepress） | 平台增强 | 低 | 否 |
| ☐ | 构建缓存按 content checksum + lockfile + toolchain | ⬜ | 暂缓 | 低 | 否 |

### 8.3 学习数据与云同步

| 勾选 | Codex 建议 | 状态 | 关联 | 优先级 | 所需 ADR |
|---|---|---|---|---|---|
| ☐ | LearningRepository 仓储接口（UI 不直碰存储） | ✅ | — | — | — |
| ☐ | 旧键迁移 + 导入导出（merge/replace）+ tombstone | ✅（hardware legacyKeys 已配） | — | — | — |
| ☐ | **IndexedDB 存储**（笔记/题目/仿真数据；localStorage 仅设置） | ⬜（现用 localStorage，代码注释明确不引入） | 暂缓 | 低 | 是（数据格式） |
| ☐ | 云同步预留（updatedAt/deviceId/revision、provider 接口、冲突策略） | 🟡（笔记有 updatedAt；无 deviceId/revision/provider） | 暂缓 | 低 | 是（云同步） |

### 8.4 质量、安全与发布

| 勾选 | Codex 建议 | 状态 | 关联 | 优先级 | 所需 ADR |
|---|---|---|---|---|---|
| ☐ | 统一 `verify` 入口、固定顺序 | ✅（`verify:all`） | — | — | — |
| ☐ | Playwright 浏览器冒烟（首页/代表章/暗色/移动/搜索/学习迁移） | 🟡（shot.py 本地自检，未进 CI、未强制） | 平台增强 | 中 | 否 |
| ☐ | **axe 无障碍检查** | ⬜ | 平台增强 | 中 | 否 |
| ☐ | **产物体积预算**（首屏/单文件/搜索索引/横向溢出） | ⬜ | 平台增强 | 中 | 否 |
| ☐ | **CSP 白名单 + 危险 HTML 清理 + ECharts 字段白名单** | ⬜（现资源全本地化，列 Backlog B10） | 暂缓（接外部内容时必需） | 中 | 是（安全） |
| ☐ | 依赖漏洞 high/critical 阻断 + 带期限例外 ADR | 🟡（可手动 `pnpm audit`，未进 CI 门禁） | 平台增强 | 中 | 否 |
| ☐ | 构建一次多处发布 + `release.json`（SHA/revision/工具链/锁哈希） | 🟡（bundle 按目标分别构建，因 base 不同；无 release.json） | 暂缓 | 低 | 是（发布） |
| ☐ | PR 预览环境 | ⬜ | 暂缓 | 低 | 是 |

### 8.5 Phase 4 产品功能（分别立项、分别建模）

| 勾选 | 功能 | 状态 | 关联 | 优先级 | 所需 ADR |
|---|---|---|---|---|---|
| ☐ | 仿真器（外链 Wokwi/Renode/Godbolt，本期不内嵌） | 🟡（仅外链，Q5=A） | 暂缓 | 低 | 是（若内嵌） |
| ☐ | 题库组卷（动态组卷/随机出题） | 🟡（硬件册有静态题库章，无动态组卷） | 暂缓 | 低 | 是 |
| ☐ | 计算器（在线工程计算器） | ⬜ | 暂缓 | 低 | 否 |
| ☐ | 间隔重复 SRS | ⬜ | 暂缓 | 低 | 是（数据） |
| ☐ | 评论（Giscus 等） | ⬜（接入即触发 CSP/外部来源） | 暂缓 | 低 | 是 |
| ☐ | PWA（可安装/离线） | ⬜ | 暂缓 | 低 | 是 |
| ☐ | 英文版 / 多语言 | ⬜ | 暂缓 | 低 | 是 |
| ☐ | 云同步 / 账号体系 | ⬜ | 暂缓 | 低 | 是 |

> 说明：以上勾选均为"是否要做"的候选，**不在本轮实施**；P4 真正必需的平台项只有"⑥ Mermaid 接入"与"① 接入清单"，其余为平台增强或暂缓。

---

## ⑨ 待用户拍板的开放问题（选择题）

> 以下为建议默认值，用户可直接选择或修改。

**Q1. Rust 嵌入式如何纳入？**
- A.（建议）进阶附录 1 章以内（生态地图 + C 对照 + 边界 + 外链），不与 C 并列
- B. 独立成篇，与 C 同等深度
- C. 仅外链，不写任何 Rust 内容
- D. 暂不收录

**Q2. AI 辅助开发是否收录？**
- A.（建议）收录 1 章方法论与边界（含三类幻觉复核清单），不做厂商测评
- B. 收录并做工具测评对比
- C. 仅外链
- D. 不收录

**Q3. 功能安全 / MISRA 深度？**
- A.（建议）功能安全概念 1 章 + MISRA C:2025 核心规则速查（30–50 条），标准全文外链
- B. 深入到可指导认证流程
- C. 仅概念科普，不做规则速查
- D. 不收录

**Q4. 仿真 / 代码运行方式？**
- A.（建议）本期仅外链（Godbolt/Wokwi/Renode），不内嵌
- B. 评估内嵌 Wokwi/Renode（需额外 ADR、安全与体积评估）
- C. 自建仿真器

**Q5. Mermaid 落地方式？**
- A.（建议）自封装共享组件（客户端渲染、确定性 ID、strict），写 ADR
- B. 直接用 `@vitepress-plugin/mermaid`
- C. 构建期渲染为静态 SVG
- D. 暂不接入

**Q6. 两册优先级与节奏？**
- A.（建议）先 MCU 试点 5 章跑通新 app，再两线并行
- B. MCU 与 Linux 完全并行起步
- C. 先完整做完 MCU 再做 Linux
- D. 先做 Linux

**Q7. MCU 主例芯片？**
- A.（建议）STM32F4 为主例（资料多、外设全），F1/ESP32/RISC-V 差异专栏
- B. STM32F1 为主例（寄存器简洁、适合入门）
- C. ESP32 为主例
- D. 多平台完全并重

**Q8. Linux 试点 L4 硬件呈现？**
- A.（建议）QEMU 演示流程 + 真实板卡（RPi4/STM32MP1）照片/日志双轨
- B. 仅 QEMU
- C. 必须真实板卡

**Q9. Codex 平台增强项（SourceRef 版权 / IndexedDB / axe / 体积预算 / CSP / release.json）勾选哪些？**
- A.（建议）本轮都不做，仅保留 backlog；待 P4 主体完成后再评估
- B. 勾选 SourceRef + 体积预算（低成本、收益直接）
- C. 勾选全部平台增强
- D. 逐项另行确认（见 §8 表格）

**Q10. 新增文档 EMBEDDED_OUTLINE.md 是否保留？**
- A.（建议）保留为详细底稿（与 EMBEDDED_PLAN 并列，供落地时引用）
- B. 并入本文后删除，只留 EMBEDDED_REQUIREMENTS
- C. 移到 docs/ 目录

---

> 本轮为 P4 评审稿，未创建任何 app、未写正文/代码、未提交、未部署；待用户对 §9 拍板后，再进入 P4-1 接入与试点。



