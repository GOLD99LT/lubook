---
id: signal-integrity
title: 信号完整性：反射、阻抗匹配与端接 Signal Integrity
part: 7
chapter: 信号完整性与 EMC
order: 35
tags: [信号完整性, 反射, 特性阻抗, 端接, 微带线, 带状线]
difficulty: 3
status: published
sources:
  - Howard Johnson, High Speed Digital Design — A Handbook of Black Magic
  - Saturn PCB Design Toolkit
  - IPC-2141 Controlled Impedance Circuit Boards
---

# 信号完整性：反射、阻抗匹配与端接 Signal Integrity

当数字信号的边沿越来越陡、走线相对变长，走线就不再是"一根导线"，而是一条**传输线（Transmission Line）**。信号在上面以有限速度传播，遇到阻抗不连续就会**反射（Reflection）**，造成振铃、过冲、误触发。信号完整性（Signal Integrity, SI）就是研究怎么让波形干净到达。

## 1. 设计动机

::: motivation 为什么会有振铃
你有没有遇到过：示波器上看一个本该干净的方波，边沿上却叠加了几 MHz 的振荡？这多半不是芯片坏了，而是走线太长、没端接，信号在源和负载之间来回反弹。低速短走线没事，高速就得按传输线设计。
:::

## 2. 图示：传输线与反射

![源、传输线、负载三段；负载阻抗不匹配产生反射波](../assets/schematics/signal-integrity.svg)

## 3. 机理与定量

### 什么时候必须按传输线处理

FR-4 上信号速度约 $v\approx c/2\approx 15\text{ cm/ns}$。经验判据：当线长对应的单向延迟 $T_d$ 与上升沿 $t_r$ 可比时，

$$T_d > \frac{t_r}{6}\quad\Longleftrightarrow\quad L > \frac{t_r}{6}\times 15\text{ cm/ns}$$

- $t_r=1\text{ ns}$ → $L>2.5\text{ cm}$ 就要端接
- $t_r=5\text{ ns}$ → $L>12.5\text{ cm}$ 才需考虑

短于这个长度，反射波还没回到源，信号已稳定，可忽略。

### 反射系数

$$\Gamma = \frac{Z_L-Z_0}{Z_L+Z_0}$$

- $Z_L=Z_0$ → $\Gamma=0$，无反射（理想匹配）
- $Z_L=\infty$（高阻负载）→ $\Gamma=+1$，全反射正电压（过冲）
- $Z_L=0$（短路）→ $\Gamma=-1$，全反射负电压

### 特性阻抗近似式

**微带线（Microstrip，表层线）**，Wheeler 近似：

$$Z_0 \approx \frac{87}{\sqrt{\varepsilon_r+1.41}}\ln\!\left(\frac{5.98h}{0.8w+t}\right)$$

**带状线（Stripline，两平面间）**：

$$Z_0 \approx \frac{60}{\sqrt{\varepsilon_r}}\ln\!\left(\frac{1.9(2h+t)}{0.8w+t}\right)$$

- $h$：线到参考平面距离，$w$：线宽，$t$：铜厚
- $\varepsilon_r$：介质常数（FR-4 ≈ 4.3）

微带线因一部分场在空气里，有效 $\varepsilon_{r,eff}$ 比 $\varepsilon_r$ 小，同阻抗下线更宽。

## 4. 完整设计示例

::: example 做 50Ω 微带线
1. **需求**：USB 需要 90Ω 差分（单端约 45Ω），先做 50Ω 单端微带。
2. **叠层**：表层线，到 L2 GND 距离 h=0.13 mm（5 mil），1oz 铜 t=35µm。
3. **代入微带式**：FR-4 εr=4.3，87/√5.71≈36.4；调 w 使 Z0≈50Ω。
4. **结果**：含铜厚 t=35µm 实算，w≈0.20 mm 时 Z0≈50Ω（若忽略铜厚近似 w 会更粗；用 Saturn PCB 反推验证）。
5. **端接**：线长若 >2.5cm（tr=1ns），源端串 22~33Ω 端接。
:::

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["无终端接(振铃)", "正确端接(干净)"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 56, "right": 24, "top": 26, "bottom": 56},
  "xAxis": {"type": "category", "name": "时间 ns", "data": [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "电压 V", "min": 0, "max": 4, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "无终端接(振铃)", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#b03a3a"},
     "data": [0,1.2,3.8,2.6,3.4,2.9,3.2,3.05,3.15,3.1,3.12]},
    {"name": "正确端接(干净)", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#2f6e4f"},
     "data": [0,1.0,3.0,3.1,3.1,3.1,3.1,3.1,3.1,3.1,3.1]}
  ]
}
```

## 5. 端接方式对比

| 方式 | 位置 | 阻值 | 功耗 | 适用 |
|---|---|---|---|---|
| 源端串联 | 源端 | Rs≈Z₀ | 无 | 点对点最常用 |
| 戴维南并联 | 负载端 | R1∥R2=Z₀ | 大 | 多负载/DDR |
| RC 并联 | 负载端 | Rt=Z₀+C | 无直流 | 单向 CMOS 总线 |

## 6. 检查与仿真

- **IBIS 仿真**：用芯片 IBIS 模型跑反射/振铃，看是否在噪声容限内。
- **实测**：示波器高带宽探头看边沿振铃与过冲。
- **阻抗 TDR**：TDR 仪器看走线阻抗是否均匀（过孔、拐角处）。

## 扩展与变种电路

### 扩展1：源端串联端接 Series Termination

最常用的端接：在源端串一只等于 Z₀ 的电阻。

![驱动源串联 Rs≈Z₀ 后接传输线到高阻负载](../assets/schematics/si-series-termination.svg)

::: example 机理与定量
- "源内阻 + Rs" = Z₀，源端匹配。
- 入射波到高阻负载全反射（Γ=+1），反射波回到源端被 Rs 吸收，不再二次反射。
- 负载端看到干净波形。
- 不耗电、占板小，点对点拓扑首选。Rs 典型 22~33Ω（源内阻已占一部分）。
:::

准则对比：

| 端接 | 功耗 | 适合拓扑 |
|---|---|---|
| 源端串联 | 0 | 点对点 |
| 负载并联 | 有 | 多负载 |

::: pitfall 串联端接用在多负载分支
- **现象**：分支上远端波形还是振铃。
- **原因**：串联端接要求负载在传输线末端，分支(stub)会引入新反射。
- **解决**：多负载用并联端接，或让负载全在同一末端。
:::

### 扩展2：戴维南并联端接 Thevenin Termination

负载端两个电阻分别上拉/下拉，等效阻抗=Z₀。

![负载端 R1 上拉 Vcc、R2 下拉 GND，二者并联=Z₀](../assets/schematics/si-thevenin-termination.svg)

::: example 机理与定量
- 要求 $R_1\parallel R_2=Z_0$，且分压偏置在逻辑阈值中间。
- 匹配吸收负载端反射，适合多负载点（DDR 地址/命令）。
- 代价：R1-R2 一直有电流到地，静态功耗大。
:::

准则对比：

| 项 | 戴维南 | 串联 |
|---|---|---|
| 功耗 | 大 | 无 |
| 多负载 | 好 | 差 |

::: pitfall 戴维南偏置偏了导致电平错误
- **现象**：端接后高/低电平偏离逻辑阈值。
- **原因**：R1/R2 分压没对准供电与阈值。
- **解决**：按 Vcc/Voh/Vol 算 R1、R2 取值。
:::

### 扩展3：RC 端接 RC Termination

电阻串电容到地，隔直不耗电。

![负载端 Rt 串 Ct 到地，电容隔直、交流吸收反射](../assets/schematics/si-rc-termination.svg)

::: example 机理与定量
- 直流下电容开路，不耗电；交流瞬态经 Rt=Z₀ 吸收反射。
- Ct 要选准：太小高频衰、太大延迟上升沿。典型 100pF~1nF。
- 适合单向 CMOS 总线（如某些 EEPROM 控制信号）。
:::

准则对比：

| 端接 | 直流功耗 | 复杂度 |
|---|---|---|
| 戴维南 | 有 | 中 |
| RC | 无 | 需选 Ct |

::: pitfall Ct 选太大拖慢边沿
- **现象**：端接后信号上升沿明显变缓。
- **原因**：Ct 与 Z₀ 构成 RC 低通，时间常数过大。
- **解决**：减小 Ct，或换串联端接。
:::

## 7. 常见坑与故障现象

::: pitfall 常见坑
- **短走线没当回事结果高速下振铃**：判据是 $T_d>t_r/6$，不是看绝对长度。1ns 上升沿下 2.5cm 就够长。
- **端接电阻放错位置**：串联端接电阻必须紧贴源端，放中间无效。
- **过孔/分支(stub)引入反射**：高速线换层打个过孔、或接个分支，都成了不连续点。
- **只算阻抗不看回流**：线宽算对了，但下方参考平面开槽，阻抗照样不连续。
:::

## 8. 自测题

<details><summary>FR-4 上信号速度约多少？上升沿 1ns 的信号，线长超过多少就要按传输线处理？</summary>

约 15 cm/ns（光速一半）。判据 $T_d>t_r/6$ → 线长 > (1/6)×15 ≈ **2.5 cm**。超过就要端接，否则反射来不及回源、造成振铃。

</details>

<details><summary>负载开路（ZL→∞）时反射系数 Γ 是多少？会发生什么？</summary>

$\Gamma=(Z_L-Z_0)/(Z_L+Z_0)\to+1$，全反射正电压。入射波叠上反射波，负载端电压冲到约 2 倍入射值 → **过冲（overshoot）**，长时间会损伤栅极氧化层。

</details>

<details><summary>源端串联端接为什么不耗电？它适合什么拓扑？</summary>

电阻串在源端与传输线之间，静态时电阻上无直流电流（负载高阻）。它匹配的是源端阻抗，反射回到源被吸收。适合**点对点**拓扑；多负载分支不适合，要用并联端接。

</details>

## 9. 参考资料

- Howard Johnson & Martin Graham, *High Speed Digital Design: A Handbook of Black Magic*
- IPC-2141 Controlled Impedance Circuit Boards
- Saturn PCB Design Toolkit（微带/带状线阻抗计算）
