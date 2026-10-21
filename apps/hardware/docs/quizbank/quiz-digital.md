---
id: quiz-digital
title: 数字电路测试题
part: 9
chapter: 硬件测试与面试题库
order: 20
tags: [题库, 自测, 数字电路]
difficulty: 2
status: published
sources:
  - Wakerly, Digital Design: Principles and Practices
  - Brown & Vranesic, Fundamentals of Digital Logic
  - Xilinx / Intel FPGA 设计文档与时序约束指南
---

# 数字电路测试题

本题库覆盖数制与补码、逻辑门/布尔代数/卡诺图、组合逻辑、触发器、寄存器与计数器、建立/保持时间与亚稳态、三态总线、逻辑电平标准、存储器、电平转换、FPGA/Verilog 入门、时钟与复位设计。题型分为「概念判断」「填空」「计算」「简答与情景」四组。

## 一、概念判断

<details><summary>判断：8 位有符号补码能表示的范围是 −128 ~ +127。</summary>

**正确。**n 位补码范围是 $-2^{n-1}\sim +(2^{n-1}-1)$。8 位即 $-128\sim +127$。多出来的负端（−128）对应补码 10000000。补码把减法化为加法，符号位参与运算。

</details>

<details><summary>判断：组合逻辑电路的输出只取决于当前输入，与历史输入无关；时序逻辑则与历史有关。</summary>

**正确。**组合逻辑（Combinational）无记忆，如加法器、译码器、MUX；时序逻辑（Sequential）含存储元件（触发器/寄存器），输出取决于当前输入与状态，如计数器、状态机。

</details>

<details><summary>判断：D 触发器在时钟上升沿把 D 端的值打入 Q；其余时间 Q 保持不变。</summary>

**正确。**D 触发器（Flip-Flop）是边沿触发，仅在时钟有效沿（上升沿/下降沿）采样 D 更新 Q，其他时刻保持。这是同步设计的基本单元。

</details>

<details><summary>判断：建立时间 $t_{su}$ 是指时钟沿到来之后数据必须保持稳定的时间；保持时间 $t_h$ 是时钟沿之前数据必须稳定的时间。</summary>

**错误，二者说反了。**建立时间（Setup Time）$t_{su}$：时钟有效沿**之前**数据必须稳定的最小时间；保持时间（Hold Time）$t_h$：时钟有效沿**之后**数据必须继续稳定的最小时间。不满足会进入亚稳态。

</details>

<details><summary>判断：亚稳态（Metastability）发生时，触发器输出会长时间停在逻辑 0 与 1 之间的不确定电平，可能最终随机落到某一电平。</summary>

**正确。**当数据在建立/保持窗口内变化，触发器进入亚稳态，输出在中间电平振荡、收敛时间不可预测。跨时钟域（CDC）必须用同步器（两级触发器）、FIFO 等降低失效概率 MTBF。

</details>

<details><summary>判断：三态门（Tri-state）输出有三种状态：0、1、高阻；多个三态输出可并接在同一总线上，但同一时刻只能有一个被使能。</summary>

**正确。**三态门第三态是高阻（Hi-Z），相当于断开。总线共享靠分时使能，若两个同时使能会发生 0 与 1 短路，产生大电流甚至损坏器件。

</details>

<details><summary>判断：3.3V 的 CMOS 输出可以直接驱动 5V 的 CMOS 输入。</summary>

**需谨慎，一般不能直接用。**5V CMOS 输入高电平门限 $V_{IH}\approx 3.5\text{V}$，3.3V 高电平（约 3.3V）可能低于门限，被判不定。需看器件 $V_{IH}$ 规格：若 5V 器件是 5V tolerant 输入且 $V_{IH}$ 较低（如 LSTTL $V_{IH}=2\text{V}$）可工作；否则需电平转换（Level Shifter）。

</details>

<details><summary>判断：同步设计中，所有触发器共用同一时钟、同一复位，是避免亚稳态与时序混乱的首选做法。</summary>

**正确。**同步设计（Synchronous Design）用全局时钟树驱动所有寄存器，组合逻辑延迟可预测。异步信号进芯片必须先同步。跨多时钟域必须做 CDC 处理。

</details>

## 二、填空

<details><summary>n 位二进制计数器最大计数状态数为 ____，模 2 计数器在时钟 $f$ 下最高输出频率为 ____。</summary>

状态数 $2^n$。模 2 分频：第 n 级输出频率为 $f/2^n$（最低位 $f/2$）。如 8 位计数器最高位频率为 $f/256$。

</details>

<details><summary>ROM/RAM/SRAM/DRAM/Flash/EEPROM 中，掉电数据保留的是 ____；需刷新（Refresh）的是 ____；按字节改写的是 ____。</summary>

掉电保留：ROM、Flash、EEPROM（非易失）。需刷新：DRAM（电容漏电）。按字节改写：EEPROM；Flash 按扇区擦写。SRAM 快但易失、不需刷新。

</details>

<details><summary>格雷码（Gray Code）相邻两码只差 ____ 位，适合 ____，避免组合逻辑冒险产生的尖峰。</summary>

只差一位。适合旋转编码器/计数器的状态编码，避免二进制跳变时多位同时翻转产生的毛刺（glitch）。

</details>

<details><summary>Verilog 中 `always @(posedge clk)` 块描述 ____ 逻辑；`assign` 连续赋值描述 ____ 逻辑。</summary>

`always @(posedge clk)` 描述时序（寄存器）逻辑；`assign` 描述组合逻辑。时序块内用非阻塞赋值 `<=`，组合块内用阻塞赋值 `=`。

</details>

<details><summary>复位分 ____ 复位与 ____ 复位；推荐同步复位以 ____。</summary>

异步复位（立即生效）与同步复位（时钟沿生效）。推荐同步复位（配合时钟）以避免复位信号在亚稳态时撤销导致的不定态；异步复位需同步释放。

</details>

## 三、计算

<details><summary>把十进制 −13 表示为 8 位补码。</summary>

+13 的 8 位原码：00001101。
取反：11110010；加 1：11110011。
故 −13 的 8 位补码为 **11110011**。
验证：符号位为 1 表示负数，其余位取反加 1 还原 $00001101=13$。

</details>

<details><summary>用卡诺图化简：$F=\sum m(0,1,2,3,4)$ 的 3 变量函数，写出最简与或式。</summary>

3 变量 ABC，最小项 0,1,2,3 对应 $A=0$ 的全部（即 $\bar A$）；再加上 $m_4$（100）。
$\bar A$ 覆盖 m0~m3；$m_4$（100）与 $m_0$（000）合并消去 A，得 $\bar B\bar C$。
故 $F=\bar A+\bar B\bar C$。
（卡诺图合并圈 2 的幂个相邻 1，圈越大项越少。）

</details>

<details><summary>某触发器数据路径延迟 $t_{co}=1\text{ns}$，组合逻辑延迟 $t_{logic}=8\text{ns}$，布线延迟 $2\text{ns}$，建立时间 $t_{su}=1\text{ns}$。求最高时钟频率。</summary>

周期约束：$T\ge t_{co}+t_{logic}+t_{route}+t_{su}=1+8+2+1=12\text{ns}$。
最高频率 $f_{max}=1/T=1/12\text{ns}\approx 83.3\text{MHz}$。
保持时间若为 0.5ns，则要求数据到达下一级时间 ≥ 保持，即 $t_{co}+t_{logic}+t_{route}\ge t_h$，本题 $11\text{ns}\gg 0.5\text{ns}$，保持满足。

</details>

<details><summary>4 位二进制计数器，输入时钟 1MHz。输出 $Q_0$、$Q_2$、$Q_3$ 的频率各是多少？</summary>

每级二分频：$Q_0=f/2=500\text{kHz}$；$Q_2=f/2^3=125\text{kHz}$；$Q_3=f/2^4=62.5\text{kHz}$。
（$Q_0$ 是第 1 级，$Q_n$ 对应 $f/2^{n+1}$：$Q_0\to /2$，$Q_2\to /8$，$Q_3\to /16$。）

</details>

<details><summary>16 位地址总线能寻址多少字节存储器？某 SRAM 芯片容量 32K×8 位，地址线几根？数据线几根？</summary>

16 位地址：$2^{16}=64\text{K}$ 地址单元，每单元 1 字节即 64KB。
32K×8：$32\text{K}=2^{15}$，地址线 15 根；数据线 8 根。

</details>

## 四、简答与情景

<details><summary>情景：一个异步按键信号直接接到某时钟域的 D 触发器输入，产品偶发死机。最可能的原因？如何修复？</summary>

异步按键（机械抖动 + 异步到达）违反建立/保持时间，触发亚稳态，使采样值随机传播到后续逻辑，导致状态机跑飞。
修复：(1) 按键经 RC 滤波消抖；(2) 用两级同步器（同步链）把异步信号同步到目标时钟域；(3) 关键控制信号加寄存器备份/状态机安全恢复。

</details>

<details><summary>简答：为什么 FPGA 设计推荐同步设计、避免组合环路与锁存器？</summary>

同步设计时序收敛可预测、易静态时序分析（STA）；组合环路（combinational loop）产生振荡、无法综合；组合逻辑中 `if`/`case` 分支不全时工具会推出隐含锁存器（latch），引入毛刺与时序问题。应让所有分支都赋值，或用 `default`，使综合出纯组合或纯寄存器。

</details>

<details><summary>情景：3.3V MCU 的 UART TX 要接 5V 串口设备，直接连接出现乱码。原因？解决方案？</summary>

电平不匹配：MCU 3.3V 高电平可能被 5V 器件判为不定；若 5V 设备 TX 输出 5V 到 MCU 引脚还可能过压损坏。
方案：(1) 用双向电平转换芯片（如 TXB010x）；(2) 用三极管/MOSFET 搭电平转换；(3) 若 MCU 引脚 5V tolerant 且 $V_{IH}$ 低，可共地直连但仍需确认规格；RX 方向务必防过压。

</details>

<details><summary>简答：什么是门控时钟（Gated Clock）？它省电但有什么风险？</summary>

门控时钟用使能信号控制时钟是否到达某模块，无操作时停止时钟省电。风险：组合逻辑生成的门控时钟会产生毛刺、偏移（skew），破坏时序。应使用集成时钟门控单元（ICG）或寄存器同步使能，避免直接用与门产生时钟。

</details>
