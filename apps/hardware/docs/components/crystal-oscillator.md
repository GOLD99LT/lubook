---
id: crystal-oscillator
title: 晶振与谐振器 Crystal Oscillator
part: 2
chapter: 频率器件与互连保护
order: 60
tags: [晶振, 谐振器, 负载电容, Pierce振荡, 频率精度, ppm]
difficulty: 2
status: published
sources:
  - The Art of Electronics (Horowitz & Hill, 3rd ed.)
  - https://github.com/ajaymnk/open-electronics
  - https://www.ibiblio.org/kuphaldt/electricCircuits/
---

# 晶振与谐振器 Crystal Oscillator

晶振（Crystal）利用石英晶体的**压电效应**：机械振动会产生电信号，外加交变电压又激发机械振动。在某个极稳定的机械谐振频率上，它的品质因数 Q 极高，因此能给数字系统提供误差仅几个 ppm 的时钟。MCU、USB、以太网都离不开它。

## 1. 设计动机：为什么不用 RC 振荡器

::: motivation RC 振荡频率不够准
MCU 内部 RC 振荡器便宜，但频率随电压、温度漂移，误差可达 ±5%~10%。USB 通信要求时钟精度 ±0.25%，串口波特率也要稳定——RC 振荡根本撑不住。晶振的频率由石英晶体的物理尺寸决定，温度稳定性好、Q 值高，能提供 ppm 级精度的时钟。
:::

## 2. 电路符号与等效模型

晶体符号是一个矩形（代表石英片）两端引出。等效电路由一条**动态支路**（R-L-C 串联，代表机械谐振）与一个**并联静电容 C₀**组成：

![晶振电路符号与等效 RLC 模型](../assets/schematics/crystal-oscillator.svg)

::: analogy 直觉类比：晶振像"音叉"
敲一下音叉，它会以非常固定的频率振动很久（高 Q）。石英晶体就是电的"音叉"：给它一个电冲击，它就在固有频率上振荡，而且衰减很慢、频率极稳。RC 振荡器像"拨一下弹簧"，振动频率受阻尼、温度影响很大；晶振则是高品质音叉。
:::

## 3. 关键参数

| 参数 | 英文 | 含义 | 典型数量级 |
|---|---|---|---|
| 标称频率 | Fnom | 谐振频率 | 常见 8MHz、12MHz、16MHz、24MHz、25MHz、32.768kHz( RTC ) |
| 负载电容 | CL | 外部需配的等效电容 | 8pF、12pF、18pF、20pF（关键） |
| 等效串联电阻 | ESR / Rm | 动态支路电阻 | 几十~上百 Ω |
| 频率精度 | Tolerance | 25℃ 下频率偏差 | ±10ppm、±20ppm、±50ppm |
| 温度稳定度 | Stability | 全温区频率偏差 | ±20~±50ppm（普通）；TCXO 可达 ±0.5ppm |
| 静态电容 | C0 | 并联极间电容 | 数 pF |

## 4. 选型要点与工程权衡

- **按芯片要求选负载电容 CL**：这是晶振最容易踩的坑。MCU 数据手册规定了推荐 CL，外部两个电容 C1/C2 要据此计算。公式：$C1=C2=2\times(C_L-C_{stray})$，其中 $C_{stray}$ 约 3~5pF（PCB 杂散）。CL 配错，振荡频率会偏离标称值，USB/通信直接失败。
- **2pin 无源晶振 vs 4pin 有源振荡器**：无源晶振（XTAL）便宜、需 MCU 内部反相器+外部电容；有源模块（振荡器）自带电源，输出干净方波，占地大、贵，但起振可靠、不敏感。量产高可靠产品常用有源。
- **ESR 要够低**：ESR 太高会导致起振困难或不起振，按数据手册选低于 MCU 推荐最大值的型号。
- **精度匹配应用**：普通 MCU 用 ±20~50ppm 即可；RTC 用 32.768kHz（15 级分频正好 1Hz）；USB/以太网要求 ±25~50ppm；GPS/基站用 TCXO/OCXO。
- **32.768kHz 是 RTC 标准**：$2^{15}=32768$，15 次分频得到 1Hz 秒信号。

## 5. 典型应用电路：Pierce 振荡

下图是最常见的 Pierce 结构：晶振跨接在 MCU 的 OSCIN/OSCOUT 之间，两端各经一只负载电容接地：

![Pierce 晶振电路：OSCIN/OSCOUT 间接晶振，两端负载电容到地](../assets/schematics/crystal-oscillator-pierce.svg)

::: example 8MHz 晶振负载电容取值
1. **需求**：STM32 用 8MHz 晶振，数据手册指定 CL=18pF。
2. **算外部电容**：$C1=C2=2\times(18-C_{stray})$，取杂散 5pF，得 $2\times13=26pF$，取标准值 22pF~27pF。
3. **选 NPO/C0G 电容**：负载电容必须用 C0G/NP0（温度稳定、压电效应小），不要用 X7R——X7R 的容值随温度/偏置漂移直接改变频率。
4. **布局**：晶振紧贴 MCU，走线短、下方不走其他信号、包地，减少噪声与杂散电容。
:::

## 6. 失效模式与常见坑

::: pitfall 常见坑
- **负载电容配错致频率偏差/不起振**：现象——USB 枚举失败、串口波特率不对，或偶尔不起振。原因——外部电容与晶振 CL 不匹配。解决——按 $C1=C2=2(C_L-C_{stray})$ 计算，用 C0G 电容，核对数据手册。
- **振荡过驱导致晶振损坏**：现象——晶振用一段时间后停振。原因——反相器增益过大，晶振被过度激励，石英片疲劳甚至破裂。解决——在反馈回路串阻尼电阻限制驱动电平，按厂家推荐驱动级别设计。
- **PCB 布局引入噪声/杂散**：现象——时钟不稳、EMI 超标。原因——晶振走线太长、靠近高速信号或板边，拾取噪声、杂散电容改变 CL。解决——晶振紧贴芯片、走线短粗、包地、下方不走线。
- **误用 X7R 做负载电容**：现象——频率随温度漂移。原因——X7R 容值温飘大。解决——负载电容一律用 C0G/NP0。
:::

## 7. 自测题

<details><summary>为什么 RTC 晶振频率是 32.768kHz 而不是别的整数？</summary>

因为 $32768=2^{15}$，经过 15 次二分频后正好得到 1Hz 的秒信号。用二进制分频链实现起来最简单、最省电。
</details>

<details><summary>晶振 CL=18pF，杂散电容按 5pF 估，两只外部负载电容应取多大？</summary>

$C1=C2=2\times(C_L-C_{stray})=2\times(18-5)=26pF$，取标准值 22pF 或 27pF（C0G/NP0 材质）。
</details>

<details><summary>无源 2pin 晶振和有源 4pin 振荡器模块有什么区别？</summary>

无源晶振只是一个谐振元件，需要 MCU 内部反相器和外部负载电容才能起振，便宜但对布局/电容敏感；有源振荡器模块内部含振荡电路，接电源就直接输出方波时钟，起振可靠、不敏感，但更贵、占地大、耗电。
</details>

## 8. 参考资料

- The Art of Electronics (Horowitz & Hill, 3rd ed.) — 晶体振荡与 Pierce 电路
- open-electronics — 晶振与振荡电路资源
- Lessons In Electric Circuits (Kuphaldt) — 谐振与振荡基础
