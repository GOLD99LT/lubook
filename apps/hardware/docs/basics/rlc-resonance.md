---
id: rlc-resonance
title: RLC 电路与谐振 RLC Circuits & Resonance
part: 1
chapter: 动态元件与交流
order: 50
tags: [RLC, 谐振, 谐振频率, 选频, 带通, Q值]
difficulty: 2
status: published
sources:
  - Lessons In Electric Circuits (Kuphaldt)
  - https://www.falstad.com/circuit/
  - Practical Electronics for Inventors (Scherz & Monk)
---

# RLC 电路与谐振 RLC Circuits & Resonance

把电阻 R、电感 L、电容 C 放在一起，会出现一个神奇现象：在某个特定频率下，电感和电容的作用互相抵消，整个电路只表现为纯电阻，电流突然达到最大。这就是**谐振（Resonance）**。收音机选台、振荡器、滤波器、无线充电都靠它。

## 1. 设计动机

::: motivation 为什么收音机只收到一个台
空中有无数电台的电磁波同时打进天线。收音机里有一个可调的 LC 谐振回路，拧旋钮就是调电容——只有当某个电台的频率正好等于回路谐振频率时，信号才被"放大选中"，其他频率被抑制。这就是谐振的选频作用。
:::

## 2. 原理图与谐振曲线

![串联 RLC 电路：R、L、C 串在交流源上](../assets/schematics/rlc-resonance.svg)

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["回路电流（相对值）"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 56, "right": 24, "top": 26, "bottom": 56},
  "xAxis": {"type": "category", "name": "频率 f / f₀", "data": [0.2,0.4,0.6,0.8,0.9,1.0,1.1,1.2,1.5,2,3], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "I / Imax", "min": 0, "max": 1.05, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "回路电流（相对值）", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.6, "color": "#1a4f8b"},
     "data": [0.04,0.1,0.2,0.42,0.72,1.0,0.72,0.42,0.2,0.1,0.05]}
  ]
}
```

## 3. 谐振频率（最重要结论）

串联 RLC 发生谐振时，感抗等于容抗、互相抵消：

$$f_0 = \frac{1}{2\pi\sqrt{L\,C}}$$

符号含义：$f_0$ 是**谐振频率**（Hz），$L$ 是电感（H），$C$ 是电容（F）。在这个频率下：

- 总阻抗最小、等于纯电阻 R；
- 回路电流最大；
- 电压与电流同相（相位差为 0）。

::: analogy 荡秋千
谐振像推秋千：你推的节奏正好和秋千自然摆动节奏一致时，秋千越荡越高——这就是谐振。推快了或慢了，都荡不起来。LC 的"自然节奏"就是 $f_0$。
:::

**Q 值（品质因数）**描述谐振曲线的"尖不尖"：$Q=\dfrac{2\pi f_0 L}{R}$。Q 越高，曲线越尖、选频越准，但带宽越窄；R 越大 Q 越低、曲线越平缓。

::: advanced 进阶：并联谐振与电压谐振
串联谐振时电流最大（电流谐振）；若 L、C 并联，则在 $f_0$ 处阻抗最大、两端电压最高（电压谐振）。推导核心都是"感抗 = 容抗，$\omega L=1/(\omega C)$，解得 $\omega_0=1/\sqrt{LC}$"，即 $f_0=1/(2\pi\sqrt{LC})$。
:::

## 4. 带数字的算例

::: example 设计一个 1MHz 谐振回路
1. **需求**：做一个谐振在 1MHz 的选频网络。
2. **选 C**：取标准电容 C=100 pF。
3. **反算 L**：由 $f_0=1/(2\pi\sqrt{LC})$，得 $L=1/((2\pi f_0)^2 C)=1/((2\pi\times10^6)^2\times100\times10^{-12})\approx$ **253 µH**（取标称 270µH）。
4. **验证**：$\sqrt{LC}=\sqrt{253\times10^{-6}\times100\times10^{-12}}=\sqrt{2.53\times10^{-14}}=1.59\times10^{-7}$，$f_0=1/(2\pi\times1.59\times10^{-7})\approx1.0$ MHz。
5. **工程意义**：只有 1MHz 附近信号被选中，偏离越多衰减越大——这就是选台/滤波的原理。
:::

## 5. 常见坑

::: pitfall 常见坑
- **以为谐振是"好事"到处用**：现象——电源线上意外出现谐振尖峰，EMI 超标。原因——寄生 L 和去耦 C 在某频率形成谐振，阻抗骤升。解决——加阻尼电阻/选低 ESR 电容，或避开该频率。
- **Q 值过高导致带宽太窄**：现象——收音机只收到一个台的一小段。原因——Q 太高、选频曲线太尖，通带不够覆盖信号带宽。解决——适当增大串联电阻降低 Q、展宽带宽。
- **忽略元件寄生参数**：现象——仿真谐振频率准，实物差很多。原因——电感自身电容、PCB 走线电感让实际 L、C 偏离计算值。解决——实物微调，预留可调电容或电感。
:::

## 6. 自测题

<details><summary>L=1mH、C=1nF，谐振频率大约多少？</summary>

$f_0=1/(2\pi\sqrt{LC})=1/(2\pi\sqrt{10^{-3}\times10^{-9}})=1/(2\pi\times10^{-6})\approx$ **159 kHz**。
</details>

<details><summary>串联谐振时，总阻抗等于多少？电流最大还是最小？</summary>

感抗与容抗抵消，总阻抗 = **纯电阻 R**（最小），因此**电流最大**。这叫电流谐振。
</details>

<details><summary>Q 值高好还是低好？</summary>

看用途：选台/振荡器要**高 Q**（曲线尖、选得准）；宽带滤波/阻尼要**低 Q**（曲线平缓、带宽宽）。没有绝对好坏，按通带宽度要求权衡。
</details>

## 7. 参考资料

- [Lessons In Electric Circuits — Resonance in AC Circuits](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [Falstad RLC 谐振仿真](https://www.falstad.com/circuit/)
- Practical Electronics for Inventors (Scherz & Monk) — Resonance chapter
