---
id: quiz-system
title: 综合系统设计与情景题
part: 9
chapter: 硬件测试与面试题库
order: 45
tags: [题库, 自测, 系统设计, 情景题, 面试]
difficulty: 2
status: published
sources:
  - Horowitz & Hill, The Art of Electronics
  - TI / ADI 系统设计应用笔记
  - 硬件工程师面试公开题库（自编，基于上述权威资料）
  - Horowitz & Hill, The Art of Electronics, 3rd ed. — practical circuit design and worst-case thinking
  - TI, SLVA477A Basic Calculation of a Buck Converter's Power Stage — duty cycle, inductor ripple and output capacitor
  - Analog Devices, AN-149 Modeling and Loop Compensation of SMPS — buck loop and compensation
  - TI, TPS7A02 / TPS7A20 Datasheets — ultra-low Iq LDO, package thermal resistance
  - Energizer, CR2032 Product Datasheet — nominal capacity, internal resistance and pulse capability
  - Vishay, NTCLE100E3 NTC Datasheet — R-T table, B value and dissipation factor
  - Vishay, AN608 Power MOSFET Basics — gate charge and switching loss
  - IEC 62368-1:2018 / GB 4943.1-2022 — safety requirements
  - IPC-2221B — current capacity and electrical clearance
---

# 综合系统设计与情景题

本题库跨电路、元器件、运放、数字、MCU、电源、PCB/EMC、测量调试等全部领域，以系统设计题（从需求→选型→计算→风险）、故障诊断、权衡决策与面试开放题为主。题型分为「系统设计」「故障诊断」「权衡决策」「开放讨论」四组，无标准答案的题目给出推荐思路与关键考点。数字题按「公式 → 代入 → 结果 → 单位」给全。

## 一、系统设计

<details><summary>设计一个 0~5V 电压采集模块：传感器输出 0~5V、内阻 10kΩ，MCU ADC 参考 3.3V、12 位。给出完整设计链路与关键计算。</summary>

**考点：输入量程超 ADC、高阻源、参考与电阻容差、ADC 建立。**

1. **量程匹配**：传感器 0~5V > ADC 3.3V，必须衰减；但不能直接用电阻分压，因为 10kΩ 源阻抗会参与分压，且分压器 Thevenin 阻抗高，ADC 采样电容充不满。
2. **加缓冲**：先接 RRIO 电压跟随器（5V 供电，输入共模含 0V/5V，$I_B$ 为 pA~nA 级），把 10kΩ 源与后级隔离。
3. **分压**：目标 5V→约 3.2V，留 3% 余量。取 $R_1=33\text{k}\Omega$（上）、$R_2=59\text{k}\Omega$（下）：

$$
k=\frac{R_2}{R_1+R_2}=\frac{59}{33+59}=0.6413
$$

$$
V_{out}=5\times0.6413=3.207\text{V}
$$

1% 电阻最坏比值约 0.646，对应 3.23V，仍低于 3.3V。若取 33k/66k，比值 0.667，5V 直接出 3.33V，已经超过 3.3V 基准，**不能用**。

4. **阻抗**：分压器 Thevenin 电阻 $R_1\parallel R_2=21.2\text{k}\Omega$。12 位 ADC、$C_{sh}=8\text{pF}$ 的建立时间：

$$
t_{acq}\ge(N+1)\ln2\,R_{eq}C_{sh}
=9.01\times21.2\times10^3\times8\times10^{-12}
=1.53\,\mu\text{s}
$$

采样窗口小于 1.53µs 时必须加第二级缓冲，或把分压电阻降到 3.3k/5.9k（$R_{eq}=2.12\text{k}\Omega$，$t_{acq}=153\text{ns}$）。推荐第二级缓冲，ADC 前再串 1kΩ + 100nF（$f_c=1.59\text{kHz}$）。

5. **保护**：ADC 前加双肖特基钳位（BAT54 系列或专用 ESD 阵列）到 3.3V/GND，串 1kΩ 限流；5V 过压时钳位电流约 $(5-3.6)/1\text{k}=1.4\text{mA}$。BAT54 漏电在高温可到 µA 级，精密测量要选低漏电或只靠 RC+TVS。
6. **精度**：12 位 $1\text{LSB}=3.3/4096=0.806\text{mV}$；输入折合 $0.806/0.6413=1.26\text{mV}$。1% 电阻的比值误差约 0.7%，对 5V 输入是 36mV（约 28LSB），远大于 1LSB；精密测量要用 0.1% 电阻或软件校准。基准源初始精度、温漂、运放失调也要进误差预算。
7. **风险**：RRIO 运放输出摆幅、5V 供电裕量、ADC 参考噪声、钳位漏电、PCB 漏电。ADC 的建立与量化细节见[ADC 原理、参数与参考电压](../mcu/adc.md)，缓冲器结构见[电压跟随器](../opamp/voltage-follower.md)。

</details>

<details><summary>设计一个 12V→5V/2A 的电源树，后端还要给 3.3V MCU 供电。给出方案与权衡。</summary>

**考点：Buck vs LDO、电源树、效率、噪声、封装热阻。**

1. **12V→5V/2A**：压差大、电流大，用同步 Buck（效率约 90%）。占空比与电感：

$$
D=\frac{V_{out}}{V_{in}}=\frac{5}{12}=0.417
$$

$$
L=\frac{V_{out}(1-D)}{\Delta I_L f_{sw}}
=\frac{5\times(1-0.417)}{0.6\times400\times10^3}
=12.15\,\mu\text{H}
$$

按 30% 纹波（$\Delta I_L=0.6\text{A}$）算得 12.15µH，取标准值 10µH（$\Delta I_L=0.73\text{A}$，36%）或 15µH（$\Delta I_L=0.49\text{A}$，24%）。峰值电流 $I_{pk}=2+0.37=2.37\text{A}$，电感 $I_{sat}$ 取 3A 以上，并注意 $I_{sat}$ 在 100°C 的降额。

2. **5V→3.3V MCU**：压差 1.7V、电流 0.2A，功耗：

$$
P_d=(5-3.3)\times0.2=0.34\text{W}
$$

SOT-23-5 的 $\theta_{JA}\approx250^{\circ}\text{C/W}$，温升 $0.34\times250=85^{\circ}\text{C}$：25°C 环境结温 110°C 已接近，50°C 环境 135°C 超限。**不能只说“可接受”**；要用 DFN/带散热焊盘（$\theta_{JA}\approx60^{\circ}\text{C/W}$，温升 20.4°C）或把电流降到 0.1A。LDO 纹波小，利于 ADC，但 400kHz 的 PSRR 通常只有几十 dB（典型量级，以器件手册为准），必要时加 LC/磁珠。

3. **去耦**：Buck 输入 10µF+0.1µF，输出 22µF+0.1µF；MCU 每个电源脚 0.1µF，ADC 另加 1µF+10nF。
4. **风险**：Buck 开关噪声耦合到模拟；3.3V 负载大时 LDO 过热；电感饱和；输入跌落时占空比撞最大限制。
5. **权衡**：若 3.3V 负载也大（>0.5A），直接 12V→3.3V Buck 效率更高，但 EMI/纹波大；本方案适合 3.3V 轻载 + 模拟。Buck 的伏秒平衡与电感计算见[开关电源原理与 Buck 降压](../power/buck.md)，LDO 的热阻与 PSRR 见[LDO 原理、选型与功耗计算](../power/ldo.md)。

</details>

<details><summary>设计一个直流有刷电机驱动：12V、峰值 2A，方向可逆，MCU PWM 控制。给出拓扑与关键器件。</summary>

**考点：H 桥、续流、PWM、死区、电流采样。**

1. **拓扑**：H 桥（H-Bridge），4 个 NMOS 或集成 H 桥 IC，实现正反转与刹车。
2. **驱动**：高边 NMOS 需自举/电荷泵驱动，或选集成栅驱 H 桥；死区取 100~500ns，防止上下管直通。栅极电阻与米勒钳位要按 $Q_g$ 和开关速度算。
3. **PWM**：20~30kHz（可听噪声之上），一侧 PWM、一侧方向，或双 PWM 互补；频率越高开关损耗越大，要折中。
4. **续流**：MOS 体二极管可续流，但压降大、反向恢复差；2A/12V 建议同步整流。
5. **采样与保护**：0.05~0.1Ω 低边采样，0.1Ω 在 2A 时功耗 $I^2R=0.4\text{W}$，选 2512/1W 并 Kelvin 连接；加比较器/ADC 过流保护、自恢复保险丝、TVS 抑制电机反电动势（钳位电压低于 MOS 的 $V_{DS}$ 额定）。
6. **PCB**：大电流回路短粗、地平面、功率与信号分区，采样电阻回流不要穿过信号地。

</details>

<details><summary>设计一个电池供电温湿度节点：CR2032 供电，要求工作 1 年，周期性采样上报。硬件上如何降功耗？</summary>

**考点：低功耗设计、占空比、电池内阻。**

1. **功耗预算**：CR2032 约 220mAh；1 年 8760h，平均电流上限：

$$
I_{avg,max}=\frac{220\text{mAh}}{8760\text{h}}=25.1\,\mu\text{A}
$$

待机 1~5µA，留给采样/发射约 20µA。

2. **电压**：CR2032 标称 3.0V、截止 2.0V，**不能再用 LDO 稳到 3.3V**；选 1.8V/2.0V MCU 直供，或用亚 µA 级 Iq 的 boost 升到 3.3V。普通 LDO 从 3V 降 3.3V 不成立。
3. **占空比**：RTC 每 10min 唤醒，采样 1s、5mA：

$$
I_{sample}=5\text{mA}\times\frac{1}{600}=8.3\,\mu\text{A}
$$

若 BLE 10mA/10ms 每 10min，平均 $10\text{mA}\times0.01/600=0.17\,\mu\text{A}$。加待机 2µA，总约 10.5µA，理论寿命 $220/10.5=21\text{kh}\approx2.4$ 年；低温/老化按 50% 折（工程假设）仍有约 1.2 年，满足 1 年但余量不大。

4. **引脚/外设**：不用的引脚设输出低或内部下拉，不悬空；关掉不用的上拉、外设时钟和 ADC 缓冲。
5. **脉冲**：CR2032 内阻 10~40Ω（随放电程度和温度上升），10mA 脉冲压降 0.1~0.4V；射频/发射大脉冲要并 100µF 低 ESR 电容。
6. **漏电**：TVS/保护二极管反向漏电选 <100nA；1µA 就吃掉 4% 预算。电池放电曲线与低功耗模式见[电池、充电管理与电量计](../power/battery-charger.md)和[看门狗、RTC 与低功耗硬件](../mcu/watchdog-rtc-lowpower.md)。

</details>

## 二、故障诊断

<details><summary>故障：一块新板 MCU 不工作，测 3.3V 正常、晶振两脚电压约 1.6V。可能原因？</summary>

1.6V 接近 $3.3/2$，是两个反相器脚的直流偏置，**不能证明起振**；不起振时也可能被偏置到中点。

排查：(1) 用高阻 FET 探头/频率计看 OSC_OUT，普通 ×10 探头有约 10pF，可能把晶振压停；不要用万用表测高频。(2) 查负载电容 $C_1=C_2\approx2(C_L-C_{stray})$，核对晶振 $C_L$、ESR、驱动电平。(3) 查负阻裕量：经验要求 $|R_{neg}|>5\times ESR$。(4) 查 BOOT/复位/调试模式、电源纹波、焊接不良。(5) 晶振走线短、包地、远离开关噪声。晶振不起振常因负载电容错、ESR 不匹配或走线太长。详见[晶振与振荡器](../components/crystal-oscillator.md)。

</details>

<details><summary>故障：Buck 输出电压只有输入的一半左右，且电感发烫。可能原因？</summary>

先测 SW 占空比 $D$ 和输入/输出，按现象分：

- **$D\approx0.5$、$V_{out}\approx6\text{V}$**：反馈分压比错/反馈脚虚焊，控制器把 6V 当目标；或控制器被强制 50% 占空比（测试模式/短路）。
- **$D$ 接近 1 而 $V_{out}$ 只有 6V**：功率级限流、电感饱和、高边驱动不足或输入跌落的共同结果；电感发烫支持饱和/过流。
- **$D$ 很小**：反馈过冲/环路振荡。

再查：电感 $I_{sat}$、续流二极管/同步管、输出电容 ESR、电流采样、环路补偿。**电感发烫优先怀疑饱和/过流，不是“电感质量差”**；输出半压先分清是“反馈设定错”还是“功率级撑不住”。

</details>

<details><summary>故障：RS-485 总线通讯距离一长就出错，短距离正常。硬件原因？</summary>

1. 总线两端未各加 120Ω 终端，长距离反射；中间节点不要端接。
2. 空闲 fail-safe 偏置不足：要保证 $V_{diff}>200\text{mV}$；按总线等效 60Ω 与偏置网络算，只在主机端加一组。
3. 总线拓扑是星形、分支过长，产生反射；改菊花链。
4. 地电位差大、未加隔离；共模范围 $-7\sim+12\text{V}$ 是器件工作范围，不是长期地电位差。
5. 速率过高超出距离极限；100kbps 可到 1200m，速率越高距离越短。
6. 电缆电容/线径/节点数超限；终端电阻功率也要算（120Ω 在 5V 时 0.2W）。

对策：手拉手总线、两端 120Ω、加 failsafe 偏置、降速、加隔离/共模电感/TVS。RS-485 的终端、偏置与共模计算见[RS-485 与 CAN 总线硬件](../mcu/rs485-can.md)。

</details>

<details><summary>故障：产品 ESD 接触放电 ±4kV 时 MCU 复位，但空气放电正常。原因与对策？</summary>

接触放电比空气放电更严酷、重复性更好；±4kV 接触能复位，说明 ESD 电流经接口/缝隙耦合到复位、电源或地，触发 BOR/看门狗复位。

对策：(1) 连接器入口 TVS 就近钳位，地回路短而宽到机壳/保护地；(2) 复位脚 RC+TVS，复位走线短、包地；(3) 电源 π 滤波、TVS；(4) 外壳接缝搭接、屏蔽；(5) 软件记录复位源并自恢复。注意 TVS 钳位电压要低于被保护引脚绝对最大额定；TVS 地端不能接到敏感信号地。

</details>

## 三、权衡决策

<details><summary>权衡：同一降压需求，用 LDO 还是 Buck？给出决策树。</summary>

决策：
- 压差小（<1V）、电流小（<300mA）、对噪声敏感（模拟/ADC）→ **LDO**（纹波小、简单、便宜），但要算 $P_d=(V_{in}-V_{out})I$ 与结温。
- 压差大、电流大、电池供电求续航 → **Buck**（效率高、发热小），但要算电感、EMI、环路。
- 既要高效率又要低噪声 → Buck 后级 LDO（Buck 主功率，LDO 给模拟）。
关键算 LDO 功耗是否过热、Buck 成本与 EMI 是否可接受；LDO 的 PSRR 随频率下降，不能只看 100Hz 指标。

</details>

<details><summary>权衡：高频时钟用晶振（XTAL）还是 RC 振荡器？</summary>

- 精度要求高（通讯、时间基准）→ **晶振**（ppm 级，全温区可校准）；
- 成本敏感、精度要求低、可软件校准 → **内部 RC**（% 级误差，温漂大）；
- 体积极限 → RC + 软件校准，但温度/电压变化后要重新校准；
- 折中：晶振 + 负载电容匹配，注意 $C_L$、ESR、负阻裕量。
晶振占板面积与 BOM 成本，RC 启动快但温漂大；通信波特率误差要按两端累计算。

</details>

<details><summary>权衡：选 MOSFET 做低边开关，$R_{DS(on)}$ 与 $Q_g$ 如何权衡？</summary>

- 低频大电流：优先低 $R_{DS(on)}$（导通损耗），$Q_g$ 大可接受；
- 高频小电流：$Q_g$ 小、栅驱容易，$R_{DS(on)}$ 稍大也无妨；
- $R_{DS(on)}$ 小的管通常 $Q_g$ 大、芯片贵。

总损耗不能只算导通：

$$
P\approx I^2R_{DS(on)}+Q_gV_{GS}f_{sw}
+\frac{1}{2}V_{DS}I_D(t_r+t_f)f_{sw}
$$

按工作点平衡导通、栅极、开关三项，不能只看 $R_{DS(on)}$。还要核对 SOA、结温、雪崩能量。

</details>

<details><summary>权衡：PCB 用 4 层还是 2 层？</summary>

- 成本敏感、低速、简单 → **2 层**（便宜，但地不完整、EMI 差）；
- 有高速信号、ADC、电源、EMC 要求 → **4 层**（完整地/电源平面，PI/SI 好）；
- 4 层板制板成本通常是 2 层的 2~3 倍（典型量级，按板厂报价；批量越大差距越小），但减少 EMI 整改迭代，长期更省。
- 工业/医疗/出口认证产品通常直接上 4 层；若 4 层仍不够（DDR/USB HS/以太网），上 6 层。

关键判据是“有没有完整参考平面、有没有高速/模拟/EMC 约束”，不是“层数越多越好”。层叠分配与阻抗计算见[PCB 层叠与阻抗](../pcb/pcb-stackup.md)。

</details>

## 四、开放讨论

<details><summary>开放题：作为硬件工程师，从接到需求到产品量产，你的完整工作流是什么？</summary>

推荐思路：
1. **需求分析**：电气指标、接口、环境、成本、认证；
2. **方案选型**：MCU/电源/接口选型，画系统框图与电源树；
3. **原理图设计**：按模块分，关键器件核 datasheet；
4. **仿真/验算**：LTspice 验证关键电路，做最坏情况/容差分析；
5. **PCB Layout**：层叠、布局、分区、阻抗、去耦；
6. **投板焊接**：首件检查、DFM/DFT；
7. **调试**：静态→动态，电源→时钟→外设；
8. **测试**：功能、性能、可靠性、EMC 预测试；
9. **认证与试产**：按目标市场做 CCC/CE/FCC/UL；
10. **BOM/文档/版本管理**。
考点：是否有结构化思维、是否重视可制造性与成本、是否闭环。

</details>

<details><summary>开放题：你调试一个“偶发”问题时，如何避免瞎试？</summary>

思路：
- **先记录**：现象、复现条件、日志、复位原因；
- **形成假设**：电源？EMI？温度？软件竞态？
- **隔离变量**：一次只改一个条件；
- **测量验证**：用仪器看，不靠猜；
- **统计复现**：偶发靠长时间老化/环境箱；
- **根因而非症状**：改根因，不是掩盖现象。
考点：方法论、数据驱动、不急躁。

</details>

<details><summary>开放题：为什么说“模拟地和数字地单点连接”在高速板上不一定适用？</summary>

思路：
- 低速/混合信号器件：若 ADC 厂商明确要求，AGND/DGND 可在一点连接；否则外部应整合成完整地平面，**不要随意分割**，否则跨分割走线增大回路面积；
- 真正需要的是让数字回流不流经模拟敏感区（布局上分开走），而不是物理分割地；
- 完整连续地平面比分割地对 EMC 更好；磁珠/0Ω 单点在高频下引入电感，可能让两侧电位差更大。
考点：是否理解返回电流路径、是否人云亦云。

</details>

<details><summary>开放题：BOM 成本优化时，硬件工程师应该抓哪几个大头？</summary>

思路：
1. **主控与电源 IC**：单价高，选型时对比；
2. **通用件替代**：电阻电容用 E96 常用值、统一规格减少料号；
3. **减料**：不必要的保护、冗余接口；
4. **国产替代**：成熟器件国产化降本；
5. **封装与工艺**：统一封装降低贴片成本；
6. **量价谈判**：批量后议价。
考点：成本意识、可制造性、可靠性与成本的平衡；降本不能降掉安规/可靠性余量。

</details>

<details><summary>设计题：用一颗 MCU 通过 NTC 热敏电阻测 −40~125°C 温度，送 3.3V 参考的 12 位 ADC。给出电路与量程匹配计算。</summary>

**考点：分压、量程、β 公式、自热、引线。**

1. **拓扑**：NTC（10kΩ@25°C，B=3950）接 GND，$R_{top}$ 接 3.3V，中点接 ADC：

$$
V_{ADC}=3.3\times\frac{R_T}{R_{top}+R_T}
$$

2. **阻值**：

$$
R_T=R_0\exp\left[B\left(\frac{1}{T}-\frac{1}{T_0}\right)\right]
$$

−40°C（233.15K）：

$$
R_T=10\text{k}\times\exp\left[3950\left(\frac{1}{233.15}-\frac{1}{298.15}\right)\right]
=402\text{k}\Omega
$$

125°C（398.15K）：

$$
R_T=10\text{k}\times\exp\left[3950\left(\frac{1}{398.15}-\frac{1}{298.15}\right)\right]
=359\,\Omega
$$

跨约 1120 倍，单个分压不可能在两端都灵敏。

3. **取 $R_{top}$**：若只看中段灵敏度，取 $R_{top}=R_T(T_{mid})$，−40~125°C 的中点 42.5°C 对应约 4.8kΩ；但两端都要留轨余量，取两端阻值的几何均值 $\sqrt{402\text{k}\times359}\approx12.0\text{k}\Omega$ 更稳。取 12kΩ 时两端电压余量对称：

$$
V_{-40}=3.3\times\frac{402}{12+402}=3.20\text{V}
$$

$$
V_{125}=3.3\times\frac{0.359}{12+0.359}=0.096\text{V}
$$

两端各距轨约 96mV。若取 10kΩ，−40°C 为 3.22V、125°C 为 0.114V，低端余量更小；若取 4.7kΩ（42.5°C 对应阻值），−40°C 升到 3.26V，只剩约 39mV，必须核对 β/电阻容差。

4. **自热**：25°C 时 $I=3.3/(12\text{k}+10\text{k})=0.15\text{mA}$：

$$
P=I^2R_T=(0.15\times10^{-3})^2\times10^4=0.225\text{mW}
$$

耗散系数 2mW/°C 时自热约 0.11°C，可忽略。高温端 $R_T$ 小、电流 0.27mA，但功耗仍约 26µW。

灵敏度也要核算：12 位、3.3V 参考的 $1\text{LSB}=0.806\text{mV}$；25°C 附近 $\mathrm{d}V/\mathrm{d}T\approx-36\text{mV/K}$，折合 0.02K/LSB；−40°C 端约 $-6.8\text{mV/K}$（0.12K/LSB），125°C 端约 $-2.3\text{mV/K}$（0.35K/LSB）。两端分辨率明显变差，这是宽温区 NTC 的固有代价。

5. **误差**：β 容差 ±1%、$R_0$ ±1%、$R_{top}$ ±1%、ADC 参考/量化；β 容差在 −40°C 端约 0.5K、125°C 端约 1.4K 量级，叠加分压/参考误差后更大。宽温区要逐点校准或用 Steinhart-Hart 三参数式。
6. **引线**：两线制引线电阻直接加到 $R_T$，长线要用四线制（Kelvin）或软件扣除已知线阻；恒流源不能消除引线电阻，只把 R 变成 V。引线还要 RC 滤波/屏蔽。NTC 的 B 值、灵敏度和自热细节见[特殊电阻：NTC/PTC/MOV/LDR](../components/special-resistors.md)。

</details>

<details><summary>开放题：电源完整性、信号完整性、EMC 三者有什么联系？</summary>

思路：
- PI 保证电源低阻抗、瞬态供电；SI 保证信号边沿完整；EMC 是前两者做不好的对外表现。
- 地弹（PI）→ 噪声耦合（SI）→ 辐射（EMC）；
- 完整地平面、合理去耦、阻抗匹配同时改善三者。
考点：系统观，把分散知识点连成整体。

</details>
