---
id: quiz-mcu
title: 单片机与嵌入式硬件测试题
part: 9
chapter: 硬件测试与面试题库
order: 25
tags: [题库, 自测, 单片机, 嵌入式]
difficulty: 2
status: published
sources:
  - STM32 Reference Manual (RM0008 / RM0383)
  - NXP / Microchip 微控制器应用笔记
  - Jan Axelson, Serial Port / USB Complete
  - STMicroelectronics, RM0008 STM32F10xxx Reference Manual, 2010 — RCC/GPIO/ADC/TIM/USART/I2C/IWDG/WWDG/PWR chapters
  - ARM, DDI 0337 Cortex-M3 Technical Reference Manual — NVIC, bus interfaces and memory model
  - NXP, UM10204 I2C-bus Specification and User Manual, Rev. 6, 2014 — pull-up window, timing and bus clear
  - TIA-232-F / ITU-T V.28 — RS-232 electrical characteristics and single-ended ground reference
  - TIA-485-A — RS-485 differential thresholds, common-mode range and 120Ω termination
  - Texas Instruments, SLVA689 I2C Bus Pullup Resistor Calculation, 2015 — R_min/R_max and 0.8473RC
  - Intel, MCS-51 Family User's Manual — separate program/data address spaces (Harvard)
---

# 单片机与嵌入式硬件测试题

本题库覆盖 MCU 架构、最小系统、GPIO 驱动、中断、ADC/DAC、定时器与 PWM、UART/RS-232、RS-485/CAN、I²C/SPI、USB/以太网物理层、看门狗/RTC/低功耗、外设设计。题型分为「概念判断」「填空」「计算」「简答与情景」四组。数字题按「公式 → 代入 → 结果 → 单位」给全，概念题给判据而不是“一般如此”。

## 一、概念判断

<details><summary>判断：MCU 的最小系统只需要芯片本身，外部晶振、复位电路和电源去耦都可以省掉。</summary>

**错误。**按本手册口径，最小系统要同时做对六件事：电源、复位、时钟、启动配置、调试口、去耦。供电与去耦必须有；时钟可用内部 RC，不强制外部晶振；复位可用内部 POR/PDR/BOR，但要在原理图上明确复位来源并预留 NRST 测试点；BOOT/启动配置脚必须有确定电平；SWD/JTAG 是烧录调试口，不是运行必需，但开发和量产都离不开，最小系统板必须留。把“外部晶振、外部复位”说成绝对必需不准确，但把它们和去耦一起省掉一定不成立。详见[最小系统](../mcu/minimum-system.md)。

</details>

<details><summary>判断：GPIO 设为推挽输出可以可靠地输出高/低电平；设为开漏输出时必须外接上拉电阻才能输出高电平。</summary>

**正确。**推挽（Push-Pull）由上下两个 MOS 驱动，主动输出 0/1，拉电流与灌电流都由芯片提供。开漏（Open-Drain）只能主动拉低，高电平靠外部上拉电阻，常用于 I²C 总线、电平转换、多线与。内部弱上拉通常只有几十 kΩ、只适合低速小电流，不能替代外部上拉；开漏输出低电平时要核对灌电流额定值。

</details>

<details><summary>判断：高抢占优先级中断可以打断低抢占优先级中断（中断嵌套）；同级中断不能互相抢占，低优先级不能打断高优先级。</summary>

**正确，但“子优先级”的说法要纠正。**Cortex-M 的 NVIC 用**抢占优先级**决定嵌套：高抢占优先级可打断低抢占优先级；抢占优先级相同的中断不能互相嵌套。**子优先级只在多个同抢占优先级中断同时挂起时决定谁先执行，不产生嵌套。**Cortex-M 的优先级数值越小，优先级越高。设计上高优先级 ISR 要短，避免阻塞低优先级任务。详见[中断机制（硬件视角）](../mcu/interrupts.md)。

</details>

<details><summary>判断：ADC 的分辨率是 12 位、参考电压 3.3V，则 1LSB 对应的电压约为 0.8mV。</summary>

**正确。**$1\text{LSB}=V_{ref}/2^n=3.3/4096\approx 0.8057\text{mV}$。量化误差在四舍五入（round）时是 $\pm\frac{1}{2}\text{LSB}\approx\pm0.403\text{mV}$；如果输出直接截断（floor），误差是 $0\sim-1\text{LSB}$。满量程输入是 $3.3\times4095/4096=3.2992\text{V}$，不是 3.3V。详见[ADC 原理、参数与参考电压](../mcu/adc.md)。

</details>

<details><summary>判断：PWM 的频率由定时器溢出决定，占空比由比较寄存器与自动重装值的比值决定。</summary>

**正确，但比值要写对。**向上计数时，周期是 $(ARR+1)$ 个计数时钟，所以 $f_{PWM}=f_{clk}/[(PSC+1)(ARR+1)]$，占空比 $D=CCR/(ARR+1)$（$0\le CCR\le ARR$）。写成 $CCR/ARR$ 会在小 ARR 时产生明显误差；$CCR>ARR$ 时部分定时器输出常高（100%）。中心对齐模式的频率是 $f_{clk}/[2(PSC+1)ARR]$，同样频率下分辨率约少 1 位。详见[定时器与 PWM](../mcu/timer-pwm.md)。

</details>

<details><summary>判断：I²C 是开漏、双线、多主总线，靠设备地址寻址；SPI 是四线、通常单主多从，靠片选寻址。</summary>

**正确。**I²C：SCL/SDA 两线、开漏上拉、7/10 位地址、半双工，带时钟同步、仲裁和时钟延展。SPI：MOSI/MISO/SCLK/CS 四线、推挽、全双工、速率高，无内置地址/ACK 协议，靠片选；还有 CPOL/CPHA 四种模式。I²C 的“多主”靠线与仲裁，SPI 通常只有一个主。详见[I²C 与 SPI 总线时序](../mcu/i2c-spi.md)。

</details>

<details><summary>判断：RS-485 用差分信号传输，抗共模干扰强、可远距离（数百米）和多节点组网；RS-232 单端、距离短（约 15m）、点对点。</summary>

**正确，但数值要按标准说。**RS-485 是差分：接收器门限 $\pm200\text{mV}$，驱动器带 54Ω 负载差分输出 $\ge1.5\text{V}$，共模范围 $-7\sim+12\text{V}$，标准拓扑是菊花链、只在最远两端各并 120Ω，多点半双工。RS-232 是**单端、以信号地为参考**：逻辑 1 为 $-3\sim-15\text{V}$、逻辑 0 为 $+3\sim+15\text{V}$（驱动器常见 $\pm5\sim\pm12\text{V}$），接收器门限 $\pm3\text{V}$，电缆电容上限 2500pF；标准数据率 20kbps，“15m”是 100pF/m、19200bps 下的经验值，不是标准硬指标。地电位差会一比一叠加到 RS-232 信号上，共模不会被抵消；“几十伏共模”是 RS-485/CAN 的能力。详见[UART 与 RS-232 物理层](../mcu/uart-rs232.md)和[RS-485 与 CAN 总线硬件](../mcu/rs485-can.md)。

</details>

<details><summary>判断：看门狗（Watchdog）必须由软件定期“喂狗”，否则溢出后复位 MCU，用于防止程序跑飞。</summary>

**正确，但要区分普通看门狗与窗口看门狗。**普通 IWDG 只要在溢出前喂都行；窗口 WWDG 必须落在 $T_{window,low}<T_{feed}<T_{window,high}$，喂得太早（说明程序跑得异常快、可能跳过任务）也会复位。完整约束是 $T_{task,max}<T_{feed}<t_{out,min}$：喂狗周期要大于最坏任务时间，又要小于最小超时；且喂狗要放主循环并检查任务标志，不能只放在定时器中断里。片内 IWDG 用 LSI，LSI 本身有 ±10% 量级误差；安全关键场合用外部看门狗芯片，其时基独立于 MCU。详见[看门狗、RTC 与低功耗硬件](../mcu/watchdog-rtc-lowpower.md)。

</details>

<details><summary>判断：经典 8051 和 ARM Cortex-M 都是冯·诺依曼结构，指令与数据共用一套地址空间。</summary>

**错误。**经典 8051 的程序存储器（Code）与数据存储器（Data）是两个独立地址空间：MOVC 访问程序区，MOVX 访问外部数据区，内部 RAM 与 SFR 另有一套编址，因此存储器层面是**哈佛结构**；它的外部总线把地址/数据复用在同一组 P0/P2 引脚上，看起来像一套总线，但“引脚复用”不等于“地址空间统一”。Cortex-M 是**改进哈佛**：统一 4GB 地址空间，但取指与取数走不同的 I-Code/D-Code/System 总线。判据是“地址空间是否分开、总线是否分开”，不是芯片引脚数。详见[MCU 概述](../mcu/mcu-overview.md)。

</details>

## 二、填空

<details><summary>GPIO 常见工作模式：输入 ____ / ____ / ____；输出 ____ / ____。</summary>

输入：浮空、上拉、下拉；输出：推挽、开漏。实际还有复用推挽/复用开漏（AF）与模拟模式；接 ADC 的引脚要配成模拟输入并关闭数字输入缓冲，以降低漏电和噪声。

</details>

<details><summary>ADC 采样前必须保证 ____ 建立时间；采样速率受 ____ 与 ____ 限制。多通道扫描时需注意 ____。</summary>

采样保持电容 $C_{sh}$ 的建立时间；采样速率受 ADC 时钟/转换时间与源阻抗（建立时间）限制。多通道扫描时要注意通道间串扰与上一次采样的电荷残留，必要时加长采样时间或丢弃第一次转换（dummy conversion）。

按 0.5 LSB 建立判据：

$$
t_{acq}\ge(N+1)\ln2\cdot(R_s+R_{on})C_{sh}
$$

其中 $N$ 是位数，$R_s$ 是源阻抗（$\Omega$），$R_{on}$ 是采样开关导通电阻（$\Omega$），$C_{sh}$ 是采样电容（F）。12 位时 $(N+1)\ln2=9.01$；源阻抗上限 $R_{s,max}=t_{acq}/[(N+1)\ln2\,C_{sh}]-R_{on}$。详见[ADC 原理、参数与参考电压](../mcu/adc.md)。

</details>

<details><summary>UART 四要素：____、____、____、____ 必须收发双方一致。</summary>

波特率（Baud Rate）、数据位（5~9）、停止位（1/1.5/2）、校验位（无/奇/偶）。另外还要一致：空闲电平（TTL 空闲高）、位序（LSB first）、逻辑电平标准（TTL 还是 RS-232）。缺一个就乱码；波特率误差要按两端累计、逐位漂移算。

</details>

<details><summary>低功耗模式按功耗由高到低：运行 → ____ → ____ → 停机/待机；唤醒源通常为 ____、____、RTC。</summary>

运行 → 睡眠（Sleep，CPU 停、外设跑）→ 停止（Stop，时钟停、RAM 和寄存器保持）→ 待机（Standby，1.8V 域断电、RAM 丢失）。唤醒源按型号不同：外部中断（EXTI）、RTC/闹钟、独立看门狗、WKUP 引脚、NRST 复位等；Stop 下可用 EXTI/RTC，Standby 下 RAM 不保持，唤醒后相当于重新上电。

</details>

<details><summary>RTC（实时时钟）靠 ____ 供电走时；后备电池 VBAT 在主电源掉电后维持 ____。</summary>

32.768kHz 晶振（LSE）经 $2^{15}=32768$ 分频得 1Hz。VBAT 维持 RTC 走时与后备寄存器内容；它不维持主 RAM、也不维持主电源域。部分 MCU 的 RTC 也可选 LSI/HSE，但精度和功耗不同。

</details>

## 三、计算

<details><summary>12 位 ADC，$V_{ref}=3.3\text{V}$，采样得到数字量 $D=2048$。求输入电压；若输入 1.65V，理论数字量是多少？</summary>

$$
V_{in}=D\frac{V_{ref}}{2^{12}}=2048\times\frac{3.3}{4096}=1.65\text{V}
$$

$$
D=\operatorname{round}\left(\frac{1.65}{3.3}\times4096\right)=2048
$$

正好是半量程。注意这是理想值，实际有 $\pm\frac{1}{2}\text{LSB}$ 量化误差、INL/DNL、参考源误差与噪声；满量程码是 4095，对应 3.2992V。

</details>

<details><summary>PWM：定时器时钟 72MHz，预分频 PSC=71（分频后 1MHz），自动重装 ARR=999。求 PWM 频率与占空比 50% 时的 CCR 值。</summary>

$$
f_{cnt}=\frac{72\text{MHz}}{71+1}=1\text{MHz}
$$

$$
f_{PWM}=\frac{f_{cnt}}{ARR+1}=\frac{1\text{MHz}}{999+1}=1\text{kHz}
$$

占空比 50%：

$$
CCR=D(ARR+1)=0.5\times1000=500
$$

向上计数模式下 $D=CCR/(ARR+1)=500/1000=50\%$。若误用 $CCR/ARR$，会算成 500/999=50.05%，小 ARR 时误差更大。

</details>

<details><summary>UART 波特率 9600，传输 1 字节（含起始位、8 数据位、1 停止位，共 10 位）需要多少时间？</summary>

$$
T_b=\frac{1}{9600}=104.17\,\mu\text{s}
$$

$$
T_{frame}=10T_b=\frac{10}{9600}=1.0417\text{ms}
$$

1 秒约传 $9600/10=960$ 字节。115200 时 $T_b=8.681\,\mu\text{s}$，单字节约 $86.81\,\mu\text{s}$。若加校验位（11 位），帧时间按 11 位算。

</details>

<details><summary>STM32 I²C 标准模式 100kHz，传输 1 字节（含 ACK）需要多少时间？若 400kHz 快速模式呢？</summary>

1 个数据字节 = 8 个数据位 + 1 个 ACK = 9 个 SCL 周期：

$$
t_{100}=\frac{9}{100\times10^3}=90\,\mu\text{s}
$$

$$
t_{400}=\frac{9}{400\times10^3}=22.5\,\mu\text{s}
$$

这是“数据字节”本身，不含起始、地址字节和停止。完整 7 位地址写一字节：START + 地址 8 位 + ACK + 数据 8 位 + ACK + STOP = 20 个位时间，100kHz 下约 200µs；10 位地址还要多一个地址字节。

</details>

<details><summary>某 MCU 每路 GPIO 高电平可吸收/输出 8mA。一只 LED 接 3.3V、正向压降 2V、要 5mA。求限流电阻；GPIO 是否够驱动？</summary>

$$
R=\frac{V_{dd}-V_F}{I}=\frac{3.3-2}{0.005}=260\,\Omega
$$

取 E24 标准值 270Ω，实际电流：

$$
I=\frac{3.3-2}{270}=4.81\text{mA}
$$

5mA 小于单脚 8mA 额定，单只 LED 够；但要查数据手册的 $V_{OH}$ 测试条件（8mA 时输出可能已跌到 2.4V 以下）与总灌/拉电流限制（如单端口 ≤25mA、全芯片 ≤100mA），多只 LED 同时亮要核算总量。高亮度 LED 建议用 MOS 管/恒流驱动，不直接吃 GPIO。

</details>

<details><summary>3.3V I²C，400kHz 快速模式，总线电容 $C_b=200\text{pF}$，$V_{OL}=0.4\text{V}$，$I_{OL}=3\text{mA}$，$t_{r,max}=300\text{ns}$。求上拉电阻窗口；4.7kΩ 能不能用？</summary>

下限由灌电流决定：

$$
R_{min}=\frac{V_{DD}-V_{OL}}{I_{OL}}=\frac{3.3-0.4}{3\times10^{-3}}=966.7\,\Omega
$$

上限由上升时间决定：

$$
R_{max}=\frac{t_{r,max}}{0.8473C_b}=\frac{300\times10^{-9}}{0.8473\times200\times10^{-12}}=1770\,\Omega
$$

窗口是 $966.7\,\Omega\le R\le1770\,\Omega$。取 1.5kΩ 验算：

$$
t_r=0.8473\times1500\times200\times10^{-12}=254.2\text{ns}<300\text{ns}
$$

$$
I_{OL}=\frac{3.3-0.4}{1500}=1.93\text{mA}<3\text{mA}
$$

4.7kΩ 时 $t_r=0.8473\times4700\times200\times10^{-12}=796\text{ns}>300\text{ns}$，400kHz 下不能用；它在 100kHz（$t_{r,max}=1000\text{ns}$）下、且总线电容不超过约 250pF 时才勉强可用。上拉不是“4.7k 万能”，要按 $C_b$ 和模式算窗口。详见[I²C 与 SPI 总线时序](../mcu/i2c-spi.md)。

</details>

<details><summary>12 位 ADC，采样电容 $C_{sh}=8\text{pF}$，源阻抗 $R_s=10\text{k}\Omega$，采样开关导通电阻忽略，采样窗口 1.5µs。按 0.5 LSB 建立判据，够不够？若 $R_s=20\text{k}\Omega$ 呢？</summary>

$$
t_{acq}\ge(N+1)\ln2\cdot R_sC_{sh}=13\times0.6931\times10^4\times8\times10^{-12}=7.21\times10^{-7}\text{s}=721\text{ns}
$$

721ns < 1.5µs，够，余量约 2 倍。若 $R_s=20\text{k}\Omega$：

$$
t_{acq}\ge13\times0.6931\times2\times10^4\times8\times10^{-12}=1.442\,\mu\text{s}
$$

只剩 58ns（约 4%）余量，电阻/电容容差、开关电阻、温度都会吃掉它，应按“不够”处理：加大采样时间、降低源阻抗或加缓冲。注意这是 0.5 LSB 判据；若按 1 LSB，系数是 $N\ln2=8.32$，结果偏小 0.693τ，刚好“差一点”。

</details>

<details><summary>看门狗：$f_{LSI}=40\text{kHz}$，PR=4（分频 $4\times2^4=64$），RL=1249，最坏任务时间 300ms。求标称超时、LSI +10% 时的最小超时与喂狗窗口。</summary>

$$
t_{out}=\frac{4\times2^{PR}\times(RL+1)}{f_{LSI}}=\frac{64\times1250}{40000}=2.0\text{s}
$$

LSI 偏快 10%（44kHz）时超时最短：

$$
t_{out,min}=\frac{64\times1250}{44000}=1.818\text{s}
$$

喂狗周期必须满足：

$$
0.3\text{s}<T_{feed}<1.818\text{s}
$$

取 1.0s 合适。若用窗口看门狗，窗口下限取 0.9s，则喂狗必须落在 0.9~1.818s；太早（<0.9s）会被判“跑太快”，太晚（>1.818s）会溢出。注意公式里的 4 倍系数因厂商而异，以数据手册为准。详见[看门狗、RTC 与低功耗硬件](../mcu/watchdog-rtc-lowpower.md)。

</details>

## 四、简答与情景

<details><summary>情景：PCB 上 MCU 偶尔复位，断电重开正常，现场长时间运行后概率上升。怀疑看门狗或电源，如何区分？</summary>

(1) 先测电源：用示波器看掉电瞬间 $V_{dd}$ 是否跌出 BOR/POR 阈值，纹波是否过大；(2) 查复位脚波形，区分看门狗复位、BOR 复位还是外部噪声；(3) 读复位原因寄存器（如 RCC_CSR），看是 IWDG/WWDG/POR/BOR/PIN/SFT/LPWR 哪一类；(4) 检查程序是否在中断/循环里漏喂狗，或喂狗点没覆盖全部任务。对策：加强去耦、按 $T_{task,max}<T_{feed}<t_{out,min}$ 设喂狗、加外部看门狗、把复位源写进日志。

</details>

<details><summary>简答：I²C 总线挂多个设备拉不起来（SDA 一直低），硬件排查顺序？</summary>

(1) 先量 SDA/SCL 静态电平与上拉是否接到正确的 VDD（5V 上拉灌进 3.3V 器件会损坏）；(2) 按 $R_{min}=(V_{DD}-V_{OL})/I_{OL}$、$R_{max}=t_{r,max}/(0.8473C_b)$ 算上拉窗口，4.7kΩ 不是万能；(3) 逐个断开从机，定位谁拉死 SDA，查地址冲突、SDA/SCL 接反、时钟延展；(4) 主机手动发 9 个 SCL 脉冲做 bus clear，释放从机状态；仍不放就断电重启从机；(5) 总线电容过大时降速或加 I²C 缓冲器。详见[I²C 与 SPI 总线时序](../mcu/i2c-spi.md)。

</details>

<details><summary>情景：ADC 采集的温度信号在静止时数值跳动十几 mV。硬件与软件上如何稳定？</summary>

硬件：(1) 信号源阻抗高时加运放缓冲；(2) RC 低通滤波（如 1k + 0.1µF，截止 $f_c=1/(2\pi\times1000\times10^{-7})=1.59\text{kHz}$）；(3) PCB 上模拟地/数字地按返回电流路径处理，避开数字噪声；(4) $V_{ref}$ 加去耦、用独立基准源；(5) 检查探头/电源地环路。

软件：(1) 多次采样取平均/中值滤波；(2) 过采样提高有效位数；(3) 限幅 + 中值/均值组合剔除异常值，不要用“看门狗式”这种没有定义的词；(4) 按 $(N+1)\ln2R_sC_{sh}$ 核对采样窗口够不够。

</details>

<details><summary>简答：为什么 USB、以太网这类高速接口需要严格的阻抗匹配和差分走线，而普通 UART 不需要？</summary>

USB 2.0 全速（FS）只有 12Mbps，通常不需要严格阻抗控制；高速（HS）480Mbps、USB 3.x 5Gbps 以上，以及千兆以太网（1000BASE-T，1Gbps），边沿快、传输线效应明显：阻抗不连续产生反射，串扰导致误码，必须按差分阻抗 90Ω（USB 2.0）/100Ω（以太网）控制走线，并保证参考平面连续。UART 常见几十 kbps~几 Mbps、边沿慢、线短，反射与串扰可忽略，普通走线即可；长线/高速 UART 应改用 RS-422/RS-485 差分。详见[USB 与以太网物理层概览](../mcu/usb-ethernet.md)。

</details>
