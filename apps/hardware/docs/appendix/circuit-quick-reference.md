---
id: circuit-quick-reference
title: 常用电路速查图集
part: 10
chapter: 附录
order: 30
tags: [电路, 速查, 原理图, 分压, 滤波, 运放, 电源, H桥]
difficulty: 2
status: published
sources:
  - https://www.ti.com/lit/an/slod006b/slod006b.pdf
  - https://www.ti.com/lit/an/sloa058/sloa058.pdf
---

# 附录 F · 常用电路速查图集

16 个工程中最常复用的小电路，每个一张示意图 + 一句话用途 + 关键公式/取值。设计时直接套用，再按需求细化。

## F.1 电阻分压

![电阻分压](../assets/schematics/circuit-divider.svg)

- **用途**：把高电压按比例降到 ADC 量程内。
- **公式**：$V_{out}=V_{in}\cdot\dfrac{R_2}{R_1+R_2}$
- **取值**：R1=R2 得 1/2；高阻抗源需让分压电阻远小于源阻抗。

## F.2 上拉电阻

![上拉电阻与按键](../assets/schematics/circuit-pullup.svg)

- **用途**：开漏/开集输出、按键常态保持高电平。
- **取值**：I²C 用 4.7k；按键/通用用 10k。太小费电，太大受噪声影响。

## F.3 RC 低通滤波

![RC 低通](../assets/schematics/circuit-rclp.svg)

- **用途**：滤除高频噪声、PWM 转模拟电压。
- **公式**：截止频率 $f_c=\dfrac{1}{2\pi RC}$；例 R=1k、C=1µF → $f_c\approx159$ Hz。

## F.4 BJT 三极管开关

![NPN 开关驱动 LED](../assets/schematics/circuit-bjt-switch.svg)

- **用途**：用 GPIO 小电流控制 LED/继电器等负载。
- **条件**：饱和 $I_B>I_C/\beta$；基极串 1k 限流；LED 回路串 220Ω~1k 限流电阻；发射极接地。

## F.5 LDO 典型应用

![LDO 典型应用](../assets/schematics/circuit-ldo.svg)

- **用途**：把 5V 稳成干净的 3.3V 给 MCU/模拟电路。
- **要点**：输入输出各并 10µF；压差越小效率越高；功耗 $P=(V_{in}-V_{out})I$。

## F.6 Buck 降压典型

![Buck 降压典型](../assets/schematics/circuit-buck.svg)

- **用途**：高效把高压降到低压（如 12V→5V/3A）。
- **公式**：$V_{out}\approx D\cdot V_{in}$（CCM）；D 为占空比；二极管续流、电感储能、输出电容滤波。

## F.7 反相比例放大器

![反相放大](../assets/schematics/circuit-inverting.svg)

- **用途**：反相放大传感器信号，增益可控。
- **公式**：$G=-\dfrac{R_f}{R_1}$；同相端接地；需双电源。

## F.8 同相比例放大器

![同相放大](../assets/schematics/circuit-noninverting.svg)

- **用途**：高输入阻抗缓冲/放大，单电源友好。
- **公式**：$G=1+\dfrac{R_f}{R_1}$；电压跟随器 $R_f=0$。

## F.9 比较器迟滞（施密特）

![迟滞比较器](../assets/schematics/circuit-comparator-hyst.svg)

- **用途**：阈值检测时抗噪声，避免输出在阈值附近抖动。
- **要点**：输出经 Rf 正反馈回同相端，上/下门限不同；Rf 越大迟滞越宽。

## F.10 MOSFET 双向电平转换

![BSS138 电平转换](../assets/schematics/circuit-level-shifter.svg)

- **用途**：3.3V MCU 与 5V 传感器/I²C 双向通信。
- **要点**：两侧各上拉到各自 Vcc；BSS138 栅极接低压侧地；I²C 经典电路。

## F.11 按键去抖

![RC 按键去抖](../assets/schematics/circuit-debounce.svg)

- **用途**：滤除机械按键按下/松开时十几 ms 的抖动。
- **取值**：R=10k、C=100nF → $\tau=1$ ms；太大则按键响应变慢。

## F.12 H 桥电机驱动

![H 桥](../assets/schematics/circuit-hbridge.svg)

- **用途**：控制直流电机正反转 + PWM 调速。
- **要点**：Q1+Q4 导通正转，Q2+Q3 导通反转；**绝不能同侧直通（shoot-through）**。

## F.13 共射放大电路

![共射放大](../assets/schematics/circuit-common-emitter.svg)

- **用途**：单管小信号电压放大（反相）。
- **公式**：$A_v\approx -R_C/r_e'$（Re 旁路时）；Re 未旁路时 $A_v\approx -R_C/R_e$；Re 稳定工作点但降低增益。

## F.14 整流与电容滤波

![整流滤波（简化）](../assets/schematics/circuit-rectifier.svg)

- **用途**：交流变平滑直流。
- **要点**：桥式整流→馒头波→大电容滤波；电容越大纹波越小；注意电容耐压与极性。

## F.15 仪表放大器（三运放）

![三运放仪放](../assets/schematics/circuit-instrumentation.svg)

- **用途**：放大微小差分信号（电桥/生物电），高 CMRR。
- **公式**：增益 $G=1+2R/R_g$；Rg 越小增益越大；输入阻抗极高。

## F.16 晶振振荡电路

![MCU 晶振](../assets/schematics/circuit-crystal.svg)

- **用途**：为 MCU 提供稳定时钟。
- **取值**：8MHz 晶振配 2×22pF 负载电容（按晶振 CL 指定）；走线尽量短、包地。

---

> 以上为最常用的 16 个基础电路；更复杂的拓扑（有源滤波、D 类功放、隔离反激等）见正文对应章节。
