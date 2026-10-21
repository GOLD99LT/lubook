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
---

# PCB 与 EMC 测试题

本题库覆盖 PCB 层叠与板材、EDA/库管理、布局、布线载流过孔、模数电源分区、信号完整性与端接、串扰与差分走线、EMI/EMC、屏蔽滤波接地、ESD 防护、热设计、DFM。题型分为「概念判断」「填空」「计算」「简答与情景」四组。

## 一、概念判断

<details><summary>判断：四层板通常信号-地-电源-信号排列，地平面与电源平面相邻以形成去耦电容。</summary>

**正确。**典型四层：Top（信号）- GND - PWR - Bottom（信号）。地/电源平面相邻构成平面间电容，改善电源完整性；关键高速信号走微带线，参考完整地平面。

</details>

<details><summary>判断：信号线越短、回路面积越小，EMI 辐射越低。</summary>

**正确。**辐射强度正比于电流回路面积（$E\propto A\,f^2 I$）。缩短高速线、让返回电流紧贴信号下方（完整参考平面），可把回路面积压到最小，显著降低辐射。

</details>

<details><summary>判断：高速信号反射是因走线阻抗不连续（端点阻抗 ≠ 线特性阻抗）。</summary>

**正确。**传输线（Transmission Line）长度超过上升沿空间延伸的约 1/6 时必须考虑反射。源端或负载端阻抗不匹配产生反射，导致过冲/振铃。用端接（Source/Load termination）匹配。

</details>

<details><summary>判断：差分走线两根线紧耦合、等长、等距平行，可抑制共模噪声，用于 USB/以太网/LVDS。</summary>

**正确。**差分对（Differential Pair）靠两线电压差传信号，外界共模干扰同时耦合到两线、在接收端相减抵消。要求等长（控 skew）、紧耦合、参考平面连续。

</details>

<details><summary>判断：串扰（Crosstalk）是相邻走线间通过互容/互感耦合的噪声，间距越小、平行越长越严重。</summary>

**正确。**串扰由容性耦合与感性耦合引起。增加线间距（如 ≥3W 规则）、缩短平行段、完整地平面、降低边沿速率可减小。

</details>

<details><summary>判断：ESD 防护应放在接口入口处，先经 TVS/滤波再进芯片，且 TVS 到接口引脚尽量短。</summary>

**正确。**ESD 器件必须在骚扰进入 PCB 的最前端（连接器旁），泄放路径短、回路面积小，再进主电路。若放在芯片旁，ESD 路径经过长走线反而辐射耦合到内部。

</details>

<details><summary>判断：模拟地与数字地应该用磁珠/0Ω 在一点连接，而不是大面积混合。</summary>

**正确但需视情况。**模数混合电路常把 AGND/DGND 在一点（星型）连接，避免数字回流流经模拟敏感区。高速数字板则倾向完整统一地平面，靠分割谨慎处理，避免跨分割走线。

</details>

<details><summary>判断：散热主要靠铜箔面积与过孔，加大铜箔可增强散热，必要时加散热器。</summary>

**正确。**功率器件下打阵列散热过孔（thermal via）把热量导到背面铜箔/地平面。铜箔散热能力有限（1oz 铜每平方英寸约耗散小面积几 W），大功率必须算热阻、加散热器/风扇。

</details>

## 二、填空

<details><summary>PCB 铜箔厚度常见 1oz ≈ ____μm；走线载流按 IPC-2152，温升 ____°C 时 1oz 铜约 ____A/mm 宽度。</summary>

1oz ≈ 35μm。粗略经验：外层 1oz、温升 10~20°C 时约 1A/mm（1mm 宽约 1A）；内层散热差约减半。大电流要铺铜/多板厚铜。

</details>

<details><summary>传输线端接两类：____ 端接（串联电阻，匹配输出阻抗）与 ____ 端接（并联终端电阻到地/电源）。</summary>

源端（串联，靠近驱动端）与负载端（并联，靠近接收端）。短距离低速可不端接；长距离高速按拓扑选端接。

</details>

<details><summary>EMC 三要素：____、____、____。抑制任一即可改善。</summary>

骚扰源（Source）、耦合路径（Coupling Path）、敏感设备（Victim）。EMC 整改：减源、断耦合（屏蔽/滤波/接地）、提高抗扰。

</details>

<details><summary>过孔（Via）分 ____ 孔、____ 孔、____ 孔；HDI 板用 ____ 孔节省空间。</summary>

通孔（Through）、盲孔（Blind）、埋孔（Buried）。HDI（高密度互连）用盲/埋孔或微孔（microvia）。过孔有寄生电容/电感，高速信号要控制。

</details>

<details><summary>DFM（可制造性设计）要点：____、____、____、焊盘与钢网匹配。</summary>

常见：线宽/间距符合厂家工艺能力、焊盘与钢网（Stencil）匹配、器件间距够贴片/返修、丝印不挡焊盘、工艺边（Breakaway rail）。

</details>

## 三、计算

<details><summary>PCB 走线载流：1oz 铜（35μm），需走 2A 电流，温升 10°C，估算所需走线宽度。</summary>

按 IPC-2152 粗略外层经验：约 1A/mm。2A 需约 2mm 宽。考虑安全余量与内层散热差，实际取 2.5~3mm；大电流直接铺铜并多打过孔。
（更保守按 IPC-2221 旧公式 $I=k\,\Delta T^{0.44} A^{0.725}$，铜 $k=0.048$，A 为横截面积 mm²，结果数量级一致。）

</details>

<details><summary>微带线特性阻抗估算：FR4、h=0.2mm、线宽 w=0.2mm，近似 $Z_0\approx 87/\sqrt{\varepsilon_r+1.41}\cdot\ln(5.98h/(0.8w+t))$。$\varepsilon_r=4.2$，t 忽略，估 $Z_0$。</summary>

$\sqrt{4.2+1.41}=\sqrt{5.61}\approx 2.37$。
$5.98h/(0.8w)=5.98\times0.2/(0.8\times0.2)=1.196/0.16=7.48$，$\ln 7.48\approx 2.01$。
$Z_0\approx 87/2.37\times 2.01\approx 36.7\times2.01\approx 74\,\Omega$。
要做 50Ω 需加宽 w 或减小 h。差分 90~100Ω 按专用阻抗工具计算。

</details>

<details><summary>过孔寄生电感约 1nH。某信号在 100MHz 时过孔阻抗感抗多少？若地过孔流过 100mA/ns 的 di/dt，产生多少地弹电压？</summary>

感抗 $X_L=2\pi f L=2\pi\times 10^8\times 1\times10^{-9}\approx 0.63\,\Omega$。
地弹 $V=L\,di/dt=1\times10^{-9}\times (0.1/10^{-9})=0.1\text{V}$。
单个地过孔在快速开关时可产生 100mV 噪声——这就是为什么大电流返回要多打地过孔、平面接地。

</details>

<details><summary>差分对等长要求：USB 2.0 High Speed 允许对内 skew 5mil（约 0.13mm）。信号传播速度 FR4 约 6 英寸/ns。0.13mm 对应 skew 时间多少？</summary>

$t=0.13\text{mm}/(15\text{cm}/\text{ns})=0.013\text{cm}/15\text{cm}/\text{ns}\approx 0.87\text{ps}$。
（15cm/ns ≈ 6inch/ns。）数 ps 量级，PCB 布线时用长度匹配（±5mil）控制。对内不等长直接变共模辐射，劣化眼图。

</details>

## 四、简答与情景

<details><summary>情景：产品 EMC 辐射测试在 100~300MHz 超标，怎么定位和整改？</summary>

(1) 近场探头找辐射源（时钟、开关电源、时钟树）；(2) 查该频段谐波来自哪个晶振/开关频率；(3) 整改：缩短高速线、包地、加屏蔽罩、给时钟串小电阻慢化边沿、电源入口加 π 型滤波、地平面完整性、接口加共模电感；(4) 区分传导（CE）与辐射（RE）路径，对症下药。

</details>

<details><summary>简答：为什么高速信号下方不能跨分割（gap）走线？</summary>

跨分割迫使返回电流绕过缝隙，回路面积增大，既产生 EMI 又增大阻抗不连续导致反射。返回电流紧贴信号线下方流动；参考平面一旦中断，回流路径被迫绕远，回路面积激增。高速线必须保持参考平面连续。

</details>

<details><summary>情景：数字部分干净，但 ADC 采集的模拟值噪声大、随数字操作跳动。布局上怎么排查？</summary>

(1) 模拟地与数字地是否大面积混合、数字回流穿过模拟敏感区；(2) 模拟输入走线是否靠近时钟/开关噪声线；(3) ADC 下方是否完整模拟地平面；(4) 去耦电容是否靠近 ADC 电源脚；(5) 数字/模拟电源是否单点连接、LDO 是否隔离；(6) 是否跨分割走线。对策：AGND/DGND 星型单点、模拟输入包地、独立模拟电源。

</details>

<details><summary>简答：ESD 放电（接触放电 ±8kV）路径在 PCB 上应如何引导？</summary>

ESD 入口（接口金属壳/引脚）→ TVS 就近钳位 → 泄放到机壳地/保护地，而不是信号地。TVS 到接口路径短、回路面积小，地平面完整。接口外壳通过电容/磁珠接大地，避免 ESD 电流流入敏感信号地。

</details>
