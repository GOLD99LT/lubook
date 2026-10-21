---
id: ideal-opamp
title: 理想模型五假设与虚短、虚断 Ideal Op-Amp Model
part: 3
chapter: 运放基础
order: 40
tags: [理想运放, 虚短, 虚断, 无限增益, 输入阻抗]
difficulty: 2
status: published
sources:
  - Op Amps for Everyone (TI SLOD006B), Ideal Op-Amp 章
  - Sergio Franco, Design with Operational Amplifiers 4e
  - MIT Roberge, Operational Amplifiers: Theory and Practice
---

# 理想模型五假设与虚短、虚断 Ideal Op-Amp Model

真实运放参数复杂，但工程上绝大多数时候先用**理想运放模型**算个八九不离十，再回头看哪些假设需要修正。本章讲透理想模型的五条假设，以及由此推出的两大法宝：**虚短**与**虚断**。

## 1. 设计动机

::: motivation 为什么先学理想模型
运放开环增益几十万倍、输入阻抗几百 MΩ、输出阻抗几十欧……直接拿真实参数算，方程又长又难。但只要接成负反馈，理想模型算出来的结果和真实结果几乎一样——因为负反馈把这些参数的影响"抹"掉了。先会用理想模型搭电路，是最高效的路径。
:::

## 2. 原理图

![理想运放：±输入、输出、电源脚，两大金律标在输入上](../assets/schematics/ideal-opamp.svg)

## 3. 五条理想假设

1. **开环增益 $A_{OL}=\infty$**：输入差为 0，输出也能是任意有限值。
2. **输入阻抗 $R_{in}=\infty$**：两个输入端都不取电流。
3. **输出阻抗 $R_{out}=0$**：输出能驱动任意负载，电压不塌。
4. **带宽无限**：从直流到无穷远增益不变。
5. **零噪声、零失调、零温漂**。

## 4. 两大金律（接成负反馈时）

::: analogy 虚短虚断像"被按住的弹簧"
负反馈像一只无形的手，强行把两个输入端的电位"按"到相等（虚短），而且这两个点既不灌电流也不抽电流（虚断）。你分析任何运放电路，都先在脑子里把这两条用上。
:::

- **虚短（Virtual Short）**：负反馈存在时，$V_+=V_-$。不是真的短路，而是被反馈"拉"到相等。
- **虚断（Virtual Open）**：$I_+=I_-=0$，输入端不取电流。

::: example 数值算例：反相放大器
同相端接地 $V_+=0$，由虚短 $V_-=0$（虚地）。由虚断，流过 R1 的电流全部流过 Rf：$I=V_{in}/R_1=-V_{out}/R_f$，得 $V_{out}=-(R_f/R_1)V_{in}$。全程没用到运放任何参数——增益只由两颗电阻决定。
:::

## 5. 什么时候假设会破

- **开环（没接反馈）**：虚短不成立，运放变比较器。
- **输出饱和（顶到电源轨）**：虚短失效，因为输出"够不着"了。
- **高频/大信号**：带宽、压摆率有限，理想模型要修正。

## 扩展与变种电路

### 扩展1：两种单位增益拓扑对比 Unity-Gain Topologies

**定位**：增益为 1 有两种接法——电压跟随器（同相）与反相−1（$R_f=R_1$），入阻与相位特性完全不同。

![两种单位增益拓扑](../assets/schematics/ideal-opamp-unity-topologies.svg)

::: example 工作原理 / 静态分析
- 电压跟随器：输出直接接反相端，$V_{out}=V_+$，输入阻抗极高、同相、不反相。
- 反相−1：$R_f=R_1$，$V_{out}=-(R_f/R_1)V_{in}=-V_{in}$，反相 180°、输入阻抗 $\approx R_1$。

$$G_{follower}=1\quad,\quad G_{inv}=-1$$
:::

设计要点：高阻信号源用跟随器；要反相或和其它信号求和用反相−1。

::: pitfall 单位增益专属坑
- **反相−1 输入阻抗被低估**：反相端虚地，输入阻抗只有 $R_1$（如 10kΩ），高内阻源会被分压。高阻源要用跟随器。
:::

## 6. 常见坑

::: pitfall 常见坑
- **虚短滥用在开环电路**：电压跟随器能 $V_{out}=V_+$ 是因为有反馈；开环比较器两个输入根本不等。
- **以为虚地真接地**：反相端≈0V 但不能真接地，否则输入信号被短路。
- **忽略输出摆幅**：理想模型输出可以无限大，实际到电源轨就停——大信号要按轨到轨能力验算。
:::

## 7. 自测题

<details><summary>理想运放同相端 2.5V，接成电压跟随器，输出多少？</summary>
由虚短 $V_-=V_+=2.5V$，跟随器输出直接等于反相端，$V_{out}=2.5V$。
</details>

<details><summary>"虚断"意味着输入端要提供多大电流？实际运放呢？</summary>
理想是 0。真实运放有输入偏置电流（双极输入 nA 级、JFET 输入 pA 级），高阻电路里它会在电阻上产生失调，需要用"平衡电阻"补偿。
</details>

## 8. 参考资料

- TI SLOD006B《Op Amps for Everyone》，Ideal Op-Amp 章
- Sergio Franco《Design with Operational Amplifiers》4e
- [MIT Roberge, Operational Amplifiers: Theory and Practice](https://web.mit.edu/klund/www/books/op2e.html)
