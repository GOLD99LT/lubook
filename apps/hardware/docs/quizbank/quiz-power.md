---
id: quiz-power
title: 电源设计测试题
part: 9
chapter: 硬件测试与面试题库
order: 30
tags: [题库, 自测, 电源]
difficulty: 2
status: published
sources:
  - Erickson & Maksimovic, Fundamentals of Power Electronics, 3rd ed. — Chapter 2 Principles of Steady-State Converter Analysis（CCM/DCM、Buck/Boost 电流波形与伏秒平衡）
  - TI, SLVA477B Basic Calculation of a Buck Converter's Power Stage — 占空比、电感纹波与输出电容纹波计算
  - TI, SLVA372C Basic Calculation of a Boost Converter's Power Stage — 升压比、输入电流与器件应力
  - Christophe Basso, Switch-Mode Power Supplies, 2nd ed. — 环路补偿、相位裕度与穿越频率
  - Analog Devices, MT-101 Decoupling Techniques — 去耦电容分层、自谐振与目标阻抗
---

# 电源设计测试题

本题库覆盖电源指标（纹波/效率/调整率）、线性电源与 LDO、Buck/Boost、功率器件选型、控制环路与补偿、反激、电池充电、电源监控与负载开关、接地与地弹、电源完整性与去耦。题型分为「概念判断」「填空」「计算」「简答与情景」四组。

**核对口径**：拓扑题先看"电感接在哪一侧、电流连不连续"，再谈公式；数字题给**公式 → 代入 → 结果 → 单位**；涉及器件应力的结论都注明测试条件。

## 一、概念判断

<details><summary>判断：LDO 的效率主要由压差决定，压差越小效率越高。</summary>

**正确。**判据：LDO 是线性调整，输入电流≈输出电流，所以 $\eta\approx\dfrac{V_{out}}{V_{in}}=\dfrac{V_{out}}{V_{out}+V_{drop}}$（忽略静态电流 $I_Q$）。压差越小，$\eta$ 越接近 1。

代入感受一下：3.3V/5V 输入 → $\eta=66\%$；3.3V/3.6V 输入 → $\eta=91.7\%$。压差（Dropout Voltage）是维持稳压所需的最小输入输出压差，好的 LDO 在额定电流下可到 100~200mV。

补充判据：轻载时静态电流 $I_Q$ 变成主角，$\eta\approx V_{out}I_{out}/(V_{in}(I_{out}+I_Q))$；µA 级负载下即使压差很小，效率也可能只有百分之几十。

详见 [LDO 低压差线性稳压器](../power/ldo.md)。

</details>

<details><summary>判断：Buck 变换器是降压开关电源，输入电流连续；Boost 是升压开关电源，输出电压高于输入。</summary>

**错误，前半句说反了。**Buck 的**输入电流是斩波脉冲、不连续**：高边管导通时输入电流等于电感电流，关断时为零，所以输入电容必须承受很大的 RMS 纹波电流；连续的是**电感电流**（CCM 下）。Boost 恰好相反：电感接在输入侧，**输入电流连续**（三角波），而输出电流是二极管的脉冲电流，输出电容压力大。

判据（一句话记住）：**电感在哪一侧，哪一侧的电流就连续**。Buck 电感在输出侧 → 输出电流连续、输入脉动；Boost 电感在输入侧 → 输入连续、输出脉动。

题目的后半句（Boost 升压、$V_{out}>V_{in}$）是对的，所以整句判为**错误**（一句错即错）。

详见 [Buck 降压变换器](../power/buck.md)、[Boost 与 Buck-Boost](../power/boost-buckboost.md)。

</details>

<details><summary>判断：开关电源中电感电流连续模式 CCM 与断续模式 DCM 由电感量与负载电流决定，轻载易进入 DCM。</summary>

**正确。**判据：CCM 的边界是 $I_{out}>\Delta I_L/2$，即电感电流最小值 $I_{out}-\Delta I_L/2>0$。$\Delta I_L=\dfrac{(V_{in}-V_{out})D}{f_{sw}L}$ 由电感量决定，所以"电感小、负载轻"都容易进 DCM。

后果：DCM 下小信号模型与增益都变了（$V_{out}/V_{in}$ 不再只由 $D$ 决定，还依赖负载），环路特性随之变化；很多控制器在 DCM 会自动降频或跳周期，轻载效率提高但纹波与 EMI 频谱改变。

详见 [Buck 降压变换器](../power/buck.md)、[开关电源控制环路](../power/smps-control-loop.md)。

</details>

<details><summary>判断：线性电源调整率好、纹波小，但效率低、发热大；开关电源效率高，但纹波噪声大、需补偿。</summary>

**正确。**判据：线性电源靠串联管压降发热，效率 $\approx V_{out}/V_{in}$，但没有开关动作，输出纹波可低到 µV 级、负载调整率好；开关电源靠高频开关储能，效率 85%~95%，代价是开关纹波、EMI 与环路补偿。

补充：两者不是替代关系而是分工——前级用开关电源做宽范围变换，后级用 LDO 做低噪声"净化"，这是模拟/射频供电的标准架构。

详见 [线性电源](../power/linear-supply.md)、[LDO 低压差线性稳压器](../power/ldo.md)。

</details>

<details><summary>判断：去耦电容越大越好，所以每个芯片电源脚只贴一颗 100µF 电解就够了。</summary>

**错误。**判据是阻抗-频率曲线：大容量电解的 ESL 大、自谐振频率低（几十 kHz~几百 kHz），超过自谐振后呈感性，对高频瞬态几乎没有去耦作用。

正确做法是**分层并联**：大容量（10~100µF，低频储能）+ 中容量（1~10µF）+ 小容量（0.1µF、0.01µF，高频、贴近电源脚），各自负责一个频段，形成宽频低阻抗；同时保证回路面积小（电容—电源脚—地平面）。

详见 [电源完整性与去耦](../power/power-integrity-decoupling.md)、[电容器全解](../components/capacitors.md)。

</details>

<details><summary>判断：地弹（Ground Bounce）是芯片内部多个输出同时翻转时，因接地引脚电感 di/dt 引起的参考地瞬时抬升。</summary>

**正确。**判据：$V=L_{gnd}\dfrac{di}{dt}$。多个输出同时翻转，$di/dt$ 叠加，接地引脚与封装内的寄生电感把芯片内部参考地瞬时抬高于系统地，造成输入判决错误、输出毛刺，严重时触发闩锁。

三个加剧条件：同时翻转的位数多（如 8/16 位总线）、边沿快（$di/dt$ 大）、地过孔/地引脚少（$L$ 大）。对策：增加地引脚与地过孔、减慢边沿（串小电阻）、缩短回流路径、必要时用展频/输出斜率控制。

详见 [接地与地弹](../power/grounding.md)。

</details>

<details><summary>判断：反激（Flyback）变换器靠变压器隔离储能，原边开关时变压器储能，关断时向副边释放，常用于中小功率隔离电源。</summary>

**正确。**判据：反激是"隔离的 Buck-Boost"，变压器兼作储能电感——原边导通时副边二极管截止、能量储在磁芯气隙中；原边关断时磁通复位、能量传到副边。所以变压器必须留气隙（否则磁芯饱和），且**原边与副边不同时导通**。

适用：5~100W 隔离电源（适配器、辅助电源、PoE），优点是结构简单、成本低、天然隔离；缺点是变压器要储能、体积大，漏感带来电压尖峰与损耗，需要 RCD 钳位。

详见 [反激变换器](../power/flyback.md)。

</details>

<details><summary>判断：锂电池充电分恒流 CC 与恒压 CV 两个阶段，满电前恒流、接近 4.2V 时转恒压，最后截止电流。</summary>

**正确。**判据：CC 阶段电流恒定（常见 0.5C~1C），电压上升；到 4.2V/节后转 CV，电压保持不变、电流指数衰减；降到截止电流（常见 0.05C~0.1C）判定充满。

两个前提：① 终止电压以电芯数据手册为准，标准锂离子是 4.20V，高压电芯有 4.35V/4.40V 规格，**不能混用**；② 过充（4.2V + 1% 误差 + 温度漂移可到 4.3V）会加速老化甚至鼓包起火，必须有独立保护板兜底。

详见 [电池充电](../power/battery-charger.md)。

</details>

<details><summary>判断：LDO 的输出电容只看容量，ESR 不影响稳定性。</summary>

**错误。**很多 LDO（尤其 PMOS 调整管、低静态电流的老型号）的环路补偿依赖输出电容的 **ESR 零点**，数据手册会给出"ESR 稳定窗口"（常见 0.1~10Ω 量级）。ESR 过低（多颗陶瓷并联只有几 mΩ）或过高都可能振荡。

判据：查数据手册的 Output Capacitor ESR stability region 图，按窗口选电容类型与容量；标称"陶瓷电容稳定"的 LDO 内部已补偿，允许低 ESR，但通常有**最小容量**要求，且大容量陶瓷的直流偏压降容要另外算。

现象：换用低 ESR 陶瓷后输出出现几十 kHz~几 MHz 的振荡。原因：ESR 零点移出补偿窗口。解决：串小电阻、换回规定 ESR 范围的电容，或换陶瓷稳定型 LDO。

详见 [LDO 低压差线性稳压器](../power/ldo.md)、[开关电源控制环路](../power/smps-control-loop.md)。

</details>

## 二、填空

<details><summary>开关电源两大损耗：____ 损耗（$I^2R_{DS(on)}$）与 ____ 损耗（开关沿过程）；轻载下 ____ 损耗占比上升。</summary>

导通损耗与开关损耗。轻载下开关损耗（与频率成正比、基本不随负载下降）占比上升，所以轻载用 PFM/跳周期/降频模式提高效率。

判据：$P_{cond}=I_{rms}^2R_{DS(on)}$（注意 $R_{DS(on)}$ 按热态取值，100°C 时约为 25°C 的 1.4~1.6 倍），$P_{sw}\approx\frac{1}{2}V_{in}I_{out}(t_r+t_f)f_{sw}+Q_{rr}V_{in}f_{sw}$。两条交叉点就是效率曲线的峰值位置。

详见 [Buck 降压变换器](../power/buck.md)、[功率器件选型](../power/power-component-selection.md)。

</details>

<details><summary>Buck 电感纹波电流常取额定输出电流的 ____%~____%；输出纹波电压由 ____ 与 ____ 决定。</summary>

纹波电流取 **20%~40%**（常用 30%）。输出纹波由输出电容的 **ESR** 与**电容值**（配合电感纹波电流）共同决定：

$$\Delta V\approx\Delta I_L\left(ESR+\frac{1}{8f_{sw}C_{out}}\right)$$

判据：高频、大纹波电流时 ESR 项主导，选低 ESR 陶瓷最有效；容量项在低频或大容值时主导，此时加大容量才有意义。两条都要算，不能只看电容标称值。

详见 [Buck 降压变换器](../power/buck.md)。

</details>

<details><summary>电源环路补偿要保证相位裕度 PM ≥ ____°（工程希望 ≥ 45°，留余量）；穿越频率通常取开关频率的 ____。</summary>

相位裕度 **PM ≥ 45°**（工程常取 45°~60°，60° 左右兼顾稳定与响应速度）；穿越频率（0 dB crossover）取开关频率的 **1/10 左右**（常见 1/5~1/20）。

判据：PM 不足会振荡/过冲大，PM 过大（>70°）则动态响应慢、恢复时间长；穿越频率越高响应越快，但必须远低于 $f_{sw}$ 才能让开关纹波被环路衰减。穿越频率处增益斜率建议 $-20\ \text{dB/dec}$。

详见 [开关电源控制环路](../power/smps-control-loop.md)。

</details>

<details><summary>LDO 热功耗 $P_d=$ ____；结温 $T_j=T_a+$ ____。</summary>

$P_d=(V_{in}-V_{out})I_{out}$（忽略静态电流；更精确为 $(V_{in}-V_{out})I_{out}+V_{in}I_Q$）。$T_j=T_a+P_d\cdot\theta_{JA}$，其中 $\theta_{JA}$ 是结到环境热阻（°C/W，与封装、铜面积、气流有关）。

判据：$T_j$ 必须低于数据手册的额定值（常见 125°C 或 150°C），并按降额留 20~30°C 余量；$\theta_{JA}$ 要用实际 PCB 条件下的值（数据手册常给 JEDEC 标准板的测试值，实际小板会更差）。

详见 [LDO 低压差线性稳压器](../power/ldo.md)、[热设计](../pcb/thermal-design.md)。

</details>

<details><summary>负载开关（Load Switch）用于 ____；电源监控 IC 提供 ____、____、____ 等功能。</summary>

负载开关：用低 $R_{DS(on)}$ 的 MOS 受控接通/切断某一路电源，带软启动限制浪涌、待机时切断漏电。电源监控：POR（上电复位）、BOR（欠压/掉电保护）、看门狗（Watchdog）、电源良好（Power Good）输出，有的还集成手动复位与电压监测比较器。

判据：选负载开关看 $R_{DS(on)}$、最大连续电流、软启动时间、反向电流阻断（RBB）与静态电流；选监控 IC 看阈值精度（±1%~±2%）、复位延时与输出级（开漏/推挽）。

详见 [电源监控与负载开关](../power/power-monitoring-loadswitch.md)。

</details>

## 三、计算

<details><summary>LDO：$V_{in}=5\text{V}$，$V_{out}=3.3\text{V}$，$I_{out}=200\text{mA}$。求效率与自身功耗；若 $\theta_{JA}=80^{\circ}\text{C/W}$、环境 $25^{\circ}\text{C}$，结温多少？</summary>

**效率**——公式：$\eta\approx\dfrac{V_{out}}{V_{in}}$。代入：$3.3/5=0.66$。结果：**66%**。

**功耗**——公式：$P_d=(V_{in}-V_{out})I_{out}$。代入：$(5-3.3)\times0.2=0.34\ \text{W}$。结果：**0.34W**。

**结温**——公式：$T_j=T_a+P_d\theta_{JA}$。代入：$25+0.34\times80=25+27.2=52.2^{\circ}\text{C}$。结果：**52.2°C**，远低于 125°C，安全。

**边界计算**：$I_{out}=1\ \text{A}$ 时 $P_d=1.7\ \text{W}$，$T_j=25+1.7\times80=161^{\circ}\text{C}$，已超额定——此时要么换 $\theta_{JA}$ 更低的封装/加铜箔与散热，要么改用 Buck 开关电源（效率 90% 时总损耗约 $\dfrac{3.3}{0.9}-3.3=0.37\ \text{W}$，且分散在开关管、电感、电容上，不是单点发热）。

**判据**：LDO 的适用边界是 $P_d\theta_{JA}<T_{j,max}-T_a$，超过就必须换拓扑。

详见 [LDO 低压差线性稳压器](../power/ldo.md)。

</details>

<details><summary>Buck：$V_{in}=12\text{V}$，$V_{out}=5\text{V}$，效率 90%，输出电流 2A。求输入电流与电感平均电流。</summary>

**输出功率**——公式：$P_{out}=V_{out}I_{out}$。代入：$5\times2=10\ \text{W}$。

**输入功率**——公式：$P_{in}=\dfrac{P_{out}}{\eta}$。代入：$10/0.9=11.11\ \text{W}$。

**输入电流**——公式：$I_{in}=\dfrac{P_{in}}{V_{in}}$。代入：$11.11/12=0.926\ \text{A}$。结果：**约 0.93A**。

**电感平均电流**——CCM 下电感电流的平均值等于输出电流，即 **2A**（峰值还要加 $\Delta I_L/2$）。

**判据**：输入电流小于输出电流，是因为输入电压高——功率守恒的直接结果；效率每降 1 个百分点，输入电流约增 1%，可以用这个比例快速估热。

详见 [Buck 降压变换器](../power/buck.md)。

</details>

<details><summary>Buck 占空比：理想 Buck $D=V_{out}/V_{in}$。$V_{in}=12\text{V}$，$V_{out}=3.3\text{V}$，求占空比 D；若效率 90%，考虑损耗后 D 大约是多少？</summary>

**理想占空比**——公式：$D=\dfrac{V_{out}}{V_{in}}$。代入：$3.3/12=0.275$。结果：**27.5%**。

**考虑效率**——公式：$D\approx\dfrac{V_{out}}{\eta V_{in}}$。代入：$\dfrac{3.3}{0.9\times12}=\dfrac{3.3}{10.8}=0.306$。结果：**约 30.6%**。

**判据**：效率越低、占空比越需要"多开一点"来补偿损耗；设计时还要按最低输入电压算 $D_{max}$（如 10.8V 时 $D_{max}=3.3/(0.9\times10.8)=0.339$），确保不超过控制器的最大占空比限制（常见 90%~95%，但受最小关断时间限制）。

详见 [Buck 降压变换器](../power/buck.md)、[开关电源控制环路](../power/smps-control-loop.md)。

</details>

<details><summary>Boost：$V_{in}=3.7\text{V}$（单节锂电），要升到 $V_{out}=12\text{V}$，效率 85%，输出 0.5A。求占空比 D 与输入平均电流。</summary>

**理想占空比**——公式：$\dfrac{V_{out}}{V_{in}}=\dfrac{1}{1-D}$。代入：$1-D=3.7/12=0.3083$，$D=0.692$。结果：**69.2%**。

**输入功率**——公式：$P_{in}=\dfrac{P_{out}}{\eta}$。代入：$P_{out}=12\times0.5=6\ \text{W}$，$P_{in}=6/0.85=7.06\ \text{W}$。

**输入平均电流**——公式：$I_{in}=\dfrac{P_{in}}{V_{in}}$。代入：$7.06/3.7=1.91\ \text{A}$。结果：**约 1.91A**（等于电感平均电流，CCM 下）。

**一致性检查**：若把 85% 效率也计入占空比，$D=1-\dfrac{\eta V_{in}}{V_{out}}=1-\dfrac{0.85\times3.7}{12}=0.738$。所以"理想式 0.692"与"含损耗式 0.738"并不矛盾——前者用于估器件应力，后者用于校核控制器最大占空比。

**结论**：升压比 3.24 倍时，低压侧电流是输出电流的 3.8 倍，电感、开关、输入走线都要按 1.9A 以上选，且 Boost 输入电流连续、纹波大，输入电容不能省。

详见 [Boost 与 Buck-Boost](../power/boost-buckboost.md)。

</details>

<details><summary>输出电容纹波：Buck 输出纹波电流 0.5A，ESR=20mΩ，$C_{out}=100\,\mu\text{F}$，开关频率 500kHz。估算纹波电压。</summary>

**ESR 分量**——公式：$\Delta V_{ESR}=\Delta I_L\cdot ESR$。代入：$0.5\times0.02=10\ \text{mV}$。

**容性分量**——公式：$\Delta V_C=\dfrac{\Delta I_L}{8f_{sw}C_{out}}$。代入：$\dfrac{0.5}{8\times5\times10^5\times100\times10^{-6}}=\dfrac{0.5}{400}=1.25\ \text{mV}$。

**合成**——两分量相位不同，取均方根：$\sqrt{10^2+1.25^2}=10.08\ \text{mV}$。结果：**约 10mV**。

**判据**：此处 ESR 分量是容性分量的 8 倍，纹波几乎全由 ESR 决定——换低 ESR 陶瓷（几 mΩ）后，ESR 分量降到约 1~2mV，容性分量才成为主角。**先算两项、看谁大，再决定加容量还是换低 ESR，这是选输出电容的正确顺序。**

详见 [Buck 降压变换器](../power/buck.md)、[电容器全解](../components/capacitors.md)。

</details>

<details><summary>Buck 电感纹波：$V_{in}=12\text{V}$，$V_{out}=5\text{V}$，$f_{sw}=500\text{kHz}$，$L=6.8\,\mu\text{H}$，$I_{out}=3\text{A}$。求纹波电流峰峰值，并判断纹波比是否落在常用区间。</summary>

**占空比**——公式：$D=\dfrac{V_{out}}{V_{in}}$。代入：$5/12=0.4167$。

**纹波电流**——公式：$\Delta I_L=\dfrac{V_{out}(1-D)}{f_{sw}L}$（等价于 $\dfrac{(V_{in}-V_{out})D}{f_{sw}L}$）。

代入：$\Delta I_L=\dfrac{5\times(1-0.4167)}{5\times10^5\times6.8\times10^{-6}}=\dfrac{2.917}{3.4}=0.858\ \text{A}$。

**结果**：**$\Delta I_L\approx0.858\ \text{A}$（峰峰值）**；纹波比 $r=\Delta I_L/I_{out}=0.858/3=28.6\%$。

**判据**：28.6% 落在 20%~40% 的常用区间（目标 30%），说明 6.8µH 合适。峰值电流 $I_{pk}=I_{out}+\Delta I_L/2=3+0.429=3.43\ \text{A}$，电感的饱和电流要按 3.43A 再留 20% 以上余量（≥4.3A）。

**验算**：用另一式 $\dfrac{(12-5)\times0.4167}{5\times10^5\times6.8\times10^{-6}}=\dfrac{2.917}{3.4}=0.858\ \text{A}$，一致。

详见 [Buck 降压变换器](../power/buck.md)。

</details>

## 四、简答与情景

<details><summary>情景：Buck 变换器输出在轻载时稳定，重载时出现低频振荡/输出跳动。可能原因？</summary>

**现象**：轻载正常，负载一加上输出就以几百 Hz~几 kHz 的低频摆动，示波器看到包络式起伏，可能伴随电感"吱"声。

**原因（按概率排序）**：

1. **环路补偿与工作点不匹配**：重载下工作点、$R_{DS(on)}$、电感 DCR 都变化，若补偿按轻载整定，重载时相位裕度不足。
2. **电感量偏小或进入 DCM**：DCM 下小信号模型改变（多一个极点/增益变化），按 CCM 设计的补偿在 DCM 失稳。
3. **输出电容 ESR 过大或容值不足**：ESR 零点位置变化，容性延迟引入额外相移。
4. **输入电源/走线阻抗大**：重载时输入电压跌落，触发 UVLO 或占空比限幅，形成"打嗝"式重启。
5. **电流采样/反馈分压受开关噪声干扰**：重载 $di/dt$ 更大，采样误判。

**解决**：先按数据手册的补偿元件推荐值复核（$R_{comp}$、$C_{comp}$），再看开关波形确认是否 DCM/限流，最后查输入跌落与反馈走线（远离电感、开尔文接法）。**判据：重载下的相位裕度 ≥45°，穿越频率 ≤ fsw/10。**

详见 [开关电源控制环路](../power/smps-control-loop.md)、[Buck 降压变换器](../power/buck.md)。

</details>

<details><summary>简答：为什么 MCU/ADC 的模拟电源要单独用 LDO 供电，而不是直接挂在数字 5V 上？</summary>

**原因**：数字电源上的噪声会通过两条路径进模拟电路——① 传导：数字翻转的电流尖峰在电源阻抗上产生纹波；② 共模/地弹：数字回流让"地"不再是 0V。ADC 的电源抑制比（PSRR）随频率下降，100kHz 以上常只剩 40~60dB；以 40dB 算，10mV 纹波折算到输入端是 $10\ \text{mV}/100=100\ \mu\text{V}$，再乘 100 倍增益就是 10mV 的输出误差。

**判据**：折算到 ADC 输入端的纹波误差应按 1 LSB 验收。12 位、3.3V 参考时 1 LSB≈0.8mV，取 0.5 LSB≈0.4mV 为目标；PSRR=60dB 时对应允许 0.4V 纹波，看似宽松——但 PSRR 在开关频率处常掉到 40dB 以下，且基准与采样网络的抑制更差，所以工程上直接把模拟轨纹波控制在 1~10mV 量级，而不是去赌那 60dB。

**做法**：数字侧用 Buck（高效率），模拟侧再用 LDO（低噪声、高 PSRR）二次稳压；模拟地与数字地在 ADC 下方单点连接，基准源单独走线。LDO 的 PSRR 在低频高、高频下降，必要时在 LDO 前加 LC/磁珠滤波。

详见 [LDO 低压差线性稳压器](../power/ldo.md)、[模拟地与数字地布线](../pcb/analog-digital-power-routing.md)。

</details>

<details><summary>情景：USB 5V 输入的设备热插拔瞬间后级 MCU 复位。如何用电源监控/负载开关解决？</summary>

**现象**：插拔 USB 的瞬间 MCU 复位或死机，稳态工作正常；用示波器抓 5V 轨能看到几十 µs 的跌落与尖峰。

**原因**：① 热插拔浪涌电流在电缆与连接器电感上产生电压跌落（$L\,di/dt$），5V 瞬间掉到 MCU 的 BOR 阈值以下；② 插拔电弧/ESD 引入尖峰；③ 上电斜率过陡，复位释放时电源还没稳。

**解决（组合拳）**：

1. **输入端**：TVS 钳位 + π 型滤波（LC）+ 足够的输入储能电容，吸收浪涌。
2. **负载开关软启动**：限制 $dI/dt$，把浪涌摊到 ms 级，避免轨跌落。
3. **电源监控**：BOR 阈值设在 MCU 最低工作电压之上，POR 延时足够长（覆盖电源上升时间），保证电压稳定后再释放复位。
4. **布局**：输入电容紧贴连接器，浪涌回路面积最小。

**判据**：热插拔时 5V 轨的最低点必须高于 MCU 的 BOR 阈值 + 余量；复位释放时刻必须晚于电源达到最小值。

详见 [电源监控与负载开关](../power/power-monitoring-loadswitch.md)、[ESD 防护](../pcb/esd-protection.md)。

</details>

<details><summary>简答：电源完整性 PI 与信号完整性 SI 的区别是什么？去耦体系为什么要分层布电容？</summary>

**区别**：PI 关注**电源/地网络**的阻抗、纹波与目标阻抗（Target Impedance），保证任何频率下瞬态电流都能由就近的电容/平面提供；SI 关注**信号路径**的边沿、反射、串扰、时序。两者共享同一个地平面与回流路径，所以常常一起设计。

**判据（目标阻抗）**：$Z_{target}=\dfrac{\Delta V_{allowed}}{\Delta I_{transient}}$。例如 1.0V 轨允许 50mV 纹波、瞬态电流 2A，则 $Z_{target}=25\ \text{m\Omega}$，去耦网络在关注频段内的阻抗必须低于这个值。

**分层原因**：单只电容只在自谐振频率附近呈低阻抗，两端都失效（低频容量不够、高频呈感性）。所以按频段分工：板级大容量（100µF 级）管 kHz 以下、陶瓷 1~10µF 管百 kHz~数 MHz、0.1µF 管数十 MHz、平面电容/埋容管更高频；每颗芯片电源脚就近放 0.1µF，且回路面积最小。

详见 [电源完整性与去耦](../power/power-integrity-decoupling.md)、[PCB 叠层](../pcb/pcb-stackup.md)。
</details>
