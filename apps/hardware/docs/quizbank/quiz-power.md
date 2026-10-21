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
  - TI, Power Management Topologies (SLUP002 等)
  - Texas Instruments, Simple Switcher Application Notes
  - ON Semiconductor / Analog Devices 电源设计指南
---

# 电源设计测试题

本题库覆盖电源指标（纹波/效率/调整率）、线性电源与 LDO、Buck/Boost、功率器件选型、控制环路与补偿、反激、电池充电、电源监控与负载开关、接地与地弹、电源完整性与去耦。题型分为「概念判断」「填空」「计算」「简答与情景」四组。

## 一、概念判断

<details><summary>判断：LDO 的效率主要由压差决定，压差越小效率越高。</summary>

**正确。**LDO（低压差线性稳压器）效率 $\eta\approx V_{out}/V_{in}$（忽略静态电流），压差 $V_{in}-V_{out}$ 越小效率越高。压差（Dropout Voltage）是维持稳压所需的最小输入输出压差，好的 LDO 可达 100~200mV。

</details>

<details><summary>判断：Buck 变换器是降压开关电源，输入电流连续；Boost 是升压开关电源，输出电压高于输入。</summary>

**正确。**Buck（降压）$V_{out}<V_{in}$，电感在续流二极管/同步管与输出间储能；Boost（升压）$V_{out}>V_{in}$，靠电感储能再叠加到输入实现升压。开关电源效率高（85%~95%）但有开关纹波与 EMI。

</details>

<details><summary>判断：开关电源中电感电流连续模式 CCM 与断续模式 DCM 由电感量与负载电流决定，轻载易进入 DCM。</summary>

**正确。**CCM（连续导通）电感电流不降到零；DCM（断续）在每个周期末尾电流归零。负载轻、电感小易进 DCM；DCM 下控制环路特性变化，小信号模型不同。

</details>

<details><summary>判断：线性电源调整率好、纹波小，但效率低、发热大；开关电源效率高，但纹波噪声大、需补偿。</summary>

**正确。**线性电源（含 LDO）靠串联管压降发热，效率 $\approx V_{out}/V_{in}$；开关电源靠高频开关储能，效率高但需要环路补偿保证稳定，且有开关噪声。

</details>

<details><summary>判断：去耦电容越大越好，所以每个芯片电源脚只贴一颗 100µF 电解就够了。</summary>

**错误。**不同容值应对不同频率：大容量电解处理低频/储能，小容量陶瓷（0.1µF、0.01µF）处理高频瞬态。单一大电容 ESL/ESR 大，高频阻抗并不低。正确做法是大小电容并联、靠近电源脚布置。

</details>

<details><summary>判断：地弹（Ground Bounce）是芯片内部多个输出同时翻转时，因接地引脚电感 di/dt 引起的参考地瞬时抬升。</summary>

**正确。**地弹（Ground Bounce）：接地引脚存在寄生电感，同时开关产生大 $di/dt$，$V=L\,di/dt$ 使芯片参考地瞬时高于系统地，造成噪声。多片同时翻转、边沿过快、地过孔不足时明显。对策：减慢边沿、增加地过孔、良好地平面。

</details>

<details><summary>判断：反激（Flyback）变换器靠变压器隔离储能，原边开关时变压器储能，关断时向副边释放，常用于中小功率隔离电源。</summary>

**正确。**反激是隔离 Buck-Boost，变压器兼储能电感；原边导通储能、关断时能量传递到副边。适合 5~100W 隔离电源（适配器、辅助电源）。

</details>

<details><summary>判断：锂电池充电分恒流 CC 与恒压 CV 两个阶段，满电前恒流、接近 4.2V 时转恒压，最后截止电流。</summary>

**正确。**锂电充电：先恒流（CC，约 0.5C）到 4.2V/节，再恒压（CV）保持 4.2V，电流逐渐减小到截止（如 0.05C）即充满。过充会析气、鼓包甚至起火。

</details>

## 二、填空

<details><summary>开关电源两大损耗：____ 损耗（$I^2R_{DS(on)}$）与 ____ 损耗（开关沿过程）；轻载下 ____ 损耗占比上升。</summary>

导通损耗与开关损耗。轻载下开关损耗（与频率成正比，不随负载下降）占比上升，所以轻载用 PFM/节能模式提高效率。

</details>

<details><summary>Buck 电感纹波电流常取额定输出电流的 ____%~____%；输出纹波电压由 ____ 与 ____ 决定。</summary>

纹波电流取 20%~40%。输出纹波由输出电容 ESR、电容值与电感纹波电流共同决定：$\Delta V\approx \Delta I_L(ESR+1/(8fC_{out}))$。

</details>

<details><summary>电源环路补偿要保证相位裕度 PM ≥ ____°（工程希望 ≥ 45°，留余量）；穿越频率通常取开关频率的 ____。</summary>

相位裕度 ≥ 45°~60°；穿越频率（0dB crossover）取开关频率的 1/10 左右。PM 不足会振荡，过高则动态响应慢。

</details>

<details><summary>LDO 热功耗 $P_d=$ ____；结温 $T_j=T_a+$ ____。</summary>

$P_d=(V_{in}-V_{out})I_{out}$（忽略静态电流）。$T_j=T_a+P_d\cdot\theta_{JA}$，$\theta_{JA}$ 是结到环境热阻。结温不得超过额定（如 125°C）。

</details>

<details><summary>负载开关（Load Switch）用于 ____；电源监控 IC 提供 ____、____、____ 等功能。</summary>

负载开关：用低 $R_{DS(on)}$ MOS 受控接通/切断某路电源，防浪涌、省电。电源监控：POR（上电复位）、BOR（欠压保护）、看门狗、电源良好（Power Good）输出。

</details>

## 三、计算

<details><summary>LDO：$V_{in}=5\text{V}$，$V_{out}=3.3\text{V}$，$I_{out}=200\text{mA}$。求效率与自身功耗；若 $\theta_{JA}=80^{\circ}\text{C/W}$、环境 $25^{\circ}\text{C}$，结温多少？</summary>

效率 $\eta\approx V_{out}/V_{in}=3.3/5=66\%$。
功耗 $P_d=(5-3.3)\times 0.2=0.34\text{W}$。
结温 $T_j=25+0.34\times 80=25+27.2=52.2^{\circ}\text{C}$。
远低于 125°C，安全；若 $I_{out}=1\text{A}$，$P_d=1.7\text{W}$，$T_j=25+136=161^{\circ}\text{C}$，过热——此时应改用开关电源。

</details>

<details><summary>Buck：$V_{in}=12\text{V}$，$V_{out}=5\text{V}$，效率 90%，输出电流 2A。求输入电流与电感平均电流。</summary>

输出功率 $P_{out}=5\times 2=10\text{W}$。
输入功率 $P_{in}=P_{out}/\eta=10/0.9\approx 11.1\text{W}$。
输入平均电流 $I_{in}=P_{in}/V_{in}=11.1/12\approx 0.93\text{A}$。
电感平均电流 ≈ 输出电流 = 2A（CCM 下电感电流平均值等于输出电流）。

</details>

<details><summary>Buck 占空比：理想 Buck $D=V_{out}/V_{in}$。$V_{in}=12\text{V}$，$V_{out}=3.3\text{V}$，求占空比 D；若效率 90%，考虑损耗后 D 大约是多少？</summary>

理想 $D=3.3/12=0.275$（27.5%）。
考虑损耗，实际开关占空比略大以补偿压降（同步 Buck 约 $D\approx V_{out}/(V_{in}\eta)\approx 3.3/(12\times0.9)\approx 0.306$）。注意 $D$ 受最小/最大占空比限制。

</details>

<details><summary>Boost：$V_{in}=3.7\text{V}$（单节锂电），要升到 $V_{out}=12\text{V}$，效率 85%，输出 0.5A。求占空比 D 与输入平均电流。</summary>

理想 Boost $V_{out}=V_{in}/(1-D)$，$1-D=V_{in}/V_{out}=3.7/12=0.308$，$D=0.692$。
输出功率 $P_{out}=12\times 0.5=6\text{W}$，输入功率 $P_{in}=6/0.85=7.06\text{W}$。
输入平均电流 $I_{in}=P_{in}/V_{in}=7.06/3.7\approx 1.91\text{A}$。
（Boost 输入电流连续且纹波大，输入需大电容。）

</details>

<details><summary>输出电容纹波：Buck 输出纹波电流 0.5A，ESR=20mΩ，$C_{out}=100\,\mu\text{F}$，开关频率 500kHz。估算纹波电压。</summary>

ESR 引起纹波 $\Delta V_{ESR}=\Delta I\cdot ESR=0.5\times 0.02=10\text{mV}$。
电容充放电纹波 $\Delta V_C=\Delta I/(8fC)=0.5/(8\times 5\times10^5\times 100\times10^{-6})=0.5/400\approx 1.25\text{mV}$。
总纹波 ≈ 两者平方和开根 ≈ 10.1mV，主要由 ESR 决定——选低 ESR 陶瓷电容可显著降纹波。

</details>

## 四、简答与情景

<details><summary>情景：Buck 变换器输出在轻载时稳定，重载时出现低频振荡/输出跳动。可能原因？</summary>

(1) 环路补偿不匹配，重载下相位裕度不足；(2) 电感量过小，进入 DCM 后模型变化、环路失稳；(3) 输出电容 ESR 过大，引入额外极点；(4) 反馈分压电阻噪声拾取；(5) 控制模式（电压模 vs 电流模）补偿不同。对策：按数据手册补偿元件推荐值设计，复核电感量与电容 ESR。

</details>

<details><summary>简答：为什么 MCU/ADC 的模拟电源要单独用 LDO 供电，而不是直接挂在数字 5V 上？</summary>

数字电源有开关噪声（数字翻转、地弹、纹波），直接给模拟部分会劣化 ADC 信噪比（SNR）。独立 LDO 隔离数字噪声、提供低纹波模拟电源，且模拟地/数字地单点连接。高精密应用还需独立基准源（Reference）。

</details>

<details><summary>情景：USB 5V 输入的设备热插拔瞬间后级 MCU 复位。如何用电源监控/负载开关解决？</summary>

(1) 输入加大容量电容 + TVS 钳位热插拔浪涌；(2) 用负载开关做软启动（Soft-Start）限制浪涌电流 $dI/dt$；(3) 电源监控 IC 设 BOR 阈值与 POR 延时，确保电压稳定到阈值后再释放复位；(4) 加 TVS/π 型滤波抑制毛刺；(5) 合理布局去耦。

</details>

<details><summary>简答：电源完整性 PI 与信号完整性 SI 的区别是什么？去耦体系为什么要分层布电容？</summary>

PI 关注电源/地平面的阻抗、纹波、目标阻抗（Target Impedance），保证瞬态电流供应；SI 关注信号边沿、反射、串扰。去耦分层：每颗芯片配 0.1µF 近距高频去耦、稍远 1~10µF 中频、板级大容量低频储能，形成宽频低阻抗；层叠用相邻电源-地平面对降低平面阻抗。

</details>
