---
id: power-integrity-decoupling
title: 电源完整性与去耦体系 Power Integrity & Decoupling
part: 6
chapter: 地与电源完整性
order: 60
tags: [电源完整性, 去耦, 目标阻抗, 反谐振, 自谐振频率, 旁路电容]
difficulty: 3
status: published
sources:
  - Henry W. Ott, Electromagnetic Compatibility Engineering
  - onsemi AND8301-D EMC/PCB Layout Guidelines
  - Howard Johnson & Martin Graham, High Speed Digital Design
---

# 电源完整性与去耦体系 Power Integrity & Decoupling

现代芯片内部瞬间开关电流可达数安培、上升沿仅 ns 级。稳压电源（VRM）响应太慢，赶不上这种瞬态——**靠芯片旁边的本地电容在瞬间供能**。这就是去耦。这一章讲怎么定目标阻抗、怎么选电容、怎么避免并联反谐振。

## 1. 设计动机

::: motivation 为什么需要一大堆电容
稳压电源距离芯片几十毫米，走线有电感。当芯片内部瞬间从空载跳到 1A，电流不可能立刻从电源沿走线流过来——电感 $L$ 阻碍电流突变，VCC 电压会瞬间往下掉，导致逻辑出错。

去耦电容紧贴芯片放置，就是本地的"小电池"：瞬态来了立刻供能，把电压稳住。**没有去耦，再贵的稳压电源也救不了芯片的瞬态压降。**
:::

## 2. 原理图

去耦不是随便并几个电容，而是一个**多级体系**：电解大电容管低频 bulk，10µF 管中频，0.1µF 紧贴引脚管高频。

![多级去耦：电解 100µF → 10µF → 0.1µF，越小越靠近芯片引脚](../assets/schematics/power-integrity-decoupling.svg)

## 3. 静态分析（DC）

- **目标阻抗（Target Impedance）**：允许电源轨上的最大阻抗。由允许纹波电压和最大瞬态电流决定：

$$Z_{target}=\frac{\Delta V_{allow}}{\Delta I_{max}}$$

以 3.3V 轨、允许 ±3%（即 $\Delta V_{allow}=100\text{mV}$）、瞬态电流 $\Delta I=1\text{A}$ 为例：

$$Z_{target}=\frac{0.1\text{V}}{1\text{A}}=0.1\Omega$$

设计目标：从 DC 到最高噪声频率，整个电源分配网络（PDN）在任何频率的阻抗都必须 **< 0.1Ω**。

- 直流时电容开路，VRM 供电；高频时电容成为低阻通路。

## 4. 动态分析（AC / 瞬态）

每颗电容都不是理想电容——它串联有等效电感 **ESL**（来自封装、过孔、走线）。于是电容在**自谐振频率（Self-Resonant Frequency, SRF）**以下呈容性、以上呈感性：

$$f_{SR}=\frac{1}{2\pi\sqrt{ESL\cdot C}}$$

以 0.1µF 陶瓷、$ESL=2\text{nH}$ 为例：$f_{SR}=\dfrac{1}{2\pi\sqrt{2\text{nH}\times0.1\mu\text{F}}}\approx11\text{MHz}$。低于此频率它是好电容，高于此频率它变成电感、失去去耦作用——所以单靠一颗电容不够，要用不同容值覆盖不同频段。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["100µF 电解", "10µF 陶瓷", "0.1µF 陶瓷", "目标阻抗 0.1Ω"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 56, "right": 24, "top": 26, "bottom": 56},
  "xAxis": {"type": "category", "name": "频率 Hz", "data": ["100","1k","10k","100k","1M","10M","100M"], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "log", "name": "阻抗 Ω", "min": 0.01, "max": 100, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "100µF 电解", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [1,0.3,0.1,0.08,0.5,5,50]},
    {"name": "10µF 陶瓷", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#b5642e"},
     "data": [10,3,0.5,0.1,0.15,2,20]},
    {"name": "0.1µF 陶瓷", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#4f9e63"},
     "data": [50,20,5,0.8,0.15,0.12,0.8]},
    {"name": "目标阻抗 0.1Ω", "type": "line", "showSymbol": false, "lineStyle": {"width": 2, "type": "dashed", "color": "#888888"},
     "data": [0.1,0.1,0.1,0.1,0.1,0.1,0.1]}
  ]
}
```

三种电容各自在不同频段把阻抗压低，共同包络要始终在 0.1Ω 虚线以下；注意两容值之间可能出现反谐振尖峰（见扩展1）。

## 5. 环路分析

PDN 不是反馈环路，但其阻抗特性决定瞬态响应。VRM 闭环带宽有限（~kHz 级），只负责 DC 到低频；**中高频的瞬态完全靠电容**。电容选择本质是在频域上拼出一条低于目标阻抗的包络线。

::: advanced 进阶：并联反谐振与频段电容选择
单颗电容阻抗在 $f_{SR}$ 最低。两颗不同容值电容并联时，在两者 $f_{SR}$ 之间，大电容已呈感性、小电容还呈容性，二者并联发生**并联谐振**，阻抗非但不降低，反而因 ESR 而冒出一个尖峰——这就是**反谐振（Anti-Resonance）**。

**各频段电容选择**（经验）：
- **低频（<10kHz）**：大容量电解/钽电容（100µF~数百 µF），储能、应付大瞬态；
- **中频（10kHz~1MHz）**：10µF X5R/X7R 陶瓷；
- **高频（<15MHz）**：0.1µF（100nF）陶瓷，最靠近引脚；
- **甚高频（>15MHz）**：0.01µF（10nF）陶瓷，进一步压高频。

缓解反谐振：在两容值间加中间容值（如 1µF、0.01µF 都放）、选低 ESR、多颗并联分散尖峰。
:::

## 6. 元件取值与工程权衡

- **容值数量级**：0.1µF 是"万金油"，每电源引脚必放；大容量 10~100µF 板级 bulk。
- **介质**：陶瓷必须 X5R/X7R（X7R 温漂更小），Y5V 温漂下容量暴跌不可用于去耦。注意陶瓷 DC bias 效应——0.1µF/6.3V 高介电常数料在 3.3V 偏置下实际容量可能只剩 30%。
- ** placement**：小电容最靠近电源引脚（<1~2mm），过孔就近打地平面；走线越短 ESL 越小，$f_{SR}$ 越高。
- **封装**：0402/0201 比 0805 ESL 小，高频去耦更好。

## 7. 完整设计示例

::: example 3.3V MCU 的去耦设计
1. **需求**：$Z_{target}=0.1\Omega$（3.3V±3%、ΔI=1A）。
2. **bulk**：板级 100µF 电解 + 10µF 陶瓷管低频中频。
3. **每引脚**：每个 VCC 引脚就近放一颗 0.1µF X7R（0402），过孔紧挨。
4. **甚高频**：关键 IC 旁再加 0.01µF。
5. **验算**：按频段拼包络，全程 <0.1Ω；两容值间反谐振尖峰用中间 1µF 电容压平。
:::

## 8. 仿真与实验

用阻抗分析仪或 VNA 测 PDN 在板上的实际阻抗曲线（探针夹电容两端），看是否全程在目标阻抗以下、有无反谐振尖峰。实测常见问题：0.1µF 离引脚太远（走线电感让 $f_{SR}$ 掉到几 MHz），把电容移近后高频阻抗显著改善。

## 扩展与变种电路

### 扩展1：电容并联反谐振 Anti-Resonance

两颗容值相差悬殊的电容并联，中间频段冒出阻抗尖峰。

![大电容与小电容并联，二者自谐振频率间出现反谐振尖峰](../assets/schematics/power-integrity-decoupling-antiresonance.svg)

::: example 工作原理
- 大电容在低频低阻但 $f_{SR}$ 低，高频已呈感性；小电容 $f_{SR}$ 高但低频阻抗大。
- 在两 $f_{SR}$ 之间，一容性一感性并联谐振，阻抗尖峰高出目标线。
- 尖峰大小由 ESR 决定，ESR 大反而"阻尼"掉尖峰。
:::

取值对比：只放 10µF+0.1µF 会有反谐振尖峰；中间加 1µF、0.01µF 把尖峰打散。适用：全频段；不适用：两容值相差 100 倍以上且无中间值。

::: pitfall 并联越多阻抗越低的误区
- **现象**：并了好几颗电容，某频段纹波反而更大。
- **原因**：容值搭配不当造成反谐振尖峰。
- **解决**：容值按十倍频程搭配（100µF/1µF/0.01µF），或用实测阻抗曲线指导。
:::

### 扩展2：VRM 与电容的分工

VRM 只在低频有效，高频瞬态完全靠本地电容。

![VRM 负责低频稳压，电容群负责中高频瞬态](../assets/schematics/power-integrity-decoupling-vrm.svg)

::: example 工作原理
- VRM 闭环响应慢（带宽 ~kHz），瞬态来临时它还没反应，电压已跌。
- 本地电容在 ns 级立刻供能；等 VRM 在 µs 级跟上后再补充电荷。
:::

取值对比：提高 VRM 带宽可替代部分电容，但受稳定性限制；电容是最廉价高效的高频手段。适用：所有数字 IC；不适用：无。

::: pitfall 只靠 VRM 不加去耦导致瞬态掉压
- **现象**：芯片满载时 VCC 瞬间跌落、死机。
- **原因**：VRM 响应赶不上瞬态，无本地电容。
- **解决**：每个引脚就近去耦，不要指望远端电源。
:::

## 9. 常见坑与故障现象

::: pitfall 常见坑
- **0.1µF 离引脚太远**：走线电感让有效 ESL 大增，$f_{SR}$ 从 10MHz 掉到 2MHz，高频去耦失效。解决：电容紧贴引脚、过孔就近打地。
- **用 Y5V/高介电陶瓷，DC bias 后容量暴跌**：标 0.1µF 实际只剩几 nF。解决：选 X5R/X7R，按 DC bias 曲线降额取值。
- **容值搭配不当产生反谐振**：两电容间阻抗尖峰。解决：十倍频程搭配、加中间容值。
- **地平面被开槽导致回流电感大**：去耦回路面积大、效果差。解决：完整地平面，电容地端就近打过孔。
:::

## 10. 自测题

<details><summary>3.3V 轨允许 ±3% 纹波、瞬态电流 1A，目标阻抗是多少？</summary>
$\Delta V_{allow}=3.3\times3\%=0.1\text{V}$，$Z_{target}=0.1\text{V}/1\text{A}=0.1\Omega$。PDN 全频段阻抗须低于此值。
</details>

<details><summary>0.1µF 陶瓷、ESL=2nH，自谐振频率约多少？高于此频率它还有用吗？</summary>
$f_{SR}=1/(2\pi\sqrt{2\text{nH}\times0.1\mu\text{F}})\approx11\text{MHz}$。高于此频率它呈感性、阻抗反而上升，失去去耦作用，需更小电容（0.01µF）接管。
</details>

<details><summary>为什么去耦电容要"大电容远、小电容近"？</summary>
小电容 ESL 小、$f_{SR}$ 高，能响应最快的瞬态，必须紧贴引脚；大电容储能多但响应慢，放在稍远处即可。距离越长引线电感越大，小电容的高频优势就被抵消。
</details>

<details><summary>什么是并联反谐振？怎么缓解？</summary>
两颗容值悬殊的电容，在各自自谐振频率之间一并一感并联谐振，冒出阻抗尖峰。缓解：按十倍频程搭配容值（100µF/1µF/0.01µF）、选低 ESR、多颗并联分散尖峰。
</details>

## 11. 参考资料

- Henry W. Ott, *Electromagnetic Compatibility Engineering*——PDN 与去耦
- onsemi AND8301-D——去耦电容频段选择（0.1µF<15MHz、0.01µF>15MHz）
- Howard Johnson & Martin Graham, *High Speed Digital Design*——电源分配网络
