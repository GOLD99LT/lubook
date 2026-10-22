---
id: quiz-pcb
title: PCB 与 EMC 测试题
part: 9
chapter: 硬件测试与面试题库
order: 35
tags: [题库, 自测, PCB, EMC]
difficulty: 2
status: published
sources:
  - Eric Bogatin, Signal and Power Integrity - Simplified
  - Henry Ott, Electromagnetic Compatibility Engineering
  - IPC-2221 / IPC-2152 载流设计标准
  - IPC-2221B, Generic Standard on Printed Board Design, 2012 — current capacity formula and electrical clearance
  - IPC-2152, Standard for Determining Current-Carrying Capacity in Printed Board Design, 2009 — copper current versus temperature rise
  - IPC-2141A, Design Guide for High-Speed Controlled Impedance Circuit Boards, 2004 — microstrip and stripline impedance
  - Henry W. Ott, Electromagnetic Compatibility Engineering, Wiley 2009 — return current, grounding and shielding
  - Eric Bogatin, Signal and Power Integrity - Simplified, 3rd ed. — transmission lines, crosstalk and differential pairs
  - Howard Johnson and Martin Graham, High Speed Digital Design, Prentice Hall 1993 — knee frequency and return paths
  - IEC 61000-4-2, Electrostatic discharge immunity test — contact and air discharge
---

# PCB 与 EMC 测试题

本题库覆盖 PCB 层叠与板材、EDA/库管理、布局、布线载流过孔、模数电源分区、信号完整性与端接、串扰与差分走线、EMI/EMC、屏蔽滤波接地、ESD 防护、热设计、DFM。题型分为「概念判断」「填空」「计算」「简答与情景」四组。数字题按「公式 → 代入 → 结果 → 单位」给全，概念题给判据。

## 一、概念判断

<details><summary>判断：四层板通常信号-地-电源-信号排列，地平面与电源平面相邻以形成去耦电容。</summary>

**正确，但不能把平面电容当去耦主力。**典型四层是 L1 信号、L2 GND、L3 PWR、L4 信号。L1 参考 L2 完整地；L4 参考 L3 电源平面，只有 L3 与 L2 在关心频段低阻抗耦合时，L4 的回流才能就近流回。GND/PWR 相邻确实构成平面电容，但容量很小（下一题算），它的价值是低扩展电感和场约束，不是替代 0.1µF 去耦。若 L4 走对回流极敏感的线，优先把 L3 也做成 GND，把电源挤到局部铺铜。详见[PCB 层叠与阻抗](../pcb/pcb-stackup.md)。

</details>

<details><summary>判断：信号线越短、回路面积越小，EMI 辐射越低。</summary>

**正确。**小环天线的远场辐射近似 $E\propto A f^2 I/r$：回路面积 $A$ 减半、频率或电流不变时，辐射也减半；频率翻倍则辐射约 4 倍。缩短高速线、让返回电流紧贴信号下方（完整参考平面），可把回路面积压到最小。但整机辐射往往由电缆共模电流主导，此时还要做共模扼流、屏蔽和接地，不能只看板上小环。

</details>

<details><summary>判断：高速信号反射是因走线阻抗不连续（端点阻抗 ≠ 线特性阻抗）。</summary>

**正确，但“高速”要有判据。**当走线单向延迟 $t_d$ 大于信号上升时间 $t_r$ 的约 $1/6$（有的规范用 $1/10$）时，必须按传输线处理；此时源端、负载端、过孔、分支、参考平面变化都会造成阻抗不连续，产生反射、过冲和振铃。端接（源端串联、末端并联/戴维南/AC 端接）的目的都是让 $Z_L\approx Z_0$。低于这个判据的短线和慢边沿，反射通常可以忽略。

</details>

<details><summary>判断：差分走线两根线紧耦合、等长、等距平行，可抑制共模噪声，用于 USB/以太网/LVDS。</summary>

**正确，但“等距”不是绝对要求。**差分对靠两线电压差传信号，外界共模干扰同时耦合到两线，在接收端相减抵消；关键是差分阻抗受控、对内等长（控 skew）、紧耦合、参考平面连续。两根线不必全程严格等距，但间距突变会改变差分阻抗；对内不等长会把差分信号转成共模，劣化眼图并增加辐射。详见[串扰与差分走线](../pcb/crosstalk-differential.md)。

</details>

<details><summary>判断：串扰（Crosstalk）是相邻走线间通过互容/互感耦合的噪声，间距越小、平行越长越严重。</summary>

**正确。**串扰由容性耦合（$C_m$）与感性耦合（$L_m$）共同引起，边沿越陡、平行段越长、间距越小越严重；近端串扰（NEXT）和远端串扰（FEXT）的波形不同。增加线间距（“3W”是中心距 ≥3 倍线宽的经验规则）、缩短平行段、完整地平面、降低边沿速率都可减小。带状线夹在两面平面之间，串扰通常比微带线小。

</details>

<details><summary>判断：ESD 防护应放在接口入口处，先经 TVS/滤波再进芯片，且 TVS 到接口引脚尽量短。</summary>

**正确。**ESD 器件必须在骚扰进入 PCB 的最前端（连接器旁），泄放路径短、回路面积小，再进主电路；若放在芯片旁，ESD 电流会先流过整段走线，沿途辐射/耦合到内部。还要核对：TVS 钳位电压低于被保护引脚的绝对最大额定；TVS 地端到连接器金属壳/保护地要短而宽；先 TVS 再串联电阻/滤波，别让 TVS 之后的走线再被耦合。详见[ESD 防护](../pcb/esd-protection.md)。

</details>

<details><summary>判断：模拟地与数字地应该用磁珠/0Ω 在一点连接，而不是大面积混合。</summary>

**不能一概而论；把它当普遍规则是错的。**判据是返回电流路径：如果分割后没有信号跨分割、且 ADC/DAC 厂商明确要求单点连接，AGND/DGND 可以在一点连；否则高速/混合信号板应保持完整连续地平面，靠布局把数字回流挡在模拟敏感区之外。磁珠/0Ω 单点连接在高频下引入电感，可能让分割两侧的电位差更大。核心是“回流不流经敏感区”，不是“地必须切开”。详见[模拟与数字电源分区](../pcb/analog-digital-power-routing.md)。

</details>

<details><summary>判断：散热主要靠铜箔面积与过孔，加大铜箔可增强散热，必要时加散热器。</summary>

**正确，但“加大铜箔”有上限。**功率器件下的热过孔阵列（thermal via）把热导到背面铜箔/地平面；1oz 铜的方块热阻约 $R_{th,\square}=1/(kt)=1/(385\times35\times10^{-6})\approx74\text{K/W}$（一阶横向估算），只靠一个方块摊热，1W 就有几十 K 温升。大功率必须算结到环境热阻 $\theta_{JA}$、铜箔面积、过孔数量和气流，加散热器/风扇/金属基板；不能只看“铜面积大”。详见[热设计](../pcb/thermal-design.md)。

</details>

<details><summary>判断：四层板 GND/PWR 相邻形成的平面电容足以替代 0.1µF 去耦电容。</summary>

**错误。**平面电容 $C=\varepsilon_0\varepsilon_r A/d$。取 $A=1\text{cm}^2=10^{-4}\text{m}^2$、$d=0.2\text{mm}=2\times10^{-4}\text{m}$、$\varepsilon_r=4.3$：

$$
C=\frac{8.854\times10^{-12}\times4.3\times10^{-4}}{2\times10^{-4}}=19.0\text{pF}
$$

100MHz 时容抗：

$$
Z_C=\frac{1}{2\pi fC}=\frac{1}{2\pi\times10^8\times19.0\times10^{-12}}=83.8\,\Omega
$$

83.8Ω 远不是“低阻抗”，不能替代 0.1µF（100MHz 时约 0.016Ω，忽略 ESL）。平面电容的价值在高频段的低扩展电感和场约束；低频/中频去耦仍靠离散电容。

</details>

## 二、填空

<details><summary>PCB 铜箔厚度常见 1oz ≈ ____μm；按 IPC-2221 外层经验式，温升 10°C 时 1oz 铜约 ____A/mm 宽度；内层约 ____A/mm。</summary>

1oz ≈ 35µm。按 IPC-2221 外层 $I=k\Delta T^{0.44}A^{0.725}$，1mm 宽、35µm 厚的截面积 $A=1\times0.035=0.035\text{mm}^2=54.2\text{mil}^2$，代入 $I=0.048\times10^{0.44}\times54.2^{0.725}=2.39\text{A}$；内层 $k=0.024$ 得约 1.20A。工程口诀“1A/mm”是留了 2~3 倍余量的保守值，不是 IPC 计算值；IPC-2152 会给出考虑板厚/散热后的更精确结果。大电流要铺铜、加厚铜或多层并联。

</details>

<details><summary>传输线端接两类：____ 端接（串联电阻，匹配输出阻抗）与 ____ 端接（并联终端电阻到地/电源）。</summary>

源端（串联，靠近驱动端）与负载端（并联，靠近接收端）。源端串联电阻与驱动器输出阻抗相加，匹配线阻抗，抑制二次反射；负载端并联到地/电源（或戴维南/AC 端接）吸收到达末端的能量。短距离低速可不端接；长距离高速按拓扑选端接。

</details>

<details><summary>EMC 三要素：____、____、____。抑制任一即可改善。</summary>

骚扰源（Source）、耦合路径（Coupling Path）、敏感设备（Victim）。EMC 整改：减源（慢边沿、扩频、滤波）、断耦合（屏蔽、滤波、接地、隔离）、提高抗扰（TVS、共模电感、软件容错）。三者缺一，骚扰就不会形成问题。

</details>

<details><summary>过孔（Via）分 ____ 孔、____ 孔、____ 孔；HDI 板用 ____ 孔节省空间。</summary>

通孔（Through）、盲孔（Blind）、埋孔（Buried）。HDI（高密度互连）用盲/埋孔或微孔（microvia，激光钻孔）。过孔有寄生电容/电感（约 1nH 量级），高速信号换层时要控制回流过孔和阻抗不连续；载流则看孔壁镀铜截面积。

</details>

<details><summary>DFM（可制造性设计）要点：____、____、____、焊盘与钢网匹配。</summary>

常见：线宽/间距符合厂家工艺能力、焊盘与钢网（Stencil）匹配、器件间距够贴片/返修、丝印不挡焊盘、工艺边（Breakaway rail）与基准点（Fiducial）、拼板与阻抗测试条。DFM 不是“画完再检查”，而是布局前就把板厂能力、贴片精度、测试与返修路径定下来。

</details>

## 三、计算

<details><summary>PCB 走线载流：1oz 铜（35μm），需走 2A 电流，温升 10°C，估算所需走线宽度。</summary>

按 IPC-2221 外层经验式：

$$
I=k\,\Delta T^{0.44}A^{0.725}
$$

其中 $I$ 是电流（A）；$\Delta T$ 是温升（$^{\circ}\text{C}$，代入数值）；$A$ 是截面积（mil²，不是 mm²）；外层 $k=0.048$、内层 $k=0.024$。

$$
\Delta T^{0.44}=10^{0.44}=2.754
$$

$$
A=\left(\frac{2}{0.048\times2.754}\right)^{1/0.725}
=\left(\frac{2}{0.1322}\right)^{1.379}
=15.13^{1.379}=42.4\text{mil}^2
$$

1oz = 1.378mil，所以：

$$
W=\frac{42.4}{1.378}=30.8\text{mil}=0.781\text{mm}
$$

这是 10°C 温升、外层、理想散热下的理论最小值。工程上考虑铜厚公差、内层、实测温升和 2 倍余量，外层取 1.5~2mm；内层按 $k=0.024$ 理论值约 2.03mm，取 2.5~3mm。大电流直接铺铜并多打过孔。注意单位：$A$ 用 mil²，1mm²=1550mil²；单位混用是载流计算最常见的错误。

</details>

<details><summary>微带线特性阻抗估算：FR4、h=0.2mm、线宽 w=0.2mm，近似 $Z_0\approx 87/\sqrt{\varepsilon_r+1.41}\cdot\ln(5.98h/(0.8w+t))$。$\varepsilon_r=4.2$，t 忽略，估 $Z_0$。</summary>

$$
\sqrt{\varepsilon_r+1.41}=\sqrt{5.61}=2.368
$$

$$
\frac{5.98h}{0.8w}=\frac{5.98\times0.2}{0.8\times0.2}=\frac{1.196}{0.16}=7.475
$$

$$
\ln7.475=2.011
$$

$$
Z_0=\frac{87}{2.368}\times2.011=36.74\times2.011=73.9\,\Omega
$$

约 74Ω。要做 50Ω 需加宽 $w$ 或减小 $h$。注意题目给的是“t 忽略”；若 1oz 铜 $t=35\mu\text{m}$，分母 $0.8w+t=0.195\text{mm}$，$Z_0\approx66.6\Omega$，差 10%。差分 90~100Ω 要用专用阻抗工具/场求解器，不能拿单端公式凑。

</details>

<details><summary>过孔寄生电感约 1nH。某信号在 100MHz 时过孔阻抗感抗多少？若地过孔流过 100mA/ns 的 di/dt，产生多少地弹电压？</summary>

$$
X_L=2\pi fL=2\pi\times10^8\times1\times10^{-9}=0.628\,\Omega
$$

$$
V=L\frac{di}{dt}=1\times10^{-9}\times\frac{0.1}{10^{-9}}=0.1\text{V}
$$

单个地过孔在快速开关时可产生 100mV 噪声；这就是为什么大电流返回要多打地过孔、平面接地。多个过孔并联时电感近似按 $1/n$ 下降，但布局不对称会引入额外回路电感。

</details>

<details><summary>差分对等长要求：USB 2.0 High Speed 允许对内 skew 5mil（约 0.13mm）。信号传播速度 FR4 约 6 英寸/ns。0.13mm 对应 skew 时间多少？</summary>

FR4 传播速度约 $6\text{in/ns}$（6in=152.4mm，工程口算常取 $150\text{mm/ns}$）：

$$
t=\frac{0.13\text{mm}}{150\text{mm/ns}}=8.67\times10^{-4}\text{ns}=0.867\text{ps}
$$

按精确的 152.4mm/ns 算是 0.853ps，两者都在 0.85~0.87ps 量级。USB 2.0 HS 的 1UI 是 $1/480\text{Mbps}=2.083\text{ns}$，0.87ps 远小于 1UI；但 5mil 是布线经验值，不是规范硬指标，实际按差分阻抗、连接器/过孔不对称和眼图余量定。对内不等长会把差分信号转成共模，既劣化眼图又增加辐射。

</details>

<details><summary>0.3mm 钻孔、25μm 镀铜的通孔，10°C 温升能过多大电流？3A 需要几个？</summary>

孔壁镀铜截面积（把孔壁展开成薄壁圆筒）：

$$
A=\pi d t=\pi\times0.3\text{mm}\times25\,\mu\text{m}=23.6\times10^{-3}\text{mm}^2
$$

换算成 mil²：

$$
A=23.6\times10^{-3}\times1550=36.6\text{mil}^2
$$

按 IPC-2221 内层档 $k=0.024$、$\Delta T=10^{\circ}\text{C}$：

$$
I=0.024\times2.754\times36.6^{0.725}
=0.024\times2.754\times13.6=0.899\text{A}
$$

单孔约 0.9A。3A 至少需要 $3/0.9=3.34$ 个，工程上取 6 个（每个 0.5A，留 2 倍余量）。若镀铜只有 20µm，单孔约 0.76A，3A 至少 4 个，仍建议 6 个。

</details>

## 四、简答与情景

<details><summary>情景：产品 EMC 辐射测试在 100~300MHz 超标，怎么定位和整改？</summary>

(1) 近场探头找辐射源（时钟、开关电源、时钟树、高速接口）；(2) 查该频段谐波来自哪个晶振/开关频率，算 $f_{harm}=n f_0$ 对上是哪一次；(3) 整改：缩短高速线、包地、加屏蔽罩、给时钟串小电阻慢化边沿（要核算时序）、电源入口加 π 型滤波、地平面完整性、接口加共模电感；(4) 区分传导（CE）与辐射（RE）路径，对症下药。辐射超标常见根因是电缆共模电流，不是板上某根线，别只盯着 PCB。

</details>

<details><summary>简答：为什么高速信号下方不能跨分割（gap）走线？</summary>

跨分割迫使返回电流绕过缝隙，回路面积增大，既产生 EMI 又增大阻抗不连续导致反射。返回电流在高速下走电感最小的路径，紧贴信号线下方；参考平面一旦中断，回流被迫绕远，回路面积激增，还可能形成缝隙天线。高速线必须保持参考平面连续；必须在分割处换层时，旁边加回流过孔/缝合电容。

</details>

<details><summary>情景：数字部分干净，但 ADC 采集的模拟值噪声大、随数字操作跳动。布局上怎么排查？</summary>

(1) 先按 ADC 数据手册确认地策略：多数高速 ADC 推荐完整地平面 + 分区布局，不分割；只有明确要求分割的器件才单点连接，且信号不得跨分割。(2) 模拟输入走线是否靠近时钟/开关噪声线，是否包地；(3) ADC 下方是否完整模拟地/参考平面；(4) 去耦电容是否靠近 ADC 电源脚，回流是否短；(5) 数字/模拟电源是否分开、LDO 是否隔离；(6) 是否跨分割走线。对策：分区布局、模拟输入包地、独立模拟电源、短回流路径；不要一上来就“星型单点”。

</details>

<details><summary>简答：ESD 放电（接触放电 ±8kV）路径在 PCB 上应如何引导？</summary>

ESD 入口（接口金属壳/引脚）→ TVS 就近钳位 → 泄放到机壳地/保护地，而不是信号地。TVS 到接口路径短、回路面积小，地平面完整；接口外壳通过电容/磁珠接大地，避免 ESD 电流流入敏感信号地。TVS 钳位电压要低于被保护引脚耐压；信号地/保护地按单点或电容连接，别让 ESD 电流穿过 MCU 地。软件还要记录复位源并自恢复，但不能拿软件当 ESD 防护。

</details>
