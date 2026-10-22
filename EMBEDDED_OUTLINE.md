# 两册嵌入式分册 · 知识地图细化与试点章写作大纲（EMBEDDED_OUTLINE）

> 状态：**前置架构文档（P4 立项前）**。本文只做知识地图与章级写作大纲，**不写正文、不写代码实现、不建 app、不改 CI/配置、不提交**。
> 输入底稿：[`EMBEDDED_PLAN.md`](EMBEDDED_PLAN.md)（§2 知识地图、§3 边界矩阵、§7 试点章）；硬件分册目录：[`apps/hardware/docs/SUMMARY.md`](apps/hardware/docs/SUMMARY.md)（交叉引用以其中 slug 为准）。
> 命名基线：`appId=embedded`《嵌入式软件开发手册》（Cortex-M / C / 裸机 / RTOS）、`appId=embedded-linux`《嵌入式 Linux 开发手册》（Cortex-A / 启动链 / 设备树 / Yocto / OTA）；base `/lubook/embedded/`、`/lubook/embedded-linux/`；学习键 `lubook.v1.embedded.learning`、`lubook.v1.embedded-linux.learning`（依据 `docs/NAMING.md`）。
> 日期：2026-10-21。文中 2026 事实均经公开资料核实，来源见第三部分 C 节。

---

## 第一部分 · 两册知识地图细化

### 约定

- **必讲**：主线章正文覆盖，落到最小代码/命令与现象；**对比讲**：与其他平台/方式同表对照、不单独成章；**外链**：只放官方文档/书/工具链接，正文不展开；**附录**：速查表/模板/清单，不占主线篇幅。
- 小节级别为章内 `##`（三级标题体系：篇 → 章 → 节）。
- 交叉引用格式：`hardware/5.x <slug>` 指硬件分册章；`MCU 第 N 篇`、`Linux 模块 N` 指本分册；`MCU 试点 M#`、`Linux 试点 L#` 指第二部分大纲章。

---

### A. MCU 线 `embedded`（Cortex-M / C / 裸机 / RTOS，9 篇 + 补 3 个结构件）

#### A1 第一篇 · 嵌入式 C 语言深度

**核心问题（读完能回答）**：为什么嵌入式 C 不等于桌面 C？段内存布局、指针、对齐、`volatile` 在固件里各自解决什么问题？代码怎么写才在资源受限、中断并发下不出错？

**建议小节**

1.1 嵌入式 C 与桌面 C 的差异（RAM/Flash 预算、无 OS、libc 裁剪、确定性要求）
1.2 内存模型与堆栈（`.text/.rodata/.data/.bss`、heap/stack 相向增长、LMA/VMA 概念引入；与第二篇链接脚本衔接）
1.3 指针进阶（数据指针/`void*`/多级指针、指针数组与函数指针；指针与数组退化；`const` 修饰指针三种读法）
1.4 结构体对齐与位域（自身大小对齐、整体对齐、尾部 padding、`packed`、非对齐访问触发 HardFault；`offsetof`/`sizeof`）
1.5 位操作与寄存器掩码（置/清/翻/取位宏、`BIT(n)`、读-改-写在中断共享寄存器上的原子性；位域布局跨编译器不确定，寄存器操作推荐掩码）
1.6 关键字语义：`volatile`/`const`/`static`/`extern`（寄存器映射、ISR 共享标志、文件域隐藏、跨单元声明；`volatile` 不保证原子性）
1.7 宏、条件编译与 X-Macro（函数式宏副作用、`do{}while(0)`、头文件保护、板型/芯片裁剪、表驱动）
1.8 类型规范与大小端（`stdint.h`/`inttypes.h`、端点判定与转换、网络/总线序）
1.9 可重入与线程安全（可重入条件、与线程安全的区别、临界区保护；newlib `malloc/printf` 默认非可重入问题；与第六篇 RTOS 衔接）
1.10 C 与汇编混合（内联汇编、`.s/.S`、AAPCS/EABI：R0–R3 传参、栈 8 字节对齐、开关中断）
1.11 标准库选型与错误处理（newlib/newlib-nano/picolibc 对比、`errno`/`assert`、错误码设计、静态分配优先于 `malloc`）

**分级**

- 必讲：1.1–1.7、1.10、1.11 基础概念；1.8、1.9 必讲基础，线程安全细节在第六篇深化。
- 外链：Barr Group《Embedded C Coding Standard》、王利涛《嵌入式 C 语言自我修养》、Barr C Standard 免费 HTML。
- 附录：AAPCS 传参速查表、`stdint.h` 类型对照表、错误码模板。

**交叉引用**

- `hardware/4.1 number-systems`（数制/补码）、`hardware/4.2 logic-gates-boole`（位运算逻辑）、`hardware/4.9 memory`（存储类型）。
- MCU 第二篇（段布局/链接符号）、第三篇（MSP/PSP）、第六篇（临界区/可重入）。
- Linux 模块 5（内核 C 子集与 GNU 扩展差异，仅一句对照）。

**本篇遗漏 / 2026 更新点**

- 底稿缺：`stdint`/大小端、错误码与断言、静态内存池、标准库选型对比、多文件工程与头文件依赖关系。
- 2026 更新：C 版本基线需写明（主流裸机 C99/C11；Zephyr 4.4 已用 C17）；picolibc 已在 ESP-IDF v6 默认替代 newlib，体积/栈占用实测数据应入正文（见第三部分 C）。

#### A2 第二篇 · 编译工具链（arm-none-eabi-gcc）

**核心问题**：一份 `.c` 如何变成可烧录的 `.bin/.hex`？链接脚本与启动文件各自保证了什么？如何用 `map/size/nm/objdump` 定位段溢出与未定义符号？

**建议小节**

2.1 工具链组成与版本基线（编译器/汇编器/链接器/`objcopy`；Arm GNU Toolchain 15.x、STM32CubeCLT 1.21；Windows/WSL/macOS 安装与 PATH；与 Linux 交叉编译器前缀对照）
2.2 构建全流程（预处理 `-E` → 编译 `-O0..-Os` → 汇编 `-S` → 链接 → `objcopy`；`.elf/.map/.bin/.hex`；关键选项表：`-Wall -Wextra -ffunction-sections -fdata-sections -Os`）
2.3 链接脚本精读（`MEMORY`、FLASH/RAM 地址、`SECTIONS`、LMA/VMA、`AT>`、`KEEP()`、`--gc-sections`；符号 `_estack/_sidata/_sdata/_ebss/_sbss`）
2.4 启动文件精读（初始 SP → `Reset_Handler` → `.data` 搬运 → `.bss` 清零 → `SystemInit` → `__libc_init_array` → `main`；CMSIS v6 启动文件由汇编转 C 的变化）
2.5 map 文件与体积分析（`size`、`nm`、`objdump -d/-t`、`readelf`；段占用定位；栈/堆预留估算方法）
2.6 系统调用桩与库裁剪（`_sbrk`、`_write/_read`、`_exit`；`nano.specs`；浮点 `printf` 体积代价；picolibc 对比实测）
2.7 静态库与工程结构（`.a` 与链接顺序、多目录组织；Makefile/CMake 概念入门，构建系统在第八篇深化）

**分级**

- 必讲：2.1–2.5；2.6 必讲基础、体积实测入附录；2.7 概念必讲、构建细节归第八篇。
- 外链：Compiler Explorer（Godbolt）源码↔汇编对照。
- 附录：常用编译/链接选项速查、链接错误消息对照表、产物文件类型表。

**交叉引用**

- MCU 第一篇 1.2（段/符号）、试点 M2（启动文件/链接脚本实战）。
- `hardware/5.2 minimum-system`（复位/时钟硬件条件）。
- Linux 模块 2 / 试点 L1（`ARCH=`/`CROSS_COMPILE=`/sysroot 对照表）。

**本篇遗漏 / 2026 更新点**

- 底稿缺：Windows 主机安装与 PATH/WSL 说明（读者多为 Windows）、链接错误与段重叠实战、picolibc、Arm Clang/LLVM 与 GCC 双工具链对照、CMake+Ninja 现代构建入口（CubeCLT 1.15+ 与 VS Code 扩展 2.0 已走 CMake/Ninja）。

#### A3 第三篇 · Cortex-M 架构与编程模型

**核心问题**：CPU 内部寄存器、模式、双栈与中断响应如何工作？异常如何自动入栈/出栈？M0 到 M33/M85 的内核差异在选型时影响什么？

**建议小节**

3.1 寄存器组与模式（R0–R15、xPSR、PRIMASK/FAULTMASK/BASEPRI/CONTROL；Thread/Handler 模式；特权级）
3.2 双栈 MSP/PSP 与栈指针切换
3.3 NVIC 与异常响应（使能/挂起/active、自动压栈 8 项、尾链/迟到、`EXC_RETURN`、优先级分组、VTOR、延迟向量）
3.4 PendSV/SVC 与上下文切换（为什么 RTOS 上下文切换用 PendSV；SVC 调用约定；为第六篇预埋）
3.5 中断优先级与临界区（PRIMASK/BASEPRI 实现临界区；中断安全原则）
3.6 SysTick 与系统节拍（24 位、RTOS tick 来源）
3.7 MPU 与内存保护（区域/权限/对齐规则；实战注意事项）
3.8 FPU 上下文与惰性压栈（Lazy stacking）、DSP/SIMD 指令概览
3.9 bit-band 位带别名访问
3.10 系列差异表（M0/M0+、M3、M4、M7、M23/M33、M85；TrustZone-M、PAC/BTI、Helium/MVE；MPU 与 MMU 边界）
3.11 调试组件（DWT/ITM/SWO、周期计数与时间戳；调试用法归第八篇）
3.12 HardFault 原理与向量表（诊断流程归第八篇/第七篇）

**分级**

- 必讲：3.1–3.7、3.10；3.8/3.9 理解级；3.11/3.12 基础概念、诊断归后篇。
- 外链：ARM DUI 系列 Generic User Guide、各内核 TRM。
- 附录：内核寄存器位速查、M0–M85 选型对照表。

**交叉引用**

- `hardware/5.4 interrupts`（NVIC/优先级硬件视角）、`hardware/4.12 clock-reset-design`。
- MCU 第四篇（中断驱动）、第六篇（PendSV 上下文切换）。
- Linux 模块 1（MMU/EL 特权级对照表，逐项对照 NVIC/SysTick/MPU）。

**本篇遗漏 / 2026 更新点**

- 底稿缺：`EXC_RETURN` 详解、FPU 惰性压栈、PendSV/SVC、DWT/SWO、HardFault 向量处理、TrustZone-M 基础、M7 cache/TCM 与 cache 一致性（与第五篇 DMA 呼应）。
- 2026 更新：补 M85/Armv8.1-M Helium、M52；CMSIS 6 头文件与内建函数现状；Armv8-M SMP 概念预埋（FreeRTOS 11.3 已支持 Armv8-M SMP）。

#### A4 第四篇 · 裸机开发

**核心问题**：不使用 RTOS，如何按参考手册把时钟、GPIO、定时器、ADC、UART、I²C、SPI、CAN 配置起来并跑通最小收发？每个外设的最小寄存器序列是什么？

**建议小节**

4.1 时钟树软件初始化（HSI/HSE→PLL→SYSCLK→AHB/APB、Flash wait state、RCC 寄存器序列）
4.2 复位类型与启动向量（复位序列、向量表位置、复位原因寄存器）
4.3 GPIO 模式与复用（输入/推挽/开漏/复用/上下拉；试点 M3 深化三方式）
4.4 EXTI 外部中断（触发沿、线映射、NVIC 使能、标志清除、按键消抖）
4.5 定时器：时基/输出比较/输入捕获/PWM/编码器（预分频/计数模式、频率与占空比计算、编码器读数实战）
4.6 ADC：单通道/扫描/DMA/校准/过采样（VREFINT 校准、软件滤波）
4.7 DAC 与 DMA 波形生成
4.8 UART 收发：轮询/中断/DMA + 环形缓冲（试点 M4）
4.9 I²C：时序/起始停止/ACK/时钟拉伸/位模拟/外设读写
4.10 SPI：CPOL/CPHA/主从/DMA
4.11 CAN：位时序/过滤器/邮箱/收发
4.12 RS-485 方向控制与半双工时序
4.13 USB 设备概览（端点/枚举/设备类；协议栈深度借第九篇）
4.14 RTC 与日历（掉电走时、闹钟唤醒）

**分级**

- 必讲：4.1–4.5、4.8、4.9、4.10；4.6/4.7/4.11/4.12 必讲最小实例；4.13 概念 + 外链协议栈；4.14 必讲基础。
- 外链：厂商参考手册对应章节、USB 设备类规范。
- 附录：各外设寄存器序列速查、参考手册章节索引表。

**交叉引用**

- `hardware/5.3 gpio`、`5.4 interrupts`、`5.5 adc`、`5.6 dac`、`5.7 timer-pwm`、`5.8 uart-rs232`、`5.9 rs485-can`、`5.10 i2c-spi`、`5.11 usb-ethernet`、`5.12 watchdog-rtc-lowpower`（逐章只链硬件原理，软件侧写配置序列）。
- MCU 第五篇（驱动封装架构）、第九篇（协议栈）。
- Linux 模块 5（内核子系统对照）、试点 L4（用户态访问对照）。

**本篇遗漏 / 2026 更新点**

- 底稿缺：按键消抖实战、编码器读数案例、ADC 内部基准校准、多外设共享向量处理、低功耗唤醒源配置（第七篇衔接）。
- 2026 更新：补 RP2040 PIO / RP2350（M33 ↔ Hazard3 RISC-V 启动可选）差异专栏；RISC-V MCU（CH32V、GD32VF、ESP32 系列）工具链与指令差异一句带过 + 附录外链，不进主线。

#### A5 第五篇 · 三种开发方式与软件架构

**核心问题**：寄存器/LL/HAL 各自代价是什么？裸机工程如何组织目录与 BSP？轮询/中断/DMA 三模式怎么选？前后台、状态机、事件队列如何落地？

**建议小节**

5.1 三种写法对照（直接寄存器 / CMSIS-LL / HAL；代码量、体积、可移植性、可读性对比；试点 M3 实例）
5.2 BSP 板级抽象层（目录组织、板级初始化、引脚定义集中化、跨板移植）
5.3 外设访问模式：轮询 vs 中断 vs DMA（响应实时性、CPU 占用、复杂度对照表）
5.4 DMA 软件机制（请求映射、宽度/增量、半传输/完成中断、循环/双缓冲乒乓、M7 cache 一致性）
5.5 ISR 编写规范（最小化、标志/队列传递、不阻塞/不浮点、`FromISR` 概念预埋）
5.6 前后台 super-loop 架构（主循环职责、任务划分、缺点与边界）
5.7 有限状态机（表驱动 FSM、层级状态机、状态转移表）
5.8 事件驱动与事件队列（事件结构、单写单读环形缓冲、事件丢失策略、优先级）
5.9 错误处理与日志基础（错误码/返回值/断言钩子；与第七篇衔接）

**分级**

- 必讲：5.1–5.5、5.7、5.8；5.6 对照讲；5.9 基础。
- 外链：状态机模式资料、厂商 HAL 用户手册。
- 附录：同一外设三种写法对照表、FSM 模板代码、事件队列容量设计公式。

**交叉引用**

- MCU 试点 M3/M4、第四篇外设、第六篇 RTOS 任务模型。
- `hardware/5.13 peripheral-design`（综合整合案例，硬件设计不重复）。
- Linux 模块 5（驱动分层对照）。

**本篇遗漏 / 2026 更新点**

- 底稿缺：回调表/函数指针注册、错误码体系设计、事件队列容量设计、super-loop 与 RTOS 的选型边界、架构可测性（第八篇单元测试衔接）。

#### A6 第六篇 · RTOS（FreeRTOS / RT-Thread / Zephyr）

**核心问题**：任务、调度、同步、IPC 如何工作？为什么会死锁、优先级翻转、栈溢出？三个内核选型依据是什么？移植一个内核需要改哪些文件？

**建议小节**

6.1 RTOS 解决什么问题（与 super-loop 对比；实时性、确定性、资源占用）
6.2 任务与 TCB（状态：运行/就绪/阻塞/挂起；优先级约定；创建/删除/挂起/恢复）
6.3 调度器（抢占 + 时间片、tick、上下文切换 = PendSV；调度时机）
6.4 同步：二值/计数信号量、mutex 与优先级继承、优先级天花板、事件组
6.5 通信：队列（拷贝式）、流缓冲/消息缓冲、任务通知（最轻量）
6.6 临界区与调度器挂起（`vTaskSuspendAll`、BASEPRI 原理、ISR 安全 API `FromISR`）
6.7 内存管理（heap_1–5、静态分配/静态任务、内存池、栈大小估算与高水位）
6.8 软件定时器（回调上下文、不可阻塞、单定时器任务）
6.9 tickless 低功耗（空闲钩子、唤醒对齐；与第七篇低功耗衔接）
6.10 典型故障：死锁四条件、优先级翻转、栈溢出（钩子/高水位）、ISR 误用 API、排查路径
6.11 移植要件（`configMAX_PRIORITIES`/堆区域/PendSV/SVC/SysTick 钩子、端口层文件清单）
6.12 三内核对照：FreeRTOS 11.3 / 202604 LTS、RT-Thread 5.3、Zephyr 4.4（架构、许可、生态、配置模型、设备模型）

**分级**

- 必讲：6.1–6.7、6.10、6.11；6.8/6.9 基础；6.12 对比表。
- 外链：各内核官方文档、《Mastering the FreeRTOS Real Time Kernel》、trace 工具（Percepio/SystemView）。
- 附录：API 对照表、配置项速查、栈估算模板。

**交叉引用**

- MCU 第三篇（PendSV/SVC/BASEPRI）、第一篇（可重入）、第五篇（事件队列演进）、第七篇（低功耗/看门狗）。
- `hardware/5.4 interrupts`。
- Linux 模块 9（RTOS vs Linux 选型）、模块 8（PREEMPT_RT 对照）。

**本篇遗漏 / 2026 更新点**

- 底稿版本过时：FreeRTOS 11.3.1 / 202604.00 LTS（MQTT v5.0、Armv8-M SMP）、Zephyr 4.4 / SDK 1.0 / C17、RT-Thread 5.3.0（2026-09），版本号与特性必须更新（第三部分 C）。
- 底稿缺：SMP/多核概念预埋、静态分配配置、ISR 上下文 API 清单、trace 工具外链；Rust RTOS（Embassy/RTIC）一句外链定位，不进主线。

#### A7 第七篇 · 系统工程

**核心问题**：产品从"例程跑通"到"现场可靠运行"还差哪些工程能力：升级、掉电保护、看门狗、日志断言、低功耗、参数存储？

**建议小节**

7.1 Bootloader 与 IAP（分区布局、跳转机制、向量表重定位、中断向量偏移）
7.2 OTA 与双分区 A/B（镜像布局、槽位选择、回滚、升级中断处理、签名/哈希校验）
7.3 安全启动基础（签名验签、哈希链、TrustZone-M 简介；深度内容外链 TF-A/OP-TEE 到 Linux 册）
7.4 配置参数存储（EEPROM/片内 Flash 模拟 EEPROM、磨损均衡、双区备份、CRC 校验）
7.5 看门狗：IWDG/WWDG 分级喂狗、任务级喂狗策略、复位原因识别（`RCC_CSR`）与复位日志
7.6 日志与断言（`configASSERT`/断言钩子、错误分级、日志 RAM 环形缓冲、崩溃寄存器转储）
7.7 HardFault 诊断与崩溃记录（栈帧回溯、PC/LR/SP、寄存器转储保存到 Flash）
7.8 低功耗软件（Sleep/Stop/Standby、唤醒源、RAM/寄存器状态保持、功耗测量方法）
7.9 上电自检 POST 与故障恢复策略（自检项、故障分级、重启/降级/安全态）

**分级**

- 必讲：7.1、7.2、7.4、7.5、7.6、7.7；7.3 概念；7.8 必讲框架；7.9 基础。
- 外链：PSA Certified / SBSFU 资料、安全启动深度文档。
- 附录：分区布局模板、复位原因寄存器表、崩溃日志格式模板。

**交叉引用**

- MCU 试点 M2（向量偏移）、第六篇（任务级喂狗/低功耗）、第八篇（崩溃日志调试）。
- `hardware/5.12 watchdog-rtc-lowpower`、`hardware/6.12 power-integrity-decoupling`、`hardware/8.2 oscilloscope`（功耗测量）、`hardware/8.8 reliability-derating`。
- Linux 模块 8（RAUC/A-B 对照）。

**本篇遗漏 / 2026 更新点**

- 底稿缺：参数持久化与磨损均衡、复位原因/崩溃日志保存、上电自检、安全启动签名链、OTA 中断恢复、掉电检测（与 `hardware/6.10 power-monitoring-loadswitch` 交叉）。
- 2026 更新：补 MCU 安全生态现状（PSA Certified、SBSFU）外链；低功耗测量方法与硬件测量手册闭环。

#### A8 第八篇 · 工程效能

**核心问题**：怎么用构建系统、调试器、单元测试、静态分析和 CI 把工程做稳、问题查快？Git 怎么组织固件工程？

**建议小节**

8.1 版本控制与协作（Git 分支/标签/发布、`.gitignore`、固件二进制与源码仓管理）
8.2 构建系统：Make / CMake / Ninja / Kconfig / CubeMX 生成代码（与第二篇衔接；现代入口 CMake+Ninja）
8.3 调试工具链：GDB + OpenOCD + ST-LINK/J-Link、断点/观察点/监视点、semihosting、RTT/ITM/SWO
8.4 HardFault/异常排查流程（PC/LR 定位、map 反查；常见崩溃：野指针/栈溢出/非对齐/除零）
8.5 性能与体积观测（DWT 周期计数、栈高水位、heap 使用、`size`/map 趋势）
8.6 单元测试：Unity/Ceedling/CMock、宿主侧测试与硬件在环、gcov/lcov 覆盖率
8.7 静态分析：cppcheck/clang-tidy/PC-lint、MISRA-C:2012 关键规则、代码评审清单
8.8 仿真免硬件：Wokwi/Renode/QEMU 适用边界（外链用法，不内嵌）
8.9 CI 矩阵（多芯片/多配置构建、静态分析门禁、固件产物归档）
8.10 工程文档规范（README/注释/变更记录/接口文档）

**分级**

- 必讲：8.1–8.5、8.7 入门；8.6 框架必讲、用例入附录；8.8 外链；8.9 概念。
- 附录：GDB 命令速查、MISRA 高频违规对照表、调试 checklist。

**交叉引用**

- MCU 第二篇工具链、第三篇 DWT、第七篇崩溃记录。
- `hardware/8.6 debug-methodology`、`hardware/8.4 logic-analyzer-spectrum`、`hardware/8.7 troubleshooting-cases`。
- Linux 模块 2（主机工具对照）、模块 8（gdbserver/strace/perf 对照）。

**本篇遗漏 / 2026 更新点**

- 底稿缺：Git 专节、clang-tidy、覆盖率、仿真免硬件、崩溃排查流程、观察点。
- 2026 更新：工具链基线 GCC 15 / CubeCLT 1.21 / VS Code 扩展 2.0 / CMake+Ninja；RTT 缓冲配置与体积代价；宿主 x86 侧测试组织方式。

#### A9 第九篇 · 通信协议栈软件实现

**核心问题**：常用现场总线与网络协议在固件侧怎么落地：帧结构、状态机、缓冲与上层应用接口如何组织？

**建议小节**

9.1 协议分层与缓冲架构（DMA + 单写单读环形缓冲、帧接收状态机、零拷贝思路）
9.2 Modbus RTU/TCP（功能码、CRC16、T3.5 帧间隔、ADU/PDU、主站/从站）
9.3 CAN 应用层与 CANopen 概念（对象字典/PDO/SDO/NMT/心跳；深度外链）
9.4 TCP/IP 栈选型：LwIP vs FreeRTOS-TCP（raw API/套接字、内存预算、以太网初始化）
9.5 MQTT/CoAP（QoS/topic/会话保持、MQTT v5.0、TLS 简介、cJSON 序列化）
9.6 AT 指令状态机与 URC 处理（模块化串口透传模组）
9.7 文件系统：FatFS / LittleFS / FlashDB（磨损均衡、挂载/读写；与 7.4 配置存储衔接）
9.8 BLE/Wi-Fi 模组与协处理器架构（概念 + 厂商 SDK 外链）

**分级**

- 必讲：9.1、9.2、9.4、9.5 基础、9.7；9.3/9.6 概念 + 最小例；9.8 概念外链。
- 附录：CRC/校验码表、协议帧结构图、常用开源库清单。

**交叉引用**

- MCU 第四篇 UART/CAN/SPI/以太网、第五篇事件队列、第六篇任务划分。
- `hardware/5.9 rs485-can`、`hardware/5.10 i2c-spi`、`hardware/5.11 usb-ethernet`。
- Linux 模块 8（NetworkManager/ConnMan 网络栈对照）。

**本篇遗漏 / 2026 更新点**

- 底稿缺：本地文件系统专节（FatFS/LittleFS/FlashDB 完全未列）、JSON/数据序列化、CoAP、BLE。
- 2026 更新：MQTT v5.0（FreeRTOS 202604 LTS 已带）、LwIP 版本与内存配置、Matter 一句外链；补协议栈与 RTOS 任务划分案例。

#### A10 拟补结构件（底稿 §2.1 未列，批次 E 已含概念但地图未落结构）

| 结构件 | 内容 | 对标硬件分册 |
|---|---|---|
| 第十篇 · 综合项目实战 | 1–2 个端到端项目：传感器采集 → RTOS 任务 → 协议上报 → OTA；需求拆解、任务划分、代码组织、复盘记录 | `hardware/8.10 development-flow` |
| 第十一篇 · 面试与复盘题库 | 概念题/代码题/调试情景题；定期复盘标记；与学习进度联动 | `hardware/9.1–9.9 quizbank` |
| 附录 A–G | 术语中英对照、工具命令速查、外设/寄存器速查、芯片选型表、书单与官方文档、实验板清单、开源作品赏析 | `hardware/appendix/A–I` |

**交叉引用**：第十篇实战串接 MCU 第四篇外设、第六篇 RTOS、第七篇 OTA、第九篇协议栈；第十一篇题库回链各篇自测题；附录术语表对齐 `hardware/appendix/glossary`；选型章双向互链 Linux 模块 9。

> 另：Q1 决策要求 MCU 册保留一章"何时升级到嵌入式 Linux"，落点为第十篇实战后的选型章，双向互链 Linux 模块 9。

---

### B. Linux 线 `embedded-linux`（Cortex-A / 启动链 / 设备树 / Yocto / OTA，9 模块）

#### B1 模块 1 · 硬件底座：Cortex-A / SoC 与执行特权

**核心问题**：Cortex-A 与 Cortex-M 在内存模型、特权级、中断控制器、定时器上有何本质差异？EL0–EL3、TrustZone、MMU 虚拟内存如何分工？

**建议小节**

1.1 M vs A 总览对照表（MMU vs MPU、DDR vs 片内 Flash、cache/TCM、实时性/功耗/开机时间/RAM 预算）
1.2 ARM 架构族：ARMv7-A（32 位）/ ARMv8-A（AArch32/AArch64、物理地址宽度）/ ARMv9-A 一句；指令集状态与大小端
1.3 特权级别 EL0–EL3（应用/内核/Hypervisor/EL3 TF-A 常驻；状态切换异常）
1.4 MMU 与虚拟内存（页表、TLB、用户态/内核态地址空间隔离、设备内存属性/Non-cacheable）
1.5 cache 一致性与 DMA（cache line、非一致内存、DMA 缓冲区分配与冲刷；与模块 5 驱动衔接）
1.6 中断控制器 GIC v2/v3/v4（分发器/CPU 接口、SPI/PPI/SGI、优先级；与 NVIC 对照）
1.7 ARM 通用定时器（物理/虚拟定时器、中断；与 SysTick 对照）
1.8 TrustZone-A（Secure/Non-secure、SMC、EL3、OP-TEE 简介；与 MCU TrustZone-M 衔接）
1.9 片上资源概念（DDR 控制器、NOR/NAND/SD/eMMC；SoC 引脚复用/时钟概念链硬件手册）

**分级**

- 必讲：1.1–1.4、1.6、1.7；1.5 必讲基础；1.8 概念；1.9 概念。
- 外链：ARM Cortex-A vs M 白皮书、ARMv8-A 概述 PDF。
- 附录：M/A 对照表、EL 切换表、GIC 中断号分类表。

**交叉引用**

- MCU 第三篇（NVIC/SysTick/MPU 逐项对照）。
- `hardware/5.1 mcu-overview`、`hardware/4.9 memory`。
- 本线模块 3（EL3/TF-A）。

**遗漏 / 2026 更新点**

- 底稿缺：MMU 页表/TLB、cache 一致性、GIC、通用定时器、EL2/虚拟化概念、多核 SMP 概念（与 FreeRTOS SMP 对照）。
- 2026 更新：ARMv9-A 与 CCA 一句带过；64 位工具链命名在模块 2 落地。

#### B2 模块 2 · 开发环境与交叉编译

**核心问题**：如何在 Linux/WSL2/Windows 主机上建立免硬件开发环境？交叉编译器与 sysroot 如何工作？QEMU 如何跑通第一个用户态程序？

**建议小节**

2.1 主机环境（Ubuntu 22.04/24.04、WSL2 on Windows、依赖包、网络镜像）
2.2 交叉编译器（`arm-linux-gnueabihf-` 32 位 / `aarch64-linux-gnu-` 64 位；前缀各段含义、浮点 ABI；与 `arm-none-eabi-` 对照）
2.3 sysroot 与交叉编译第三方库（目标系统头文件/库位置、`pkg-config` 交叉包装、依赖传递）
2.4 用户态交叉编译 Hello World（编译 → `file` 查看架构 → QEMU user-mode 运行）
2.5 主机工具链：make/CMake/ninja/pkg-config/rsync，版本基线
2.6 连接方式总览：串口 / SSH（dropbear/openssh）/ NFS root / tftp / scp-sftp；免硬件先用 QEMU 系统模式
2.7 gdbserver 远程调试基础（概念，模块 8 深化）

**分级**

- 必讲：2.1–2.5；2.6 总览；2.7 概念。
- 外链：Bootlin 交叉编译培训资料。
- 附录：工具链前缀对照表、WSL2 安装清单、QEMU user-mode 命令速查。

**交叉引用**

- MCU 第二篇工具链（编译流程/选项对照）、试点 M1 环境章。
- 本线试点 L1、模块 3（QEMU 系统模式预热）。

**遗漏 / 2026 更新点**

- 底稿缺：WSL2/Windows 主机路径（读者多 Windows）、QEMU user-mode、sysroot/pkg-config 实战、第三方库交叉编译、gdbserver 入口、工具链来源（Linaro/Bootlin/ARM 官方/Yocto SDK）对比。
- 2026 更新：写死工具链版本基线（GCC 15 系、对应 glibc 版本），避免正文引用浮动版本。

#### B3 模块 3 · 启动链

**核心问题**：上电第一行代码到用户空间之间发生了什么？ROM/SPL/TF-A/U-Boot/内核各自职责、跳转与内存布局？`bootm/bootz/booti` 参数怎么传？

**建议小节**

3.1 启动全景图（上电 → ROM → SPL → TF-A BL1/BL2/BL31/BL32/BL33 → U-Boot → 内核+DTB+rootfs；与 MCU 复位到 main 对照）
3.2 ROM code 与 SPL（最小初始化 DDR/时钟、加载下一级；SPL 为什么小）
3.3 TF-A 各 BL 职责（BL1 ROM、BL2 可信固件、BL31 EL3 常驻、BL32 OP-TEE、BL33=U-Boot；SMC 切换）
3.4 U-Boot proper（driver model、环境变量 `bootcmd/bootargs/fdt_addr_r`、`bootm/bootz/booti/bootefi`、FIT 校验）
3.5 内核映像格式（Image/zImage/uImage 区别、解压、DTB 传递地址）
3.6 命令行参数解析（`bootargs`：console/root/rootwait/initrd/memory/ro、`init=`）
3.7 设备树在启动中的传递（QEMU 自动生成 DTB vs 自定义 `-dtb`；`dumpdtb`；模块 4 深化）
3.8 QEMU virt 逐段演示（一条 `qemu-system-aarch64` 命令拆解；`gic-version=3`；`-kernel/-dtb/-append/-initrd`）
3.9 安全启动与测量启动基础（签名链、ROT；与 MCU 安全启动衔接）

**分级**

- 必讲：3.1–3.6、3.8；3.7 衔接模块 4；3.9 概念。
- 外链：TF-A、U-Boot 官方文档。
- 附录：各阶段职责表、跳转内存地址表、`bootcmd` 常用变量表。

**交叉引用**

- MCU 试点 M2（复位到 main 逐点对照）、第七篇 Bootloader/IAP。
- `hardware/5.2 minimum-system`。
- 本线模块 4（DTB）、试点 L2。

**遗漏 / 2026 更新点**

- 底稿缺：内核解压/映像格式、命令行参数逐项、`init=` 与 PID1、QEMU virt 演示命令、FIT 签名校验细节、早期日志 earlycon、无 TF-A 的简化板卡路径（RPi BootROM 模式）对照。
- 2026 更新：内核 7.x / 6.18 LTS 基线、U-Boot 2025.x 现状，引用版本需在写章时复核。

#### B4 模块 4 · 设备树

**核心问题**：Linux 为什么不用寄存器头文件而用 DTB 描述硬件？节点属性 compatible/reg/interrupts 如何对应硬件？如何在 QEMU 上新增节点并被内核识别？

**建议小节**

4.1 为什么需要设备树（驱动与板级分离、编译期 vs 运行期；与 MCU 寄存器直写对照）
4.2 DTS/DTSI/dtc 流程（源 → 编译 DTB、包含/继承、`aliases`、`chosen`）
4.3 节点与属性基础（节点命名规范、compatible 匹配规则、`reg` 地址翻译：`#address-cells/#size-cells/ranges`）
4.4 中断属性（`interrupt-parent`、`interrupts`、`#interrupt-cells`；与 GIC 编号对应）
4.5 GPIO 与 pinctrl 属性（`gpio-controller`、`#gpio-cells`、`pinctrl-0/-1`、`clocks`/`clock-names`）
4.6 常用绑定查阅方法（`Documentation/devicetree/bindings`、YAML binding、compatible 检索）
4.7 内核侧匹配（`of_match_table`、platform device 实例化、probe；模块 5 深化）
4.8 Overlay 入门（`/plugin/`、`target`、`__overlay__`；应用时机 U-Boot vs 内核；`configfs` 动态叠加）
4.9 QEMU 实战：修改 DTB 加节点，启动后 `/proc/device-tree` 查看验证

**分级**

- 必讲：4.1–4.5、4.7、4.9；4.6 方法必讲；4.8 概念。
- 外链：kernel.org 设备树用法模型/overlay/binding 规范。
- 附录：属性速查表、标准节点示例、binding 路径索引。

**交叉引用**

- MCU 第四篇（外设寄存器配置对照）、第三篇 NVIC（interrupts 对照）。
- `hardware/5.3 gpio`、`hardware/5.10 i2c-spi`。
- 本线模块 1 GIC、模块 5、试点 L3。

**遗漏 / 2026 更新点**

- 底稿缺：`aliases/chosen`、`ranges/#cells` 地址翻译、pinctrl/clocks、binding YAML 查阅法、`/proc/device-tree` 验证、Overlay 应用时机、设备树与 ACPI 边界一句。
- 2026 更新：binding 强制 YAML 校验现状需在写章时复核。

#### B5 模块 5 · 内核与驱动入门

**核心问题**：字符设备/platform driver/I2C/SPI 子系统如何组织？内核模块怎么编译、加载与卸载？用户态访问硬件有哪些官方接口？

**建议小节**

5.1 内核版本与配置（`defconfig/menuconfig`、`ARCH=`/`CROSS_COMPILE=`、`Image/dtbs` 构建；6.18 LTS/7.x 基线）
5.2 内核模块（Makefile KBUILD、`obj-m`、`insmod/rmmod/modprobe`、依赖、`modinfo`）
5.3 设备模型基础（kobject/sysfs/class/bus、驱动模型分层）
5.4 字符设备（cdev、`file_operations`、主/次设备号、miscdevice、udev 规则生成 `/dev` 节点）
5.5 platform bus（platform_device/platform_driver、`of_match_table`、probe/remove、`platform_get_resource` 资源获取）
5.6 I2C 子系统（adapter/client/driver、probe 匹配、读写时序；与 MCU I²C 驱动对照）
5.7 SPI 子系统（spi_device/spi_driver、传输 API、片选/模式对照 CPOL/CPHA）
5.8 中断与并发（`request_irq`、顶半部/底半部 tasklet/workqueue/threaded irq、spinlock/mutex/atomic）
5.9 内核内 DMA 与 cache 一致性（dmaengine、coherent/dma-noncoherent；呼应模块 1）
5.10 用户态访问接口总览（libgpiod chardev v2、i2c-dev、spidev、`/dev/mem` 风险与禁忌；深度在试点 L4）

**分级**

- 必讲：5.1–5.5、5.8；5.6/5.7 最小例；5.9 概念；5.10 总览。
- 外链：Linux Kernel 官方文档；LDD3 仅作概念参考并标注 2005 年 API 已漂移。
- 附录：`file_operations` 表、probe 模板、并发原语对照表。

**交叉引用**

- MCU 第四篇外设、第五篇架构（分层对照）。
- `hardware/5.3 gpio`、`hardware/5.10 i2c-spi`。
- 本线模块 1 GIC/cache、试点 L4、模块 7 构建系统。

**遗漏 / 2026 更新点**

- 底稿缺：模块构建细节、`file_operations`、platform driver 完整生命周期、并发控制、顶/底半部、sysfs/kobject、udev 规则、`/dev/mem` 风险警示、内核版本 API 漂移提示。
- 2026 更新：内核 Rust 驱动一句外链（不进主线）；binding 与驱动配合（模块 4 衔接）。

#### B6 模块 6 · rootfs 与启动初始化

**核心问题**：内核启动后 PID1 是谁？rootfs 如何组装、挂载与持久化？BusyBox/systemd/initramfs 各自角色？

**建议小节**

6.1 PID1 与 init（`init=/linuxrc`、PID1 退出后果、BusyBox init vs systemd 选型）
6.2 目录结构与挂载（`/proc /sys /dev /tmp` 虚拟文件系统、devtmpfs+mdev/udev、FHS 嵌入式裁剪）
6.3 BusyBox（单二进制、applet、`/etc/init.d` 脚本、`inittab`）
6.4 systemd 基础（unit、服务使能、journald 日志；适用场景与体积代价）
6.5 文件系统选型（ext4、SquashFS 只读、overlayfs 可写层持久化、UBIFS raw NAND、initramfs/initrd）
6.6 分区布局（boot/rootfs/data 分区、只读 rootfs + 可写 data、A/B 分区概念衔接模块 8）
6.7 网络与服务初始化脚本（DHCP/静态 IP、dropbear/ssh、NTP、日志）
6.8 故障排查：kernel panic / 找不到 rootfs / 串口 earlycon 日志阅读

**分级**

- 必讲：6.1–6.3、6.5、6.6；6.4 概念；6.7 基础；6.8 必讲排错。
- 附录：`inittab` 模板、分区布局表、启动脚本模板。

**交叉引用**

- 本线模块 3（`bootargs root=`）、模块 7（rootfs 生成）。
- MCU 第七篇配置存储。

**遗漏 / 2026 更新点**

- 底稿缺：PID1 职责、initramfs、overlay 持久化原理、虚拟文件系统挂载、devtmpfs/udev、网络/服务初始化、panic 排错、只读 rootfs 与可写层设计、Debian/Ubuntu 预编译 rootfs 路线（RPi 模式）与 Buildroot/Yocto 对照。
- 2026 更新：systemd 与 BusyBox 在工业现场的实际选型占比需在写章时复核。

#### B7 模块 7 · 构建系统（Buildroot / Yocto）

**核心问题**：固件 rootfs 与应用如何从零可复现地构建？Buildroot 与 Yocto 的机制、学习曲线与选型依据？如何添加一个自定义包？

**建议小节**

7.1 构建系统为什么存在（手动交叉编译的不可复现性；依赖/版本/补丁管理）
7.2 Buildroot 机制（Kconfig/menuconfig、`output/host-target-staging-images` 目录、package 目录结构、补丁/overlay、构建产物）
7.3 自定义 package 实战（`Config.in`、`*.mk`、版本/下载/补丁/安装；第三方软件加入）
7.4 Buildroot 选型：快速/中小项目/单二进制；局限（可复现性弱、无长期维护 SDK）
7.5 Yocto 机制（recipe/layer/BitBake、`local.conf/bblayers.conf`、image recipe、rootfs 自定义、SDK 生成、wic 镜像）
7.6 Yocto 选型：企业长维护/可复现/合规/CRA；学习成本与磁盘/时间代价
7.7 选型决策表（团队规模/产品生命周期/网络栈需求/启动时间/合规要求）
7.8 替代路线：预编译发行版 rootfs（Debian/Ubuntu）；容器化一句带过

**分级**

- 必讲：7.1–7.3、7.5 入门、7.7；7.4/7.6 对照；7.8 概念。
- 外链：Buildroot 手册、Yocto Mega-Manual、Bootlin slides。
- 附录：目录结构速查、常用 recipe 片段、构建命令表。

**交叉引用**

- 本线模块 2 工具链、模块 6 rootfs、试点 L1。
- MCU 第八篇构建系统（Make/CMake 对照）。

**遗漏 / 2026 更新点**

- 底稿缺：Buildroot 内部目录与自定义包写法、Yocto 目录结构/SDK/wic、选型量化标准、构建时间/磁盘成本、预编译 rootfs 路线。
- 2026 更新：Yocto 6.0 "Wrynose" LTS（支持至 2030-04）、Buildroot 2026.08；EU CRA 合规成为 Yocto 选型驱动因素（2026 时事，写章时复核版本号）。

#### B8 模块 8 · OTA / 网络 / 调试 / 可靠性

**核心问题**：产品上线后如何升级、联网、排障？Linux 侧 OTA 方案对比？远程调试与日志工具有哪些？

**建议小节**

8.1 网络配置（`ifconfig/ip`、静态/DHCP、NetworkManager/ConnMan/systemd-networkd 选型；串口与 SSH）
8.2 时间同步（NTP/chrony、RTC 概念；与 MCU RTC 对照）
8.3 日志体系（syslog/journald、printk 级别、dmesg、早期日志 earlycon）
8.4 远程调试（strace/ltrace、gdbserver、perf 概念、内核 oops/panic 解读、NFS root 调试）
8.5 OTA 总览：A/B 分区与回滚（槽位/bootloader 选择/回滚计数器；与 MCU 双分区对照）
8.6 RAUC（A/B + squashfs + PKCS#7、bundle、适配层）
8.7 SWUpdate（`.swu`、多组件、灵活性、描述文件）
8.8 Mender（A/B rootfs + 托管服务、客户端架构）
8.9 看门狗与实时性（Linux watchdog、PREEMPT_RT 主线 6.12+ 现状、软/硬实时边界、Xenomai 概念外链）
8.10 可靠性工程概览（降额/老化/认证参照硬件手册、看门狗喂狗、崩溃 core dump）

**分级**

- 必讲：8.1–8.5、8.9 概念；8.6–8.8 对比表 + 一个主例；8.10 交叉硬件。
- 外链：各 OTA 方案官方文档。
- 附录：网络命令速查、OTA 方案对比表、调试命令表。

**交叉引用**

- MCU 第七篇（OTA/看门狗/低功耗对照）、第八篇（调试工具对照）。
- `hardware/5.12 watchdog-rtc-lowpower`、`hardware/8.8 reliability-derating`。
- 本线模块 6 分区布局、模块 9 选型。

**遗漏 / 2026 更新点**

- 底稿缺：NTP、journald/syslog 对比、strace/perf、core dump、watchdog、PREEMPT_RT（6.12 主线，2026 现状必须更新）、Xenomai、NFS root 排错、安全网（防火墙/签名/密钥管理）基础概念。
- OTA 三方案缺分区/签名/回滚机制细节对比。

#### B9 模块 9 · 选型：MCU/RTOS vs 嵌入式 Linux

**核心问题**：一个新项目在 MCU+RTOS、裸机、嵌入式 Linux、异构 SoC 之间如何决策？量化依据是什么？

**建议小节**

9.1 决策维度表（实时性 µs/ms、RAM KB–MB vs ≥32–64MB、Flash/ROM、开机时间、功耗/睡眠电流、成本、网络/文件系统/GUI/生态复用、团队技能、生命周期/合规）
9.2 典型案例分类（传感器节点/采集器/工业控制器/网关/HMI/视觉/音视频）
9.3 异构架构（Cortex-A+M、AMP/SMP、STM32MP1/i.MX 8M/93 类；核间通信 rpmsg/共享内存概念）
9.4 Linux 实时性边界（PREEMPT_RT 能力与局限；何时仍需 MCU 协处理器）
9.5 升级路径（MCU 产品何时引入 Linux、双芯方案演进；与 MCU 册选型章双向互链）

**分级**

- 必讲：9.1、9.2、9.5；9.3/9.4 概念。
- 外链：ARM 选型白皮书。
- 附录：决策检查清单、典型芯片资源表。

**交叉引用**

- MCU 第六篇 RTOS、第九篇协议栈。
- `hardware/5.1 mcu-overview`、`hardware/appendix/chip-selection`。
- 本线模块 1 M/A 对照、模块 8 PREEMPT_RT。

**遗漏 / 2026 更新点**

- 底稿缺：量化决策清单、典型案例库、异构核间通信、PREEMPT_RT 边界、预编译发行版成本。
- 2026 更新：高端 SoC 现状（i.MX93/STM32MP25/RPi5/CM4 类）选几款列资源对照表。

---

## 第二部分 · 9 个试点章写作大纲

> 试点目标（沿用底稿 §7.1/§7.3）：用最少章节打通两条主线——MCU：工具链 → 启动 → 一个外设驱动 → RTOS 最小任务；Linux：环境/交叉编译 → 启动链 → 设备树 → 用户态硬件访问。每章只写大纲，代码为最小骨架占位，现象为预期目标。
> 章 slug 为建议值，落地时在 `apps/<slug>/docs/SUMMARY.md` 注册；图示标注「Mermaid」的由 Mermaid 渲染，其余为静态 SVG/表格（与硬件册风格统一）。

### MCU 试点 M1 · 开发环境与第一个工程：点亮 LED

- **建议路径**：`getting-started/toolchain-blink.md`（`appId=embedded`）
- **目标**：在 Windows/WSL 主机装好 Arm GNU Toolchain 与烧录工具，用 Makefile 或 CMake 构建最小工程，烧录到开发板或 Wokwi 仿真，LED 按周期闪烁；能说出工程目录每个文件的职责。
- **小节列表**
  1.1 手册范围与平台约定（通用 Cortex-M 概念打底，STM32F4/F1 主例，差异专栏；开发板/仿真清单）
  1.2 主机环境安装（Arm GNU Toolchain 15.x、STM32CubeCLT/OpenOCD/ST-LINK 或 J-Link、VS Code 扩展；Windows PATH/WSL 说明）
  1.3 最小工程目录结构（Core/Src/Inc、startup、linker、`.vscode`、Makefile/CMakeLists、README 各自职责）
  1.4 第一个 main（HAL 初始化 → GPIO 推挽 → 延时循环翻转）
  1.5 构建与产物（`make`/`cmake` 命令、`.elf/.map/.hex/.bin`、`size` 段占用读数）
  1.6 烧录与验证（`st-flash`/OpenOCD/CubeProgrammer；无硬件时 Wokwi 外链替代）
  1.7 常见报错对照（编译器未找到、未定义符号、烧录连接失败、跑飞复位）
- **最小代码 / 命令与预期现象**
  - 代码骨架：`HAL_Init` → `GPIO_Init` → `while(HAL_GPIO_TogglePin + HAL_Delay(500))`；Makefile 关键变量（`CC/CFLAGS/LDSCRIPT`）。
  - 命令：构建 → `size` → 烧录；预期：LED 1s 周期闪烁；`size` 输出 text/data/bss 三段占用可读出。
- **图示**
  - 工程目录树（代码块静态展示）
  - 构建-烧录-运行链路（**Mermaid flowchart LR**）
  - GPIO 输出级原理：复用 `hardware/5.3 gpio` 配图，不重画。
- **交叉引用**
  - `hardware/5.2 minimum-system`（电源/时钟/调试器硬件）、`hardware/5.3 gpio`（电气参数链）
  - MCU 试点 M2（启动文件/链接脚本在后续章展开）
  - Linux 试点 L1（裸机工具链 vs Linux 交叉编译器对照）
- **验收方式**
  1. 命令行可从零构建出 `.hex/.bin`，无需 IDE 点击；
  2. `size` 三段占用能逐项解释；
  3. LED 闪烁现象在板卡或 Wokwi 复现；
  4. 目录中每个文件能说出职责；
  5. 报错表覆盖安装/链接/烧录三类各 ≥1 条；
  6. 章末自测题 ≥5 题，答案可在正文定位。

### MCU 试点 M2 · 从复位到 main：启动文件、链接脚本与内存布局

- **建议路径**：`boot/reset-to-main.md`
- **目标**：对照启动文件与链接脚本，逐步说出上电复位到 `main()` 第一条语句之间 CPU 做了什么；看懂 map 中段地址与符号；指出 `.data/.bss` 初始化错误对应的故障现象。
- **小节列表**
  2.1 复位信号到取指（复位向量、SP/PC 初始值、VTOR；链硬件 5.2）
  2.2 启动文件逐行：`Reset_Handler`（SP 加载 → `.data` 从 FLASH LMA 搬运到 RAM VMA → `.bss` 清零 → `SystemInit` → `__libc_init_array` → `main`）
  2.3 链接脚本精读（`MEMORY`、`SECTIONS`、段符号 `_sidata/_sdata/_edata/_sbss/_ebss/_estack`、`KEEP`、`AT>`）
  2.4 内存布局图（Flash/RAM 地址范围，text/rodata/data/bss/heap/stack 位置，栈向下、堆向上）
  2.5 map 文件解读（段地址/大小、符号表、段溢出定位）
  2.6 三种故障定位（未搬运 data、未清零 bss、栈空间不足的现象与排查路径）
  2.7 扩展：全局对象构造、中断向量表本质是函数指针数组、CMSIS v6 C 启动变化
- **最小代码 / 命令与预期现象**
  - `Reset_Handler` 汇编片段（逐行注释）；linker script 片段；
  - 预期：map 中 `.data` 的 LMA 在 Flash、VMA 在 RAM；故意注释搬运代码（实验提示）后全局变量初值异常，作为故障演示。
- **图示**
  - 上电到 main 流程（**Mermaid flowchart TD**，标注每步对应代码行）
  - 内存布局静态图（SVG，与 `hardware/4.9 memory` 风格统一）
  - data 搬运 LMA→VMA 示意（静态图；可选 **Mermaid sequenceDiagram** 辅助）
- **交叉引用**
  - MCU 第一篇 1.2（内存模型）、第二篇 2.3/2.4/2.5（链接脚本/map）
  - `hardware/5.2 minimum-system`、`hardware/4.9 memory`
  - Linux 试点 L2（MCU 两级启动 vs Linux 多级启动对照表）
- **验收方式**
  1. 能默画启动流程 7 步并对应到启动文件行；
  2. 能在 linker script 中指出每个段符号定义位置；
  3. 能从 map 读出 Flash/RAM 占用；
  4. 能解释 data/bss 未初始化的故障现象；
  5. 不重复硬件 5.2 原理，只写软件侧序列；
  6. 章末自测题 ≥5 题。

### MCU 试点 M3 · GPIO 与外部中断（寄存器 / LL / HAL 三方式）

- **建议路径**：`peripherals/gpio-exti-three-ways.md`
- **目标**：同一 GPIO 输出 + 按键外部中断，分别用寄存器/CMSIS-LL/HAL 实现；对比三种写法的代码量、可读性、体积与可移植性；说清 EXTI 配置序列与中断标志清除时机。
- **小节列表**
  3.1 GPIO 模式回顾与本章目标（电气参数链 `hardware/5.3`，本章只写配置序列）
  3.2 方式一：直接寄存器（RCC 使能时钟 → MODER → PUPD → ODR；位掩码宏）
  3.3 方式二：CMSIS-LL（`LL_GPIO_*` API 序列，结构体定址）
  3.4 方式三：HAL（`GPIO_InitTypeDef`、`HAL_GPIO_WritePin/TogglePin`）
  3.5 外部中断 EXTI（线映射 → 触发沿 → NVIC 使能 → ISR 标志清除；软件消抖）
  3.6 三方式对照表（代码行数/Flash 增量/可读性/移植成本/适用场景，附实测数据）
  3.7 常见问题（时钟未使能、标志未清除导致中断风暴、上下拉配置错误、5V 电平烧毁链硬件 5.3/4.8）
- **最小代码 / 命令与预期现象**
  - 三段 GPIO 初始化与 ISR 骨架；
  - 预期：按键按下翻转 LED；串口打印中断计数（链 M4）；不消抖时可见计数抖动，作为消抖必要性演示。
- **图示**
  - EXTI 信号路径（**Mermaid flowchart**：GPIO → EXTI → NVIC → CPU → ISR）
  - 三方式代码对照静态表
  - 消抖时序示意（SVG；可选 **Mermaid sequenceDiagram**）
- **交叉引用**
  - `hardware/5.3 gpio`、`hardware/5.4 interrupts`（NVIC/优先级硬件视角）、`hardware/4.7 tri-state-bus-pull`、`hardware/4.8 logic-levels`
  - MCU 第四篇 4.3/4.4、第五篇 5.1
  - Linux 试点 L4（libgpiod 用户态访问对照）
- **验收方式**
  1. 三种方式均编译通过且现象一致；
  2. 对照表有实测行数与体积数据，非定性描述；
  3. ISR 中能指出标志清除位置并解释漏清后果；
  4. 能解释时钟使能必须先于外设配置；
  5. 电气安全提示引用硬件手册参数，不自行给电流阈值；
  6. 章末自测题 ≥5 题。

### MCU 试点 M4 · 串口收发与 printf 重定向（中断 / DMA / 环形缓冲）

- **建议路径**：`peripherals/uart-ringbuffer-dma.md`
- **目标**：UART 收发按轮询 → 中断 → DMA 三级演进；`printf` 重定向到串口；单写单读环形缓冲组织接收数据；解释帧错误、溢出与缓冲满策略。
- **小节列表**
  4.1 UART 硬件接线与波特率计算（物理层链 `hardware/5.8`；时钟/分频公式与误差，KaTeX）
  4.2 轮询收发最小例（阻塞方式与缺点）
  4.3 中断接收 + 环形缓冲（ISR 只入队、主循环解析；头/尾指针；满/空判定）
  4.4 printf 重定向（`_write` 桩、newlib-nano 浮点体积、阻塞发送 vs 队列化日志）
  4.5 DMA 接收：IDLE 空闲中断 + DMA 双缓冲/半满，零拷贝思路；发送 DMA 与完成标志
  4.6 帧协议解析状态机（链第五篇事件队列；换行/CRC 定界）
  4.7 故障排查（overrun、FE 帧错误、NE 噪声、波特率不匹配现象；调试工具链硬件 8.4 交叉）
- **最小代码 / 命令与预期现象**
  - 环形缓冲结构与 `put/get` 骨架；ISR 骨架；`fputc/_write` 桩；DMA 初始化骨架；
  - 预期：串口助手回显、定时打印计数；DMA 模式下 CPU 占用下降（配合 8.5 观测方法）。
- **图示**
  - 三级演进对照（静态表 + 可选 **Mermaid flowchart**）
  - 环形缓冲读写指针示意（SVG）
  - DMA + IDLE 接收时序（**Mermaid sequenceDiagram**）
- **交叉引用**
  - `hardware/5.8 uart-rs232`（物理层/电平）、`hardware/5.10 i2c-spi`（同期通信对照）、`hardware/8.4 logic-analyzer-spectrum`
  - MCU 试点 M3（中断基础）、第五篇 5.4 DMA / 5.8 事件队列、第八篇 RTT 调试
  - Linux 试点 L4（i2c-dev/libgpiod 用户态对照）
- **验收方式**
  1. 中断 + 环形缓冲在长时压力测试下不丢字节；
  2. printf 整数/浮点两种配置的 Flash 体积有实测对比；
  3. DMA 配置序列能口述（请求映射/宽度/增量/双缓冲）；
  4. 四类帧错误能对应到现象与标志位；
  5. 缓冲满策略明确（丢弃/覆盖/阻塞三选一并说明理由）；
  6. 章末自测题 ≥5 题。

### MCU 试点 M5 · RTOS 入门：任务创建、调度与延时

- **建议路径**：`rtos/first-task-scheduler.md`
- **目标**：用 FreeRTOS（主例，RT-Thread 对照）创建两个任务 + 一个队列，演示抢占调度、延时与任务通知；理解任务状态、优先级与临界区；识别栈溢出钩子与优先级反转概念。
- **小节列表**
  5.1 为什么上 RTOS（super-loop 局限、实时性/确定性；链第五篇）
  5.2 内核移植要件与配置（`FreeRTOSConfig.h` 关键项：tick 频率/优先级数/堆大小；端口文件；对照第三篇 PendSV/SVC）
  5.3 第一个任务（`xTaskCreate`、任务循环 `vTaskDelay`、栈大小参数）
  5.4 调度器启动与任务状态（运行/就绪/阻塞/挂起；抢占时机；tick）
  5.5 任务间通信入门（队列 `xQueueSend/Receive` 拷贝式；任务通知替代信号量）
  5.6 临界区与 ISR 安全 API（`vTaskEnter/ExitCritical`、`FromISR` 概念预埋）
  5.7 调试基础（栈高水位 `uxTaskGetStackHighWaterMark`、空闲钩子、钩子函数配置）
  5.8 三内核快速对照（FreeRTOS 11.3/202604 LTS、RT-Thread 5.3、Zephyr 4.4；API 对照表；选一种动手）
- **最小代码 / 命令与预期现象**
  - 两任务 + 一队列骨架；
  - 预期：两任务按优先级交替打印、计数无冲突；高水位读数可见；`vTaskDelay` 期间其他任务可运行。
- **图示**
  - 任务状态迁移（**Mermaid stateDiagram-v2**）
  - 调度抢占时序（**Mermaid sequenceDiagram**）
  - 队列生产者/消费者示意（静态图）
- **交叉引用**
  - MCU 第三篇 PendSV/SVC/BASEPRI、第一篇可重入、第五篇事件队列
  - `hardware/5.4 interrupts`
  - Linux 模块 9（RTOS vs Linux 选型）、模块 8（PREEMPT_RT 对照）
- **验收方式**
  1. 工程编译并在板卡/仿真上跑通，调度行为可观察；
  2. 队列读写不依赖共享可变变量；
  3. 能列出 ≥5 个 `FreeRTOSConfig.h` 关键项及作用；
  4. 栈高水位能读出剩余字数并据此判断栈大小是否合理；
  5. 三内核对照表 ≥4 维度（许可/内存/配置模型/生态）；
  6. 章末自测题 ≥5 题。

### Linux 试点 L1 · 开发环境与交叉编译（QEMU 免硬件）

- **建议路径**：`getting-started/cross-compile-qemu.md`（`appId=embedded-linux`）
- **目标**：在 WSL2/Ubuntu 主机装好 aarch64 交叉工具链，写出 Hello World 并交叉编译，用 QEMU user-mode 运行；理解 sysroot 与工具链前缀；与 MCU 裸机工具链逐项对照。
- **小节列表**
  1.1 本手册范围与实验基线（QEMU virt aarch64 免硬件；内核 6.18 LTS/7.x、发行版工具链版本基线）
  1.2 主机准备（WSL2 Ubuntu、依赖包、网络镜像；Windows 用户路径提示）
  1.3 交叉工具链安装（apt `gcc-aarch64-linux-gnu` 或 ARM 官方包；前缀 `aarch64-linux-gnu-` 各段拆解；浮点 ABI）
  1.4 第一个交叉程序（编译选项、`file`/`readelf` 确认架构、QEMU user-mode 运行）
  1.5 sysroot 与第三方库（头文件/库位置、`-I/-L`、`pkg-config` 交叉包装；概念为主）
  1.6 与 MCU 工具链对照表（`arm-none-eabi-` vs `aarch64-linux-gnu-`：裸机 vs glibc、semihosting vs syscall）
  1.7 主机开发工具（make/CMake/ninja/pkg-config/rsync/gdb-multiarch 安装检查）
  1.8 常见报错（架构不匹配、找不到 libc、QEMU 未安装、sysroot 缺失）
- **最小代码 / 命令与预期现象**
  - `aarch64-linux-gnu-gcc hello.c -o hello` → `file hello` → `qemu-aarch64 hello`；
  - 预期：打印 Hello，`file` 输出确认 ARM aarch64 架构。
- **图示**
  - 主机 → 交叉编译器 → QEMU 运行链路（**Mermaid flowchart LR**）
  - 工具链前缀拆解静态表
  - MCU vs Linux 工具链对照表（静态表，回链 MCU 试点 M1）
- **交叉引用**
  - MCU 试点 M1、MCU 第二篇工具链
  - 本线模块 2 全模块、模块 3（QEMU 系统模式预热）
- **验收方式**
  1. 三条命令复现编译/架构确认/运行；
  2. 能解释工具链前缀各段含义；
  3. 能说清 sysroot 作用；
  4. 对照表覆盖 ≥6 项差异；
  5. 常见报错表 ≥4 条并附排查命令；
  6. 章末自测题 ≥5 题。

### Linux 试点 L2 · 启动链全景（ROM → SPL → TF-A → U-Boot → 内核 + DTB）

- **建议路径**：`boot/boot-chain-panorama.md`
- **目标**：画出从 ROM code 到用户空间的完整启动链，说出各阶段职责、镜像格式与内存传递；在 QEMU virt 上一条命令启动内核，从串口日志定位每个阶段；与 MCU 复位到 main 建立对照。
- **小节列表**
  2.1 为什么 Linux 启动链长（MMU/驱动/文件系统/用户空间 vs MCU 单片 Flash 执行；链模块 1）
  2.2 全景图：ROM → SPL → TF-A（BL1/BL2/BL31/BL32/BL33）→ U-Boot → 内核 + DTB + rootfs
  2.3 各阶段职责与产物（片内 ROM、SPL DDR 初始化、BL31 EL3 常驻、U-Boot 环境与命令、内核解压）
  2.4 U-Boot 关键变量与命令（`bootcmd/bootargs/fdt_addr_r`、`bootm/bootz/booti`；FIT 校验概念）
  2.5 内核命令行参数（console、root、rootwait、initrd、memory、init；串口日志对应位置）
  2.6 QEMU virt 启动实战（`qemu-system-aarch64 -M virt,gic-version=3 -kernel Image -dtb -append -initrd -serial`；日志逐行解读）
  2.7 无 TF-A 的简化路径（RPi BootROM 模式；真实板卡差异提示）
  2.8 与 MCU 启动链对照表（层级/职责/控制转移/向量表/DTB）
- **最小代码 / 命令与预期现象**
  - 一条 `qemu-system-aarch64` 启动命令；
  - 预期：串口依次打印引导 → 内核解压 → 内核日志 → BusyBox login；各阶段标志可在日志中指认。
- **图示**
  - 启动链全景（**Mermaid flowchart TD**，标注 EL 级别）
  - 各阶段内存加载布局静态图（地址区间 SVG）
  - MCU/Linux 启动流程对照表（静态表）
- **交叉引用**
  - MCU 试点 M2（逐点对照）
  - 本线模块 1 EL/TrustZone、模块 3 全模块、模块 4 DTB 传递、试点 L3
  - `hardware/5.2 minimum-system`
- **验收方式**
  1. 能默画 7 级启动链并写出各阶段职责；
  2. QEMU 命令每个参数能解释；
  3. 串口日志至少指认 5 个阶段标志；
  4. `bootargs` 5 个常用参数答对作用；
  5. 对照表 MCU/Linux 各列 ≥5 行；
  6. 章末自测题 ≥5 题。

### Linux 试点 L3 · 设备树入门（DTS / compatible / reg / interrupts）

- **建议路径**：`devicetree/first-dts.md`
- **目标**：看懂 DTS 节点结构与 compatible/reg/interrupts 三个核心属性；编译自定义 DTB 并用 QEMU 传入；通过 `/proc/device-tree` 验证节点；理解 `of_match_table` 匹配概念（衔接模块 5）。
- **小节列表**
  3.1 为什么是设备树（板级描述与驱动分离；与 MCU 寄存器头文件对照）
  3.2 DTS/DTSI 结构与编译流程（`dtc`、包含/继承、`aliases`、`chosen`）
  3.3 compatible 与匹配规则（字符串优先级；驱动 `of_match_table` 对应）
  3.4 reg 地址与 `#address-cells/#size-cells/ranges` 翻译规则
  3.5 interrupts/interrupt-parent/`#interrupt-cells` 与 GIC 编号
  3.6 GPIO/pinctrl/clocks 属性入门（硬件绑定概念）
  3.7 实战：基于 QEMU `dumpdtb` 提取基础 DTS，新增一个 led 节点，编译 DTB，QEMU `-dtb` 启动
  3.8 验证：`/proc/device-tree` 下查看节点属性；binding 文档查阅路径
  3.9 Overlay 概念入门（应用时机、动态叠加；深度外链）
- **最小代码 / 命令与预期现象**
  - `dtc -I dts -O dtb -o board.dtb board.dts`；`qemu-system-aarch64 -M virt -kernel Image -dtb board.dtb`；`cat /proc/device-tree/led/compatible`；
  - 预期：新节点出现在 sysfs 路径；驱动匹配日志（模块 5 展开）。
- **图示**
  - DTS → DTB → 内核解析（**Mermaid flowchart**）
  - 地址翻译示意静态图（SVG）
  - 节点-驱动匹配流程（**Mermaid flowchart**）
- **交叉引用**
  - 本线模块 1 GIC/通用定时器、模块 3 DTB 传递、模块 5 `of_match_table`、试点 L4
  - MCU 第四篇外设寄存器配置对照
  - `hardware/5.3 gpio`、`hardware/5.10 i2c-spi`
- **验收方式**
  1. 能独立写出含 compatible/reg/interrupts 的最小节点；
  2. 地址翻译计算正确；
  3. QEMU 启动后 `/proc/device-tree` 可见新节点；
  4. 能在 bindings 目录找到对应文档；
  5. 与 MCU 寄存器写法对照 ≥4 点；
  6. 章末自测题 ≥5 题。

### Linux 试点 L4 · 用户态硬件访问（libgpiod 点灯 / i2c-dev 读传感器）

- **建议路径**：`userspace/gpio-i2c-access.md`
- **目标**：在 QEMU 或真实板卡上用 libgpiod v2 控制一个 GPIO（点灯），用 i2c-dev ioctl 读取一个传感器；理解字符设备接口、权限与设备节点由来；与 MCU 直接寄存器访问对照。
- **小节列表**
  4.1 用户态访问硬件的三条官方路径（字符设备驱动暴露；sysfs 已废弃；`/dev/mem` 风险禁忌）
  4.2 GPIO chardev v2 模型（gpiochip、line request、consumer、方向/值/边沿事件；libgpiod 2.x CLI 与库 API）
  4.3 实战一：libgpiod 点灯（`gpiodetect/gpioinfo/gpioset`；C 程序 line request 骨架；QEMU virt 外设限制说明）
  4.4 i2c-dev 模型（adapter 号、ioctl `I2C_SLAVE`、read/write 事务、地址/寄存器字节顺序；对照硬件 5.10 时序）
  4.5 实战二：i2c-dev 读传感器（常见温度/加速度器件清单；`i2cdetect`；C 读写骨架）
  4.6 spidev 概念与边界（ioctl/spi_message；一句对照）
  4.7 权限、设备节点与 udev 规则（gpiochip/i2c 节点归属、普通用户访问、udev 规则示例）
  4.8 与 MCU 外设访问对照表（寄存器直写 vs 字符设备 API；延迟/并发/可移植性）
- **最小代码 / 命令与预期现象**
  - `gpioset`；`i2cdetect -y 1`；`i2cget/i2cset`；C 骨架；
  - 预期：LED 电平翻转（真实板）或事件可读；`i2cdetect` 列出器件地址；传感器读数可解释。
- **图示**
  - 用户态 → 字符设备 → 驱动 → 硬件调用链（**Mermaid flowchart**）
  - I²C 事务时序：复用 `hardware/5.10 i2c-spi` 配图，不重画
  - MCU vs Linux 访问路径对照表（静态）
- **交叉引用**
  - MCU 试点 M3（GPIO 三方式）、试点 M4（UART 缓冲）
  - `hardware/5.3 gpio`、`hardware/5.10 i2c-spi`
  - 本线模块 5 字符设备/platform driver、模块 4 设备树节点
- **验收方式**
  1. libgpiod 三命令跑通并解释输出字段；
  2. C 程序 request line/设置值骨架完整；
  3. `i2cdetect` 结果与原理图器件地址对应；
  4. 能说明 sysfs 废弃状态与 `/dev/mem` 风险；
  5. 对照表 ≥5 项；
  6. 章末自测题 ≥5 题。

---

## 第三部分 · 底稿缺口 / 2026 更新点 / 风险

### A. 底稿结构缺口（MCU 线）

1. **地图缺结构件**：§2.1 只有 9 篇，未列出"综合项目实战篇 / 题库篇 / 附录"；批次 E 在 §7.2 提及但知识地图未落结构，建议按 A10 补第十、十一篇与附录 A–G。
2. **缺 Git/版本控制与工程文档规范**：第八篇只讲构建、调试、测试，缺分支/标签/发布与 `.gitignore` 约定。
3. **缺参数持久化与 Flash 磨损均衡**：第七篇只覆盖 Bootloader/OTA，未展开 EEPROM/Flash 模拟 EEPROM、双区备份、CRC。
4. **缺 HardFault 诊断流程与崩溃寄存器转储**：第八篇调试未覆盖 PC/LR/SP 回溯与转储落 Flash。
5. **缺本地文件系统**：第九篇协议栈未含 FatFS/LittleFS/FlashDB。
6. **第一篇 C 深度缺工程基础**：`stdint`/大小端、错误码/断言、静态内存池、多文件工程与头文件依赖。
7. **缺非 Arm 架构专栏**：RISC-V MCU 与 Embedded Rust 生态在 2026 就业市场不可忽略，应给专栏/附录定位，不进主线。
8. **"何时升级 Linux"章未编号**：Q1 决策要求 MCU 册保留一章双向互链，落点建议在第十篇选型章。

### B. 底稿结构缺口（Linux 线）

1. **模块 1**：缺 MMU/页表/TLB、cache 一致性、GIC、通用定时器、EL2、多核 SMP 概念。
2. **模块 2**：缺 WSL2/Windows 主机路径、QEMU user-mode、sysroot/pkg-config 实战、第三方库交叉编译、gdbserver 入口。
3. **模块 3**：缺内核映像格式、命令行参数逐项、`init=` 与 PID1、QEMU virt 演示命令、FIT 校验细节、无 TF-A 板卡路径对照。
4. **模块 4**：缺 `aliases/chosen`、`ranges/#cells` 地址翻译、pinctrl/clocks、binding YAML 查阅、`/proc/device-tree` 验证、Overlay 应用时机。
5. **模块 5**：缺模块构建、`file_operations`、platform 生命周期、并发原语、顶/底半部、sysfs/kobject、udev 规则、`/dev/mem` 风险；LDD3（2005）API 已漂移，只能作概念参考并显式标注。
6. **模块 6**：缺 PID1 职责、initramfs、overlay 持久化、虚拟文件系统挂载、devtmpfs/udev、panic 排错、Debian rootfs 路线对照。
7. **模块 7**：缺 Buildroot 内部机制/自定义包、Yocto 目录/SDK/wic、选型量化标准、构建时间与磁盘成本、CRA 合规驱动。
8. **模块 8**：缺 NTP、journald、strace/perf、core dump、watchdog、PREEMPT_RT、Xenomai、安全网基础。
9. **模块 9**：缺量化决策表、案例库、异构核间通信（rpmsg/共享内存）、SoC 资源对照表。

### C. 2026 年需更新事实（已核实，写章时复核版本号）

| 项 | 2026-10 现状 | 对底稿的影响 | 来源 |
|---|---|---|---|
| Linux 内核 | mainline 7.3；longterm 6.18、6.6 | 模块 5/6/7 基线版本需写死，旧 5.x/6.1 表述更新 | https://www.kernel.org/finger_banner |
| PREEMPT_RT | 6.12 主线合并（ARM64/x86/RISC-V），仍需调优、非硬实时 | 模块 8/9 删除"必须打 RT 补丁"旧说法，补主线现状与局限 | https://bootlin.com/pub/conferences/2025/cdl/kernel-review.pdf ；https://realtime-linux.org/ |
| Yocto | 6.0 "Wrynose" LTS（2026-05，支持至 2030-04）；6.1 Blacksail 开发中 | 模块 7 版本与合规叙事更新 | https://www.yoctoproject.org/blog/2026/05/13/yocto-project-6-0-wrynose-is-here/ |
| Buildroot | 2026.08 稳定；2026.05 维护版；2025.02 LTS 至 2026-03 | 模块 7 版本基线更新 | https://buildroot.org/downloads/ |
| FreeRTOS | kernel 11.3.0/11.3.1；202604.00 LTS（支持至 2028-04-30）；MQTT v5.0；Armv8-M SMP | 第六篇版本/特性表更新 | https://www.freertos.org/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries ；https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history |
| Zephyr | 4.4 稳定（4.5 计划 2026-10）；Zephyr SDK 1.0；C17 | 第六篇版本与工具链表述更新 | https://docs.zephyrproject.org/latest/releases ；https://docs.zephyrproject.org/latest/releases/release-notes-4.4.html |
| RT-Thread | 5.3.0（2026-09） | 第六篇版本号更新 | https://www.rt-thread.org/document/site/ |
| CMSIS | 6.4.0（2026-10-08）；C-based startup、ACLE、头文件重构；工具链 Arm GNU v12+/LLVM v16+/IAR 9.30+/ArmClang v6+ | 第二篇/第三篇启动文件与内建函数表述更新 | https://www.keil.arm.com/packs/cmsis-arm/versions/ ；https://learn.arm.com/learning-paths/embedded-and-microcontrollers/project-migration-cmsis-v6/ |
| Arm GNU Toolchain | 15.3.rel2（GCC 15 系）；STM32CubeCLT 1.21.0（GCC 14/Clang/CubeProgrammer 2.22）；VS Code 扩展 2.0 走 CMake/Ninja、CMSIS-Pack DFP | 第二篇/M1 环境章版本与构建入口更新 | https://git.gitlab.arm.com/tooling/gnu-toolchains-for-arm/ ；https://qa-community.st.com/stm32cubeide-mcus-28/stm32cubeclt-1-21-0-released-163059 |
| picolibc | ESP-IDF v6 默认由 newlib 切 picolibc；ESP32-C3 实测 ROM -19.8%、栈 -54.1% | 第二篇 2.6 补 newlib vs picolibc 选型与实测 | https://developer.espressif.com/blog/2026/04/esp-idf-6-default-libc-picolibc/ |
| GPIO 用户态 | sysfs ABI obsolete，新代码一律 chardev v2 ioctl；libgpiod v2 为当前、v1 旧 API | 模块 5/L4 明确不教 sysfs，命令与 API 用 v2 | https://docs.kernel.org/6.12/userspace-api/gpio/sysfs.html ；https://www.kernel.org/doc/html/latest/userspace-api/gpio/chardev.html |
| RP2350 | 双核 Cortex-M33 或双核 Hazard3 RISC-V 启动可选 | 第四篇 RISC-V 专栏硬件依据 | https://www.raspberrypi.com/products/rp2350/ |
| QEMU virt | 自动生成 DTB；`-dtb` 自定义；`dumpdtb=` 随 machine 参数；`gic-version=3` | L2/L3 命令参数依据 | https://www.qemu.org/docs/master/system/arm/virt ；https://docs.u-boot.org/en/latest/develop/devicetree/control.html |
| 内核 Rust 驱动 | 主线持续演进，未到固件主流 | 仅作附录外链，不进主线 | — |

### D. 风险与对策

1. **范围膨胀**：9 篇 + 9 模块 + 实战/题库，总量易超硬件册。对策：大纲冻结前逐块标注"必讲/对比/外链/附录"；按底稿 §7.2 批次验收，附录内容不占主线章数；试点 9 章先跑通 schema/搜索/学习数据隔离/离线包。
2. **平台绑定 vs 通用性**：主例 STM32F4，每外设先讲通用寄存器概念；ESP32/RP2350/RISC-V 差异用专栏；Linux 主例 QEMU virt aarch64，真实板卡差异用对照表。
3. **与硬件手册重复**：严格执行底稿 §3 边界矩阵；每章开篇列"硬件原理 → hardware 5.x 链接"，软件侧只写配置序列/代码/现象；大纲评审逐章核对不抄原理。
4. **工具链版本漂移**：每章环境小节写死版本基线与下载链接；工具链升级走 ADR 与快照；代码只锁 API 不锁小版本。
5. **代码可复现性**：试点章必须给出"命令可从零复现"清单；板卡不可得时给 Wokwi（MCU）/QEMU（Linux）替代路径；仿真外链只跳转不内嵌（Q5=A 决策）。
6. **Windows 读者环境**：主线命令同时给 WSL2/PowerShell 说明，不假设 bash 原生环境；L1 主机准备小节显式覆盖 WSL2。
7. **API/文档漂移**：LDD3（2005）仅作概念参考并标注；正文引用 kernel.org 最新文档；每批扩展前复核版本号与上游现状。
8. **共享地基前置**：两条线试点依赖 P4-0 参数化质检/离线/快照/部署合并 ADR/Mermaid 接入（底稿 §7.3）；大纲完成不等于内容开工，落地顺序不变。
9. **图示工作量**：试点 9 章图清单先行；Mermaid 仅用于时序/状态/流程，内存布局与时序波形走 SVG，与硬件册风格统一；寄存器表按 §6.3 评估专用组件（P5 立项，本期不做）。
10. **学习数据隔离**：两 app 学习键分别为 `lubook.v1.embedded.learning`、`lubook.v1.embedded-linux.learning`；大纲不含学习 UI 内容，落地时按 PLAYBOOK §8 装配与单测。

### E. 待底稿作者决策的开放项

1. MCU 主例芯片最终选 STM32F4 还是 F1（资料量、寄存器简洁度、仿真支持三者权衡）；试点 M1–M5 的三方式对照深度是否一致。
2. Linux 试点 L4 在 QEMU virt 上 GPIO/I2C 外设有限，是否约定"QEMU 演示流程 + 真实板卡（RPi4/CM4 或 STM32MP157）照片/日志"双轨呈现。
3. 第六篇三内核是否在试点 M5 只讲 FreeRTOS，RT-Thread/Zephyr 留到批次 C；对照表保留在 M5 章末。
4. 模块 7 是否在试点阶段只建目录与选型章，Buildroot/Yocto 实战章排到批次后段。
