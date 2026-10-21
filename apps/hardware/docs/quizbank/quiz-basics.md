---
id: quiz-basics
title: 电路基础测试题
part: 9
chapter: 硬件测试与面试题库
order: 5
tags: [题库, 自测, 电路基础]
difficulty: 2
status: published
sources:
  - TI Precision Labs - Electronics Foundations
  - Horowitz & Hill, The Art of Electronics, 3rd ed.
  - Alexander & Sadiku, Fundamentals of Electric Circuits
---

# 电路基础测试题

本题库覆盖电压/电流/功率、欧姆定律与焦耳定律、串并联分压分流、基尔霍夫定律（KCL/KVL）、RC/RL 时间常数、交流有效值、阻抗与谐振、变压器与三相电、安全用电。题型分为「概念判断」「填空」「计算」「简答与情景」四组，由浅入深。建议先闭卷作答，再展开折叠核对详解。

## 一、概念判断

<details><summary>判断：两点间电位差为 5V，若把参考点（地）向上抬高 3V，则这两点间的电压也变成 8V。</summary>

**错误。**电压是两点电位之差，与参考点（Reference Point）的选取无关。参考点整体抬高 3V，两点电位 $V_A$、$V_B$ 各加 3V，差值 $V_{AB}=V_A-V_B$ 不变，仍为 5V。参考点只改变各点对地电位的绝对值，不改变电路中任意两点间的电压。

</details>

<details><summary>判断：100Ω 电阻流过 2A 电流，其消耗功率为 200W。</summary>

**错误。**题干 200W 少算了一倍，正确功率应为 **400W**。由焦耳定律 $P=I^2R=2^2\times 100=400\text{W}$。补充验算：$V=IR=2\times 100=200\text{V}$，$P=VI=200\times 2=400\text{W}$，三式一致。常见错误是只算 $I\times R$（得 200V，误当成功率），漏掉了再乘一次电流。

</details>

<details><summary>判断：串联电阻越多，总电阻越大；并联电阻越多，总电阻越小。</summary>

**正确。**串联 $R_{eq}=\sum R_i$，并联 $\dfrac{1}{R_{eq}}=\sum\dfrac{1}{R_i}$。并联相当于增大导电截面积，等效电阻比其中最小的一只还小。例如两只 100Ω 并联等效 50Ω。

</details>

<details><summary>判断：在纯电容交流电路中，电流相位超前电压 90°；在纯电感交流电路中，电流相位滞后电压 90°。</summary>

**正确。**电容电流 $i=C\,dv/dt$，正弦电压下电流相位超前 $90^{\circ}$；电感电压 $v=L\,di/dt$，正弦电流下电压相位超前 $90^{\circ}$，即电流滞后电压 $90^{\circ}$。可记为「电容电流跑得快（超前），电感电流跟不上（滞后）」。

</details>

<details><summary>判断：交流市电 220V 指的是峰值电压，其峰值约为 220V。</summary>

**错误。**220V 是有效值（RMS, Root Mean Square）。正弦波峰值 $V_p=\sqrt{2}\,V_{rms}\approx 1.414\times 220\approx 311\text{V}$；峰峰值约 622V。示波器看到的市电波形峰值接近 311V，而万用表交流档读的是有效值 220V。

</details>

<details><summary>判断：理想变压器既能变电压、变电流，也能变功率、提升总能量。</summary>

**错误。**理想变压器只按匝数比 $n=N_1/N_2$ 变换电压（$V_1/V_2=n$）与电流（$I_1/I_2=1/n$），功率守恒 $P_1=P_2$，不产生能量。实际变压器还有铜损、铁损、漏感，效率小于 100%。

</details>

<details><summary>判断：三相市电的相电压是 380V，线电压是 220V。</summary>

**错误。**低压配电中相电压（相线对中性线）为 220V，线电压（两根相线之间）为 $220\times\sqrt{3}\approx 380\text{V}$。关系为 $V_{line}=\sqrt{3}\,V_{phase}$。

</details>

## 二、填空

<details><summary>欧姆定律的表达式为 ____；焦耳定律电阻发热功率为 ____ 或 ____。</summary>

欧姆定律 $V=IR$；电阻发热功率 $P=VI=I^2R=\dfrac{V^2}{R}$。三者在纯电阻上等价，分别适合已知电流、已知电压的不同代入场景。

</details>

<details><summary>RC 电路的时间常数 $\tau=$ ____；RL 电路的时间常数 $\tau=$ ____。RC 充电约经 ____ 个 $\tau$ 后达到稳态值的 99%。</summary>

RC：$\tau=RC$；RL：$\tau=L/R$。RC 充电 $v(t)=V_s(1-e^{-t/\tau})$，约 $5\tau$ 达到稳态的 99%（$e^{-5}\approx 0.0067$）。

</details>

<details><summary>正弦电压有效值与峰值的关系为 $V_{rms}=$ ____；一周期平均值（全波整流后）为 $V_{avg}=$ ____。</summary>

$V_{rms}=V_p/\sqrt{2}\approx 0.707\,V_p$；全波整流平均值 $V_{avg}=2V_p/\pi\approx 0.637\,V_p$。注意平均值只在整流/检波计算中用，仪表精度等级常涉及这两个系数。

</details>

<details><summary>RLC 串联谐振频率 $f_0=$ ____；谐振时电路总阻抗呈 ____ 性，电流达到最 ____。</summary>

$f_0=\dfrac{1}{2\pi\sqrt{LC}}$。谐振时感抗与容抗抵消，$Z=R$ 呈纯阻性，阻抗最小、电流最大。品质因数 $Q=\dfrac{\omega_0 L}{R}=\dfrac{1}{\omega_0 CR}$ 决定谐振峰的尖锐程度。

</details>

<details><summary>基尔霍夫电流定律 KCL：任一节点流入电流之和 ____ 流出电流之和；基尔霍夫电压定律 KVL：任一闭合回路各段电压代数和为 ____。</summary>

KCL：$\sum I_{in}=\sum I_{out}$（节点电荷守恒）；KVL：$\sum V=0$（沿回路电位升降守恒）。二者是一切电路分析（节点法、网孔法）的基石。

</details>

## 三、计算

<details><summary>一只 LED 串联限流电阻接 5V 电源，LED 正向压降 $V_f=2.0\text{V}$，要求流过 LED 的电流为 10mA。求限流电阻阻值与该电阻功耗。</summary>

电阻上压降 $V_R=V_{cc}-V_f=5-2=3\text{V}$。
由欧姆定律 $R=\dfrac{V_R}{I}=\dfrac{3}{0.01}=300\,\Omega$，取标称值 300Ω 或 330Ω。
电阻功耗 $P_R=V_R\cdot I=3\times 0.01=0.03\text{W}$，选 0805（额定 0.125W）即可，降额充足。
若误按 $R=V/I=5/0.01=500\Omega$ 会忽略 LED 压降导致电流偏小。

</details>

<details><summary>用两只电阻 $R_1=10\text{k}\Omega$、$R_2=30\text{k}\Omega$ 串联在 12V 上，求 $R_2$ 上分得的电压；若改为并联接 12V，求总电流。</summary>

串联分压：$V_{R2}=V_{cc}\cdot\dfrac{R_2}{R_1+R_2}=12\times\dfrac{30}{10+30}=9\text{V}$。
并联：等效电阻 $R_{eq}=\dfrac{R_1 R_2}{R_1+R_2}=\dfrac{10\times 30}{10+30}=7.5\text{k}\Omega$，总电流 $I=\dfrac{12}{7.5\text{k}}=1.6\text{mA}$。
串联时电流处处相等 $I=12/40\text{k}=0.3\text{mA}$；并联时各支路电压相等、电流相加。

</details>

<details><summary>RC 电路 $R=10\text{k}\Omega$，$C=1\,\mu\text{F}$，从 0V 接到 5V 阶跃电源。求时间常数 $\tau$，以及 $t=20\text{ms}$ 时电容两端电压。</summary>

$\tau=RC=10\text{k}\times 1\,\mu=10\times 10^3\times 1\times 10^{-6}=0.01\text{s}=10\text{ms}$。
充电公式 $v_C(t)=V_s(1-e^{-t/\tau})=5(1-e^{-20/10})=5(1-e^{-2})$。
$e^{-2}\approx 0.135$，故 $v_C\approx 5\times(1-0.135)=5\times 0.865\approx 4.33\text{V}$。
即两个时间常数后充到约 86.5%。

</details>

<details><summary>RL 电路 $V_s=12\text{V}$，$R=120\,\Omega$，$L=12\text{mH}$。求稳态电流与时间常数 $\tau$。</summary>

稳态时电感相当于短路，$I_{ss}=\dfrac{V_s}{R}=\dfrac{12}{120}=0.1\text{A}=100\text{mA}$。
$\tau=\dfrac{L}{R}=\dfrac{12\text{mH}}{120\,\Omega}=0.0001\text{s}=100\,\mu\text{s}$。
电流上升规律 $i(t)=I_{ss}(1-e^{-t/\tau})$，约 $5\tau=500\,\mu\text{s}$ 达到稳态。

</details>

<details><summary>某正弦电压 $v(t)=10\sin(2\pi\cdot 1000\,t)\text{V}$（峰值 10V）。求其有效值与频率。若接 $R=100\,\Omega$ 电阻，电阻上消耗功率多少？</summary>

峰值 $V_p=10\text{V}$，有效值 $V_{rms}=V_p/\sqrt{2}\approx 7.07\text{V}$。
频率 $f=1000\text{Hz}=1\text{kHz}$。
电阻功率 $P=\dfrac{V_{rms}^2}{R}=\dfrac{7.07^2}{100}=\dfrac{50}{100}=0.5\text{W}$。
（也可 $P=V_{rms}^2/R=(V_p^2/2)/R=100/(2\times100)=0.5\text{W}$。）

</details>

<details><summary>LC 回路 $L=100\,\mu\text{H}$，$C=100\text{nF}$。求谐振频率 $f_0$；若串联 $R=1\,\Omega$，求品质因数 $Q$。</summary>

$f_0=\dfrac{1}{2\pi\sqrt{LC}}=\dfrac{1}{2\pi\sqrt{100\times 10^{-6}\times 100\times 10^{-9}}}$。
$LC=100\times10^{-6}\times100\times10^{-9}=10^{-11}$，$\sqrt{LC}\approx 3.16\times 10^{-6}\text{s}$。
$f_0=\dfrac{1}{2\pi\times 3.16\times 10^{-6}}\approx 50.3\text{kHz}$。
$\omega_0=2\pi f_0\approx 3.16\times 10^5\text{rad/s}$，$Q=\dfrac{\omega_0 L}{R}=\dfrac{3.16\times10^5\times 100\times10^{-6}}{1}\approx 31.6$。
Q 值较高，谐振峰尖锐，选频特性好。

</details>

## 四、简答与情景

<details><summary>情景：面包板上一只 1/4W、1kΩ 电阻接 12V，摸上去发烫。它是否安全？请定量判断。</summary>

电阻功耗 $P=\dfrac{V^2}{R}=\dfrac{12^2}{1000}=0.144\text{W}$。
额定 1/4W=0.25W，占比 $0.144/0.25=58\%$。一般可靠性设计要求降额到额定的 50% 以下，此处已接近极限，且密闭/高温环境下温升更大。
结论：短时间不烧毁，但偏热；应换 0.5W 电阻或增大阻值。**教训：小功率电阻不能只看「不烧」，要看降额与温升。**

</details>

<details><summary>简答：为什么电器金属外壳要接保护接地（PE）？人体触电时哪条路径最危险？</summary>

保护接地（Protective Earth, PE）把金属外壳与大地可靠连接，当绝缘破损使外壳带电时，电流经低阻 PE 线入地，使漏电保护（RCD/漏电断路器）跳闸或把外壳电位钳到接近地电位，避免电流经人体入地。
最危险的是「手—脚」路径（电流经过心脏区域），工频 50/60Hz、数十毫安即可致室颤。因此湿手操作、站在地上触电最危险；干燥时站在绝缘垫上、穿绝缘鞋可大幅降低触电电流。

</details>

<details><summary>情景：用万用表测一节电池电压，量程误拨在电流档，两表笔直接并在电池两端，会发生什么？为什么禁止这样做？</summary>

电流档内阻极低（近乎短路），表笔并在电池两端相当于把电池经电流表短路，极大的短路电流会烧断万用表内部保险丝，甚至损伤表头/电池。
**正确做法**：测电压时并联在被测点（高内阻），测电流时必须把表**串**入电路（断开一处导线再串入）。这是入门者最易犯、也最易损表的错误。

</details>
