---
id: quiz-components
title: 元器件测试题
part: 9
chapter: 硬件测试与面试题库
order: 10
tags: [题库, 自测, 元器件]
difficulty: 2
status: published
sources:
  - Vishay / Murata / TDK 元器件应用手册
  - Horowitz & Hill, The Art of Electronics, 3rd ed.
  - TI Power Management Selection Guides
---

# 元器件测试题

本题库覆盖电阻/电容/电感的参数与选型、二极管/稳压管/LED/TVS、BJT/MOSFET/IGBT、继电器与光耦、晶振、接插件与保险丝。题型分为「概念判断」「填空」「计算」「简答与情景」四组。

## 一、概念判断

<details><summary>判断：贴片电阻上印 "103" 表示阻值为 103Ω。</summary>

**错误。**三位数字码前两位为有效数字、第三位为 10 的幂：$10\times 10^3=10\text{k}\Omega$。"103" = 10kΩ；"472" = 4.7kΩ；"0" 或 "000" = 0Ω（跳线）。四位码则前三位有效、第四位为幂，如 "1001" = 1.00kΩ。

</details>

<details><summary>判断：MLCC（多层陶瓷电容）在直流偏压下实际容量会下降，X7R/Y5V 比 COG/NP0 下降更明显。</summary>

**正确。**直流偏置效应（DC Bias Effect）使高介电常数材料（X7R、Y5V）在加电压后容量大幅缩水，可能只剩标称值的 30%~60%；COG/NP0 几乎不随偏压变化。电源去耦选 MLCC 时必须按「偏压后的有效容量」而非标称值估算。

</details>

<details><summary>判断：电解电容可以随便用在高频大电流去耦位置，因为它容量大。</summary>

**错误。**铝电解电容 ESR、ESL 大，高频阻抗并不低，且纹波电流能力有限；高频去耦要用低 ESL 的陶瓷电容。正确做法是大容量电解（储能、低频）并联小容量陶瓷（高频），形成宽频去耦。

</details>

<details><summary>判断：肖特基二极管正向压降低（约 0.3~0.5V），但反向漏电流较大、反向耐压相对低。</summary>

**正确。**肖特基（Schottky）靠金属—半导体结，正向压降 $V_F\approx 0.3\sim 0.5\text{V}$、开关快；代价是反向漏电流大、反向耐压通常 ≤ 200V。适合低压整流、续流、防反接。

</details>

<details><summary>判断：MOSFET 是电压控制器件，栅极几乎不取直流电流；BJT 是电流控制器件，需要持续基极电流。</summary>

**正确。**MOSFET（金属氧化物半导体场效应管）栅极绝缘，稳态栅流近似 0，靠 $V_{GS}$ 沟道控制漏极电流；BJT（双极型三极管）靠基极电流 $I_B$ 控制 $I_C=\beta I_B$，持续导通需维持基流。

</details>

<details><summary>判断：NMOS 适合做高边开关，PMOS 适合做低边开关。</summary>

**错误，恰好相反。**NMOS 低边开关（源极接地）最常用，栅极只要高于源极几伏即可导通；做高边开关需把栅极驱动到比源极（接 $V_{cc}$）还高，需自举或电荷泵。PMOS 天然适合高边（源极接 $V_{cc}$，栅极拉低即导通），但导通电阻大、价格高。

</details>

<details><summary>判断：TVS（瞬态抑制二极管）平时反向偏置近乎不导通，遇到过压雪崩击穿时把电压钳位并泄放大电流。</summary>

**正确。**TVS（Transient Voltage Suppressor）工作在反向截止状态，当浪涌超过击穿电压 $V_{BR}$ 时迅速导通雪崩，把端口电压钳在最大钳位电压 $V_C$，保护后级。响应快（ps~ns 级），用于 ESD/浪涌防护。

</details>

<details><summary>判断：光耦（Optocoupler）输入 LED 与输出光敏管之间靠光传递信号，电气上彼此隔离。</summary>

**正确。**光耦输入侧 LED 发光，输出侧光敏三极管/光敏电阻接收，两侧无导线连接，隔离耐压可达数千伏，用于高低压隔离、电平隔离与防地环流。代价是速度慢、CTR（电流传输比）离散且随老化下降。

</details>

## 二、填空

<details><summary>电阻额定功率常见封装：0402 约 ____W，0603 约 ____W，0805 约 ____W。</summary>

0402 ≈ 0.063W（1/16W）；0603 ≈ 0.1W（1/10W）；0805 ≈ 0.125W（1/8W）。1206 ≈ 0.25W。实际选型要按降额（≤50%）留余量。

</details>

<details><summary>二极管反向恢复时间 $t_{rr}$：普通整流管 ____，快恢复 ____，肖特基 ____（填「长/中/短」）。</summary>

普通整流管 $t_{rr}$ 长（数 $\mu$s）；快恢复中等（数百 ns）；肖特基最短（无少数载流子存储，近乎无反向恢复）。高频开关电源续流/整流优先肖特基或同步整流。

</details>

<details><summary>MOSFET 三个关键参数：$R_{DS(on)}$（____）、$V_{GS(th)}$（____）、$Q_g$（____）。</summary>

$R_{DS(on)}$：导通电阻（决定导通损耗）；$V_{GS(th)}$：栅极开启阈值电压；$Q_g$：栅极总电荷（决定开关速度与驱动功耗，$P_{drive}=Q_g V_{GS} f_{sw}$）。

</details>

<details><summary>晶振主要参数：负载电容 $C_L$、频率精度（ppm）、等效串联电阻 ____。两个对地电容之和（含寄生）应约等于 ____。</summary>

等效串联电阻 ESR。PCB 上两只对地电容 $C_1=C_2$，满足 $\dfrac{C_1 C_2}{C_1+C_2}+C_{stray}\approx C_L$。若 $C_1=C_2=C$，则 $C/2+C_{stray}\approx C_L$，常取 $C\approx 2(C_L-C_{stray})$。

</details>

<details><summary>保险丝按保护对象分：____ 保险丝防过流，____（PTC）可自恢复；慢断（T）适合 ____ 场合，快断（F）适合 ____ 场合。</summary>

一次性保险丝防过流；PTC（正温度系数）自恢复。慢断 T（Time-lag）耐受开机浪涌，适合电机/开关电源；快断 F（Fast）保护半导体等对过流敏感的电路。

</details>

## 三、计算

<details><summary>一只硅 BJT 做开关，$V_{CC}=12\text{V}$，负载 $R_C=120\,\Omega$，$\beta=100$。求饱和所需最小基极电流；若取过驱动系数 10，基极限流电阻（$V_{BE}\approx 0.7\text{V}$，驱动高电平 3.3V）取多少？</summary>

饱和集电极电流 $I_{C(sat)}\approx V_{CC}/R_C=12/120=0.1\text{A}=100\text{mA}$。
临界饱和基流 $I_{B(min)}=I_C/\beta=100\text{mA}/100=1\text{mA}$。
过驱动 10 倍：$I_B=10\text{mA}$。
基极电阻 $R_B=\dfrac{V_{drive}-V_{BE}}{I_B}=\dfrac{3.3-0.7}{0.01}=260\,\Omega$，取 220Ω。
过驱动保证深度饱和、$V_{CE(sat)}\approx 0.2\text{V}$，开关可靠。

</details>

<details><summary>MOSFET 低边驱动 $V_{IN}=12\text{V}$，负载电流 5A，$R_{DS(on)}=20\text{m}\Omega$。求导通损耗；若开关频率 200kHz、每次开关损耗能量 $5\mu\text{J}$，求开关损耗总功率。</summary>

导通损耗 $P_{cond}=I^2 R_{DS(on)}=5^2\times 0.02=0.5\text{W}$。
单次开关损耗 $E=5\,\mu\text{J}$，频率 200kHz，开关损耗 $P_{sw}=E\cdot f=5\times10^{-6}\times 2\times10^5=1\text{W}$。
总损耗 $P_{total}\approx 0.5+1=1.5\text{W}$，需评估结温与散热。高频下开关损耗常超过导通损耗。

</details>

<details><summary>稳压管电路：$V_{in}=12\text{V}$，稳压值 $V_Z=5.1\text{V}$，限流电阻 $R_S=1\text{k}\Omega$，负载 $R_L=1\text{k}\Omega$。求稳压管电流与负载电流。</summary>

负载电流 $I_L=V_Z/R_L=5.1/1\text{k}=5.1\text{mA}$。
限流电阻压降 $V_{RS}=V_{in}-V_Z=12-5.1=6.9\text{V}$，$I_{RS}=6.9/1\text{k}=6.9\text{mA}$。
由 KCL，稳压管电流 $I_Z=I_{RS}-I_L=6.9-5.1=1.8\text{mA}$。
该电流须落在稳压管推荐工作电流范围内（一般数 mA 以上才能良好稳压）；若负载拉走全部电流使 $I_Z\to 0$，稳压失效。

</details>

<details><summary>继电器线圈 5V、电阻 70Ω，触点允许 5A/30Vdc。求线圈功耗；用 NPN 驱动时，线圈两端为何必须反向并联续流二极管？</summary>

线圈功耗 $P=V^2/R=5^2/70\approx 0.36\text{W}$，线圈电流 $I=5/70\approx 71\text{mA}$。
线圈是感性负载，三极管关断瞬间电感试图维持电流，$L\,di/dt$ 产生很高的反向尖峰电压，会击穿三极管。反向并联续流二极管（Freewheeling Diode）为该电流提供泄放回路，把线圈两端电压钳在约 $-0.7\text{V}$。

</details>

<details><summary>接插件载流估算：走线/触点额定按 $1\text{A}/\text{mm}^2$（保守）。某信号排针单针需过 0.5A，截面积 0.5mm² 是否够？</summary>

0.5mm² 按 1A/mm² 可过 0.5A，刚好临界。考虑温升、接触电阻、多针并载与降额，余量不足；建议单针 ≤ 0.3A，或用多针并联/大电流专用触点。大电流连接器必须按厂家额定电流与温升曲线选型，不能只按截面积粗算。

</details>

## 四、简答与情景

<details><summary>情景：电源输入口选 TVS 时，$V_{RWM}$、$V_{BR}$、$V_C$ 三个参数应如何与被保护电路配合？</summary>

$V_{RWM}$（最大反向工作电压）应 ≥ 电路正常工作最大电压（如 24V 系统选 $V_{RWM}=26\sim 28\text{V}$），否则正常工作时 TVS 已漏电；$V_{BR}$（开始雪崩击穿电压）略高于 $V_{RWM}$；$V_C$（最大钳位电压）必须低于后级芯片的绝对最大额定电压，否则浪涌时后级仍会损坏。三者关系：$V_{RWM}<V_{BR}<V_C$，且 $V_C<\text{芯片耐压}$。

</details>

<details><summary>简答：X7R、COG/NP0、Y5V 三种电容各适合什么场合？</summary>

COG/NP0：温度稳定性好、无压电效应、精度高，适合谐振、滤波、定时、高频；容量小。X7R：容量较大、温度范围宽（$-55\sim 125^{\circ}\text{C}$，±15%），适合一般去耦、旁路；注意直流偏压降容。Y5V/Z5U：容量大但温度/偏压稳定性差，仅适合对精度不敏感的耦合、低频，工业环境少用。

</details>

<details><summary>情景：一颗 NMOS 做高边开关，源极接 12V，栅极直接由 MCU 3.3V 驱动，MOS 无法完全导通。为什么？怎么解决？</summary>

NMOS 导通要求 $V_{GS}>V_{GS(th)}$（且要到栅极电荷充分、$R_{DS(on)}$ 小的过驱动区，通常 $V_{GS}=10\text{V}$）。高边时源极电位 ≈ 12V，栅极 3.3V 意味着 $V_{GS}=3.3-12=-8.7\text{V}$，反而截止。
解决：用高边驱动 IC（自举/电荷泵把栅极驱动到比源极高 10V），或改用 PMOS 高边开关，或用理想二极管/负载开关 IC。

</details>

<details><summary>简答：晶振不起振或频率偏差大，硬件上常见原因有哪些？</summary>

(1) 负载电容取值不匹配（两只对地电容过大/过小）；(2) PCB 上晶振走线太长、靠近干扰源；(3) 晶振 ESR 超出 MCU 反相器驱动能力；(4) 增益裕量不足；(5) 焊接冷焊、晶振外壳接地不良；(6) 寄生电容估算错误。排查时先核对 $C_L$ 公式与实际对地电容，再查走线与接地。

</details>
