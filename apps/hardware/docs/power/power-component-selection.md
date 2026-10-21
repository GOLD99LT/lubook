---
id: power-component-selection
title: 功率电感、电容、MOS 与二极管选型 Power Component Selection
part: 6
chapter: 开关电源
order: 30
tags: [功率电感, MLCC, MOSFET, 肖特基, 损耗, 降额, 选型]
difficulty: 3
status: published
sources:
  - TI SLVA477A Basic Calculation of a Buck Converter's Power Stage
  - onsemi AND9596 Thermal Calculation for Power Devices
  - Maniktala, Switching Power Supplies A–Z, 2nd ed.
---

# 功率电感、电容、MOS 与二极管选型 Power Component Selection

## 1. 设计动机

::: motivation 为什么单独讲选型
拓扑和公式算出来后，真正决定电源成败的是具体元件。**电感饱和电流不够会烧 MOS，MLCC 直流偏置降额会让纹波翻倍，MOS 开关损耗没算准会过热，二极管反压选小会击穿**。本章把 Buck 功率级四个关键元件（L、Cin/Cout、MOS、二极管）的选型参数、数量级与权衡一次讲清。
:::

## 2. 原理图

![Buck 功率级上各元件的选型要点标注：Cin 低 ESR 纹波电流、Q1 RDSon/Qg、D VF/反压、L Isat/DCR、Cout ESR/DC bias](../assets/schematics/power-component-selection.svg)

## 3. 静态分析（DC）

选型的静态约束：

- **电感直流电流** = $I_{out}$；**饱和电流 $I_{sat}$** 必须 > $I_{SW(peak)}=I_{out}+\Delta I_L/2$，并留 20~30% 降额。
- **MOS 电压应力** = $V_{in(max)}$（Buck），耐压留到 1.5~2 倍。
- **二极管反向电压** = $V_{in(max)}$（Buck），正向平均电流 = $I_{out}(1-D)$。
- **电容耐压**：Cin > $V_{in(max)}$，Cout > $V_{out}$，留量 1.5~2 倍。

## 4. 动态分析（AC / 瞬态）

动态约束决定发热与纹波：

- **电感 RMS 电流 ≈ $I_{out}$**，DCR 上铜损 $I^2 DCR$。
- **电容纹波电流**：Cin 承受方波脉冲电流（RMS 大），Cout 承受三角纹波。
- **MOS 开关损耗**随 fs 增大；**二极管反向恢复** Qrr 损耗。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["MOS 损耗构成占比"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 60, "right": 30, "top": 26, "bottom": 50},
  "xAxis": {"type": "category", "data": ["导通损", "开关损", "栅损", "二极管Qrr"], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "损耗 W", "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "MOS 损耗构成占比", "type": "bar", "itemStyle": {"color": "#1a4f8b"},
     "data": [0.05, 0.12, 0.02, 0.06]}
  ]
}
```

## 5. 环路分析

元件选型会影响环路稳定性：

- **Cout 的 ESR** 引入一个零点，太高/太低都影响相位裕度（见 [LDO](ldo.md) 与 [Buck 环路](buck.md)）。
- **内部补偿型 IC** 要求按推荐 L、C 组合选元件，随意换大电容会失配。

::: advanced 进阶：损耗与热的定量估算
- MOS 导通损：$P_{cond}=I_{out}^2 R_{DSon} D$；开关损：$P_{sw}=0.5 V_{in} I_{out}(t_r+t_f) f_s$。
- 二极管：$P_D=I_F V_F$（异步），同步时换成 $I^2 R_{DSon}$。
- 电感：铜损 $I^2 DCR$ + 磁损（与 fs、磁通摆幅有关）。
- 电容：$P_{cap}=I_{ripple}^2 ESR$。
总损耗求和后按效率和热阻核算结温/温升。
:::

## 6. 元件取值与工程权衡

- **电感**：µH 值由纹波定，$I_{sat}$ 由峰值电流定，DCR 越小铜损越低但体积越大。数量级：手机几 µH~几十 µH，功率几百 µH~mH。
- **电容**：MLCC 选 X5R/X7R（别用 Y5V），耐压留量；Cin 要低 ESR、高纹波电流额定。
- **MOS**：低压选低 RDSon（如 30~100mΩ），高频选低 Qg；RDSon 与 Qg 互相矛盾。
- **二极管**：续流优先肖特基（低 VF）；高频注意 Qrr，必要用同步 MOS。

## 7. 完整设计示例

::: example 为 12V→5V/1A Buck 选全套功率元件
1. **电感**：由 [Buck 设计](buck.md) 得 L=22µH，$I_{SW(peak)}=1.15A$。选 **22µH、Isat≥1.5A、DCR≤50mΩ** 的屏蔽电感。
2. **输入电容 Cin**：Vin=12V，选 **2×10µF/25V X5R 0805**（低 ESR、纹波电流额定足够），DC bias 后仍 >10µF。
3. **输出电容 Cout**：2×22µF/10V X5R，ESR <10mΩ，保证纹波 <50mV。
4. **MOS（同步）**：30V 耐压、RDSon<20mΩ、Qg 小，3×3 DFN。
5. **二极管（异步方案备选）**：肖特基 30V/1A，VF=0.5V。
6. **验算损耗**：MOS 导通 0.046W、开关 ~0.1W、电感铜损 0.05W、Cin/Cout ESR 损忽略，总损 ~0.2W（同步方案），加外壳温升在安全范围。
:::

## 8. 仿真与实验

- LTspice 用具体器件 SPICE 模型（厂商官网下载）替换理想开关，跑温升/损耗；
- 用热像仪（或热电偶）测满载下电感、MOS、电容外壳温升；
- 测 Cin 纹波电流（用电流探头），核对是否超过额定；
- 示波器测 MOS 开关节点的 tr/tf，估算开关损耗。

## 扩展与变种电路

### 扩展1：MLCC 直流偏置降额与纹波电流

MLCC 标称 22µF，加直流偏压后实际容量可能腰斩；且必须承受开关纹波电流而不过热。

![12V 偏置下 22µF MLCC 实际只剩约 10µF，选型必须查 DC bias 曲线](../assets/schematics/power-component-selection-mlcc.svg)

::: example 工作原理与静态
- 铁电介质（X5R/X7R）在 DC 偏压下容量下降，0805/10µF 在 5V 下可能只剩 5µF。
- 纹波电流在 ESR 上发热 $P=I^2_{rms}ESR$，超额定会加速老化。
- 静态：按"实际有效容量"而非标称值设计纹波。
:::

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["X5R 容量随 DC 偏压下降"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 60, "right": 30, "top": 26, "bottom": 50},
  "xAxis": {"type": "category", "name": "DC 偏压 V", "data": [0,3,6,9,12], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "实际容量 %", "min": 0, "max": 100, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "X5R 容量随 DC 偏压下降", "type": "line", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [100, 75, 55, 45, 40]}
  ]
}
```

取值对比：多颗小 MLCC 并联对比单颗大 MLCC：等效 ESR 低、DC bias 降额分散、纹波电流能力强。适用：开关电源输入输出；不适用：Y5V 介质（降额严重）。

::: pitfall 按标称容量算纹波导致超标
- **现象**：实测纹波比设计大一倍。
- **原因**：DC bias 降额使实际容量减半。
- **解决**：按 DC bias 曲线选有效容量，多颗并联或选大封装。
:::

### 扩展2：MOSFET 导通与开关损耗、SOA

MOS 选型要在 RDSon（导通损）与 Qg（开关损）间权衡，并保证工作点在安全工作区（SOA）内。

![MOS 损耗分导通、开关、栅驱动三部分，开关损随 fs 增大](../assets/schematics/power-component-selection-mos.svg)

::: example 工作原理与静态
- 导通损 $I^2 R_{DSon} D$：选低 RDSon 管子。
- 开关损 $0.5 V I (t_r+t_f) f_s$：高频时占主导，选低 Qg、快开关管子。
- SOA：保证 Vds×Id 的工作点不超出硅片安全边界（脉冲/直流曲线）。
:::

取值对比：低 RDSon 大芯片对比小芯片：导通损低但 Qg 大、开关损高、贵。低频大电流选低 RDSon；高频选低 Qg。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["导通损", "开关损"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 60, "right": 30, "top": 26, "bottom": 50},
  "xAxis": {"type": "category", "name": "fs kHz", "data": ["100", "300", "500", "1000"], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "损耗 W", "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "导通损", "type": "line", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [0.05, 0.05, 0.05, 0.05]},
    {"name": "开关损", "type": "line", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#b5642e"},
     "data": [0.03, 0.08, 0.13, 0.25]}
  ]
}
```

::: pitfall 只看 RDSon 选 MOS 高频过热
- **现象**：低频效率好、高频发烫。
- **原因**：RDSon 低的大芯片 Qg 大，开关损随 fs 飙升。
- **解决**：按工作频率权衡 RDSon/Qg，高频选低 Qg 型号。
:::

## 9. 常见坑与故障现象

::: pitfall 常见坑
- **电感 Isat 选小**：重载饱和后电流尖峰烧 MOS。Isat 必须 > 峰值电流并降额。
- **Cin 纹波电流额定不够**：长期发热鼓包。选低 ESR、纹波电流额定足够的陶瓷。
- **MOS 耐压留量不足**：开关节点尖峰超过耐压击穿。按 $V_{in(max)}$ 加尖峰留到 1.5~2 倍。
- **二极管用普通整流管做高频续流**：Qrr 大、反向恢复损耗大发热。高频用肖特基或同步 MOS。
:::

## 10. 自测题

<details><summary>Buck：Iout=1A、ΔIL=0.3A，电感饱和电流至少选多大？</summary>

峰值电流 $I_{SW(peak)}=1+0.15=1.15A$。Isat 必须 >1.15A，按 20~30% 降额选 **≥1.5A**。

</details>

<details><summary>为什么 MLCC 标称 22µF 在 12V 下实际可能只有 10µF？选型怎么办？</summary>

铁电介质（X5R/X7R）有直流偏置效应，加偏压后容量下降。选型要查厂商 DC bias 曲线，按"实际有效容量"设计纹波，必要时多颗并联或选更大封装/更硬介质。

</details>

<details><summary>MOS 的导通损和开关损耗分别与什么有关？高频时哪个占主导？</summary>

导通损 $I^2 R_{DSon} D$ 与电流、RDSon、占空比有关，与频率无关；开关损 $0.5VI(t_r+t_f)f_s$ 与开关频率成正比。**高频时开关损耗占主导**，要选低 Qg、快开关的管子。

</details>

## 11. 参考资料

- [TI SLVA477A — Basic Calculation of a Buck Converter's Power Stage](https://www.ti.com/lit/an/slva477a/slva477a.pdf)
- [onsemi AND9596 — PCB Thermal Calculation for Power Devices](https://www.onsemi.com/pub/Collateral/AND9596-D.PDF)
- Maniktala, *Switching Power Supplies A–Z*, 2nd ed.
