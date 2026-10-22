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
  - Horowitz & Hill, The Art of Electronics, 3rd ed. — Chapter 1 Foundations（电压电流、功率、RC/RL、交流与有效值）
  - Alexander & Sadiku, Fundamentals of Electric Circuits — Chapter 1 Basic Concepts、Chapter 9 Sinusoids and Phasors、Chapter 14 Frequency Response
  - TI Precision Labs - Electronics Foundations — 直流电路、分压器带载与 RC 充电系列
  - IEC 60038:2009 IEC 标准电压 — 220 V 相电压与 380 V 线电压的定义与容差
  - IEC 60479-1:2018 电流对人和家畜的效应 — 人体阻抗、电流路径与工频心室纤维性颤动的电流-时间阈值
---

# 电路基础测试题

本题库覆盖电压/电流/功率、欧姆定律与焦耳定律、串并联分压分流、基尔霍夫定律（KCL/KVL）、RC/RL 时间常数、交流有效值、阻抗与谐振、变压器与三相电、安全用电。题型分为「概念判断」「填空」「计算」「简答与情景」四组，由浅入深。建议先闭卷作答，再展开折叠核对详解。

**核对口径**：概念题给**判据**（一句话能判断对错的那条式子或定义），不给"一般如此"；数字题一律给**公式 → 代入 → 结果 → 单位**四步。每个答案末尾给出对应的正文出处，便于追到推导。

## 一、概念判断

<details><summary>判断：两点间电位差为 5V，若把参考点（地）向上抬高 3V，则这两点间的电压也变成 8V。</summary>

**错误。**电压是两点电位之差，与参考点（Reference Point）的选取无关。

判据：$V_{AB}=V_A-V_B$。参考点整体抬高 3V，$V_A$、$V_B$ 各加 3V，差值 $(V_A+3)-(V_B+3)=V_A-V_B$ 不变，仍为 5V。参考点只改变各点对地电位的绝对值，不改变电路中任意两点间的电压。

详见 [电压、电流与功率](../basics/voltage-current-power.md)。

</details>

<details><summary>判断：100Ω 电阻流过 2A 电流，其消耗功率为 200W。</summary>

**错误。**题干少算了 200W（差 2 倍），正确功率为 **400W**。

判据：焦耳定律 $P=I^2R$。代入 $P=2^2\times 100=400\ \text{W}$。

交叉验算：$V=IR=2\times 100=200\ \text{V}$，$P=VI=200\times 2=400\ \text{W}$，与 $P=V^2/R=200^2/100=400\ \text{W}$ 三式一致。常见错误是只算 $I\times R$（得 200V，误当成功率），漏掉再乘一次电流。

详见 [欧姆定律与焦耳定律](../basics/ohms-law.md)。

</details>

<details><summary>判断：串联电阻越多，总电阻越大；并联电阻越多，总电阻越小。</summary>

**正确。**串联 $R_{eq}=\sum R_i$，并联 $\dfrac{1}{R_{eq}}=\sum\dfrac{1}{R_i}$。

判据：并联相当于增大导电截面积，等效电阻必然小于其中**最小的一只**。两只 100Ω 并联得 $R_{eq}=50\ \Omega$，小于 100Ω，这个"比最小的还小"是可以秒判的检查点。

详见 [串联与并联](../basics/series-parallel.md)。

</details>

<details><summary>判断：在纯电容交流电路中，电流相位超前电压 90°；在纯电感交流电路中，电流相位滞后电压 90°。</summary>

**正确。**判据是元件自身的 $v$-$i$ 关系：电容 $i=C\,dv/dt$，正弦电压下电流相位超前 $90^{\circ}$；电感 $v=L\,di/dt$，正弦电流下电压相位超前 $90^{\circ}$，即电流滞后电压 $90^{\circ}$。

口诀：电容电流跑得快（超前），电感电流跟不上（滞后）。用阻抗写更清楚：$Z_C=1/(j\omega C)=-j/(\omega C)$，$Z_L=j\omega L$，$j$ 即 $+90^{\circ}$ 旋转。

详见 [交流与直流、相量与阻抗](../basics/dc-ac.md)。

</details>

<details><summary>判断：交流市电 220V 指的是峰值电压，其峰值约为 220V。</summary>

**错误。**220V 是**有效值**（RMS, Root Mean Square），不是峰值。

判据：正弦波 $V_p=\sqrt{2}\,V_{rms}$。代入 $V_p=1.414\times 220\approx 311\ \text{V}$，峰峰值 $2V_p\approx 622\ \text{V}$。

两个补充判据：(1) 万用表交流档按正弦有效值标定，读 220V 表示有效值；测非正弦（如可控硅调光、变频器输出）时会严重偏小，需要 True-RMS 表。(2) 电网电压有容差，按上限 240V 算峰值是 $1.414\times240\approx 339\ \text{V}$，选整流桥、X 电容、光耦的耐压要按这个上限留余量，不能按 311V 算。

详见 [交流与直流、相量与阻抗](../basics/dc-ac.md)。

</details>

<details><summary>判断：理想变压器既能变电压、变电流，也能变功率、提升总能量。</summary>

**错误。**理想变压器按匝数比 $n=N_1/N_2$ 变换电压（$V_1/V_2=n$）与电流（$I_1/I_2=1/n$），功率守恒 $P_1=P_2$，**不产生也不放大能量**。

判据：$V_1I_1=V_2I_2$ 是理想变压器的功率约束；升压必然降流，降压必然升流。所谓"变压器省电"是误把电流比当成功率比。

实际变压器还有铜损（绕组电阻）、铁损（磁滞与涡流）、漏感（耦合不完全），效率小于 100%——小功率变压器约 80%~95%，大功率可到 98% 以上，具体看数据手册。

详见 [变压器](../basics/transformer.md)。

</details>

<details><summary>判断：三相市电的相电压是 380V，线电压是 220V。</summary>

**错误，说反了。**低压配电中相电压（相线对中性线）为 220V，线电压（两根相线之间）为 $220\times\sqrt{3}\approx 380\ \text{V}$。

判据：三相星形接法下，两个相位差 $120^{\circ}$ 的相电压相减，幅值为 $2V_{ph}\sin 60^{\circ}=\sqrt{3}V_{ph}$。代入 $\sqrt{3}\times220=381\ \text{V}$，工程上称 380V。

记忆锚点：**"220 对零线，380 对相线"**；线电压永远是相电压的 $\sqrt{3}$ 倍（星形接法）。

详见 [市电与三相电](../basics/mains-three-phase.md)。

</details>

<details><summary>判断：用万用表电阻档可以在通电的电路上直接测量电阻，读数不受影响。</summary>

**错误。**电阻档靠表内电池向被测支路注入电流、测压降反算阻值，通电电路上表内电源与电路电压叠加，读数无意义，严重时会损坏万用表。

判据：测电阻必须满足两个条件——**断电**、**被测元件与并联支路断开**（至少一端脱开）。板上直接量一只电阻，读数实际是它和所有并联路径的等效值，只能更小、不会更大，这是"量出来永远偏小"的原因。

现象：在路测 10kΩ 读数 3kΩ，拆下来一量正好 10kΩ。原因：并联支路分流。解决：脱开一端或断电后单点测量。

详见 [数字万用表](../practice/multimeter.md)。

</details>

## 二、填空

<details><summary>欧姆定律的表达式为 ____；焦耳定律电阻发热功率为 ____ 或 ____。</summary>

欧姆定律 $V=IR$；电阻发热功率 $P=VI=I^2R=\dfrac{V^2}{R}$。

三式在纯电阻上等价，按已知量选最省事的一式：已知电流用 $I^2R$，已知电压用 $V^2/R$，已知两者用 $VI$。注意 $P=VI$ 只在**纯电阻**上等于发热功率；含电容、电感的电路里 $VI$ 是视在功率，发热只由 $I^2R$ 决定。

详见 [欧姆定律与焦耳定律](../basics/ohms-law.md)。

</details>

<details><summary>RC 电路的时间常数 $\tau=$ ____；RL 电路的时间常数 $\tau=$ ____。RC 充电约经 ____ 个 $\tau$ 后达到稳态值的 99%。</summary>

RC：$\tau=RC$；RL：$\tau=L/R$。

判据与数值：$v(t)=V_s(1-e^{-t/\tau})$，令 $1-e^{-t/\tau}=0.99$ 得 $t=-\tau\ln 0.01=4.6\tau$；工程上取 **5τ**，此时 $e^{-5}\approx 0.0067$，即到 99.3%。

顺序记法：**RC 是"乘"（$RC$），RL 是"除"（$L/R$）**，两者单位都是秒（$\Omega\cdot\text{F}=\text{s}$，$\text{H}/\Omega=\text{s}$）。

详见 [RC 充放电与时间常数](../basics/capacitor-rc.md)、[RL 暂态与时间常数](../basics/inductor-rl.md)。

</details>

<details><summary>正弦电压有效值与峰值的关系为 $V_{rms}=$ ____；一周期平均值（全波整流后）为 $V_{avg}=$ ____。</summary>

$V_{rms}=V_p/\sqrt{2}\approx 0.707\,V_p$；全波整流平均值 $V_{avg}=2V_p/\pi\approx 0.637\,V_p$。

判据：有效值按"同功率"定义，$V_{rms}=\sqrt{\frac{1}{T}\int_0^T v^2dt}$，正弦积分得 $V_p/\sqrt{2}$；平均值是绝对值在一个周期内的均值。

两个派生系数：波形因数 $K_f=V_{rms}/V_{avg}=0.707/0.637\approx1.11$；峰值因数 $K_p=V_p/V_{rms}=\sqrt{2}\approx1.414$。万用表的"AC 档精度"就是按这两个系数标定的，所以非正弦波形读数不可信。

详见 [交流与直流、相量与阻抗](../basics/dc-ac.md)。

</details>

<details><summary>RLC 串联谐振频率 $f_0=$ ____；谐振时电路总阻抗呈 ____ 性，电流达到最 ____。</summary>

$f_0=\dfrac{1}{2\pi\sqrt{LC}}$。

判据：谐振时 $\omega_0 L=1/(\omega_0 C)$，感抗与容抗大小相等、符号相反，$Z=R$ 呈纯阻性，阻抗最小、电流最大。

品质因数 $Q=\dfrac{\omega_0 L}{R}=\dfrac{1}{\omega_0 CR}=\dfrac{1}{R}\sqrt{\dfrac{L}{C}}$，它同时给出带宽：$BW=f_0/Q$。Q 越高谐振峰越尖、选择性越好，但通带越窄。

详见 [RLC 谐振](../basics/rlc-resonance.md)。

</details>

<details><summary>基尔霍夫电流定律 KCL：任一节点流入电流之和 ____ 流出电流之和；基尔霍夫电压定律 KVL：任一闭合回路各段电压代数和为 ____。</summary>

KCL：$\sum I_{in}=\sum I_{out}$（节点电荷守恒）；KVL：$\sum V=0$（沿回路电位升降守恒）。

判据的本质：KCL 是**电荷守恒**（节点不能积累电荷），KVL 是**能量守恒**（绕一圈回到原点，电位必须回到同一值）。二者是一切电路分析（节点法、网孔法）的基石，且与元件是否线性无关。

详见 [基尔霍夫定律](../basics/kcl-kvl.md)。

</details>

## 三、计算

<details><summary>一只 LED 串联限流电阻接 5V 电源，LED 正向压降 $V_f=2.0\text{V}$，要求流过 LED 的电流为 10mA。求限流电阻阻值与该电阻功耗。</summary>

**公式**：$R=\dfrac{V_{cc}-V_f}{I}$，$P_R=(V_{cc}-V_f)I$。

**代入**：$V_R=5-2=3\ \text{V}$，$R=\dfrac{3}{0.01}=300\ \Omega$。

**结果**：$R=300\ \Omega$（E24 标称值有 300Ω；取 330Ω 时 $I=3/330=9.1\ \text{mA}$，仍可用）。

**功耗**：$P_R=3\times 0.01=0.03\ \text{W}$。选 0805（额定 0.125W）时占额定 24%，降额充足；0402（0.0625W）也能用，但 85°C 环境下额定会降到约 0.05W，余量只剩 40%。

**常见错误**：按 $R=V_{cc}/I=5/0.01=500\ \Omega$ 计算，忽略 LED 压降，实际电流只有 $(5-2)/500=6\ \text{mA}$，亮度明显偏暗。

详见 [电阻器：参数、选型与降额](../components/resistors.md)。

</details>

<details><summary>用两只电阻 $R_1=10\text{k}\Omega$、$R_2=30\text{k}\Omega$ 串联在 12V 上，求 $R_2$ 上分得的电压；若改为并联接 12V，求总电流。</summary>

**串联分压**——公式：$V_{R2}=V_{cc}\dfrac{R_2}{R_1+R_2}$。

代入：$V_{R2}=12\times\dfrac{30}{10+30}=12\times0.75=9\ \text{V}$。结果：$R_2$ 上 9V（$R_1$ 上 3V，两段之和等于 12V，可作验算）。

**并联总电流**——公式：$R_{eq}=\dfrac{R_1R_2}{R_1+R_2}$，$I=\dfrac{V_{cc}}{R_{eq}}$。

代入：$R_{eq}=\dfrac{10\times30}{10+30}=7.5\ \text{k}\Omega$，$I=\dfrac{12}{7.5\times10^3}=1.6\times10^{-3}\ \text{A}$。结果：总电流 1.6mA（两条支路分别 1.2mA 与 0.4mA，相加为 1.6mA）。

**对照**：串联时电流处处相等 $I=12/40\text{k}=0.3\ \text{mA}$；并联时各支路电压相等、电流相加。分压看电阻比，分流看电阻反比。

详见 [串联与并联](../basics/series-parallel.md)。

</details>

<details><summary>RC 电路 $R=10\text{k}\Omega$，$C=1\,\mu\text{F}$，从 0V 接到 5V 阶跃电源。求时间常数 $\tau$，以及 $t=20\text{ms}$ 时电容两端电压。</summary>

**公式**：$\tau=RC$，$v_C(t)=V_s(1-e^{-t/\tau})$。

**代入**：$\tau=10\times10^3\times1\times10^{-6}=0.01\ \text{s}=10\ \text{ms}$；$t/\tau=20/10=2$。

$v_C=5(1-e^{-2})=5(1-0.1353)=5\times0.8647=4.32\ \text{V}$。

**结果**：$\tau=10\ \text{ms}$，$t=20\ \text{ms}$ 时 $v_C\approx4.32\ \text{V}$，即充到 86.5%。

**判据表**：1τ→63.2%，2τ→86.5%，3τ→95.0%，5τ→99.3%。看到"两个时间常数"就要立刻想到 86.5% 而不是"充满了"。

详见 [RC 充放电与时间常数](../basics/capacitor-rc.md)。

</details>

<details><summary>RL 电路 $V_s=12\text{V}$，$R=120\,\Omega$，$L=12\text{mH}$。求稳态电流与时间常数 $\tau$。</summary>

**稳态电流**——公式：稳态时电感相当于短路，$I_{ss}=\dfrac{V_s}{R}$。

代入：$I_{ss}=12/120=0.1\ \text{A}$。结果：**100mA**。

**时间常数**——公式：$\tau=\dfrac{L}{R}$。

代入：$\tau=\dfrac{12\times10^{-3}}{120}=1\times10^{-4}\ \text{s}$。结果：$\tau=100\ \mu\text{s}$。

电流上升规律 $i(t)=I_{ss}(1-e^{-t/\tau})$，约 $5\tau=500\ \mu\text{s}$ 达到稳态的 99.3%。判据：电感的"惯性"是阻碍电流变化，所以稳态看短路（$V_L=0$），暂态看时间常数 $L/R$。

详见 [RL 暂态与时间常数](../basics/inductor-rl.md)。

</details>

<details><summary>某正弦电压 $v(t)=10\sin(2\pi\cdot 1000\,t)\text{V}$（峰值 10V）。求其有效值与频率。若接 $R=100\,\Omega$ 电阻，电阻上消耗功率多少？</summary>

**有效值**——公式：$V_{rms}=V_p/\sqrt{2}$。代入：$V_{rms}=10/1.414=7.07\ \text{V}$。

**频率**——公式：$\omega=2\pi f$。代入：$2\pi f=2\pi\times1000$，故 $f=1000\ \text{Hz}=1\ \text{kHz}$；周期 $T=1\ \text{ms}$。

**功率**——公式：$P=V_{rms}^2/R$。代入：$P=7.07^2/100=50/100=0.5\ \text{W}$。结果：**0.5W**。

也可用峰值直接算：$P=V_p^2/(2R)=100/200=0.5\ \text{W}$，两式一致。注意功率必须用有效值，直接用峰值会算成 1W（大 2 倍）。

详见 [交流与直流、相量与阻抗](../basics/dc-ac.md)。

</details>

<details><summary>LC 回路 $L=100\,\mu\text{H}$，$C=100\text{nF}$。求谐振频率 $f_0$；若串联 $R=1\,\Omega$，求品质因数 $Q$。</summary>

**谐振频率**——公式：$f_0=\dfrac{1}{2\pi\sqrt{LC}}$。

代入：$LC=100\times10^{-6}\times100\times10^{-9}=1\times10^{-11}\ \text{s}^2$；$\sqrt{LC}=3.162\times10^{-6}\ \text{s}$；$f_0=\dfrac{1}{2\pi\times3.162\times10^{-6}}=50.3\times10^{3}\ \text{Hz}$。

结果：$f_0\approx50.3\ \text{kHz}$，$\omega_0=2\pi f_0=3.16\times10^{5}\ \text{rad/s}$。

**品质因数**——公式：$Q=\dfrac{\omega_0 L}{R}$。

代入：$Q=\dfrac{3.16\times10^{5}\times100\times10^{-6}}{1}=31.6$。结果：**Q≈31.6**。

交叉验算：$Q=\frac{1}{R}\sqrt{L/C}=\sqrt{100\times10^{-6}/100\times10^{-9}}=\sqrt{1000}=31.6$，一致。$Q=31.6$ 对应带宽 $BW=f_0/Q=50.3\text{k}/31.6\approx1.59\ \text{kHz}$，谐振峰尖锐、选频好。

详见 [RLC 谐振](../basics/rlc-resonance.md)。

</details>

<details><summary>用 $R_1=R_2=10\text{k}\Omega$ 从 12V 分压得到 6V，接到一个 $10\text{k}\Omega$ 负载上。求实际输出电压与相对误差；负载至少多大时误差可控制在 1% 以内？</summary>

**空载**——公式：$V_{o,open}=V_{cc}\dfrac{R_2}{R_1+R_2}$。代入：$12\times\dfrac{10}{20}=6\ \text{V}$。

**带载**——公式：$R_2'=R_2\parallel R_L$，$V_o=V_{cc}\dfrac{R_2'}{R_1+R_2'}$。

代入：$R_2'=\dfrac{10\times10}{10+10}=5\ \text{k}\Omega$，$V_o=12\times\dfrac{5}{10+5}=4\ \text{V}$。

结果：实际 **4V**，相对误差 $\dfrac{4-6}{6}=-33.3\%$——分压比完全变了。

**判据**：分压器输出阻抗 $R_o=R_1\parallel R_2=5\ \text{k}\Omega$，负载引入的相对误差约 $R_o/R_L$。要求 ≤1% 需 $R_L\ge100R_o=500\ \text{k}\Omega$（取 500kΩ 验算：$R_2'=9.80\ \text{k}\Omega$，$V_o=5.94\ \text{V}$，误差 0.99%）。

**解决**：负载不能太轻就加电压跟随器做缓冲，或把分压电阻整体缩小 10 倍（代价是静态电流从 0.6mA 涨到 6mA）。

详见 [串联与并联](../basics/series-parallel.md)、[电压跟随器](../opamp/voltage-follower.md)。

</details>

## 四、简答与情景

<details><summary>情景：面包板上一只 1/4W、1kΩ 电阻接 12V，摸上去发烫。它是否安全？请定量判断。</summary>

**现象**：电阻明显发烫，但阻值未变、也未烧黑。

**计算**——公式：$P=\dfrac{V^2}{R}$。代入：$P=\dfrac{12^2}{1000}=0.144\ \text{W}$。结果：144mW，占 1/4W（250mW）的 **58%**。

**原因**：① 58% 已超过常规降额线（可靠性设计常要求 ≤50%）；② 电阻额定功率是 25°C（部分系列 70°C）下标定的，环境温度升高后按曲线线性降额；③ 面包板簧片接触电阻与电阻本体串联，实际功耗略高于计算值；④ 电阻紧贴面包板、无对流，热阻比自由空气中大。

**结论**：短时间不烧毁，但长期偏热、阻值会漂移。**解决**：换 1/2W 电阻（占额 29%），或把阻值加到 2.2kΩ（$P=65\ \text{mW}$），或改用串联的多个电阻分摊。

**教训**：小功率电阻不能只看"不烧"，要看降额、环境温度与实际热阻。

详见 [电阻器：参数、选型与降额](../components/resistors.md)、[降额设计](../practice/reliability-derating.md)。

</details>

<details><summary>简答：为什么电器金属外壳要接保护接地（PE）？人体触电时哪条路径最危险？</summary>

**保护接地（Protective Earth, PE）**把金属外壳与大地可靠连接。判据是两条：

1. **故障电流走低阻通路**：绝缘破损使外壳带电时，电流经 PE 线（阻抗远小于人体）回到电源，形成足够大的故障电流，让熔断器/断路器动作，或让 RCD（剩余电流装置）检测到相线与中性线电流不等而跳闸。
2. **钳位外壳电位**：即使保护器件未动作，PE 也把外壳电位钳在接近地电位，人体接触时承受的电压被大幅降低。

**最危险的路径是"左手—胸部—双脚"**：电流经过心脏区域。IEC 60479-1 的判据是电流-时间组合：工频 50/60Hz、路径为左手到双脚时，数十毫安、持续 1s 量级即可引发心室纤维性颤动；电流更大或时间更长，阈值继续下降。**决定伤害的是电流路径、幅值和持续时间三者，不是电压本身。** 所以湿手、赤脚站在地面上操作最危险；干燥环境、绝缘鞋、绝缘垫能显著降低通过人体的电流。

详见 [安全用电](../basics/electrical-safety.md)。

</details>

<details><summary>情景：用万用表测一节电池电压，量程误拨在电流档，两表笔直接并在电池两端，会发生什么？为什么禁止这样做？</summary>

**现象**：表内保险丝熔断（或表笔/表座打火），mA 档尤其容易；没有保险丝的 10A 档可能直接烧分流电阻、损伤表头，电池也会明显发热。

**原因**：电流档内阻是分流器，只有几毫欧到几欧，等效于一根导线。表笔并在电池两端 = 把电池经分流器短路，电流只受电池内阻 + 分流器 + 表笔限制。以 1.5V 碱性电池、内阻约 0.3Ω 估算，短路电流达 $1.5/(0.3+0.01)\approx4.8\ \text{A}$，远超 mA 档保险丝（常见 0.2~0.5A）。

**解决/正确做法**：测电压时表**并联**在被测点（电压档内阻高，MΩ 级）；测电流时必须把表**串**入回路（断开一处导线再串入），并先估计电流大小选档。养成"先看档位、再看表笔插孔"的顺序，是入门者最易犯、也最易损表的错误。

详见 [数字万用表](../practice/multimeter.md)。

</details>
