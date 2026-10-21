# 《嵌入式软件开发手册》前置构思与方案（EMBEDDED_PLAN）

> 状态：**前置研究 / 构思阶段（P4 立项前）**。本文只做调研与方案，不创建 `apps/embedded`、不写章节、不改代码/CI、不提交。
>
> 与 [`ARCHITECTURE.md`](ARCHITECTURE.md) 第 9 节对齐：规划路径为 `cp -r templates/site-template apps/embedded`，`appId='embedded'`、title《嵌入式软件开发手册》、base `/hardware-handbook/embedded/`，先 3–5 章验证 schema / 搜索 / 学习数据隔离 / 离线包，再决定门户。
>
> 本文凡涉及"现有架构如何复用"，均以仓库实际代码/配置为准（已核对：根 `package.json`、`run_quality.py`、`templates/site-template`、`apps/handbook`、`.github/workflows/*.yml`）。
>
> **命名基线（2026-10-21 品牌已定为「路书 Lubook」）：本文一切 appId/base/scope/学习键以 [`docs/NAMING.md`](docs/NAMING.md) 与 [ADR-0006](docs/adr/ADR-0006.md) 为准。`appId=embedded` / `embedded-linux` 不变；base 改为 `/lubook/embedded/` 与 `/lubook/embedded-linux/`；scope `@hw/*` → `@lubook/*`；硬件分册 `apps/handbook` → `apps/hardware`；学习键 `lubook.v1.<slug>.learning`。下文若仍出现旧 `hardware-handbook` / `@hw` 路径，一律按此替换。**

---

## 0. 决策结论（2026-10-21 已拍板：1A 2A 3A 4A 5A 6A 7B）

| 决策 | 选择 | 含义 |
|---|---|---|
| Q1 Linux 范围 | **A 另立第三个 app** | MCU 手册独立成册；嵌入式 Linux 作为第三个独立 app；MCU 手册只保留一章"何时升级到嵌入式 Linux" |
| Q2 与硬件手册重叠 | **A 交叉引用** | 硬件原理只放链接、不重复，软件实现重点写 |
| Q3 代码平台 | **A 多平台对照** | 以通用 Cortex-M/CMSIS 概念为底，STM32 为主例，ESP32/通用在关键差异处补专栏 |
| Q4 离线单文件 | **A 双形态** | 每个 app 各出一个离线 HTML，manifest 对账，embedded 起步即做 |
| Q5 交互/图示 | **A 仅 Mermaid** | 引入 Mermaid（时序/状态机/流程图）；代码运行/仿真暂外链 Godbolt/Wokwi/Renode，不内嵌 |
| Q6 语言/命名/许可/品牌 | **A 全部沿用** | 简体中文、kebab-case、文档 CC BY-SA 4.0 + 代码 MIT、appId=`embedded`、base `/lubook/embedded/`（品牌与命名以 NAMING/ADR-0006 为准） |
| Q7 Linux 时机 | **B 并行推进** | MCU 与 Linux 两条线并行（派独立子线）；**前置：先完成多 app 共享地基（参数化 verify/CI + 部署合并 ADR）** |

> 两个非推荐项的影响：Q3=A（非 B）要求代码组织为"通用 Cortex-M 概念 + STM32 主例 + ESP32/差异专栏"，不绑定单一厂商；Q7=B（非 A）使嵌入式 Linux 作为第三个 app（建议 `apps/embedded-linux`、appId=`embedded-linux`、base `/lubook/embedded-linux/`）与 MCU 手册并行启动，但共享地基（P4-0）必须先串行做完。

---

## 1. 定位与受众

### 1.1 一句话定位

《嵌入式软件开发手册》是硬件学习生态的第二本专项：**面向"让芯片跑起来、把系统做可靠"的软件侧**——从嵌入式 C 与编译工具链、Cortex-M 编程模型、裸机驱动，到 RTOS、Bootloader/OTA、构建调试测试与协议栈；与已上线的《硬件工程师手册》（"让电路成立、把信号做对"）互为表里、交叉引用。

- 硬件手册回答：**为什么这样设计电路**（原理、拓扑、电气参数、PCB/EMC）。
- 软件手册回答：**怎么用代码稳定地驱动与组织它**（寄存器/固件、驱动、RTOS、构建/调试、架构）。

### 1.2 目标读者与能力模型

| 读者 | 起点 | 目标 | 与硬件手册的关系 |
|---|---|---|---|
| 硬件工程师转软件 | 懂电路、会看原理图，代码薄弱 | 能独立写裸机外设驱动、用 RTOS、做 OTA | 先读硬件手册第 5 篇打底，再读本手册 |
| 嵌入式软件初中级 | 会用例程/HAL，原理与体系不清 | 打通工具链/启动/架构/调试/可靠性，能做项目 | 用硬件手册补电气与硬件边界 |
| 电子/计算机学生 | 学过 C 与数电，缺工程实践 | 建立完整工程知识地图与动手路线 | 两本对照，形成"软硬贯通" |

学习目标（能力模型）：
1. 读得懂链接脚本/启动文件/map，说得清"按下复位到 main 发生了什么"。
2. 能用寄存器 / LL / HAL 三种方式写常用外设驱动，并理解 DMA 与中断。
3. 能在 RTOS 上做任务划分、同步通信，规避死锁/优先级翻转/栈溢出。
4. 能做 Bootloader/IAP/OTA、低功耗、看门狗、日志断言等工程化能力。
5. 会用 CMake/构建、GDB/OpenOCD/RTT 调试、Unity/Ceedling 测试、cppcheck 与 MISRA。

### 1.3 内容形态基调

软件手册以**代码为主角**：大量可复制的 C 代码、寄存器/位定义、状态机与时序图、流程图、寄存器表；图文比例与硬件手册相反（硬件手册原理图/公式为主，软件手册代码/流程为主）。延续"不写代码用例外的空泛理论"，每个概念都落到可运行的最小代码与现象。

---

## 2. 嵌入式软件知识地图（详细大纲草案）

### 2.1 MCU 线（Cortex-M，9 篇大纲草案）

**第一篇 · 嵌入式 C 语言深度**
- 内存模型：`.text/.rodata/.data/.bss`、heap/stack 区段与 LMA/VMA、堆栈相向增长互踩、链接脚本符号（`_estack/_sidata/_sdata/_sbss`）。
- 指针：数据指针/`void*`/多级、指针与数组退化、`const` 修饰指针读法；函数指针与回调表、状态机跳转表、中断向量本质是函数指针数组。
- 结构体对齐：成员按自身大小对齐、整体对齐、尾部 padding、`packed`/`#pragma pack`、非对齐访问触发 HardFault；`offsetof`/`sizeof`。
- 位域与位操作：置/清/翻/取位宏、`BIT(n)`、读-改-写在中断共享寄存器上的原子性；位域跨编译器布局不确定，操作寄存器推荐掩码。
- 关键字：volatile（寄存器/ISR 共享/多线程标志，不保证原子性）、const（只读契约、省 RAM）、static（文件域隐藏/函数内保持状态）、extern（跨单元声明）。
- 宏与条件编译：函数式宏副作用、`do{}while(0)`、X-Macro 表驱动、头文件保护、芯片/板型裁剪。
- 可重入与线程安全：可重入条件、与线程安全的区别、临界区保护；newlib `malloc/printf` 默认可重入问题。
- C 与汇编混合：内联汇编、`.s/.S`、AAPCS/EABI（R0–R3 传参、栈 8 字节对齐）、上下文切换与开关中断。

**第二篇 · 编译工具链（arm-none-eabi-gcc）**
- 全流程：预处理→编译(-O0..-Os)→汇编→链接→objcopy/size/nm/objdump；`.elf/.map/.bin/.hex`。
- 链接脚本：`MEMORY`(FLASH 0x08000000 / RAM 0x20000000)、`SECTIONS` 段布局、LMA/VMA、`AT>`、`KEEP()`、`--gc-sections` + `-ffunction/-fdata-sections`。
- 启动文件：栈指针→Reset_Handler→`.data` 搬运→`.bss` 清零→`SystemInit`→`__libc_init_array`→`main`。
- CMSIS：`core_cm4.h`、SCB/NVIC/SysTick 内建函数、设备头外设定址结构体、IRQn、CMSIS-RTOS2。
- map 分析与 newlib-nano：`nano.specs`、`_printf_float`、`_sbrk`、`_write/_read` 重定向。

**第三篇 · Cortex-M 架构与编程模型**
- 寄存器组 R0–R15、xPSR/PRIMASK/FAULTMASK/BASEPRI/CONTROL；Thread/Handler 模式与特权级。
- 双栈 MSP/PSP；NVIC（使能/挂起/active、尾链、迟到）、异常自动入栈 8 项、EXC_RETURN、优先级分组（抢占/子）、VTOR、PRIMASK/BASEPRI。
- SysTick（24 位、RTOS tick）；MPU；bit-band 位带。
- 系列差异：M0/M0+（Thumb 子集、无 bit-band/无自由非对齐）、M3（硬除/bit-band/MPU）、M4（FPU+DSP/SIMD）、M7（cache/双 FPU/TCM/分支预测）、M23/M33（Armv8-M、TrustZone、PAC/BTI、可选 MVE）。

**第四篇 · 裸机开发**
- main 之前流程、时钟树 RCC（HSI/HSE→PLL→SYSCLK→AHB/APB、Flash wait state）、复位与向量表。
- 外设软件驱动：GPIO 模式/复用、EXTI 边沿、TIM 时基/PWM/输入捕获/编码器、ADC 扫描+DMA、UART 收发、I²C（起始/ACK/时钟拉伸/位模拟）、SPI（CPOL/CPHA）、CAN（位时序/过滤器/邮箱）、USB（端点/枚举，多借栈）。

**第五篇 · 三种开发方式与软件架构**
- 寄存器/LL/HAL 对比（透明体积 vs 可移植）、BSP 板级抽象。
- DMA 软件：请求映射、宽度/增量、半/完成中断、M7 cache 一致性、循环/双缓冲乒乓。
- 架构：中断 vs 轮询、ISR 最小化；有限状态机（表驱动）、事件驱动（事件队列）、前后台 super-loop。

**第六篇 · RTOS（FreeRTOS / RT-Thread / Zephyr）**
- 任务/TCB、优先级约定、抢占+时间片、任务状态（运行/就绪/阻塞/挂起）。
- 同步通信：二值/计数信号量、mutex（优先级继承）、事件组、队列（拷贝式）、流/消息缓冲、任务通知（最轻量）。
- 内存（heap_1..5）、软件定时器（回调不可阻塞）、tickless。
- 典型问题：死锁、优先级翻转、栈溢出（high-water mark/hook）、ISR 仅可用 `FromISR`、优先级设计。
- 三者对比：FreeRTOS（MIT、占有率最高、极简）、RT-Thread（国产、组件丰富、Kconfig、安全认证）、Zephyr（Linux 基金会、Armv8-M/设备树、IoT 模块化）。

**第七篇 · 系统工程**
- Bootloader/IAP、OTA、双分区 A-B、回滚、安全启动（签名/哈希链、TrustZone）。
- 日志/断言（configASSERT、错误分级）、低功耗软件（Sleep/Stop/Standby、唤醒源、状态保持）、IWDG/WWDG 喂狗策略与复位记录。

**第八篇 · 工程效能**
- 构建：Make / CMake / Kconfig / STM32CubeMX。
- 调试：GDB、OpenOCD、JTAG/SWD、SEGGER RTT、ITM/SWO、semihosting、printf 重定向。
- 测试：Unity / Ceedling / CMock；静态分析：cppcheck / PC-lint Plus；MISRA-C:2012 关键规则；CI 矩阵。

**第九篇 · 通信协议栈软件实现**
- Modbus RTU/TCP（功能码/CRC16/T3.5 帧间隔、ADU/PDU）；CAN 应用层/CANopen 概念（对象字典/PDO/SDO/NMT/心跳）；LwIP/MQTT（QoS/TLS）；AT 指令状态机与 URC；DMA+单写单读环形缓冲零拷贝。

### 2.2 嵌入式 Linux 线（大纲草案，建议另立第三 app）

**知识模块（9 块）**
1. 硬件底座：Cortex-A/SoC（MMU 虚拟内存/L1·L2 cache/外部 DDR/外部存储）vs Cortex-M（MPU/无 MMU/片内 Flash）；ARMv7-A（32 位）/ARMv8-A（AArch64，物理寻址 48-bit）；运行级别 EL0（应用）/EL1（内核）/EL2（Hypervisor）/EL3（Secure Monitor，TF-A 常驻）；TrustZone（Secure/Non-secure，SMC 切换，OP-TEE）。
2. 交叉编译：`arm-linux-gnueabihf-`/`aarch64-linux-gnu-`、sysroot、`ARCH=`/`CROSS_COMPILE=`、外部工具链（Linaro）；开发主机 Linux，串口/SSH/NFS/tftp 连接。
3. 启动链：ROM code → SPL（初始化 DDR）→ TF-A（BL1→BL2→BL31 常驻/BL32 OP-TEE/BL33=U-Boot）→ U-Boot Proper → Linux+DTB+rootfs；U-Boot 环境变量（`bootcmd/bootargs/fdt_addr_r`）、`bootm/bootz/booti/bootefi`、driver model、FIT 校验。
4. 设备树：DTS/DTSI→`dtc`→DTB；`compatible/reg/interrupts/pinctrl/clocks`；binding YAML；Overlay（DTO `/plugin/`、`target`、`__overlay__`、`of_overlay_fdt_apply`）；`of_match_table` 匹配实例化 platform device。
5. 内核与驱动：`defconfig/menuconfig`、`Image/zImage`、`.ko` 模块；字符设备 cdev、platform bus、I2C/SPI 子系统、`request_irq`；用户态访问——libgpiod（gpiochip chardev v2，旧 sysfs 已废弃）、i2c-dev、spidev、sysfs/ioctl。
6. rootfs：BusyBox（单二进制/init/sh）；init（SysV/BusyBox init/systemd）；镜像（ext4、SquashFS+overlayfs、UBIFS for raw NAND）；devtmpfs+mdev/udev。
7. 构建系统：Buildroot（Kconfig/menuconfig、快、中小项目）vs Yocto（recipe/layer/BitBake、可复现、SDK、企业长维护，学习陡）；选型。
8. OTA（RAUC：A/B+squashfs+PKCS#7；SWUpdate：`.swu`/多组件/最灵活；Mender：A/B rootfs+托管服务）；网络（NetworkManager/ConnMan/systemd-networkd）；调试（串口/printk/strace/gdbserver/OpenOCD/NFS root）。
9. 选型（MCU/RTOS vs Linux）：硬实时中断延迟 µs 级、RAM KB–MB、<100ms 开机、µA 睡眠、低成本 → MCU；富网络/GUI/文件系统/复用 Linux 生态、RAM≥32–64MB → Linux；高端常见异构（Cortex-A+M，如 i.MX 8M/STM32MP1）。

**纳入/另立结论（研究子智能体 C 论证）**：建议**另立《嵌入式 Linux 手册》作为第三个独立 app**；MCU 手册只保留一章"何时升级到嵌入式 Linux"决策指引 + 异构 SoC 一句带过 + 双向互链。理由：① 知识规模各成 700+ 页独立体系；② 受众日常命令/调试器/心智不同；③ 核心抽象互斥（物理寄存器单地址空间 vs MMU+设备树+用户态）；④ 工具链/构建/启动/调试工程管线几乎不共享；⑤ 仅 C 语言与 I2C/SPI 等底层常识可复用（属硬件基础层）。不建议同册大附录（膨胀）或同 app 多卷（工程上纠缠）。

---

## 3. 与《硬件工程师手册》的边界矩阵

逐章对比硬件手册第五篇《单片机与嵌入式硬件》（硬件视角，章节为 5.1–5.13）与软件手册潜在重叠，给出明确归属。约定：**交叉引用**=只放链接、不重复；**软件侧重写**=硬件原理不重复、软件实现重点写；**不重复**=完全不覆盖。

| 硬件手册章节（硬件视角） | 重叠点 | 软件手册处理 | 软件侧具体内容 |
|---|---|---|---|
| 5.1 MCU 概览：51/STM32/ESP32 架构 | 内核/资源 | 软件侧重写（角度不同） | 软件视角选型：位宽/Flash/RAM/生态/可移植性；交叉引用 5.1 |
| 5.2 最小系统：电源/时钟/复位/调试 | 复位、时钟 | 软件侧重写 | 复位与启动链、main 前流程、时钟树 RCC 软件初始化；硬件最小系统交叉引用 |
| 5.3 GPIO 原理与驱动能力 | GPIO | 软件侧重写 | GPIO 模式配置、HAL/LL/寄存器三种写法、外部中断；电气驱动能力交叉引用 |
| 5.4 中断机制（硬件视角） | NVIC/优先级 | 软件侧重写 | ISR 编写规范、NVIC 配置、优先级分组设计、中断安全/可重入；向量表硬件交叉引用 |
| 5.5 ADC 原理、参数与参考电压 | ADC | 软件侧重写 | 采样时序、校准、DMA 搬运、软件滤波/过采样；参数与参考电压交叉引用 |
| 5.6 DAC 与模拟输出 | DAC | 软件侧重写 | DAC 输出、DMA 波形生成、触发配置；模拟输出原理交叉引用 |
| 5.7 定时器与 PWM 原理 | 定时器 | 软件侧重写 | 时基/输出比较/输入捕获/PWM 软件配置；计数原理交叉引用 |
| 5.8 UART 与 RS-232 物理层 | UART | 软件侧重写 | 收发、中断/DMA 环形缓冲、printf 重定向、帧错误处理；RS-232 物理层交叉引用 |
| 5.9 RS-485 与 CAN 总线硬件 | 总线 | 软件侧重写 | CAN 驱动/过滤器/应用层、RS-485 方向控制、Modbus；收发器/电平交叉引用 |
| 5.10 I²C 与 SPI 总线时序 | 总线 | 软件侧重写 | I²C/SPI 驱动、外设读写、时序配合、DMA；时序图交叉引用 |
| 5.11 USB 与以太网物理层概览 | 总线 | 软件侧重写 | USB 设备协议栈/设备类、LwIP/MQTT/以太网初始化；物理层交叉引用 |
| 5.12 看门狗、RTC 与低功耗硬件 | 看门狗/低功耗 | 软件侧重写 | IWDG/WWDG 喂狗策略、RTC 软件、低功耗模式/唤醒/状态保持；硬件原理交叉引用 |
| 5.13 常用外设接口设计 | 系统整合 | 交叉引用 | 仅做"驱动如何整合"的综合案例；硬件设计不重复 |

其它篇的边界：

| 硬件手册 | 软件手册如何处理 |
|---|---|
| 第一篇 电路基础（电压/电流/RC 等） | 不重复；仅在涉及"上拉/电平/滤波对软件的影响"时交叉引用 |
| 第四篇 数字电路（数制/布尔/触发器/存储器） | 不重复讲授；C 位操作/寄存器直接复用，标注链接（数制、逻辑运算、存储类型） |
| 第二篇 元器件（晶振/电阻/电容等） | 时钟树软件处交叉引用晶振；去耦/电源不重复 |
| 第三篇 运放/信号链 | 不重复；仅在"传感器信号如何被 ADC 采样"处交叉引用 |
| 第六篇 电源、第七篇 PCB/EMC | 不重复；低功耗/ESD 对软件的约束处交叉引用 |

**软件手册不可替代的内容**（硬件手册完全不覆盖）：嵌入式 C 深度与内存模型、编译工具链/链接脚本/启动文件/map、Cortex-M 编程模型与 CMSIS、寄存器/LL/HAL 驱动代码、DMA 软件、裸机架构（状态机/事件驱动/前后台）、RTOS（任务/调度/同步/IPC/低功耗）、Bootloader/IAP/OTA/双分区、构建系统（Make/CMake/Kconfig）、调试（GDB/OpenOCD/RTT）、单元测试（Unity/Ceedling）、静态分析与 MISRA-C、协议栈软件实现、（另一条线）嵌入式 Linux。

---

## 4. 行业权威资料清单

### 4.1 MCU / Cortex-M 官方文档（URL 已核实）

| 资料 | 出处 | 权威性 |
|---|---|---|
| Cortex-M Generic User Guide（M0/M0+ DUI0552、M4 DUI0553、M7 DUI0646 等） | https://developer.arm.com ；资源汇总 https://community.arm.com/ （Cortex-M resources） | 编程模型/指令集官方定义 |
| Cortex-M Technical Reference Manual（如 M7 DDI0489） | https://developer.arm.com | 处理器规格官方手册 |
| CMSIS（CMSIS-Core） | https://github.com/ARM-software/CMSIS | ARM 官方 Cortex-M 软件抽象标准 |
| FreeRTOS 官方文档 | https://www.freertos.org/Documentation | 内核 API/配置官方权威 |
| 《Mastering the FreeRTOS Real Time Kernel》, Richard Barry | https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book | FreeRTOS 创始人亲著官方免费教材 |
| RT-Thread 官方文档 | https://www.rt-thread.org/document/site/ | 官方内核/组件 API |
| Zephyr 官方文档 | https://docs.zephyrproject.org/ | Linux 基金会官方（域名公认，本轮未二次抓取） |
| MISRA-C:2012 | https://misra.org/ （付费标准，购买页未核实） | 安全关键 C 编码国际标准 |

### 4.2 MCU 书籍（ISBN 已核实）

| 书名 | 作者 | 核实结果 |
|---|---|---|
| The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors, 3rd ed. (2013, Elsevier) | Joseph Yiu | ISBN 978-0-12-408082-9；作者为 ARM Distinguished Engineer |
| 嵌入式 C 语言自我修养——从芯片、编译器到操作系统 (2021, 电子工业出版社) | **王利涛**（⚠️ 非"李云"） | ISBN 978-7-121-40856-4 |
| Mastering STM32, 2nd ed. (2022, Leanpub) | Carmine Noviello | Leanpub 电子版 https://leanpub.com/mastering-stm32-2nd ；无纸本 ISBN |
| RT-Thread 内核实现与应用开发实战指南——基于 STM32 (2019, 机械工业出版社) | 刘火良、杨森 | ISBN 978-7-111-61366-4 |
| Making Embedded Systems, 2nd ed. (O'Reilly, 2022) | Elecia White | ISBN 978-1-0981-5154-6 |
| Embedded C Coding Standard (BARR-C:2018) | Michael Barr / Barr Group | ISBN 978-1-72112-798-6；官网免费 HTML/PDF https://barrgroup.com/ |

### 4.3 嵌入式 Linux 官方文档（URL 已核实）

| 资料 | URL |
|---|---|
| Kernel 设备树用法模型 / Overlay / binding 规范 | https://docs.kernel.org/devicetree/usage-model.html ；…/overlay-notes.html ；…/bindings/submitting-patches.html |
| UBIFS 文件系统 | https://docs.kernel.org/filesystems/ubifs.html |
| GPIO chardev v2 / 内核用 GPIO 指引 | https://www.kernel.org/doc/html/latest/userspace-api/gpio/chardev.html ；https://docs.kernel.org/driver-api/gpio/using-gpio.html |
| I2C i2c-dev 用户态接口 | https://www.kernel.org/doc/Documentation/i2c/dev-interface |
| U-Boot（环境/bootz/设备树） | https://docs.u-boot.org/en/latest/usage/environment.html ；…/usage/cmd/bootz.html ；…/develop/devicetree/control.html |
| TF-A | https://trustedfirmware-a.readthedocs.org/ ；https://tf-a.docs.trustedfirmware.org/ |
| Buildroot 手册 / Yocto Mega-Manual / init 管理器 | https://buildroot.org/downloads/manual/manual.html ；https://docs.yoctoproject.org/mega-manual/ ；…/dev-manual/init-manager.html |
| Bootlin 培训资料（Buildroot slides） | https://bootlin.com/doc/training/buildroot/buildroot-slides.pdf |
| RAUC / BusyBox | https://rauc.io/ ；https://www.busybox.net/ |
| Cortex-A vs Cortex-M 白皮书 / ARMv8-A 概述 | https://www.arm.com/-/media/Files/pdf/white-paper/optimizing-arm-cortex-a-and-cortex-m-whitepaper.pdf ；https://armkeil.blob.core.windows.net/developer/Files/pdf/graphics-and-multimedia/ARMv8_Overview.pdf |

### 4.4 嵌入式 Linux 书籍（ISBN 已核实）

| 书名 | 作者 | ISBN |
|---|---|---|
| Linux Device Drivers, 3rd ed. (O'Reilly, 2005) | Corbet, Rubini, Kroah-Hartman | 0-596-00590-3 |
| Mastering Embedded Linux Programming, 3rd ed. (Packt, 2021) | Frank Vasquez, Chris Simmonds | 978-1-78953-038-4 |
| Embedded Linux Systems with the Yocto Project (Pearson, 2016) | Rudolf J. Streif | 978-0-13-344324-0 |
| Embedded Linux Primer, 2nd ed. (2010) | Christopher Hallinan | 978-0-13-701783-6 |

> 未核实项：spidev 独立文档直链（内核树 `Documentation/spi/spidev.rst` 存在，未单独抓取）；RAUC/SWUpdate/Mender 逐项参数来自第三方对比资料，引用以各官网为准。

---

## 5. 类似开源项目 / 文档站调研

核实基准 2026-10-14；star 数经 GitHub API / 官方文档交叉核实，未取到的标注"未核实"。共 11 个真实项目。

| # | 名称 | 真实 URL | 形态/技术栈 | 内容范围 | License | 活跃度 | 可借鉴点 | 我们的差异化空间 |
|---|---|---|---|---|---|---|---|---|
| 1 | Awesome-Embedded | https://github.com/nhivp/Awesome-Embedded | GitHub awesome 列表 | MCU 编程、RTOS、Linux 驱动、汇编、Bootloader、GUI 导航 | CC-BY-SA-4.0 | ≈9.2k star（精确值未核实）；持续收录 | Interview/Skill/Common 分类体系成熟 | 纯链接，无代码/交互/系统讲解；我们做体系+可运行代码 |
| 2 | FreeRTOS 内核 +《Mastering the FreeRTOS RT Kernel》 | https://github.com/FreeRTOS/FreeRTOS ；书 https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book | 仓库 + 文档站 + PDF | 内核源码、API、手把手配套书（QEMU 免硬件实验） | MIT | star 精确值未核实（量级 5k+）；文档 2026-10 仍更新 | 书+示例源码+QEMU 免硬件三位一体 | 英文、单 RTOS 中心；我们做跨内核原理+中文+浏览器可跑 |
| 3 | Zephyr Project | https://github.com/zephyrproject-rtos/zephyr ；https://docs.zephyrproject.org | 仓库(C) + Sphinx 文档站 | 安全可扩展 RTOS、多架构、设备模型、子系统、样例 | Apache-2.0 | **16.8k star / 10.2k fork，pushed 2026-10-14** | 概念→API→样例→移植分层清晰，docs 与源码同仓 | 偏平台手册、入门陡峭；我们做精简代码密集的桥梁 |
| 4 | RT-Thread | https://github.com/RT-Thread/rt-thread ；https://www.rt-thread.org/document/site/ | 仓库(C) + 中文文档站(VuePress 类) | 国产 IoT RTOS、Nano/标准版、软件包、Studio、驱动教程 | Apache-2.0 | **12.3k star / 5.5k fork，pushed 2026-10-14** | 中文社区+中文文档+视频教程的成功范本 | 偏"使用 RT-Thread"；我们做不绑 RTOS 的通用原理+可视化 |
| 5 | ESP-IDF | https://github.com/espressif/esp-idf ；https://docs.espressif.com/projects/esp-idf | 仓库(C) + Sphinx 文档站 | ESP32 全系列框架、环境到网络/安全/驱动 | Apache-2.0 | **19.2k star / 8.5k fork，pushed 2026-10-09** | Get-Started→API Guide→Reference 分层、多语言版本化 | 绑乐鑫芯片；我们做厂商无关的通用底座 |
| 6 | arduino-esp32 | https://github.com/espressif/arduino-esp32 | 仓库(C++) | ESP32 的 Arduino core，易用封装 | LGPL-2.1 | **17.5k star / 7.9k fork，pushed 2026-10-09** | 低门槛封装 vs 底层裸机的对比参照 | Arduino 隐藏细节；我们反向讲透被封装的底层 |
| 7 | Compiler Explorer | https://github.com/compiler-explorer/compiler-explorer ；https://godbolt.org | 开源 Web 应用(TS) + 在线工具 | 浏览器内编译，源码↔汇编实时对照、开关对比 | BSD-2-Clause | **19.1k star，pushed 2026-09-15** | 源码到汇编交互标杆，支持 iframe/embed | 只看汇编、不讲嵌入式上下文；我们嵌进知识点 |
| 8 | Renode | https://github.com/renode/renode ；https://renode.readthedocs.io | 开源仿真框架(Antmicro) + ReadTheDocs | 多节点嵌入式网络仿真、免硬件跑固件、板级 demo | GPL-3.0 | ≈2.6k star（精确值未核实）；持续维护 | CI/离线级仿真，配套板级 demo | 桌面/CLI、**无法网页 iframe 直跑**，仅放 Colab/本地跳转 |
| 9 | Wokwi | https://wokwi.com ；https://docs.wokwi.com ；https://github.com/wokwi | 在线仿真（核心闭源）+ 开源 CLI/插件 | 浏览器仿真 Arduino/ESP32/STM32/RP2040，含串口/示波器 | 核心闭源；CLI/插件开源（条款未逐一核实） | 文档 2026-10 仍更新、板型扩张 | 最适合网页内嵌的 MCU 仿真，有 diagram.json/wokwi.toml | 保真度/免费额度有限；只在关键节点嵌最小 demo |
| 10 | Awesome C | https://github.com/inputsh/awesome-c | GitHub awesome 列表 | C 语言库/工具/教程/风格 | CC 类 | 长期维护（2026-05 仍同步） | C 语言资源导航 | 链接列表无交互；我们聚焦嵌入式 C 工程实践 |
| 11 | awesome-embedded-software | https://github.com/iDoka/awesome-embedded-software | GitHub awesome 列表 | 资源受限 MCU 的软件库/协议/接口 | 开源列表 | 长期维护 | 按 8/16/32 位资源受限组织，贴近裸机 | 与 #1 重叠，作选材参考 |

**调研结论**：未发现"以 VitePress 搭建且专注嵌入式"的知名中文开源手册；现有中文嵌入式文档（RT-Thread、ESP-IDF/Zephyr）多为厂商绑定。"中立、代码密集、VitePress 中文、浏览器内可看汇编/跑最小仿真"的通用手册存在明确空白。

### 5.1 文档站技术选型：维持 VitePress

| 方案 | 代码密集 | 嵌自定义交互 | 中文生态 | 与 pnpm/Vite 契合 | 结论 |
|---|---|---|---|---|---|
| **VitePress** | 代码块/行高亮/分组齐全 | **原生支持在 .md 中嵌 Vue 组件**，可自写寄存器表/时序图/仿真容器 | 中文文档完整 | 天然一致、构建快 | **选定** |
| MkDocs Material | 强、插件多 | 靠 HTML/JS 注入，交互笨重 | 一般 | 弱（Python） | Zephyr/ESP-IDF 用，我们要嵌 Vue 不划算 |
| Docusaurus | 强 | React 可交互 | 一般 | Node | React 栈，团队偏 Vue |
| Docsify | 轻、无构建 | 运行时加载、SEO 弱 | 教程常用 | 一般 | 适合轻笔记，不适合代码密集 |
| Antora | 多仓聚合强 | 弱 | 弱 | 弱 | 对单本手册过重 |

**对"代码密集 + 可交互"的建议**：
1. 代码块用 VitePress 内置分组/行高亮/复制；可加"一键到 Godbolt/Wokwi"自定义按钮。
2. 寄存器表用自定义 Vue 组件（JSON 驱动、可悬停位域），不用静态表格硬画。
3. 时序图/状态机/流程图：建议引入 **Mermaid**（`sequenceDiagram`/`stateDiagram-v2`/`flowchart`）。**注意：VitePress 并不内置 Mermaid，需在主题里用 `vitepress-plugin-mermaid` 或自行包装 `@mermaid-js/mermaid`（客户端/构建期渲染）**——属新增依赖，落地时需评估并记录。
4. 代码沙箱按成熟度：**Compiler Explorer**（iframe 预填代码看汇编，最成熟）；**Wokwi**（网页内嵌最现实的 MCU 仿真，只在关键节点嵌最小示例）；**Renode**（强但为桌面/CLI，网页只放跳转链接）。

---

## 6. 技术落地方案（在现有 Monorepo 内）

### 6.1 直接复用（无需改动）

| 资产 | 复用方式 |
|---|---|
| `templates/site-template` | 直接 `cp -r` 作为 embedded 骨架（已含薄 config、content.config、theme、SUMMARY、示例章、gen 脚本） |
| `@hw/shared-config` | `defineHwConfig` 提供五类容器、KaTeX、CJK 强调、折叠题、ECharts、中文本地搜索、cleanUrls——软件手册全部继承 |
| `@hw/theme` | `createHwTheme({catalog, repository, logo?})` 提供布局、品牌、EChart、图片查看器、学习 UI（进度/收藏/笔记/导入导出） |
| `@hw/content-core` | manifest 生成 + 纯数据 `catalog.generated.mjs`，embedded 走同一套 `--appId` 流程 |
| `@hw/learning` | 已按 **appId 隔离**（localStorage 键 `hb.v1.embedded.learning`），与 handbook 数据天然不串；迁移/导入导出/tombstone 直接复用 |
| `packages/tooling` | 离线构建/质检/vendor 已参数化（`paths_util`：`--app/--src/--out/--vendor`） |

### 6.2 需要改动 / 新增（多 app 带来的工程项）

> 这些属于 P4 落地时的改动，**本轮只记录、不实施**；其中部分触发"部署拓扑/构建"类变更，需补 ADR。

1. **`run_quality.py` 当前写死 handbook**：现状 `check_manifest()` 直接 `F.build_manifest()`（默认 handbook 路径）、读 `tests/routes.snapshot.json` + `manifest.snapshot.json`、且断言 `appId=='handbook'`。多 app 需参数化：接受 `--app/--src/--snapshot-prefix`，或新增外层脚本对 `apps/*` 逐个跑（每 app 独立快照，如 `tests/embedded.routes.snapshot.json`）。
2. **离线单文件**：现 `build_single_html` 默认 `src=apps/handbook/docs`、输出一个 `hardware-handbook.html`。embedded 需 `--app embedded --src apps/embedded/docs --out dist/embedded.html`，并各自 `--manifest` 对账；"一个 app 一个离线文件"还是"合并册"为决策点（见 Q4）。
3. **CI 质量门禁 `quality.yml`**：现只 `--filter @hw/handbook` 构建 + handbook 的离线/快照。需新增：
   - `pnpm --filter @hw/embedded docs:build`；
   - 对 embedded 跑 `run_quality.py --app embedded`（依赖 1）；
   - embedded 的 freeze + 离线对账。
   - 可用 `pnpm -r --filter ./apps/* run docs:build` 收敛成一条。
4. **部署 `deploy-docs.yml`（GitHub Pages）**：现仅 `upload-pages-artifact` 上传 `apps/handbook/docs/.vitepress/dist`。embedded base 为 `/hardware-handbook/embedded/`，需在一次部署里**构建两个 app 并合并产物**：handbook dist 放暂存区根，embedded dist 放 `staging/hardware-handbook/embedded/`，再整体上传。这是部署拓扑变更，**需补 ADR**。
5. **Cloudflare 镜像 `deploy-cloudflare.yml`**：同步处理双 app 合并；`VP_BASE` 策略需按 app 分别给（handbook 根/镜像根、embedded 子路径）。
6. **根 `package.json` 脚本**：现 `verify` 只串 handbook。需新增 `build:embedded`、`offline:embedded`，并把 `verify` 扩展为覆盖 apps/*；或保留 `verify:handbook` 与新的 `verify:all`。
7. **门户/导航（后议）**：生态首页如何并列两个专项（卡片式入口），按 ARCHITECTURE 第 9 节"先 3–5 章验证后再决定门户"，本期不做。

### 6.3 软件手册特有的内容形态（组件/渲染）

| 需求 | 现状能力 | 建议 |
|---|---|---|
| 代码块（C/ld/CMake/脚本） | VitePress 内置高亮 + 复制 | 直接用；统一代码块语言标注与注释风格 |
| 时序图 / 状态机 / 流程图 | 仅 ECharts（graph 可做状态机/流程图，但时序图弱）、内联 SVG | 决策点 Q5：是否引入 Mermaid（时序/状态机/流程最省事）；或用 ECharts graph + 内联 SVG |
| 寄存器表 / 位域表 | GFM 表格可做 | 表格 + 内联代码（寄存器名/复位值）；如量大可评估专用寄存器组件（P5） |
| 代码可运行 / 内联仿真 | 无 | 评估 Wokwi（在线仿真）/ Renode（开源仿真）/ Compiler Explorer 嵌入（Q5）；可外链为主、组件为辅 |
| 图示（启动流程/内存布局） | 内联 SVG / ECharts | 与硬件手册同套 SVG 规范，保持风格统一 |
| 公式（如比特率/占空比/波特率误差） | KaTeX | 复用 |

---

## 7. 分阶段路线（3–5 章试点 → 批次扩展）

### 7.1 试点章（建议首批 4–5 章，最有代表性）

> 试点目标：用最少章节打通"工具链→启动→一个外设驱动→RTOS 最小任务"的主链路，并验证 schema/搜索/学习数据隔离/离线包。

| 建议章 | 所属篇 | 理由 |
|---|---|---|
| ① 开发环境与第一个工程：点亮 LED（工具链 + 构建 + 烧录 + 工程结构） | 起步篇 | 端到端跑通"写代码→编译→烧录→看现象"，是所有后续章节的脚手架 |
| ② 从复位到 main：启动文件、链接脚本与内存布局 | 工具链篇 | 最能体现"软件手册不可替代"的硬知识，打通 main 前黑盒 |
| ③ GPIO 与外部中断（寄存器/LL/HAL 三方式） | 外设驱动篇 | 最经典、最易对比三种开发方式的外设，与硬件手册 5.3/5.4 直接交叉 |
| ④ 串口收发与 printf 重定向（中断/DMA/环形缓冲） | 外设驱动篇 | 调试与日志的基石，顺带覆盖 DMA、环形缓冲、中断 |
| ⑤ RTOS 入门：任务创建、调度与延时（FreeRTOS 或 RT-Thread） | RTOS 篇 | 验证第二大块（RTOS）在我们的主题/构建下成立 |

### 7.2 批次扩展（试点验证后）

按 9 篇大纲，建议 5 个批次（试点 4–5 章先行，每批可独立验收、构建与截图）：

| 批次 | 篇/内容 | 预估章数 | 出口 |
|---|---|---|---|
| 试点 | 见 7.1 的 4–5 章（环境/启动/GPIO 中断/串口/RTOS 入门） | 4–5 | schema、搜索、`hb.v1.embedded` 隔离、离线包全验证 |
| 批次 A | 起步（环境/工程结构）+ 第一篇 C 深度 + 第二篇 工具链 + 第八篇 调试 | 18–24 | 能讲清工具链/链接/启动/main 前全流程 |
| 批次 B | 第三篇 Cortex-M 架构 + 第四篇 裸机外设驱动（GPIO/EXTI/TIM/ADC/UART/I2C/SPI/CAN/USB） | 18–26 | 三方式写常用外设，DMA 与中断到位 |
| 批次 C | 第五篇 架构模式（状态机/事件驱动/前后台）+ 第六篇 RTOS（三内核） | 14–20 | 任务划分/同步/IPC/低功耗与典型问题 |
| 批次 D | 第七篇 系统工程（Bootloader/OTA/低功耗/看门狗/日志断言）+ 第九篇 协议栈 + 选型决策章（含异构/Linux 升级） | 14–20 | 工程化与协议栈完整，给出升级 Linux 的路径 |
| 批次 E | 第八篇 工程效能（测试/静态分析/MISRA/CI）+ 综合项目实战 + 题库 + 附录 | 12–18 | 全流程闭环、可维护 |

**预估总规模**：MCU 软件手册约 **90–115 章**（与硬件手册 140 章相近量级，软件章代码密集可略短）；嵌入式 Linux 若另立，约 **40–60 章**（按 9 模块展开）。

### 7.3 并行执行顺序（Q7=B：MCU 与 Linux 并行）

嵌入式 Linux 与 MCU 并行启动，但必须先一次完成**共享地基**，再分两条独立子线并行：

**P4-0 · 共享地基（串行，先做，不产出内容章）**

1. 参数化 `run_quality.py`：`--app/--src/--snapshot-prefix`，每 app 独立快照（`tests/embedded.*.snapshot.json`、`tests/embedded-linux.*.snapshot.json`）；
2. 离线 `build_single_html` 对两个新 app 各跑 `--manifest` 对账（每 app 一个离线 HTML）；
3. 根 `package.json` 增加 `build:embedded`/`build:embedded-linux`、`offline:*`，并把 `verify` 扩展为覆盖 `apps/*` 的 `verify:all`；
4. `quality.yml` 扩为多 app 矩阵（或 `pnpm -r --filter ./apps/* run docs:build`）；
5. **ADR-0006 多 app 部署拓扑**：一次部署合并多 app 产物（handbook→根、embedded→`embedded/`、embedded-linux→`embedded-linux/`），同步改造 Pages 与 Cloudflare，`VP_BASE` 按 app 处理；
6. **Mermaid 接入 ADR**（Q5=A）：评估 `vitepress-plugin-mermaid` 或自封装 `@mermaid-js/mermaid`（构建期渲染），确认在 `@hw/shared-config`/`@hw/theme` 中以共享能力接入，两个 app 共用。

**P4-1 · 两 app 并行试点（P4-0 完成后派两条独立子线）**

- MCU 线：7.1 的 5 章试点（环境/点亮 LED → 复位到 main → GPIO/中断 → 串口/DMA → RTOS 入门）。
- Linux 线（新增 4 章试点）：

| 建议章 | 模块 | 理由 |
|---|---|---|
| ① 开发环境与交叉编译（工具链/sysroot/QEMU 免硬件） | 交叉编译 | 端到端跑通；QEMU 代替开发板，全部可本地复现 |
| ② 启动链全景（ROM→SPL→TF-A→U-Boot→内核+DTB） | 启动链 | 最能体现 Linux 与 MCU 心智差异的主干，用 QEMU 演示 |
| ③ 设备树入门（DTS/compatible/reg/interrupts，QEMU 加节点） | 设备树 | Linux 硬件描述核心，与 MCU 寄存器直写形成对照 |
| ④ 用户态硬件访问（libgpiod 点灯 / i2c-dev 读传感器） | 内核/驱动 | 与 MCU 线"点亮 LED"呼应，跑通最常见硬件交互 |

> Linux 线以静态代码/命令日志/流程图为主，QEMU 仅本地运行（无法网页内嵌，外链），与 MCU 线可外链 Wokwi 的形态不同。

**P4-2 · 自审 → 用户核实 → 批次扩展**：两条线各自按 7.2 批次扩展（MCU 5 批；Linux 按 9 模块展开 40–60 章），每批独立验收、截图、过门禁；门户 `apps/portal` 等两个以上专项稳定后再议。

---

## 8. 风险与待决策点

### 8.1 风险

- **范围膨胀**：MCU + RTOS + 嵌入式 Linux 全做，规模可能超过硬件手册；需先收敛主线，Linux 另议。
- **与硬件手册重叠**：若处理不好会重复维护 5.x 内容；用边界矩阵 + 交叉引用严格约束。
- **平台绑定**：代码示例若只写 STM32，会削弱通用性；过度通用又会抽象难懂。
- **组件/工具提前引入**：Mermaid、内联仿真、寄存器组件若过早做会增加维护面；应先纯内容跑通再按需立项。

### 8.2 决策结果（2026-10-21 已拍板：1A 2A 3A 4A 5A 6A 7B）

> 已决策：Q1=A、Q2=A、Q3=A、Q4=A、Q5=A、Q6=A、Q7=B（详见文首第 0 节）。下列选项原样保留供追溯；与推荐不同的是 Q3（选 A 多平台对照）与 Q7（选 B 并行）。

**Q1 范围是否包含嵌入式 Linux？**
- A（推荐）：本期**另立规划**——MCU 软件手册先做完整，嵌入式 Linux 作为后续第三个 app（知识规模与受众差异大，混在一册心智负担重）。
- B：同册包含，Linux 作为最后一篇/大附录。
- C：暂不做 Linux，只专注 MCU/RTOS。

**Q2 与硬件手册 5.x 重叠内容的策略？**
- A（推荐）：严格"硬件原理交叉引用、软件实现重点写"，不重复硬件内容（靠边界矩阵约束）。
- B：重叠处软件手册也完整重述，方便单册阅读（代价是重复维护）。

**Q3 代码示例的芯片平台？**
- A：多平台对照（通用 Cortex-M 概念 + STM32 为主例，ESP32/通用在关键差异处补）。
- B（推荐）：以 **STM32（Cortex-M，如 F1/F4）为主线**，概念层用通用 Cortex-M 与 CMSIS，关键章节附 ESP32/通用说明（STM32 最通用、资料全、HAL/LL/寄存器三方式都典型；中文读者熟悉）。
- C：完全平台无关（只讲 Cortex-M/CMSIS，不绑具体厂商）。
- D：以 ESP32 为主线。

**Q4 是否一开始就做离线单文件？**
- A（推荐）：是，延续双形态与"离线零依赖"，每个 app 各出一个离线 HTML（`dist/embedded.html`），用 manifest 对账。
- B：先只做在线站，离线后期再补。

**Q5 是否引入 Mermaid / 代码可运行 / 内联仿真？**
- A（推荐）：**只引入 Mermaid**（时序/状态机/流程图，成熟、构建期渲染、不增加运行时负担）；代码可运行/仿真暂以外链 Wokwi/Renode/Compiler Explorer，不内嵌。
- B：Mermaid + 内嵌 Wokwi/Renode 仿真（能力强但维护与安全面更大）。
- C：都不引入，时序图/状态机用 ECharts + 内联 SVG（与硬件手册完全一致，但制作成本高）。

**Q6 语言、命名、许可证、品牌是否沿用？**
- A（推荐）：全部沿用——简体中文、kebab-case 路径、文档 CC BY-SA 4.0 + 代码 MIT、与硬件手册同品牌（软件手册可配次级标识）；appId=`embedded`、base `/hardware-handbook/embedded/`。
- B：需要调整（请说明）。

**Q7（若 Q1 选 A）嵌入式 Linux 何时启动？**
- A（推荐）：MCU 手册主体完成、门户与多 app 验证稳定后再立项。
- B：MCU 手册与 Linux 手册并行推进（派独立子线）。

---

## 9. 参考链接附录

以下为本文涉及的真实 URL（去重，分组）。访问/活跃度以 2026-10-14 核实为准。

**官方/标准**
- ARM Developer（Cortex-M 手册/TRM）：https://developer.arm.com/
- ARM 社区 Cortex-M 资源：https://community.arm.com/
- CMSIS：https://github.com/ARM-software/CMSIS
- FreeRTOS 文档：https://www.freertos.org/Documentation ；RTOS 书：https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book
- RT-Thread 文档：https://www.rt-thread.org/document/site/
- Zephyr 文档：https://docs.zephyrproject.org/
- MISRA：https://misra.org/
- Linux Kernel 文档：https://docs.kernel.org/
- TF-A：https://trustedfirmware-a.readthedocs.org/
- U-Boot 文档：https://docs.u-boot.org/
- Buildroot：https://buildroot.org/ ；手册：https://buildroot.org/downloads/manual/manual.html
- Yocto 文档：https://docs.yoctoproject.org/mega-manual/
- Bootlin 资料：https://bootlin.com/docs/ （Buildroot slides：https://bootlin.com/doc/training/buildroot/buildroot-slides.pdf）
- BusyBox：https://www.busybox.net/ ；RAUC：https://rauc.io/
- Barr Group（Embedded C Coding Standard）：https://barrgroup.com/

**GitHub 项目**
- FreeRTOS：https://github.com/FreeRTOS/FreeRTOS
- Zephyr：https://github.com/zephyrproject-rtos/zephyr
- RT-Thread：https://github.com/RT-Thread/rt-thread
- ESP-IDF：https://github.com/espressif/esp-idf
- arduino-esp32：https://github.com/espressif/arduino-esp32
- Compiler Explorer：https://github.com/compiler-explorer/compiler-explorer
- Renode：https://github.com/renode/renode
- Wokwi 生态：https://github.com/wokwi
- Awesome-Embedded：https://github.com/nhivp/Awesome-Embedded
- Awesome C：https://github.com/inputsh/awesome-c
- awesome-embedded-software：https://github.com/iDoka/awesome-embedded-software

**在线工具**
- Compiler Explorer：https://godbolt.org/
- Wokwi：https://wokwi.com/ ；文档：https://docs.wokwi.com/
- Renode 文档：https://renode.readthedocs.io/
- ESP-IDF 文档：https://docs.espressif.com/projects/esp-idf/

**书籍（电子版/出版页）**
- Mastering STM32（Leanpub）：https://leanpub.com/mastering-stm32-2nd
- Mastering the FreeRTOS Real Time Kernel（官方 PDF，见上 FreeRTOS 链接）

**白皮书**
- Cortex-A vs Cortex-M：https://www.arm.com/-/media/Files/pdf/white-paper/optimizing-arm-cortex-a-and-cortex-m-whitepaper.pdf
- ARMv8-A 概述：https://armkeil.blob.core.windows.net/developer/Files/pdf/graphics-and-multimedia/ARMv8_Overview.pdf
