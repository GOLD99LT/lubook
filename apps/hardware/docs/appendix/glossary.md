---
id: glossary
title: 术语中英对照表
part: 10
chapter: 附录
order: 5
tags: [术语, 词汇表, 中英对照, 速查]
difficulty: 1
status: published
sources:
  - IEC 60050 International Electrotechnical Vocabulary
  - IEEE Std 100 The Authoritative Dictionary of IEEE Standards Terms
  - IPC-7351B Surface Mount Design and Land Pattern Standard
  - Sedra and Smith, Microelectronic Circuits, 8th ed. — feedback and stability chapters
  - Sergio Franco, Design with Operational Amplifiers and Analog Integrated Circuits, 4th ed.
  - JEDEC JESD88 Dictionary of Terms for Solid-State Technology
  - https://github.com/kitspace/awesome-electronics
---

# 附录 A · 术语中英对照表 Glossary

本表汇总全书常用硬件术语的中英对照与一句话简释，按主题分组。正文中首次出现的术语均给出中英对照，此处统一备查。英文缩写按行业惯例保留大写。**易混术语（建立时间/保持时间、环路增益/闭环增益、噪声增益/信号增益）单独加了辨析**，查表时先看简释里的限定条件。

## A.1 电路基础 Fundamentals

| 中文术语 | English | 简释 |
|---|---|---|
| 电压 | Voltage | 两点间单位电荷的势能差，单位伏特（V） |
| 电流 | Current | 单位时间流过截面的电荷量，单位安培（A） |
| 电阻 | Resistance | 导体对电流的阻碍作用，单位欧姆（Ω） |
| 电导 | Conductance | 电阻的倒数，单位西门子（S） |
| 功率 | Power | 单位时间做功，单位瓦特（W） |
| 能量 | Energy | 功率对时间的积分，单位焦耳（J） |
| 电动势 | Electromotive Force (EMF) | 非静电力把其他形式能量转化为电能的能力，单位 V；开路时等于端电压 |
| 电位 / 电势 | Electric Potential | 单位电荷在电场中的势能 |
| 电位差 | Potential Difference | 两点电势之差，即电压 |
| 直流 | Direct Current (DC) | 方向不随时间变化的电流/电压 |
| 交流 | Alternating Current (AC) | 大小方向随时间周期变化的电流/电压 |
| 频率 | Frequency | 单位时间周期数，单位赫兹（Hz） |
| 周期 | Period | 完成一次完整变化所需时间，单位秒（s） |
| 相位 | Phase | 周期信号在时间轴上的相对位置，单位度或弧度 |
| 有效值 | Root Mean Square (RMS) | 与交流量产生相同热效应的直流值；正弦波 $V_{rms}=V_{pk}/\sqrt{2}$ |
| 峰值 | Peak Value | 信号偏离零点的最大幅值 |
| 峰峰值 | Peak-to-Peak ($V_{pp}$) | 波峰到波谷的总摆幅 |
| 阻抗 | Impedance | 交流电路中电阻与电抗的复数组合，单位欧姆 |
| 电抗 | Reactance | 电感/电容对交流的阻碍，单位欧姆 |
| 导纳 | Admittance | 阻抗的倒数，单位西门子 |
| 谐振 | Resonance | 感抗与容抗相等、电路呈纯阻性的状态；串联谐振阻抗最小，并联谐振阻抗最大 |
| 品质因数 | Quality Factor (Q) | 谐振电路储能与每周期耗能之比，$Q=f_0/BW$；Q 越高选择性越好、振铃越久 |
| 时间常数 | Time Constant ($\tau$) | RC/RL 电路充电到终值 63.2%（放电降到 36.8%）所需时间，$\tau=RC$ 或 $L/R$ |
| 趋肤效应 | Skin Effect | 高频电流集中在导体表面，有效截面减小、电阻增大；铜在 1 MHz 的趋肤深度约 66 µm |
| 欧姆定律 | Ohm's Law | $V=IR$ 的线性伏安关系 |
| 基尔霍夫电流定律 | Kirchhoff's Current Law (KCL) | 节点流入电流之和等于流出之和 |
| 基尔霍夫电压定律 | Kirchhoff's Voltage Law (KVL) | 闭合回路电压代数和为零 |
| 分贝 | Decibel (dB) | 对数比值单位，$20\log_{10}(V_2/V_1)$ 或 $10\log_{10}(P_2/P_1)$；dBm 是绝对功率，不是比值 |
| 热噪声 | Thermal Noise | 电阻载流子热运动产生的白噪声，$e_n=\sqrt{4kTR}$，只与温度和阻值有关 |

## A.2 元器件 Components

| 中文术语 | English | 简释 |
|---|---|---|
| 贴片电阻 | Chip Resistor / SMD Resistor | 表面贴装片式电阻，常见 0402/0603/0805 |
| 直插电阻 | Through-hole Resistor | 引脚穿孔焊接的电阻，常见碳膜/金属膜 |
| 精度 / 公差 | Tolerance | 实际阻值与标称值的允许偏差，如 ±1% |
| 额定功率 | Power Rating | 电阻长期工作不损坏的最大功率 |
| 温漂 | Temperature Coefficient (TCR) | 阻值随温度变化率，单位 ppm/°C |
| 多层陶瓷电容 | Multi-Layer Ceramic Capacitor (MLCC) | 叠层陶瓷介质贴片电容，容量大体积小 |
| 电解电容 | Electrolytic Capacitor | 氧化铝介质电容，容量大但有极性 |
| 钽电容 | Tantalum Capacitor | 钽介质有极性电容，体积小但过压/反接易失效 |
| 等效串联电阻 | Equivalent Series Resistance (ESR) | 电容/电感的寄生串联电阻 |
| 等效串联电感 | Equivalent Series Inductance (ESL) | 电容引脚与电极的寄生电感 |
| 电感 | Inductor | 储存磁场能量的元件，单位亨利（H） |
| 磁珠 | Ferrite Bead | 高频耗能型阻抗元件，用于抑制噪声 |
| 二极管 | Diode | 单向导电器件，正向导通反向截止 |
| 肖特基二极管 | Schottky Diode | 低正向压降、快恢复的二极管 |
| 稳压二极管 | Zener Diode | 工作在反向击穿区提供稳定电压 |
| 发光二极管 | Light Emitting Diode (LED) | 电致发光的二极管 |
| 瞬态抑制二极管 | Transient Voltage Suppressor (TVS) | 吸收瞬态过压保护后级电路 |
| 压敏电阻 | Metal Oxide Varistor (MOV) | 过压时非线性导通吸收浪涌，常用于市电入口；会老化 |
| 自恢复保险丝 | Polymeric PTC Resettable Fuse | 过流发热使电阻骤增限流，故障消失后恢复；动作较慢 |
| 双极型晶体管 | Bipolar Junction Transistor (BJT) | 电流控制电流的三端器件 |
| 金属氧化物半导体场效应管 | MOS Field-Effect Transistor (MOSFET) | 电压控制电流的三端器件 |
| 绝缘栅双极型晶体管 | Insulated Gate Bipolar Transistor (IGBT) | 高功率电压控制器件 |
| 晶闸管 | Silicon Controlled Rectifier (SCR) | 可控整流的闸流器件 |
| 继电器 | Relay | 用小电流控制大电流通断的机电开关 |
| 光耦 | Optocoupler / Optoisolator | 用光实现电气隔离的输入输出器件 |
| 晶体谐振器 | Crystal Resonator | 无源石英晶体，需外部振荡电路，用压电效应稳频 |
| 晶体振荡器 | Crystal Oscillator | 有源时钟源，内部含振荡电路，直接输出方波 |
| 保险丝 | Fuse | 过流时熔断保护电路的器件 |
| 连接器 | Connector | 实现电路可拆卸连接的元件 |

## A.3 模拟电路与运放 Analog & Op-Amp

| 中文术语 | English | 简释 |
|---|---|---|
| 运算放大器 | Operational Amplifier (Op-Amp) | 高增益差分输入直接耦合放大器 |
| 开环增益 | Open-loop Gain ($A_{OL}$) | 无反馈时运放的固有电压增益，随频率下降 |
| 闭环增益 | Closed-loop Gain | 接入反馈后电路的实际增益，由外部元件决定 |
| 环路增益 | Loop Gain ($T$) | $T=A_{OL}\cdot\beta$，$\beta$ 为反馈系数；$\lvert T\rvert=1$ 的频率为交越频率 |
| 噪声增益 | Noise Gain | 运放输入端看到的增益，同相与反相拓扑都等于 $1+R_f/R_1$（反相时信号增益为 $-R_f/R_1$）；决定噪声/失调放大与稳定性，不等于信号增益 |
| 虚短 | Virtual Short | 负反馈且未饱和时两输入端电压近似相等 |
| 虚断 | Virtual Open | 理想运放输入端不取电流 |
| 负反馈 | Negative Feedback | 输出回授反相输入以稳定工作点 |
| 正反馈 | Positive Feedback | 输出回授同相输入，用于振荡/比较器 |
| 共模抑制比 | Common-Mode Rejection Ratio (CMRR) | 差模增益与共模增益之比，单位 dB，抑制两输入端共同信号的能力 |
| 电源抑制比 | Power Supply Rejection Ratio (PSRR) | 电源变化到输出的增益倒数，单位 dB，抑制电源纹波的能力 |
| 失调电压 | Input Offset Voltage ($V_{OS}$) | 使输出为零时需在输入端加的差分补偿电压 |
| 失调电压温漂 | $V_{OS}$ Drift | 失调电压随温度的变化率，单位 µV/°C |
| 偏置电流 | Input Bias Current ($I_B$) | 运放输入端的直流偏置电流 |
| 失调电流 | Input Offset Current ($I_{OS}$) | 两输入端偏置电流之差 |
| 增益带宽积 | Gain-Bandwidth Product (GBP/GBW) | 开环增益与频率的乘积，运放常数；闭环带宽约 GBP/G |
| 压摆率 | Slew Rate (SR) | 输出电压最大变化速率，单位 V/µs；全功率带宽 $f_{FPBW}=SR/(2\pi V_{pk})$ |
| 全功率带宽 | Full-Power Bandwidth (FPBW) | 压摆率限制下不失真输出最大正弦频率 |
| 建立时间 | Settling Time | 输出进入并保持在终值误差带（如 ±0.1%）内所需时间，含压摆、振铃与热拖尾 |
| 上升时间 | Rise Time ($t_r$) | 阶跃响应 10%→90% 的时间；一阶系统 $t_r\approx0.35/BW$ |
| 轨到轨 | Rail-to-Rail | 输入共模范围或输出摆幅可达电源轨（仍受负载电流限制） |
| 共模输入范围 | Input Common-Mode Range | 输入差放级正常工作的输入电压范围 |
| 单位增益稳定 | Unity-Gain Stable | 噪声增益 ≥1 时相位裕度足够、不自激；非单位增益稳定运放要求最小噪声增益 |
| 比较器 | Comparator | 开环工作比较两电压大小的器件 |
| 施密特触发器 | Schmitt Trigger | 带迟滞的比较器，抗噪声 |
| 迟滞 | Hysteresis | 上门限与下门限之差，宽度由正反馈强度决定 |
| 仪表放大器 | Instrumentation Amplifier (In-Amp) | 高 CMRR 三运放差分放大器，增益 $1+2R/R_g$ |
| 差分放大器 | Differential Amplifier | 放大两电压之差的电路 |
| 有源滤波器 | Active Filter | 含运放的 RC 滤波器 |
| 巴特沃斯响应 | Butterworth Response | 通带最平坦的滤波器幅频特性 |
| 切比雪夫响应 | Chebyshev Response | 通带等波纹的滤波器响应 |
| 相位裕度 | Phase Margin (PM) | $\text{PM}=180^{\circ}+\angle T(j\omega_c)$，$\omega_c$ 为 $\lvert T\rvert=1$ 的频率；PM>0 稳定，工程目标 45°–60° |
| 伯德图 | Bode Plot | 幅频/相频随频率变化的图 |
| 噪声密度 | Noise Spectral Density | 单位带宽内的噪声，nV/√Hz |
| 基准电压源 | Voltage Reference | 高精度低漂移的电压基准 |
| 整流 | Rectification | 把交流变成单向脉动直流 |
| 滤波 | Filtering | 滤除纹波保留直流成分 |
| 稳压 | Regulation | 保持输出电压恒定 |

## A.4 数字电路与逻辑 Digital

| 中文术语 | English | 简释 |
|---|---|---|
| 逻辑门 | Logic Gate | 实现布尔运算的基本单元 |
| 真值表 | Truth Table | 列出所有输入组合对应输出的表 |
| 布尔代数 | Boolean Algebra | 逻辑运算的代数系统 |
| 卡诺图 | Karnaugh Map | 化简逻辑函数的图形方法 |
| 组合逻辑 | Combinational Logic | 输出仅取决于当前输入的电路 |
| 时序逻辑 | Sequential Logic | 输出取决于输入与历史状态的电路 |
| 触发器 | Flip-Flop | 存储 1 位二进制的同步时序单元 |
| 锁存器 | Latch | 电平敏感的存储单元 |
| 寄存器 | Register | 一组触发器并行存储多位数据 |
| 计数器 | Counter | 对脉冲计数的时序电路 |
| 建立时间 | Setup Time ($t_{su}$) | 数据在时钟有效沿**之前**须稳定的最小时间（与模拟的 settling time 不是一回事） |
| 保持时间 | Hold Time ($t_h$) | 数据在时钟有效沿**之后**须保持稳定的最小时间 |
| 亚稳态 | Metastability | 触发器在时钟沿采样到临界电平时输出长时间停在 0/1 之间；用两级同步器降低概率 |
| 同步器 | Synchronizer | 两级触发器串联消除异步输入亚稳态 |
| 三态门 | Tri-state Gate | 输出有高/低/高阻三种状态 |
| 上拉电阻 | Pull-up Resistor | 把信号线拉至高电平的电阻 |
| 下拉电阻 | Pull-down Resistor | 把信号线拉至低电平的电阻 |
| 开漏输出 | Open-drain Output | 输出只有下拉管、需外部上拉 |
| TTL 电平 | Transistor-Transistor Logic | 5 V 供电的经典逻辑电平，$V_{IH}\ge2.0$ V、$V_{IL}\le0.8$ V |
| CMOS 电平 | CMOS Logic Level | 按电源轨比例的逻辑电平，典型 $V_{IH}\ge0.7V_{DD}$、$V_{IL}\le0.3V_{DD}$ |
| LVDS | Low-Voltage Differential Signaling | 低电压差分信号标准，差分约 350 mV、共模约 1.2 V，用于高速点对点/背板 |
| 扇出 | Fan-out | 一个输出能可靠驱动的同类输入个数 |
| 传播延迟 | Propagation Delay ($t_{pd}$) | 输入变化到输出变化的时间 |
| 存储器 | Memory | 存储数字数据的器件 |
| 静态随机存储器 | Static RAM (SRAM) | 双稳态锁存存储，不需刷新 |
| 动态随机存储器 | Dynamic RAM (DRAM) | 电容存储需定期刷新 |
| 闪存 | Flash Memory | 电可擦除非易失性存储器，按块擦除 |
| 电可擦除只读存储器 | EEPROM | 字节级可擦写非易失存储器 |
| 现场可编程门阵列 | Field-Programmable Gate Array (FPGA) | 可编程逻辑阵列器件 |
| 硬件描述语言 | Hardware Description Language (HDL) | Verilog/VHDL 等描述电路的语言 |

## A.5 单片机与嵌入式 MCU & Embedded

| 中文术语 | English | 简释 |
|---|---|---|
| 微控制器 | Microcontroller Unit (MCU) | 集成 CPU/存储器/外设的单芯片计算机 |
| 中央处理器 | Central Processing Unit (CPU) | 执行指令的核心单元 |
| 通用输入输出口 | General Purpose Input/Output (GPIO) | 可配置为输入或输出的引脚 |
| 模数转换器 | Analog-to-Digital Converter (ADC) | 把模拟电压量化为数字量 |
| 数模转换器 | Digital-to-Analog Converter (DAC) | 把数字量转换为模拟电压/电流 |
| 分辨率 | Resolution | ADC/DAC 能区分的最小增量；$n$ 位 ADC 的分辨率为满量程 $/2^n$ |
| 量化误差 | Quantization Error | 量化台阶造成的误差，理想 $n$ 位 ADC 为 $\pm0.5$ LSB |
| 最低有效位 | Least Significant Bit (LSB) | 数字量最低位对应的电压/电流增量 |
| 采样率 | Sampling Rate ($f_s$) | 每秒采样点数；奈奎斯特要求 $f_s>2f_{max}$ |
| 奈奎斯特频率 | Nyquist Frequency | $f_s/2$；输入超过它会产生混叠 |
| 脉冲宽度调制 | Pulse Width Modulation (PWM) | 用占空比调节输出平均电压 |
| 定时器 | Timer | 计数时钟产生定时中断的外设 |
| 中断 | Interrupt | 外设事件打断 CPU 现行流程 |
| 中断服务程序 | Interrupt Service Routine (ISR) | 响应中断执行的函数 |
| 直接存储器访问 | Direct Memory Access (DMA) | 外设与存储器间直接搬数据，不占 CPU |
| 通用异步收发器 | Universal Asynchronous Receiver/Transmitter (UART) | 异步串行通信口 |
| 串行外设接口 | Serial Peripheral Interface (SPI) | 四线全双工同步串行总线 |
| 集成电路总线 | Inter-Integrated Circuit (I²C) | 两线半双工同步串行总线，开漏+上拉 |
| 控制器局域网 | Controller Area Network (CAN) | 汽车/工业差分多主总线 |
| RS-485 | Recommended Standard 485 | 差分多点串行物理层标准，常见两线半双工、可四线全双工；共模 −7~+12 V，终端 120 Ω |
| 以太网 | Ethernet | 局域网组网标准 |
| 通用串行总线 | Universal Serial Bus (USB) | 外设串行总线标准 |
| 看门狗 | Watchdog Timer (WDT) | 程序跑飞时自动复位的定时器 |
| 实时时钟 | Real-Time Clock (RTC) | 走日历时钟的低耗外设 |
| 最小系统 | Minimum System | MCU 能运行的最少电路（电源/时钟/复位） |
| 硬件抽象层 | Hardware Abstraction Layer (HAL) | 封装寄存器操作的中间层 |
| 片上系统 | System on Chip (SoC) | 集成计算与外设的单芯片系统 |
| 固件 | Firmware | 烧录在 MCU 中的底层程序 |
| 引导程序 | Bootloader | 上电先运行的小程序，用于升级固件或跳转到应用 |
| 烧录 / 下载 | Programming / Flashing | 把固件写入芯片存储器 |
| 在线调试 | In-Circuit Debugging | 通过调试器在线单步/断点运行 |

## A.6 电源设计 Power

| 中文术语 | English | 简释 |
|---|---|---|
| 线性稳压器 | Linear Regulator | 用功率管压降稳压，LDO 为低压差型 |
| 低压差稳压器 | Low-Dropout Regulator (LDO) | 输入输出压差可很小的线性稳压器 |
| 压差 | Dropout Voltage | 维持稳压所需最小输入输出压差，随电流/温度变差 |
| 静态电流 | Quiescent Current ($I_q$) | 器件无负载时自身消耗的电流 |
| 开关电源 | Switch-Mode Power Supply (SMPS) | 用开关管储能元件高效变换电压 |
| 降压变换器 | Buck Converter | 输出低于输入的开关拓扑 |
| 升压变换器 | Boost Converter | 输出高于输入的开关拓扑 |
| 升降压变换器 | Buck-Boost Converter | 输出可高于或低于输入的拓扑 |
| 反激变换器 | Flyback Converter | 带变压器隔离的反激拓扑 |
| 占空比 | Duty Cycle | 开关导通时间占周期的比例 |
| 连续导通模式 | Continuous Conduction Mode (CCM) | 电感电流始终大于零 |
| 断续导通模式 | Discontinuous Conduction Mode (DCM) | 电感电流降到零后停顿 |
| 死区时间 | Dead Time | 半桥/全桥上下管都关断的保护间隔，防直通；典型 0.5–2 µs |
| 直通 | Shoot-through | 同一桥臂上下管同时导通，电源经两管短路，可瞬间损坏器件 |
| 续流二极管 | Freewheeling Diode | 电感关断时为电流提供通路，防止电压尖峰 |
| 自举 | Bootstrap | 用二极管+电容把高边驱动电源抬到开关节点之上 |
| 软启动 | Soft Start | 限制上电占空比/电流上升斜率，防输入浪涌 |
| 纹波 | Ripple | 输出电压/电流的周期波动 |
| 效率 | Efficiency | 输出功率与输入功率之比 |
| 线性调整率 | Line Regulation | 输入变化时输出电压的稳定度 |
| 负载调整率 | Load Regulation | 负载变化时输出电压的稳定度 |
| 交越频率 | Crossover Frequency | 环路增益幅值过 0 dB 的频率，决定带宽与动态响应 |
| 电池管理系统 | Battery Management System (BMS) | 监控保护充放电的电路 |
| 充电器 | Charger | 给电池充电管理的 IC |
| 电量计 | Fuel Gauge | 估算电池剩余电量的器件 |
| 去耦电容 | Decoupling Capacitor | 就近提供瞬态电流、滤电源噪声；与旁路电容常混用 |
| 负载开关 | Load Switch | 受控通断一路电源的开关 |
| 电源轨 | Power Rail | 系统中某一电压的供电网络 |
| 地弹 | Ground Bounce | 地线因瞬态电流产生的电压尖峰 |
| 热阻 | Thermal Resistance ($R_{\theta JA}$) | 每瓦功耗引起的温升，单位 °C/W；$R_{\theta JA}$ 随 PCB 铜箔/风速变化，$R_{\theta JC}$ 由封装决定 |
| 降额 | Derating | 让器件在低于额定值下工作以提高可靠性；如 $T_j\le80\%T_{j(max)}$、电阻功率 ≤50%–60% |

## A.7 PCB 设计与 EMC

| 中文术语 | English | 简释 |
|---|---|---|
| 印制电路板 | Printed Circuit Board (PCB) | 承载元件与走线的基板 |
| 层叠 | Stack-up | PCB 各铜层与介质的叠放结构 |
| 介电常数 | Dielectric Constant ($\varepsilon_r$) | 相对介电常数，决定阻抗与信号传播速度 $v=c/\sqrt{\varepsilon_r}$ |
| 布线 | Routing | 在板上绘制连接导线 |
| 过孔 | Via | 层间电气连接孔 |
| 焊盘 | Pad | 元件引脚焊接的铜区 |
| 丝印 | Silkscreen | 板上白色字符标识 |
| 阻焊层 | Solder Mask | 防止焊锡桥接的覆盖层 |
| 表面贴装器件 | Surface-Mount Device (SMD) | 贴装在板面的器件 |
| 寄生参数 | Parasitic Parameter | 走线/焊盘引入的意外 R/L/C |
| 信号完整性 | Signal Integrity (SI) | 信号波形质量不劣化的研究 |
| 阻抗控制 | Impedance Control | 按目标阻抗设计线宽/介质厚度 |
| 反射 | Reflection | 阻抗不连续处信号能量反射 |
| 端接 | Termination | 加匹配电阻消除反射 |
| 串扰 | Crosstalk | 相邻走线间的容性/感性耦合 |
| 差分走线 | Differential Pair | 等长紧耦合的对称走线对 |
| 参考平面 | Reference Plane | 为走线提供回流路径的完整铜层（地或电源） |
| 回流路径 | Return Path | 信号电流返回源头的路径；高频时走最小电感路径，紧贴走线下方 |
| 电磁干扰 | Electromagnetic Interference (EMI) | 对外辐射或传导的噪声 |
| 电磁兼容 | Electromagnetic Compatibility (EMC) | 设备既不干扰别人也不被干扰 |
| 屏蔽 | Shielding | 用导体隔断电场/磁场 |
| 接地 | Grounding | 为信号/电源提供参考电位 |
| 模拟地 | Analog Ground (AGND) | 模拟电路的地 |
| 数字地 | Digital Ground (DGND) | 数字电路的地 |
| DFM | Design for Manufacturing | 可制造性设计 |
| 球栅阵列 | Ball Grid Array (BGA) | 底面焊球阵列的封装 |
| 方形扁平封装 | Quad Flat Package (QFP) | 四面引脚表贴封装 |
| 方形扁平无引脚 | Quad Flat No-leads (QFN) | 底部焊盘无翼形引脚封装 |

## A.8 测量与调试 Measurement & Debug

| 中文术语 | English | 简释 |
|---|---|---|
| 万用表 | Multimeter (DMM) | 测量电压/电流/电阻等的仪表 |
| 示波器 | Oscilloscope | 显示电压随时间波形的仪表 |
| 探头 | Probe | 连接示波器与被测点的前端 |
| 带宽 | Bandwidth | 仪表幅度下降到 0.707 倍的频率 |
| 采样率 | Sampling Rate | 模数转换每秒采样点数；示波器要求 ≥2.5–5 倍信号带宽 |
| 触发 | Trigger | 让波形稳定显示的同步机制 |
| 信号发生器 | Signal Generator | 产生标准波形的仪器 |
| 直流电源 | DC Power Supply | 提供可调直流电压电流的电源 |
| 电子负载 | Electronic Load | 可编程吸收功率的测试负载 |
| 逻辑分析仪 | Logic Analyzer | 采集多通道数字时序的仪器 |
| 频谱分析仪 | Spectrum Analyzer | 显示信号频域分布的仪器 |
| 网络分析仪 | Vector Network Analyzer (VNA) | 测量网络 S 参数的仪器 |
| 校准 | Calibration | 用标准源比对并修正测量误差 |
| 精度 | Accuracy | 测量值与真值的接近程度，含增益、偏移、非线性 |
| 真有效值 | True RMS | 按定义计算 RMS 的测量方式，非正弦波也准确 |
| 开尔文连接 | Kelvin Connection | 四线法，电流与电压引线分开，消除引线电阻 |
| 焊接 | Soldering | 用熔融锡合金连接元件与板 |
| 热风拆焊台 | Hot Air Rework Station | 用热风返修贴片器件的工具 |
| 调试 | Debugging | 定位并修复硬件/软件缺陷 |
| 上电时序 | Power-up Sequence | 各路电源按顺序建立的过程 |
| 故障排查 | Troubleshooting | 系统化定位故障根因 |
| 老化测试 | Burn-in | 高温长时间运行筛选早期失效 |
| 安规认证 | Safety Certification | CE/FCC/UL/CCC 等合规认证 |
| 数据手册 | Datasheet | 厂商提供器件参数与应用的官方文档 |
| 应用笔记 | Application Note (AN) | 厂商推荐的电路设计指南 |
| 物料清单 | Bill of Materials (BOM) | 产品全部元器件清单 |

> 共收录 8 大主题、约 240 条术语。术语缩写首次出现时已在正文中展开全称，可配合索引检索。定义以 IEC 60050/IEEE Std 100 的通用口径为准；厂商 datasheet 若有更具体的限定（如测试条件），以 datasheet 为准。
