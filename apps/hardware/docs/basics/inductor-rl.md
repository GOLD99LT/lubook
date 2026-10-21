---
id: inductor-rl
title: 电感原理与 RL 暂态 Inductor & RL Transient
part: 1
chapter: 动态元件与交流
order: 35
tags: [电感, RL, 暂态, 反电动势, 时间常数]
difficulty: 1
status: published
sources:
  - Lessons In Electric Circuits (Kuphaldt)
  - Practical Electronics for Inventors (Scherz & Monk)
  - https://www.falstad.com/circuit/
---

# 电感原理与 RL 暂态 Inductor & RL Transient

电容是"电压不能突变"，电感正好是它的**镜像**：**电流不能突变**。电感是绕成圈的导线，通电后储存磁场能量；你想突然改变电流，它就用自感电动势"顶"住你。这一章讲电感的直觉和 RL 电路的暂态过程。

## 1. 设计动机

::: motivation 为什么要懂电感
开关电源里到处是功率电感、继电器线圈要续流二极管、电机断电时会打出尖峰电压、PCB 走线也有寄生电感——这些全来自"电感电流不能突变、要阻止电流变化就产生高压"。看不懂电感，开关电源、继电器驱动、EMC 噪声全都无法理解。
:::

## 2. 原理图

![RL 通电电路：合上开关后电流 I 不能突变，按指数爬向稳态 Vs/R，时间常数 τ=L/R](../assets/schematics/inductor-rl.svg)

## 3. 电感是什么

::: analogy 电感像一个水车的惯性
电感是一圈导线，电流流过时产生磁场、储存能量。

- 电感 = **带很大惯性的水车**；
- 流过的电流 = **水车转速**；
- 想突然让水车转起来或停住，它都"不情愿"，要反抗你的力。

关键直觉：**电流不能突变**。你断开一个大电感回路，电流要瞬间掉到 0，电感就拼命产生高压（反电动势）试图维持电流——这就是继电器/电机断电时打火花、需要续流二极管的原因。
:::

电感的核心关系（只给结论）：

$$V_L = L\,\frac{dI}{dt}$$

符号含义：$V_L$ 是电感两端电压（V），$L$ 是电感量（亨利 H），$dI/dt$ 是电流变化率（A/s）。**电感电压正比于电流的变化率**——电流不变（直流稳态）时电压为 0，电感相当于短路。

## 4. RL 暂态（只给结论）

通电后电流按指数爬向稳态值：

$$I(t) = I_{\infty}\bigl(1 - e^{-t/\tau}\bigr),\qquad I_{\infty}=\frac{V_S}{R},\qquad \tau=\frac{L}{R}$$

符号含义：$I_\infty$ 是稳态电流（电感最终相当于短路，只剩电阻限流）；$\tau=L/R$ 是 RL 时间常数。注意和 RC 的 $\tau=RC$ 对比——一个是乘、一个是除。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["I(t)（回路电流）", "I∞（稳态电流）"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 56, "right": 24, "top": 26, "bottom": 56},
  "xAxis": {"type": "category", "name": "t / τ", "data": [0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.5,3,3.5,4,5], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "电流 / I∞", "min": 0, "max": 1.1, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "I(t)（回路电流）", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.6, "color": "#1a4f8b"},
     "data": [0,0.22,0.39,0.53,0.63,0.71,0.78,0.83,0.86,0.92,0.95,0.97,0.98,0.99]},
    {"name": "I∞（稳态电流）", "type": "line", "smooth": false, "showSymbol": false, "lineStyle": {"width": 2, "color": "#b5642e", "type": "dashed"},
     "data": [1,1,1,1,1,1,1,1,1,1,1,1,1,1]}
  ]
}
```

::: advanced 进阶：断电与续流
稳态时突然断开开关，电流要骤降到 0，$dI/dt$ 极大，电感产生很高的反电动势 $V_L$——它会试图维持原电流，于是在开关触点间打出电弧（可高达几百伏）。工程上在电感两端**反向并联续流二极管**，给断电时的环流一条低阻通路，把尖峰钳位住。继电器、电机线圈必须这么做。
:::

## 5. 带数字的算例

::: example 继电器线圈的续流
1. **电路**：12V 继电器线圈电阻 R=120Ω，电感 L=0.5 H，由 MCU 经三极管驱动。
2. **稳态电流**：$I_\infty=V_S/R=12/120=$ **100 mA**。
3. **时间常数**：$\tau=L/R=0.5/120\approx$ **4.2 ms**。通电后约 5τ≈21 ms 电流才到 100 mA，触点才可靠吸合。
4. **断电**：若不接续流二极管，三极管断开瞬间电流骤降，电感打出尖峰可能击穿三极管。**必须在线圈两端反向并一个 1N4148/1N4007**。
:::

## 6. 常见坑

::: pitfall 常见坑
- **驱动继电器/电机不接续流二极管**：现象——三极管/ MOS 管用几次就击穿，或触点烧蚀。原因——断电时电感反电动势尖峰。解决——感性负载两端反向并联续流二极管（快恢复更好）。
- **直流分析时把电感当开路**：现象——算静态电流算成 0。原因——混淆了电容和电感。解决——**直流稳态下电容开路、电感短路**，记反了就全错。
- **以为电感量越大越好**：现象——大电感导致电流上升太慢，开关电源响应迟缓。原因——$\tau=L/R$，L 大则暂态慢。解决——按开关频率和纹波要求选 L，不是越大越好。
:::

## 7. 自测题

<details><summary>直流稳态下，电感相当于什么？电容呢？</summary>

直流稳态电流不变，$dI/dt=0$ → $V_L=0$ → 电感相当于**短路（导线）**。电容 $dV/dt=0$ → 电流 0 → **开路**。
</details>

<details><summary>为什么断开继电器线圈时会打火花/击穿驱动管？怎么解决？</summary>

电感要维持原有电流不变，开关断开迫使电流骤降，$dI/dt$ 极大，产生很高的反电动势。解决：线圈两端**反向并联续流二极管**，断电时给感应电流一个回路，把电压钳在 0.7V 左右。
</details>

<details><summary>L=10mH、R=10Ω，时间常数 τ 是多少？</summary>

$\tau=L/R=0.01/10=$ **1 ms**。约 5τ=5ms 后电流到达稳态。
</details>

## 8. 参考资料

- [Lessons In Electric Circuits — Chapter 15: Inductors](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [Falstad RL 暂态仿真](https://www.falstad.com/circuit/)
- Practical Electronics for Inventors (Scherz & Monk) — Inductors & Relays
