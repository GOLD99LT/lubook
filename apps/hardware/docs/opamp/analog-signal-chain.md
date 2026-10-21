---
id: analog-signal-chain
title: 模拟信号与信号链概述 Analog Signal Chain
part: 3
chapter: 运放基础
order: 5
tags: [模拟信号, 信号链, 概述, 模数转换]
difficulty: 1
status: published
sources:
  - TI SLOA058 Single-Supply Op-Amp Circuit Collection
  - ADI MT-035 Op Amp Inputs, Outputs, Single-Supply & Rail-to-Rail Issues
  - https://github.com/kitspace/awesome-electronics
---

# 模拟信号与信号链概述 Analog Signal Chain

## 1. 设计动机

::: motivation 为什么要先讲信号链
现实世界的物理量——温度、压力、光照、声音、电压——是**连续的模拟量**。传感器把它们转换成毫伏级电压，而后 MCU/ADC 只认识数字。中间这一段"模拟调理"就是本手册第三篇要解决的全部问题：如何把一个又小、又脏、内阻又高的信号，不失真、低噪声地送到 ADC 门口。
:::

数字电路只需要 0 和 1，设计思路是"逻辑正确即可"。模拟电路完全不同：信号**真实存在**——它的幅度可能只有 10 mV，它的内阻可能有 10 kΩ，它身上还叠着 50 Hz 工频和开关电源尖峰。任何一级处理不当，后面所有数字算法都救不回来。**垃圾进，垃圾出（Garbage In, Garbage Out）**。

## 2. 信号链框图

![一条典型模拟信号链：传感器→信号调理→滤波→ADC→MCU](../assets/schematics/analog-signal-chain.svg)

::: analogy 信号链像水管系统
把信号想象成水流：传感器是水源（流量小、压力低），放大器是增压泵，滤波器是滤沙器，ADC 是流量计（只认数字读数）。水源压力太弱、管路太细（阻抗不匹配）、途中混进泥沙（噪声），最后流量计读到的数就是错的。**每一级都要先问：上一级带得动吗？下一级需要什么？**
:::

一条标准信号链包含四个环节：

1. **传感器（Sensor）**：热电偶、应变片、光电二极管等，输出常为 mV 级或电流环。
2. **信号调理（Signal Conditioning）**：放大、电平搬移、阻抗变换、偏置。
3. **滤波（Filter）**：滤除带外噪声、抗混叠。
4. **ADC 采样**：把连续电压变成离散数字量。

## 3. 关键概念：信号幅度、内阻与噪声

### 3.1 信号幅度 vs ADC 量程

ADC 的输入范围通常是 0~3.3V 或 0~5V（参考电压 $V_{REF}$ 决定）。信号只用到量程的 10%，就白白浪费了 90% 的分辨率。

$$\text{量化步长} = \frac{V_{REF}}{2^N}$$

::: example 数值算例：12 位 ADC 的分辨率
$V_{REF}=3.3\text{V}$、12 位 ADC，量化步长 $=3.3/4096\approx 0.8\text{mV}$。若传感器满幅输出只有 20 mV，直接采样只能区分 $20\text{mV}/0.8\text{mV}=25$ 个台阶——相当于把 12 位 ADC 当成了 4.6 位在用。**先放大再采样**是基本动作。
:::

### 3.2 信号源内阻

传感器都有内阻 $R_s$。后级输入阻抗 $Z_{in}$ 若不够大，信号会在 $R_s$ 上被分压衰减：

$$V_{\text{实际到达}} = V_{\text{信号}}\cdot\frac{Z_{in}}{R_s+Z_{in}}$$

经验法则：让 $Z_{in}\ge 100\,R_s$，分压损失才能压到 1% 以内。

## 4. 单电源 vs 双电源

电池供电设备常只有一个 0~5V 电源。而交流信号（如音频）会在正负之间摆动，单电源下负半周直接被削掉。解决办法是给信号加一个**直流偏置（Vcc/2）**，把整个信号"抬"到电源中点，交流分量再被隔直电容隔离。这部分在 [单电源电路与电平偏置搬移](../opamp/single-supply-biasing.md) 展开。

## 扩展与变种电路

### 扩展1：温度测量完整信号链 Temperature Measurement Chain

**定位**：把第 2 节的抽象信号链落到一颗 NTC/热电偶上，逐级给出接口与阻抗匹配要求——与主电路的关键差异是"每一级都要核对输入阻抗 $\ge 100\times$ 前级输出阻抗"。

![温度测量完整信号链](../assets/schematics/analog-signal-chain-temp-chain.svg)

::: example 工作原理 / 静态分析
链路：传感器（内阻 $R_s$）→ PGA（仪表放大器）→ RC 抗混叠 → ADC → MCU。

- PGA 增益取 $G=100$，把 0~20mV 满幅信号放到 0~2V，匹配 $V_{REF}=3.3\text{V}$ 的 12 位 ADC。
- 抗混叠截止频率设 $f_c=f_s/2.4$（$f_s$ 为采样率），保证高于 $f_s/2$ 的分量被压到量化噪声以下。
- 阻抗匹配：PGA 输入阻抗 $\ge 100\,R_s$，分压损失 $<1\%$。

量化步长 $=V_{REF}/2^N=3.3/4096\approx 0.8\text{mV}$，经 PGA 后等效到传感器端分辨率约 $8\,\mu\text{V}$。

温度是秒级缓变量，纯直流工作点，无需动态波形图。
:::

设计要点：NTC 用分压电桥、热电偶要做冷端补偿；PGA 选低漂移仪放（如 INA333）；抗混叠用二阶 Sallen-Key 比单级 RC 衰减更陡。适用工业温度采集；不适用高频振动/声发射等快变信号（需更高采样率与带宽）。

::: pitfall 温度链专属坑
- **PGA 增益开太高**：为小信号把 $G$ 开到 1000，结果 50Hz 工频与温漂也被放大 1000 倍，输出满是噪声。正确顺序是先抗混叠/滤波，再按需增益放大。
:::

## 5. 常见坑

::: pitfall 常见坑
- **直接把传感器接 ADC**：信号太弱、内阻太高，量化精度白白浪费，还拾进一堆噪声。正确顺序永远是"调理→滤波→采样"。
- **忽略 50Hz 工频干扰**：面包板上信号线走线长、没屏蔽，示波器上能看到稳定的 50Hz 正弦波叠在信号上。靠滤波解决，而不是靠 ADC 软件去猜。
- **信号链每级都要"重新算"**：上一级的输出阻抗就是下一级的信号源内阻，级联时必须逐级核对，不能假设后级是理想高阻。
:::

## 6. 自测题

<details><summary>12 位 ADC、Vref=3.3V，传感器满幅只输出 50mV，信号实际占了 ADC 量程的百分之几？相当于几位有效分辨率？</summary>

占比 $50/3300\approx 1.5\%$。有效分辨率：$2^N=4096\times 1.5\%\approx 61\Rightarrow N\approx 5.9$ 位。信号太弱必须先放大。
</details>

<details><summary>传感器内阻 10kΩ，后级输入阻抗 10kΩ，信号被分压衰减到多少？</summary>

$Z_{in}/(R_s+Z_{in})=10/(10+10)=0.5$，只剩一半。要做到衰减<1%，输入阻抗至少要 100 倍信号源内阻。
</details>

## 7. 参考资料

- TI SLOA058《Single-Supply Op-Amp Circuit Collection》——单电源信号链偏置与交流耦合电路
- ADI MT-035《Op Amp Inputs, Outputs, Single-Supply & Rail-to-Rail Issues》
- [Kitspace awesome-electronics](https://github.com/kitspace/awesome-electronics)——硬件学习资源索引
