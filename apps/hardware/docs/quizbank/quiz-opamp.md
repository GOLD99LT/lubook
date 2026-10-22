---
id: quiz-opamp
title: 模拟电路与运放测试题
part: 9
chapter: 硬件测试与面试题库
order: 15
tags: [题库, 自测, 运放, 模拟电路]
difficulty: 2
status: published
sources:
  - TI, Op Amps for Everyone（Ron Mancini, SLOD006B）— Chapter 4 Single-Supply Op Amp Design Techniques、Chapter 5 Feedback and Stability Theory、Chapter 11 Understanding Op Amp Parameters
  - TI Precision Labs - Op Amps — 输入失调与偏置电流、增益带宽积与压摆率、容性负载稳定性系列
  - Analog Devices, Op Amp Applications Handbook（Walt Jung）— Chapter 1 Op Amp Basics、Chapter 6 Signal Amplifiers
  - Analog Devices, MT-042 Op Amp Common-Mode Rejection Ratio — 四电阻差分网络的 CMRR 与电阻匹配
  - Sergio Franco, Design with Operational Amplifiers and Analog Integrated Systems, 4th ed. — Chapter 1 Operational Amplifier Fundamentals、Chapter 8 Stability
---

# 模拟电路与运放测试题

本题库覆盖虚短虚断、反相/同相/电压跟随器/差分/仪表放大器、加法器、积分微分、有源滤波器、比较器与迟滞、振荡器、555 定时器、精密整流，以及噪声/失调/GBP/压摆率/稳定性等运放非理想参数。题型分为「概念判断」「填空」「计算」「简答与情景」四组。

**核对口径**：涉及"虚短""轨到轨""无限带宽"这类理想化说法的题，判据一律写成**成立条件**；数字题给**公式 → 代入 → 结果 → 单位**。

## 一、概念判断

<details><summary>判断：只要给运放接上负反馈，反相端与同相端电位就严格相等（虚短），与运放开环增益无关。</summary>

**错误。**虚短是**近似**，不是恒等式，而且恰好与开环增益有关。

判据与三条边界：

1. 真实运放 $V_{out}=A_{OL}(V_+-V_-)$，所以 $V_+-V_-=V_{out}/A_{OL}$。$A_{OL}=10^5\sim10^6$ 时差值在 µV 量级，"近似相等"成立；$A_{OL}$ 越小偏差越大，**"与开环增益无关"是错的**。
2. 前提是**深度负反馈**（环路增益 $T=A_{OL}\beta\gg1$）且运放**工作在线性区**。开环、正反馈（比较器、迟滞）时输出饱和，虚短完全不成立。
3. 即使有负反馈，输入过大或输出限幅使运放饱和时，反馈失效，虚短也不成立——所以"虚短 + 虚断"必须和"输出未饱和"一起检查。

详见 [理想运放与虚短虚断](../opamp/ideal-opamp.md)、[开环、闭环增益与负反馈](../opamp/open-loop-feedback.md)。

</details>

<details><summary>判断：电压跟随器增益为 1，所以它没什么用，不如直接用导线连接。</summary>

**错误。**增益确实为 1，但"没什么用"不成立——跟随器的价值不在增益，而在阻抗变换。

判据：跟随器把**输入阻抗抬到极高**（MΩ~GΩ，由输入级决定）、把**输出阻抗压到极低**（闭环输出阻抗 $R_{out}=R_{out,OL}/(1+T)$，mΩ 量级）。导线做不到这一点——导线会把前级的高内阻信号源直接暴露给后级负载，形成分压误差。

典型用途：传感器/高阻分压网络与 ADC 之间做缓冲、驱动容性负载、隔离前后级。所以该判断错误。

详见 [电压跟随器](../opamp/voltage-follower.md)。

</details>

<details><summary>判断：反相放大器的输入阻抗等于反馈电阻 Rf；同相放大器的输入阻抗很高。</summary>

**错误。**反相放大器的输入阻抗等于**输入电阻 $R_1$**，不是 $R_f$。

判据：反相端是虚地（≈0V），信号源看到的阻抗就是从输入端经 $R_1$ 到虚地的阻抗，$Z_{in}\approx R_1$（严格为 $R_1+R_f/(1+A_{OL})$，第二项可忽略）。$R_f$ 在虚地与输出之间，不参与输入阻抗。

同相放大器信号从同相端进，输入阻抗由运放输入级决定（BJT 输入 MΩ 级、CMOS/JFET 可到 GΩ~TΩ），所以需要高输入阻抗时优先选同相结构。

详见 [反相比例放大器](../opamp/inverting-amplifier.md)、[同相放大器](../opamp/non-inverting-amplifier.md)。

</details>

<details><summary>判断：比较器工作在开环（或正反馈）状态，输出在两个电源轨之间切换，不是线性放大器。</summary>

**正确。**判据：比较器要的是"谁大谁小"的判决，不是线性放大，所以故意不给负反馈——开环增益 $10^5$ 让 µV 级差值就足以把输出推到轨。

加正反馈构成迟滞比较器（Schmitt Trigger），用回差换抗噪声能力与干净翻转；普通运放也能做低速比较器，但输出级不是为饱和设计的（恢复慢、无内置迟滞、逻辑电平不匹配），高速或数字接口场合要用专用比较器。

详见 [比较器与迟滞](../opamp/comparator-hysteresis.md)。

</details>

<details><summary>判断：运放的增益带宽积 GBP 在某型号上近似为常数，增益越大，带宽越小。</summary>

**正确（有前提）。**判据：主极点补偿的电压反馈运放，开环幅频在穿越频率前以 $-20\ \text{dB/dec}$ 下降，所以 $|A_{OL}(f)|\cdot f\approx GBP$ 为常数；闭环 $-3\ \text{dB}$ 带宽 $f_c\approx GBP/G_n$（$G_n$ 是噪声增益）。

三个前提必须记住：① 工作在**主极点之后、第二极点之前**的频段；② $G_n$ 按噪声增益算（反相放大是 $1+R_f/R_1$，比信号增益大 1）；③ 去补偿（decompensated）运放不满足这个简单关系。

详见 [带宽 GBP、压摆率与建立时间](../opamp/gbp-slew-rate.md)。

</details>

<details><summary>判断：压摆率 SR 只影响小信号带宽，与大信号高速输出无关。</summary>

**错误，说反了。**压摆率是大信号参数：它限定输出电压的最大变化速率（V/µs），与增益无关。

判据：正弦输出 $v=V_p\sin(2\pi ft)$ 的最大斜率是 $2\pi fV_p$，不产生压摆失真的条件是 $2\pi fV_p\le SR$。工程上还要留 2 倍余量（即所需斜率 ≤ $0.5SR$）。由此得到**满功率带宽** $f_{FPB}=\dfrac{SR}{2\pi V_p}$。

小信号看 GBP，大信号看 SR——两个都要核对，缺一个就会出现"频响够、波形却削成三角波"。

详见 [带宽 GBP、压摆率与建立时间](../opamp/gbp-slew-rate.md)。

</details>

<details><summary>判断：仪表放大器（Instrumentation Amplifier）高输入阻抗、高共模抑制比，适合放大小差分信号并抑制共模干扰。</summary>

**正确。**经典三运放结构分两级：第一级是两只同相放大器（各接一个输入端），提供极高的输入阻抗并承担主要增益，**共模信号在这一级不被放大**；第二级是差分放大器，把双端转单端并进一步抑制共模。增益由一只 $R_G$ 设定（如 $G=1+50\text{k}\Omega/R_G$）。

判据：CMRR 主要由第一级的匹配（集成化保证）与第二级电阻匹配决定，单片仪放常见 90~120dB 且随增益升高；分立四电阻差分放大器的 CMRR 受电阻容差限制，低增益时只有 30~50dB。

详见 [仪表放大器](../opamp/instrumentation-amplifier.md)、[差分放大器](../opamp/differential-amplifier.md)。

</details>

<details><summary>判断：积分器在直流输入下输出会一直积分直到饱和，因此实际积分器必须并联反馈电阻或加复位开关。</summary>

**正确。**判据：理想积分器 $V_{out}(t)=-\dfrac{1}{RC}\int V_{in}dt$，直流输入（哪怕是 µV 级失调）积分后线性增长，必然撞到电源轨。

实际做法：在反馈电容上并一只大电阻 $R_f$ 提供直流反馈（把直流增益钳在 $-R_f/R_1$，同时引入一个低频极点 $1/(2\pi R_fC)$），或加模拟开关/继电器做复位；高精度场合还要选低 $V_{OS}$、低 $I_B$ 的运放，并注意电容的介质吸收。

详见 [积分器与微分器](../opamp/integrator-differentiator.md)。

</details>

## 二、填空

<details><summary>反相放大器增益 $G=$ ____；同相放大器增益 $G=$ ____；电压跟随器增益 $G=$ ____。</summary>

反相：$G=-R_f/R_1$；同相：$G=1+R_f/R_1$；跟随器：$G=1$。

判据补充：反相放大器的**噪声增益**（同相端看进去的增益）是 $1+R_f/R_1$，比信号增益的绝对值大 1；带宽、噪声、稳定性都按噪声增益算，不按信号增益算。这就是"反相 G=−10 的带宽按 11 算"的原因。

详见 [反相比例放大器](../opamp/inverting-amplifier.md)、[同相放大器](../opamp/non-inverting-amplifier.md)。

</details>

<details><summary>差分放大器要获得高 CMRR，要求四个电阻 ____；CMRR 与电阻匹配精度 $\delta$ 的关系约为 $CMRR\approx$ ____。</summary>

四个电阻的**两臂比值相等**（$R_2/R_1=R_4/R_3$，通常取 $R_1=R_3$、$R_2=R_4$）。

CMRR 的工程估计：$CMRR\approx\dfrac{1+G}{4\delta}$，其中 $G=R_2/R_1$ 是差模增益，$\delta$ 是**单只电阻的相对容差**（四只独立失配的最坏情况，系数 4 已含保守量）。

代入验算三条：$G=1$、$\delta=1\%$ → $2/0.04=50$，即 **34dB**；$G=1$、$\delta=0.1\%$ → 500，即 **54dB**；$G=100$、$\delta=0.1\%$ → $101/0.004=25250$，即 **88dB**。结论：低增益时电阻精度是瓶颈，靠堆精密电阻才能上 70dB，不如直接用集成仪放。

详见 [差分放大器](../opamp/differential-amplifier.md)、[共模范围、CMRR 与 PSRR](../opamp/cmrr-psrr.md)。

</details>

<details><summary>一阶 RC 低通截止频率 $f_c=$ ____；二阶 Sallen-Key 滤波器的阻尼由 ____ 决定，Q 值过高会 ____。</summary>

$f_c=\dfrac{1}{2\pi RC}$。

Sallen-Key 的阻尼由**增益 $K$ 与两级 RC 的元件比值**共同决定（等阻等容时 $Q=1/(3-K)$，$K\to3$ 时 $Q\to\infty$）；Q 过高会在 $f_c$ 附近出现幅频尖峰与阶跃振铃，甚至自激。设计取 $Q\approx0.707$（巴特沃斯）得最平坦幅频，$Q\approx0.577$（贝塞尔）得最平群时延。

详见 [一阶滤波器](../opamp/first-order-filters.md)、[Sallen-Key 滤波器](../opamp/sallen-key-filters.md)。

</details>

<details><summary>555 多谐振荡周期 $T\approx$ ____；占空比由两只定时电阻决定，要实现 <50% 占空比需 ____。</summary>

$T\approx0.693(R_A+2R_B)C$，其中高电平 $t_{high}=0.693(R_A+R_B)C$、低电平 $t_{low}=0.693R_BC$。

判据：标准接法占空比 $D=\dfrac{R_A+R_B}{R_A+2R_B}$，$R_A>0$ 时恒 **>50%**，$R_A=0$ 又会把 $V_{cc}$ 直接加到放电管上，所以靠调电阻得不到 <50%。

要 <50% 需在 **$R_B$ 两端（7 脚 DIS 与 6/2 脚之间）加二极管旁路 $R_B$**：充电只走 $R_A$（经二极管），放电仍走 $R_B$，此时 $t_{high}=0.693R_AC$、$t_{low}=0.693R_BC$、$D=R_A/(R_A+R_B)$，取 $R_A<R_B$ 即得 <50%。

详见 [555 定时器](../opamp/555-timer.md)。

</details>

<details><summary>运放非理想三参数：输入失调电压 $V_{OS}$、输入偏置电流 $I_B$、输入失调电流 $I_{OS}$。BJT 输入级 $I_B$ 较 ____，CMOS 输入级 $I_B$ 极 ____。</summary>

BJT 输入级 $I_B$ 较大（nA~µA 级）；CMOS/JFET 输入级 $I_B$ 极小（pA~fA 级）。

判据：$I_B$ 的误差是**电流乘电阻**——$V_{err}=I_B\times R_{source}$。所以高阻信号源（>100kΩ）必须选 CMOS/JFET 输入运放，否则 $I_B$ 在源阻抗上产生的压降直接变成误差；低阻电路里 $I_B$ 项可以忽略，$V_{OS}$ 才是主角。$I_{OS}$ 造成的是差分项误差，可用平衡电阻部分抵消。

详见 [失调电压、偏置电流与漂移](../opamp/offset-bias.md)。

</details>

## 三、计算

<details><summary>反相放大器 $R_1=10\text{k}\Omega$，$R_f=100\text{k}\Omega$，输入 $V_{in}=0.2\text{V}$。求输出；若运放 GBP=1MHz，求闭环小信号带宽。</summary>

**增益**——公式：$G=-\dfrac{R_f}{R_1}$。代入：$G=-100\text{k}/10\text{k}=-10$。

**输出**——公式：$V_{out}=G\cdot V_{in}$。代入：$V_{out}=-10\times0.2=-2\ \text{V}$。结果：**−2V**（反相，需负电源或轨到轨输出且负轨允许）。

**带宽**——公式：$f_c=\dfrac{GBP}{G_n}$，$G_n=1+\dfrac{R_f}{R_1}$。

代入：$G_n=1+10=11$，$f_c=\dfrac{1\times10^{6}}{11}=90.9\times10^{3}\ \text{Hz}$。结果：**约 90.9kHz**。

**判据**：带宽按噪声增益 11 算，不是按信号增益 10（差 10%，小增益时差别明显）。若信号是 100kHz 方波，基频已经超过 90.9kHz，边沿会被明显圆化。

详见 [反相比例放大器](../opamp/inverting-amplifier.md)、[带宽 GBP、压摆率与建立时间](../opamp/gbp-slew-rate.md)。

</details>

<details><summary>同相放大器 $R_1=1\text{k}\Omega$，$R_f=9\text{k}\Omega$。求增益；若输入 0.5V，输出多少？该电路输入阻抗数量级如何？</summary>

**增益**——公式：$G=1+\dfrac{R_f}{R_1}$。代入：$G=1+9=10$。

**输出**——公式：$V_{out}=G\cdot V_{in}$。代入：$10\times0.5=5\ \text{V}$。结果：**5V**。

**判据检查**：输出 5V 要求电源轨至少 5V + 摆幅余量（普通运放输出距轨 0.5~1.5V，轨到轨约 50~100mV），单电源 5V 供电时这个电路**已经饱和**，必须用更高电源或降低增益。

**输入阻抗**：极高，BJT 输入级 MΩ 级、CMOS/JFET 输入级 GΩ 以上，具体查数据手册的 $R_{in}$（不是"无限大"）。

详见 [同相放大器](../opamp/non-inverting-amplifier.md)、[电源轨与输出摆幅](../opamp/supply-rails.md)。

</details>

<details><summary>用反相加法器对两路信号求和：$R_1=R_2=10\text{k}\Omega$，$R_f=20\text{k}\Omega$，$V_1=0.1\text{V}$，$V_2=0.2\text{V}$。求输出。</summary>

**公式**：$V_{out}=-R_f\left(\dfrac{V_1}{R_1}+\dfrac{V_2}{R_2}\right)$。

**代入**：$\dfrac{0.1}{10\text{k}}=10\ \mu\text{A}$，$\dfrac{0.2}{10\text{k}}=20\ \mu\text{A}$，两路电流之和 $30\ \mu\text{A}$；$V_{out}=-20\text{k}\times30\ \mu\text{A}=-0.6\ \text{V}$。

**结果**：**−0.6V**。每路增益均为 $-R_f/R_i=-2$，注意求和输出天然带负号。

**判据**：反相加法器的优点是各路输入互不影响（都接到虚地），缺点是输入阻抗等于各自的 $R_i$、输出反相；需要同相求和时要用同相求和电路或后级再加一级反相。

详见 [加法器](../opamp/summing-amplifier.md)。

</details>

<details><summary>某运放 $SR=1\text{V}/\mu\text{s}$，要求输出 1V 峰值、100kHz 正弦波。是否会压摆率失真？（正弦最大斜率 $2\pi f V_p$）</summary>

**公式**：所需最大斜率 $=\dfrac{dv}{dt}\Big|_{max}=2\pi fV_p$；判据 $2\pi fV_p\le SR$（工程上留 2 倍余量）。

**代入**：$2\pi\times10^{5}\times1=6.283\times10^{5}\ \text{V/s}=0.628\ \text{V}/\mu\text{s}$。

**结果**：0.628 V/µs < 1 V/µs，**不产生压摆失真**，但余量只有 1.6 倍，低于推荐的 2 倍——批量与温漂下临界。

**边界计算**：满功率带宽 $f_{FPB}=\dfrac{SR}{2\pi V_p}=\dfrac{10^{6}}{2\pi\times1}=159\ \text{kHz}$。所以 100kHz 能过、200kHz 过不了：$2\pi\times2\times10^{5}\times1=1.26\ \text{V}/\mu\text{s}>1\ \text{V}/\mu\text{s}$，输出会被削成接近三角波。

**判据**：小信号看 GBP、大信号看 SR；设计时两个都要算，且 SR 要留 2 倍余量。

详见 [带宽 GBP、压摆率与建立时间](../opamp/gbp-slew-rate.md)。

</details>

<details><summary>一阶有源低通 $R=10\text{k}\Omega$，$C=1\text{nF}$，求截止频率；增益 2 倍时该截止频率是否变化？</summary>

**设定拓扑**（题干必须补全，否则答案不唯一）：RC 网络单独决定一阶极点（输入端 RC 后接同相放大，或反馈网络里 $R$、$C$ 并联），增益由独立电阻网络设定。

**公式**：$f_c=\dfrac{1}{2\pi RC}$。

**代入**：$f_c=\dfrac{1}{2\pi\times10^{4}\times10^{-9}}=\dfrac{1}{6.283\times10^{-5}}=15.9\times10^{3}\ \text{Hz}$。结果：**15.9kHz**。

**增益影响**：一阶 RC 的极点只由 $R$、$C$ 决定，增益不改变 $f_c$；但增益会抬高噪声增益，使运放自身的闭环带宽 $GBP/G_n$ 下降。取 GBP=1MHz、$G_n=2$，运放闭环带宽 500kHz，远高于 15.9kHz，所以 $f_c$ 基本不变。若 GBP 只有 20kHz，运放自身的滚降会先出现，实测 $f_c$ 会低于计算值——**判据：运放闭环带宽至少为滤波器截止频率的 10 倍。**

详见 [一阶滤波器](../opamp/first-order-filters.md)。

</details>

<details><summary>仪放增益电阻 $R_G$ 设定：$G=1+50\text{k}\Omega/R_G$（典型三运放仪放结构）。要求 G=100，求 $R_G$。</summary>

**公式**：$G=1+\dfrac{50\ \text{k}\Omega}{R_G}$。

**代入**：$100=1+\dfrac{50\text{k}}{R_G}$ → $\dfrac{50\text{k}}{R_G}=99$ → $R_G=\dfrac{50\times10^{3}}{99}=505.05\ \Omega$。

**结果**：$R_G\approx505\ \Omega$，取 E96 标称 **499Ω**（实际 $G=1+50000/499=101.2$，增益误差 +1.2%）；要求 0.1% 增益精度时用 0.1% 电阻或精密可调。

**判据**：增益越大 $R_G$ 越小，$R_G$ 的绝对误差（含引线、接触电阻）直接变成增益误差——$G=100$ 时 $R_G$ 上多 1Ω 就是 0.2% 的增益误差，所以 $R_G$ 要短走线、低热电势，必要时用四线开尔文接法。

详见 [仪表放大器](../opamp/instrumentation-amplifier.md)。

</details>

<details><summary>反相放大器 $R_1=10\text{k}\Omega$、$R_f=1\text{M}\Omega$，运放输入偏置电流 $I_B=50\text{nA}$，信号源内阻可忽略、同相端直接接地。求 $I_B$ 造成的输出误差；平衡电阻应取多少？</summary>

**反相端等效电阻**——公式：$R_-=R_1\parallel R_f$。代入：$\dfrac{10\text{k}\times1\text{M}}{10\text{k}+1\text{M}}=9.90\ \text{k}\Omega$。

**输入折算误差**——公式：$V_{err}=I_B\cdot R_-$。代入：$50\ \text{nA}\times9.90\ \text{k}\Omega=495\ \mu\text{V}$。

**输出误差**——公式：$V_{out,err}=V_{err}\left(1+\dfrac{R_f}{R_1}\right)$。代入：$495\ \mu\text{V}\times101=50.0\ \text{mV}$。

**结果**：**约 50mV**。等价简式：$V_{out,err}=I_B\cdot R_f=50\ \text{nA}\times1\ \text{M}\Omega=50\ \text{mV}$（因为 $(R_1\parallel R_f)(1+R_f/R_1)=R_f$），所以**反相放大器的偏置电流误差只看 $R_f$**，与 $R_1$ 无关。

**量级判断**：50mV 对 12 位、5V 量程 ADC（1 LSB=1.22mV）是 41 个码，完全不可接受。

**平衡电阻**：在同相端串 $R_c=R_1\parallel R_f=9.9\ \text{k}\Omega$（取 10kΩ），一阶偏置项被抵消，残余由 $I_{OS}$ 决定。

**解决顺序**：先减小 $R_f$（信号增益不变时同步减小 $R_1$），再选低 $I_B$ 运放（CMOS/JFET 可到 pA 级），最后才考虑平衡电阻。

详见 [失调电压、偏置电流与漂移](../opamp/offset-bias.md)。

</details>

## 四、简答与情景

<details><summary>情景：反相放大器输入接地，输出却停在 +4.8V 不随输入变化。最可能的硬件原因有哪些？</summary>

**现象**：输入 0V，输出贴正轨（+4.8V，接近 5V 电源），调输入毫无反应。

**原因（按概率排序）**：

1. **反馈电阻 $R_f$ 虚焊/未接**：负反馈断开，运放开环，$V_{OS}$ 被放大 $10^5$ 倍，输出必然锁轨。
2. **输入电阻 $R_1$ 开路**：输入信号进不来，反相端只剩 $R_f$ 与漏电流，输入端等效悬空，输出漂到某一轨。
3. **$R_f$ 误接到同相端**：正反馈，输出同样锁轨（而且可能振荡）。
4. **输出对地短路/负载过重**：运放限流，输出偏离正常值。
5. **电源未接/接反/单电源下输入超出共模范围**：输出贴轨。

**排查步骤**：先量电源与地（现象常被误判为"运放坏了"），再断电用万用表量 $R_1$、$R_f$ 的实际阻值与连通性，最后用示波器看输入是否真的到达反相端。

**判据**：输入端为 0 时，理想输出也应为 0（反相结构在 $V_{in}=0$ 时输出为 $0+$ 失调项）；输出贴轨 = 反馈失效或电源异常，先查反馈回路。

详见 [反相比例放大器](../opamp/inverting-amplifier.md)、[排故方法论](../practice/debug-methodology.md)。

</details>

<details><summary>简答：为什么仪表放大器比普通差分放大器 CMRR 更高？</summary>

**核心区别在"共模在哪一级被处理"**：

- **单运放差分放大器**：靠四只电阻的比值匹配把共模减掉。CMRR 上限约 $\dfrac{1+G}{4\delta}$——1% 电阻、$G=1$ 时只有 34dB；0.1% 电阻、$G=1$ 时 54dB；只有 $G=100$ 且 0.1% 电阻才能到 88dB。低增益时电阻容差就是天花板。
- **三运放仪放**：第一级两只同相放大器把差分信号放大 $G_1$ 倍，而共模信号在同相端是"同相跟随"，**第一级对共模的增益接近 1**（不放大）；第二级差分放大器再把残余共模减掉。于是总 CMRR 近似为 $CMRR_{tot}\approx G_1\cdot CMRR_2$（$CMRR_2$ 是第二级的共模抑制比），**增益越高 CMRR 越好**，且匹配在芯片内部完成、不依赖外部四只电阻的精度。实际还受第一级运放自身 CMRR 与芯片内匹配限制，所以不会随增益无限增长。

单片仪放 CMRR 常见 90~120dB（随增益升高），比同价位分立差分高 30~50dB。代价是成本、功耗、带宽（常见几百 kHz~几 MHz）与共模范围限制。

详见 [仪表放大器](../opamp/instrumentation-amplifier.md)、[共模范围、CMRR 与 PSRR](../opamp/cmrr-psrr.md)。

</details>

<details><summary>情景：驱动容性负载（如一段电缆）后，原本稳定的电压跟随器出现高频自激振荡。原因与对策？</summary>

**现象**：输出叠加几十 MHz 的等幅振荡，接上电缆才出现，空载正常；用示波器靠近探头还会改变波形。

**原因**：负载电容 $C_L$ 与运放开环输出电阻 $R_{out,OL}$ 形成第二个极点 $f_{p2}=1/(2\pi R_{out,OL}C_L)$，给环路额外加相位滞后；跟随器的噪声增益是 1，穿越频率 $f_c=GBW/1$ 最高，离 $f_{p2}$ 最近，所以**跟随器最容易因容性负载振荡**。判据：$f_{p2}\ge10f_c$ 才有足够裕量。

**对策（按代价排序）**：

1. **输出串隔离电阻 $R_s$**（几十 Ω），反馈仍取自运放输出脚（$R_s$ 在反馈环外），把 $C_L$ 与输出隔离，$f_{p2}$ 被推到 $1/(2\pi R_sC_L)$ 之外。
2. **前馈电容**：若是有 $R_f$ 的放大结构，在 $R_f$ 上并小电容 $C_f$ 产生零点，抵消输出极点（超前补偿）。
3. **换容性负载稳定型运放**，或在环路内加缓冲器。
4. **提高噪声增益**（不是降低！）：$f_c=GBW/N$ 随 $N=1/\beta$ 反比下降，$N$ 从 1 抬到 2~5 可让 $f_c$ 远离 $f_{p2}$、PM 立刻改善；代价是带宽与噪声变差，跟随器可改接成 $G\ge2$ 的同相结构（此时功能已变）。
5. 输出加 RC 缓冲网络（snubber）吸收高频能量。

**注意**：网上常见的"降低噪声增益可以改善稳定性"是**反的**——降低 $N$ 会让 $f_c$ 升高、更靠近第二极点，PM 更差。

详见 [稳定性与伯德图](../opamp/stability-bode.md)。

</details>

<details><summary>简答：精密整流为什么需要运放配合普通二极管，而不能直接用二极管？</summary>

**原因**：普通硅二极管正向压降 0.6~0.7V，且导通前有一段指数区；mV 级小信号根本推不动它，直接整流会把小信号整段丢掉（小于 $V_F$ 的部分输出为零），大信号也会少掉一个 $V_F$ 的台阶。

**做法（超二极管 / Superdiode）**：把二极管放进运放的反馈环路里。只要 $V_{in}>0$，运放就自动把输出抬高到"让反相端等于同相端"的程度，二极管压降被环路增益"吃掉"——输出精确跟随输入，等效于一只 $V_F\to0$、导通电阻极小的理想二极管。

**代价与边界**：① 过零附近运放要退出饱和、恢复需要时间，高频或小信号下会出现死区与失真；② 单电源供电时要在同相端加偏置，否则负半周无处可去；③ 反相精密整流在 $V_{in}<0$ 时二极管截止，反馈断开，运放饱和，恢复时间决定最高工作频率。改进方案是加第二只二极管钳位防止深度饱和。

详见 [精密整流、峰值检测与采样保持](../opamp/precision-rectifier-peak-samplehold.md)、[二极管电路](../opamp/diode-circuits.md)。
</details>
