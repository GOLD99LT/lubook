---
id: power-specs
title: 电源指标：纹波、效率、调整率与时序 Power Supply Specifications
part: 6
chapter: 电源基础
order: 5
tags: [电源, 纹波, 效率, 线性调整率, 负载调整率, 上电时序]
difficulty: 2
status: published
sources:
  - TI SLVA477A Basic Calculation of a Buck Converter's Power Stage
  - Erickson & Maksimovic, Fundamentals of Power Electronics, 2nd ed.
  - Pressman, Billings, Morey, Switching Power Supply Design, 3rd ed.
---

# 电源指标：纹波、效率、调整率与时序 Power Supply Specifications

## 1. 设计动机

::: motivation 为什么要先谈指标
一块电路板上 MCU、FPGA、ADC、射频模块对"电"的要求各不相同：MCU 要干净的 3.3V，ADC 要噪声极低的基准，FPGA  core 电压可能只有 0.9V 且要求多路电源按顺序上电。电源设计的第一步不是画电路，而是**把"多干净、多稳、多省电、怎么排序"这些要求量化成指标**。指标定错了，后面拓扑再好也是白做——比如给噪声敏感的 ADC 直接用开关电源而不评估纹波，就是指标没把好关。
:::

本章先建立一套通用的"电源体检表"：无论线性稳压、LDO 还是开关电源，评价它们的尺子是同一组指标。后续各章都用这把尺子去衡量具体电路。

## 2. 原理图

![电源指标测量框架：输入源给 UUT 供电，输出接电子负载，示波器在输出端测纹波，效率由输入输出功率比得到](../assets/schematics/power-specs.svg)

测量时三件套：**可调输入源**（扫描 Vin 范围）、**电子负载**（扫描 Iout 范围）、**示波器 + 真有效值功率计**。所有指标都是在这台架子上、扫过输入与负载两个极端后读出来的。

## 3. 静态分析（DC）

静态指标回答"输出到底准不准、稳不稳"，都在直流下测：

- **输出电压精度 $V_{out}$（Output Voltage Accuracy）**：标称值加全温、全输入、全负载后的偏差，通常 ±2%~±5%。
- **线性调整率（Line Regulation）**：负载固定，输入在全范围内变化时输出的漂移：
  $$\text{Line Reg}=\frac{\Delta V_{out}}{\Delta V_{in}}\quad(\text{mV/V，或用 \%/V})$$
  例：Vin 从 9V 扫到 15V（ΔVin=6V），Vout 漂移 6mV，则线性调整率 = 1mV/V。
- **负载调整率（Load Regulation）**：输入固定，负载电流从空载到满载变化时输出的漂移：
  $$\text{Load Reg}=\frac{\Delta V_{out}}{\Delta I_{out}}\quad(\text{mV/A})$$
  本质上就是输出阻抗 $Z_{out}$：负载调整率越小，电源带负载越"硬"。
- ** dropout 压差（详见 [LDO 一章](ldo.md)）**：维持稳压所需的最小输入-输出压差。

## 4. 动态分析（AC / 瞬态）

动态指标回答"输出在时间上抖不抖、突变时恢复快不快"。

**输出纹波与噪声（Ripple & Noise）**：开关电源输出上叠加的周期性三角波（纹波）加高频毛刺（噪声），单位 mVpp，用示波器 AC 耦合、20MHz 带宽限制测。下图是 5V 输出上约 50mVpp 的开关纹波：

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["Vout（含纹波）"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 70, "right": 30, "top": 30, "bottom": 50},
  "xAxis": {"type": "category", "name": "时间 µs", "data": [0,1,2,3,4,5,6,7,8], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "Vout V", "min": 4.95, "max": 5.05, "interval": 0.025, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "Vout（含纹波）", "type": "line", "step": "end", "showSymbol": false, "lineStyle": {"width": 2.6, "color": "#1a4f8b"},
     "data": [5.0, 5.0125, 5.025, 5.0125, 5.0, 4.9875, 4.975, 4.9875, 5.0]}
  ]
}
```

**负载瞬态响应（Load Transient Response）**：负载电流阶跃时，输出先掉/冲一个坑，再由反馈环拉回来。坑的深度 $\Delta V_{step}$ 和恢复时间 $t_{settle}$ 直接反映环路快慢（详见 [Buck 环路一节](buck.md)）。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["Vout 负载阶跃恢复"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 70, "right": 30, "top": 30, "bottom": 50},
  "xAxis": {"type": "category", "name": "时间 µs", "data": [0,5,10,12,14,18,25,35,50], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "Vout V", "min": 4.9, "max": 5.1, "interval": 0.05, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "Vout 负载阶跃恢复", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.6, "color": "#b5642e"},
     "data": [5.0, 5.0, 4.94, 4.93, 4.96, 4.99, 5.0, 5.0, 5.0]}
  ]
}
```

## 5. 环路分析

所有稳压电源都是一个**负反馈闭环**：采样输出 → 与基准比较 → 误差放大器驱动调整管 → 把输出拉回设定值。

- 结论：线性调整率、负载调整率、纹波抑制（PSRR，见 [LDO](ldo.md)）都是**环路增益的外在表现**——环路增益越高，这三项越好。
- 环路带宽决定瞬态恢复速度：带宽越高，负载阶跃坑越浅、恢复越快，但太高会振荡。工程上开关电源环路穿越频率通常取开关频率的 1/10~1/5。

::: advanced 进阶：调整率与环路增益的关系
把电源看成理想增益 $A$（误差放大器+调整管）与反馈系数 $\beta$ 的闭环。输出对输入扰动的抑制比为 $1/(1+A\beta)$，对负载扰动的抑制由输出阻抗 $Z_{out}=Z_{open}/(1+A\beta)$ 决定。
故负载调整率 $=\Delta V_{out}/\Delta I_{out}\approx Z_{open}/(1+T)$，环路增益 $T=A\beta$ 越大，调整率越小。这解释了为什么"加电容、改补偿"改善瞬态的同时也改善了 DC 调整率——它们本质上是同一个环路。
:::

## 6. 元件取值与工程权衡

选型时这些指标互相拉扯，不可能同时最优：

- **效率 vs 纹波**：开关频率越高，电感电容可越小、动态越快，但开关损耗越大、效率越低。
- **输出电容 vs 纹波/瞬态**：电容越大纹波越小、瞬态坑越浅，但成本、体积、上电冲击电流增大。
- **压差 vs 发热**：LDO/线性电源 Vin−Vout 越大，功耗 $(V_{in}-V_{out})I_{out}$ 越大，越要散热。
- **典型数量级**：通用数字电源纹波目标 ≤ 1% Vout；模拟/ADC 供电要 mV 级；效率目标开关电源 ≥ 85%，LDO 看压差（低压差时效率≈Vout/Vin）。

## 7. 完整设计示例

::: example 给 ADC 定电源指标
1. **需求**：12bit ADC 满量程 3.3V，1 LSB = 3.3V/4096 ≈ 0.8mV。电源噪声应远小于 1 LSB，取目标 ≤ 0.5mVpp。
2. **定纹波指标**：选 LDO 而非直接用开关电源后级，纹波压到 <1mVpp，PSRR 在 ADC 采样频率处 > 50dB。
3. **定精度**：基准/电源精度 ±1%（±33mV）远大于 1 LSB，所以精度由基准决定，电源纹波只占小头。
4. **定效率**：整机由 USB 5V 供电、电池备份，3.3V/100mA，LDO 功耗 (5−3.3)×0.1=0.17W，可接受；若 5V 由电池来且电流大，则改开关预稳压 + LDO 后级。
5. **定时序**：ADC 与 MCU 共用 3.3V 单轨，无需复杂时序；若后续加 FPGA core 0.9V，则要求 3.3V 先于 0.9V 上电（见扩展）。
6. **验算**：1 LSB = 0.8mV，电源纹波应远小于它（工程上宜 ≤ 1/2 LSB ≈ 0.4mV）。原拟 0.5mVpp 仍偏近 1 LSB，故收紧纹波预算 ≤ 0.3mVpp，靠 LDO + 10µF+0.1µF 去耦实现。
:::

## 8. 仿真与实验

在 LTspice 里搭一个理想 DC-DC 行为模型（或用厂商免费的 LTpowerCAD / WEBENCH），按下面步骤读指标：

- **DC 扫描**：`.dc vin 9 15 0.5`，测 Vout 随 Vin 的斜率 = 线性调整率；
- **负载扫描**：把 Rload 从 1k 扫到 5Ω，测 Vout 跌落 = 负载调整率；
- **瞬态**：`.tran 200u`，观察开关节点与输出纹波；
- **瞬态阶跃**：用一个脉冲电流源（50mA↔500mA，边沿 1µs）模拟负载突变，测坑深与恢复时间。

## 扩展与变种电路

### 扩展1：多路电源上电时序 Power-Up Sequencing

数字 SoC/FPGA 常要求多组电压按固定顺序、固定斜率上电，否则闩锁（latch-up）或损坏内核。用时序控制器或带跟踪/延时的 LDO/DCDC 实现。

![3.3V 先爬升，延迟后 1.8V 再爬升，两轨都达标后 RESET# 才释放](../assets/schematics/power-specs-sequencing.svg)

::: example 工作原理与静态
- **顺序（Sequencing）**：先上电的轨通常是 I/O 轨（3.3V），后上电 core 轨（1.0V），避免 I/O 引脚向未上电 core 倒灌电流。
- **比例/跟踪（Tracking）**：多轨以相同斜率一起爬升，适合对端接电压敏感的接口。
- **复位释放（POR）**：用电源监控芯片（如带延时的复位 IC），等所有轨进入阈值窗口后才放开 RESET#，让 MCU 在电源稳定后才启动。
- 静态：每轨输出直流值由各自反馈分压设定；时序由使能引脚 EN 的先后拉到决定。
:::

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["VDD_3V3", "VDD_1V8", "RESET#"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 60, "right": 30, "top": 26, "bottom": 50},
  "xAxis": {"type": "category", "name": "时间 ms", "data": [0,2,4,6,8,10,12,16,20], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "电压 V", "min": 0, "max": 3.6, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "VDD_3V3", "type": "line", "step": "end", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [0, 0.8, 2.0, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3]},
    {"name": "VDD_1V8", "type": "line", "step": "end", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#b5642e"},
     "data": [0, 0, 0, 0.3, 0.9, 1.8, 1.8, 1.8, 1.8]},
    {"name": "RESET#", "type": "line", "step": "end", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#4f9e63"},
     "data": [0, 0, 0, 0, 0, 0.1, 0.1, 3.3, 3.3]}
  ]
}
```

取值对比：用"上电顺序控制器 + 复位 IC"（一颗 ~¥1–2）对比"纯 RC 延时凑"（省一颗芯片但不精确、不耐温）。时序延迟 $t_{delay}$ 由 EN 引脚 RC 或控制器寄存器设定，典型 1–100ms。适用：多轨 FPGA/SoC、工业板卡；不适用：单轨简单 MCU。

::: pitfall core 先于 I/O 上电导致闩锁
- **现象**：core 轨先起来、I/O 轨还慢，芯片大电流锁定、发烫。
- **原因**：I/O 引脚通过内部 ESD 二极管向未上电 core 倒灌，触发寄生 SCR 闩锁。
- **解决**：严格按手册要求 I/O 先、core 后，或用跟踪同时爬升；关键板加时序控制器与 POR。
:::

## 9. 常见坑与故障现象

::: pitfall 常见坑
- **用示波器普通探头测纹波、读数偏大**：普通地线夹像天线，拾入空间高频噪声，纹波读数可能虚高数倍。解决：用弹簧地针、AC 耦合、20MHz 带宽限制，探头尽量靠近电容。
- **只看 DC 精度不看全温全载**：规格书 ±2% 是 25℃ 典型值，全温范围可能 ±4%。精密电路要按最差工况（最低 Vin、最高温、满载）验算。
- **效率只测额定点**：锂电池设备多数时间在轻载，额定 90% 不代表轻载省电；要看轻载效率曲线（PFM/auto mode，见 [Buck 扩展](buck.md)）。
:::

## 10. 自测题

<details><summary>负载固定，Vin 从 12V 升到 18V，Vout 从 5.000V 漂到 5.006V，线性调整率是多少 mV/V？</summary>

ΔVin = 18−12 = 6V，ΔVout = 6mV。线性调整率 = 6mV / 6V = **1 mV/V**（即每伏输入变化引起 1mV 输出漂移）。

</details>

<details><summary>为什么说"负载调整率本质上就是输出阻抗"？一个输出阻抗 10mΩ 的电源，负载从 0.1A 跳到 1A 时输出掉多少？</summary>

负载电流变化 ΔI=0.9A 在输出阻抗上产生 ΔV = Zout·ΔI = 10mΩ × 0.9A = **9mV**。这正是负载调整率（mV/A × ΔI），所以负载调整率越小 = 输出阻抗越低 = 带载越硬。

</details>

## 11. 参考资料

- [TI SLVA477A — Basic Calculation of a Buck Converter's Power Stage](https://www.ti.com/lit/an/slva477a/slva477a.pdf)
- Erickson & Maksimovic, *Fundamentals of Power Electronics*, 2nd ed.（调整率与环路增益）
- Pressman, Billings, Morey, *Switching Power Supply Design*, 3rd ed.
- [ADI LTpowerCAD / LTpowerPlanner 设计工具](https://www.analog.com/en/design-center/design-tools-and-calculators.html)
