---
id: kcl-kvl
title: 基尔霍夫定律 KCL / KVL Kirchhoff's Laws
part: 1
chapter: 直流电路基础
order: 20
tags: [KCL, KVL, 基尔霍夫, 节点电流, 回路电压]
difficulty: 1
status: published
sources:
  - Lessons In Electric Circuits (Kuphaldt)
  - Practical Electronics for Inventors (Scherz & Monk)
  - https://www.khanacademy.org/science/electrical-engineering
---

# 基尔霍夫定律 KCL / KVL Kirchhoff's Laws

分压分流是"一眼能看出串并联"的简单情况。但真实电路会有多个电源、桥形网络、互相套着的回路——这时欧姆定律单独使不动了，需要两条更根本的守恒定律：**基尔霍夫电流定律 KCL** 和 **基尔霍夫电压定律 KVL**。它们是所有电路分析的地基。

## 1. 设计动机

::: motivation 为什么需要这两条定律
一个电桥电路（四个电阻搭成菱形），你没法直接说出哪个串哪个并。但只要列出"节点上电流进出相等"和"绕一圈电压和为零"两组方程，任何复杂电阻网络都能解出来。万用表排查时，"这个节点进来多少电流、出去多少"也是 KCL 的直觉。
:::

## 2. 原理图

![三个电阻并联在电源上：上轨节点处电流 I总 分成 I₁/I₂/I₃（KCL）；沿任一回路电压升等于电压降（KVL）](../assets/schematics/kcl-kvl.svg)

## 3. 两条定律（只给结论）

**KCL（基尔霍夫电流定律，节点电流守恒）**：

$$\sum I_{in} = \sum I_{out} \qquad\Longleftrightarrow\qquad \sum I = 0$$

含义：**流入任一节点的电流之和 = 流出该节点的电流之和**。电荷不会在节点凭空产生或消失——就像几条水管汇到一个三通，进多少水就出多少水。

**KVL（基尔霍夫电压定律，回路电压守恒）**：

$$\sum V_{rise} = \sum V_{drop} \qquad\Longleftrightarrow\qquad \sum V = 0 \text{（绕任一闭合回路一圈）}$$

含义：**沿任意闭合回路走一圈，所有电压升之和 = 所有电压降之和**。就像爬山：上爬多高、下降多低，回到原地时高度变化为零。

::: analogy 三通水管与环山公路
- KCL = 水管三通：进来几股水流，出去几股水流，总量守恒，不可能凭空多出来。
- KVL = 绕山一圈：你从起点出发，上坡累计多少米、下坡累计多少米，回到起点时净高度变化为 0。
:::

## 4. 怎么用（工程师的两步走）

1. **标方向**：先任意假定每条支路电流方向（猜反了没关系，最后算出负值就是方向反了）。
2. **列方程**：对每个独立节点列 KCL，对每个独立回路列 KVL，联立求解。

::: advanced 进阶：方程个数与独立性
n 个节点的电路，独立 KCL 方程只有 n−1 个（选一个节点做参考地）；b 条支路、n 个节点时，独立 KVL 方程数 = b−(n−1)。这正是下一章"节点法/网孔法"系统化的依据——本质就是选最少的独立未知量，列最少的方程。
:::

## 5. 带数字的算例

::: example 三个并联电阻的电流分配
1. **电路**：电源 Vs=12V 并联 R₁=12Ω、R₂=6Ω、R₃=4Ω（见上图）。
2. **各支路电流**：$I_1=12/12=1$ A，$I_2=12/6=2$ A，$I_3=12/4=3$ A。
3. **用 KCL 验算总电流**：$I_{\text{总}}=I_1+I_2+I_3=1+2+3=$ **6 A**。
4. **用 KVL 验算**：取"电源→R₁→回电源"这个回路，电压升 12V（电源），电压降 $I_1 R_1=12$ V，$12-12=0$，闭合。换 R₂、R₃ 回路同样成立。
:::

::: example 单回路两电阻分压
电源 9V 串 R₁=2kΩ、R₂=1kΩ。回路电流 $I=9/(2k+1k)=3$ mA。KVL：电源升 9V，R₁ 降 $3mA\times2k=6V$，R₂ 降 $3mA\times1k=3V$，$6+3=9$ V，正好等于电源——这就是分压公式的底层来历。
:::

## 6. 常见坑

::: pitfall 常见坑
- **电流方向随便假定后，算出负值不知道意味着什么**：现象——列方程解出某支路电流是 −0.5A。原因——一开始方向假设反了。解决——负值只表示真实方向与你画的箭头相反，大小仍正确，按实际方向修正即可，不必推翻重算。
- **把节点当成"会储存电荷"**：现象——以为节点上电流可以"积压"。原因——理想导线节点不储存电荷，进多少必须出多少。解决——牢记 KCL 是瞬时守恒，节点只是个交汇点。
- **KVL 绕回路时漏算一个元件或重复算**：现象——列出来的方程加起来对不上电源电压。原因——绕圈时走线路径不闭合或把并联支路算重了。解决——用笔尖沿着一条具体的闭合路径走一圈，逐个元件记录升降，别跳步。
:::

## 7. 自测题

<details><summary>某节点有三条支路：流入 2A、流入 3A，第三条支路电流是多少？方向呢？</summary>

KCL：流入 = 流出。总流入 $2+3=5$ A，所以第三条支路必须**流出 5 A**。若第三条支路上你之前标的是"流入"，那它的真实值就是 −5A。
</details>

<details><summary>一个回路里：电源升 5V，一个电阻降 3V，另一个元件压降是多少？</summary>

KVL：$5 - 3 - V_2 = 0 \Rightarrow V_2=$ **2V**。绕一圈电压代数和必须为零。
</details>

<details><summary>KCL 和 KVL 是近似吗？在多高频电路里还成立吗？</summary>

集总参数电路（尺寸远小于信号波长）下严格成立，是电荷守恒与能量守恒的结果。当频率极高、元件尺寸可与波长相比（GHz 以上），要考虑分布参数，电流在导线上不再处处相等——但那是射频领域，普通数字/模拟电路放心用。
</details>

## 8. 参考资料

- [Lessons In Electric Circuits — Chapter 6: Divider Circuits & Kirchhoff's Laws](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- Practical Electronics for Inventors (Scherz & Monk) — Kirchhoff's Laws
- [Khan Academy — Kirchhoff's laws](https://www.khanacademy.org/science/electrical-engineering)
