---
id: capacitor-rc
title: 电容原理与 RC 时间常数 Capacitor & RC Time Constant
part: 1
chapter: 动态元件与交流
order: 30
tags: [电容, RC, 时间常数, 暂态, 充放电]
difficulty: 1
status: published
sources:
  - Lessons In Electric Circuits (Kuphaldt)
  - Practical Electronics for Inventors (Scherz & Monk)
  - https://www.falstad.com/circuit/
---

# 电容原理与 RC 时间常数 Capacitor & RC Time Constant

从这一章开始进入**动态元件**：电容和电感。它们不像电阻那样"电流正比于电压"，而是和电压/电流的**变化率**打交道，于是电路出现了"时间"概念——通电后电压不是瞬间到稳态，而是一步步爬过去。这个爬升有多快，由时间常数 $\tau=RC$ 决定。

## 1. 设计动机

::: motivation 为什么到处都有电容
电源入口要加大电容滤波、MCU 每个芯片旁要加 0.1µF 去耦、按键消抖要用 RC、上电复位靠电容慢上电——这些全是在利用"电容电压不能突变"和"RC 决定快慢"。看不懂 RC，就看不懂为什么电源要滤波、为什么上电要延时。
:::

## 2. 原理图

![RC 充电电路：t=0 合上开关，电源 Vs 经电阻 R 向电容 C 充电，Vc 逐渐上升](../assets/schematics/capacitor-rc.svg)

## 3. 电容是什么

::: analogy 电容像一个小水桶
电容是两片靠近的金属板，中间绝缘。往板上"灌"电荷，它就存起来；电压越高存得越多。

- 电容 = **水桶**，容量 C = 桶的粗细；
- 电容电压 = **桶里的水位**；
- 电流 = **进水龙头的流量**。

关键直觉：**水位不能瞬间跳变**——你再怎么开水龙头，桶里的水也要时间才能涨上去。电容电压也一样：$V_C$ 不能突变，突变意味着电流无穷大，物理上不可能。
:::

电容的核心关系（只给结论）：

$$Q = C\,V_C \qquad\Longleftrightarrow\qquad I_C = C\,\frac{dV_C}{dt}$$

符号含义：$Q$ 是存的电荷（库仑 C），$C$ 是电容量（法拉 F），$V_C$ 是电容两端电压（V）；第二个式子说**电容电流正比于电压的变化率**——电压不变时电流为 0（直流稳态下电容相当于开路），电压变化越快电流越大。

## 4. RC 时间常数（最重要的结论）

充电时电容电压按指数曲线逼近电源电压：

$$V_C(t) = V_S\bigl(1 - e^{-t/\tau}\bigr),\qquad \tau = R\,C$$

符号含义：$V_S$ 是电源电压，$t$ 是合上开关后的时间，$\tau$（读作 tau）是**时间常数**，等于电阻乘电容。几个记住就行的数：

- **1τ** 时，电容充到约 **63%**；
- **3τ** 时，约 **95%**；
- **5τ** 时，约 **99%**，工程上认为充满。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["Vc（电容电压）", "Vs（电源）"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 56, "right": 24, "top": 26, "bottom": 56},
  "xAxis": {"type": "category", "name": "t / τ", "data": [0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.5,3,3.5,4,5], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "电压 V", "min": 0, "max": 5.5, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "Vc（电容电压）", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.6, "color": "#1a4f8b"},
     "data": [0,1.10,1.97,2.64,3.16,3.57,3.88,4.13,4.32,4.59,4.75,4.85,4.91,4.97]},
    {"name": "Vs（电源）", "type": "line", "smooth": false, "showSymbol": false, "lineStyle": {"width": 2, "color": "#b5642e", "type": "dashed"},
     "data": [5,5,5,5,5,5,5,5,5,5,5,5,5,5]}
  ]
}
```

::: advanced 进阶：放电曲线与推导
电容经电阻放电时 $V_C(t)=V_0 e^{-t/\tau}$，同样按指数衰减，时间常数还是 $\tau=RC$。推导：回路 KVL 给 $V_R+V_C=0$，即 $RC\,dV_C/dt+V_C=0$，解就是指数。充电方程同理 $RC\,dV_C/dt+V_C=V_S$。记住"指数趋近、τ 决定快慢"即可，推导不必背。
:::

## 5. 带数字的算例

::: example MCU 上电复位的 RC
1. **需求**：MCU 的复位脚要一个慢慢上升的电压，让它晚一点开始工作，电源才稳定。
2. **取值**：$R=100$ kΩ，$C=10$ µF。
3. **时间常数**：$\tau=RC=100\times10^3 \times 10\times10^{-6}=$ **1 秒**。
4. **复位脚判到 0.9×3.3V≈3V 才算高电平**：约 $3\tau=3$ 秒后才越过阈值——MCU 延时约 3 秒才开始运行。
5. **工程调整**：想要 0.3 秒延时，把 C 降到 1µF 即可（τ=0.1s，3τ=0.3s）。
:::

::: example 按键消抖
机械按键按下/松开时会抖动几毫秒。用 R=10k、C=0.1µF：$\tau=10^4\times10^{-7}=1$ ms。滤波后尖刺被电容吸收，后面读到的是干净电平。
:::

## 6. 常见坑

::: pitfall 常见坑
- **以为电容越大越好，结果上电慢得离谱**：现象——电源入口电容取到几百 mF，设备开机半天才能用。原因——大容量电容经电源内阻充电，τ 大、上电慢。解决——按实际需要选容值，大容量电解用于储能，小容量陶瓷用于高频去耦，分工明确。
- **断电后电容里还有高压，摸上去触电**：现象——设备断电一段时间，大电容两脚仍有电。原因——电容电荷没放掉。解决——大电容并联泄放电阻，维修前先放电；这是安全红线。
- **直流稳态下把电容当导线**：现象——分析直流电路时以为电容导通。原因——直流稳态 $dV/dt=0$，$I_C=0$，电容相当于**开路**。解决——直流分析一律先把电容拿掉（开路）；交流/暂态才考虑它。
:::

## 7. 自测题

<details><summary>R=1kΩ、C=1µF，时间常数 τ 是多少？大约多久充满？</summary>

$\tau=RC=10^3\times10^{-6}=$ **1 ms**。工程上 **5τ = 5 ms** 充满到 99%。
</details>

<details><summary>为什么说"电容两端电压不能突变"？硬要突变会怎样？</summary>

由 $I=C\,dV/dt$，电压突变意味着 $dV/dt=\infty$，需要无穷大电流——现实中做不到。所以电容电压只能连续变化，电流可以突变。这就是 RC 上电缓启动、按键消抖的物理基础。
</details>

<details><summary>直流稳态下，电容相当于开路还是短路？电感呢？</summary>

电容在直流稳态 $dV/dt=0$ → 电流 0 → **开路**。（对照：电感在直流稳态 $dI/dt=0$ → 电压 0 → **短路**，下一章讲。）
</details>

## 8. 参考资料

- [Lessons In Electric Circuits — Chapter 13: Capacitors](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [Falstad RC 充放电仿真](https://www.falstad.com/circuit/)
- Practical Electronics for Inventors (Scherz & Monk) — Capacitors & RC chapter
