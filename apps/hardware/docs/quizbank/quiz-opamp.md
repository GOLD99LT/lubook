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
  - TI, Op Amps for Everyone (Ron Mancini)
  - TI Precision Labs - Op Amps
  - Analog Devices MT Application Notes
---

# 模拟电路与运放测试题

本题库覆盖虚短虚断、反相/同相/电压跟随器/差分/仪表放大器、加法器、积分微分、有源滤波器、比较器与迟滞、振荡器、555 定时器、精密整流，以及噪声/失调/GBP/压摆率/稳定性等运放非理想参数。题型分为「概念判断」「填空」「计算」「简答与情景」四组。

## 一、概念判断

<details><summary>判断：只要给运放接上负反馈，反相端与同相端电位就严格相等（虚短），与运放开环增益无关。</summary>

**近似正确但需理解前提。**虚短成立的前提是深度负反馈（环路增益 $T=A_{OL}\beta\gg 1$）。真实运放 $V_{out}=A_{OL}(V_+-V_-)$，故 $V_+-V_-=V_{out}/A_{OL}$；$A_{OL}$ 越大（$10^5\sim 10^6$），两端偏差越小。开环（无反馈）时运放不是放大器，输出锁在电源轨，虚短不成立。

</details>

<details><summary>判断：电压跟随器增益为 1，所以它没什么用，不如直接用导线连接。</summary>

**错误。**电压跟随器（Voltage Follower）增益为 1，但输入阻抗极高、输出阻抗极低，作用是「缓冲（Buffer）」：不让高内阻信号源被后级低负载拉低。它常接在传感器/分压网络与 ADC 之间，避免负载效应。

</details>

<details><summary>判断：反相放大器的输入阻抗等于反馈电阻 Rf；同相放大器的输入阻抗很高。</summary>

**错误。**反相放大器输入阻抗等于输入电阻 $R_1$（反相端虚地）；同相放大器输入阻抗极高（接运放同相端）。需要高输入阻抗时优先用同相结构。

</details>

<details><summary>判断：比较器工作在开环（或正反馈）状态，输出在两个电源轨之间切换，不是线性放大器。</summary>

**正确。**比较器（Comparator）把两输入端电压直接比较，开环高增益使输出饱和到正/负电源轨。加正反馈构成迟滞比较器（Schmitt Trigger），可抗噪声、加速翻转。普通运放也能做简单比较器，但速度慢、无输出级设计，专用比较器更快更可靠。

</details>

<details><summary>判断：运放的增益带宽积 GBP 在某型号上近似为常数，增益越大，带宽越小。</summary>

**正确。**GBP（Gain-Bandwidth Product）≈ 常数，如 GBP=1MHz 时闭环增益 100 倍对应带宽 $f_c=1\text{MHz}/100=10\text{kHz}$。这就是「增益—带宽互换」。

</details>

<details><summary>判断：压摆率 SR 只影响小信号带宽，与大信号高速输出无关。</summary>

**错误。**压摆率（Slew Rate）是大信号参数，限定输出电压最大变化速率（V/μs）。高频大信号若要求 $dv/dt$ 超过 SR，输出斜率被削、产生失真。正弦波最大斜率 $2\pi f V_p$ 须小于 SR。

</details>

<details><summary>判断：仪表放大器（Instrumentation Amplifier）高输入阻抗、高共模抑制比，适合放大小差分信号并抑制共模干扰。</summary>

**正确。**仪放通常由三运放构成，两级高输入阻抗 + 一级差分，靠一只增益电阻设增益，CMRR 可达 100dB 以上，适合电桥、热电偶、生物电等小差分、大共模信号。

</details>

<details><summary>判断：积分器在直流输入下输出会一直积分直到饱和，因此实际积分器必须并联反馈电阻或加复位开关。</summary>

**正确。**理想积分器对直流失调 $V_{OS}$ 持续积分，输出漂移到电源轨饱和。实际电路在反馈电容上并联大电阻提供直流反馈（泄漏电阻），或加电子复位开关。

</details>

## 二、填空

<details><summary>反相放大器增益 $G=$ ____；同相放大器增益 $G=$ ____；电压跟随器增益 $G=$ ____。</summary>

反相：$G=-R_f/R_1$；同相：$G=1+R_f/R_1$；跟随器：$G=1$。反相放大器噪声增益（同相端看进去的增益）为 $1+R_f/R_1$，带宽按噪声增益算。

</details>

<details><summary>差分放大器要获得高 CMRR，要求四个电阻 ____；CMRR 与电阻匹配精度 $\delta$ 的关系约为 $CMRR\approx$ ____。</summary>

四个电阻精确匹配（两臂比值相等）。近似 $CMRR\approx (1+R_f/R_1)/(2\delta)$，电阻失配 $\delta$ 越小，CMRR 越高。用精密电阻或集成仪放保证匹配。

</details>

<details><summary>一阶 RC 低通截止频率 $f_c=$ ____；二阶 Sallen-Key 滤波器的阻尼由 ____ 决定，Q 值过高会 ____。</summary>

$f_c=1/(2\pi RC)$。Sallen-Key 的阻尼由增益与电阻比值决定；Q 值过高在 $f_c$ 处出现尖峰（振铃），设计时取 Q≈0.707（巴特沃斯）获得最平坦幅频。

</details>

<details><summary>555 多谐振荡周期 $T\approx$ ____；占空比由两只定时电阻决定，要实现 <50% 占空比需 ____。</summary>

$T\approx 0.693(R_A+2R_B)C$（高电平 $0.693(R_A+R_B)C$、低电平 $0.693R_B C$）。普通接法占空比恒 >50%；要 <50% 需在 **RB 两端**（7 脚 DIS 与 6/2 脚之间）加二极管旁路 $R_B$，让充电路径只走 $R_A$：此时 $t_{high}=0.693R_A C$、$t_{low}=0.693R_B C$，$D=R_A/(R_A+R_B)$。

</details>

<details><summary>运放非理想三参数：输入失调电压 $V_{OS}$、输入偏置电流 $I_B$、输入失调电流 $I_{OS}$。BJT 输入级 $I_B$ 较 ____，CMOS 输入级 $I_B$ 极 ____。</summary>

BJT 输入级 $I_B$ 较大（nA 级）；CMOS/JFET 输入级 $I_B$ 极小（pA~fA 级）。高阻信号源选 CMOS/JFET 输入运放以避免偏置电流误差。

</details>

## 三、计算

<details><summary>反相放大器 $R_1=10\text{k}\Omega$，$R_f=100\text{k}\Omega$，输入 $V_{in}=0.2\text{V}$。求输出；若运放 GBP=1MHz，求闭环小信号带宽。</summary>

增益 $G=-R_f/R_1=-10$，$V_{out}=-10\times 0.2=-2\text{V}$。
噪声增益 $G_n=1+R_f/R_1=11$，带宽 $f_c=GBP/G_n=1\text{MHz}/11\approx 91\text{kHz}$。
注意带宽按噪声增益 11 算，而非信号增益 10。

</details>

<details><summary>同相放大器 $R_1=1\text{k}\Omega$，$R_f=9\text{k}\Omega$。求增益；若输入 0.5V，输出多少？该电路输入阻抗数量级如何？</summary>

$G=1+R_f/R_1=1+9=10$，$V_{out}=10\times 0.5=5\text{V}$（需供电轨 ≥5V 留摆幅余量）。同相结构输入阻抗极高（MΩ~GΩ 级，由运放输入级决定），适合高内阻传感器。

</details>

<details><summary>用反相加法器对两路信号求和：$R_1=R_2=10\text{k}\Omega$，$R_f=20\text{k}\Omega$，$V_1=0.1\text{V}$，$V_2=0.2\text{V}$。求输出。</summary>

反相加法器 $V_{out}=-R_f(V_1/R_1+V_2/R_2)=-20\text{k}(0.1/10\text{k}+0.2/10\text{k})=-2\times(0.1+0.2)=-0.6\text{V}$。
两路增益均为 $-R_f/R_i=-2$，注意反相求和输出带负号。

</details>

<details><summary>某运放 $SR=1\text{V}/\mu\text{s}$，要求输出 1V 峰值、100kHz 正弦波。是否会压摆率失真？（正弦最大斜率 $2\pi f V_p$）</summary>

要求最大斜率 $2\pi f V_p=2\pi\times 10^5\times 1\approx 6.28\times 10^5\text{V/s}=0.628\text{V}/\mu\text{s}$。
SR=1V/μs > 0.628V/μs，满足，无明显压摆失真。
若频率升到 200kHz，要求 $2\pi\times 2\times10^5\times1=1.26\text{V}/\mu\text{s}>1\text{V}/\mu\text{s}$，则出现压摆受限失真。**大信号设计必须同时核对 GBP（小信号）与 SR（大信号）。**

</details>

<details><summary>一阶有源低通 $R=10\text{k}\Omega$，$C=1\text{nF}$，求截止频率；增益 2 倍时该截止频率是否变化？</summary>

$f_c=1/(2\pi RC)=1/(2\pi\times10^4\times10^{-9})=1/(6.28\times10^{-5})\approx 15.9\text{kHz}$。
一阶 RC 的 $f_c$ 只由 $R$、$C$ 决定，与增益无关（增益由同相放大倍数决定）；但若增益过高、运放带宽不足，实际高频衰减会提前。

</details>

<details><summary>仪放增益电阻 $R_G$ 设定：$G=1+50\text{k}\Omega/R_G$（典型三运放仪放结构）。要求 G=100，求 $R_G$。</summary>

$100=1+50\text{k}/R_G\Rightarrow R_G=50\text{k}/99\approx 505\,\Omega$，取标称 499Ω 或精密可调。增益越大 $R_G$ 越小，高增益时 $R_G$ 取值精度直接影响增益精度。

</details>

## 四、简答与情景

<details><summary>情景：反相放大器输入接地，输出却停在 +4.8V 不随输入变化。最可能的硬件原因有哪些？</summary>

(1) 反馈电阻 $R_f$ 虚焊/未接，运放开环工作输出锁轨；(2) $R_f$ 误接到同相端形成正反馈；(3) 输出对地短路或负载过重；(4) 运放电源未接/接反；(5) 失调电压过大叠加增益使输出饱和。优先检查反馈回路与供电。

</details>

<details><summary>简答：为什么仪表放大器比普通差分放大器 CMRR 更高？</summary>

普通单运放差分放大器靠四个电阻匹配，CMRR 受电阻精度限制（约 60~80dB）。三运放仪放第一级是两个同相放大器（高输入阻抗），第二级差分；增益主要由第一级决定，共模信号在第一级不被放大，差分信号被放大，因此 CMRR 可达 100dB 以上，且增益越高 CMRR 越好。

</details>

<details><summary>情景：驱动容性负载（如一段电缆）后，原本稳定的电压跟随器出现高频自激振荡。原因与对策？</summary>

容性负载与运放输出电阻在环路中引入额外极点，相位裕度下降导致自激。对策：(1) 输出端串小电阻（几十 Ω）把负载电容与运放隔离开，分离极点；(2) 在反馈电阻上并小电容（超前补偿）；(3) 选「容性负载稳定」型运放；(4) 减小噪声增益。

</details>

<details><summary>简答：精密整流为什么需要运放配合普通二极管，而不能直接用二极管？</summary>

普通硅二极管正向压降约 0.6~0.7V，mV 级小信号根本无法导通，直接整流会丢失小信号。把二极管放在运放反馈环路内，运放自身增益抵消二极管压降——输入 $V_{in}$ 哪怕很小，输出也会自动抬高 $V_D$ 使整流后输出精确跟随 $V_{in}$，实现「超二极管（Superdiode）」精密整流。

</details>
