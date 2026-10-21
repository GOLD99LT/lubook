---
id: esd-protection
title: ESD 防护与接口保护 ESD Protection & Interface Protection
part: 7
chapter: 信号完整性与 EMC
order: 55
tags: [ESD, TVS, 静电, 接口保护, 钳位, IEC61000-4-2]
difficulty: 2
status: published
sources:
  - TI SLVA680A ESD Protection Layout Guide
  - IEC 61000-4-2 Electrostatic Discharge Test
  - onsemi AND8301-D
---

# ESD 防护与接口保护 ESD Protection

人手摸一下接口，可能带上 **±8 kV** 静电，在 ns 级瞬间放电。这个能量若直接进到 IC 的 CMOS 栅极，薄薄的栅氧瞬间击穿——板子当时可能还能工作，几天内慢慢失效。ESD（Electrostatic Discharge，静电放电）防护就是在接口处给这个 kV 能量一个就近的泄放通道。

## 1. 设计动机

::: motivation 为什么要专门防护
ESD 是 kV 级、ns 级的快脉冲。TVS 二极管即使只有 5 mm 的引线，那点寄生电感在 ns 边沿下就有几十伏压降——ESD 已经穿过、IC 已经受损，TVS 才刚反应。所以 ESD 防护**布局比选件还重要**：保护器件必须紧贴入口，让能量就近入地。
:::

## 2. 图示：TVS 紧贴连接器

![连接器入口处 TVS 就近把 ESD 泄放到地，被保护 IC 在下游远处](../assets/schematics/esd-protection.svg)

## 3. 机理与定量

ESD 等效：一个数百 pF 的电容在极短时间（~1 ns）通过小电阻放电，峰值电流可达数 10 A。IEC 61000-4-2 标准波形：

- **接触放电（Contact）**：±8 kV，直接接触金属注入，最严酷。
- **空气放电（Air）**：±15 kV，打火空气间隙。

TVS（Transient Voltage Suppressor）工作原理：正常电压下高阻不导通；一旦电压超过击穿电压，瞬间低阻导通，把钳位电压 $V_C$ 拉到 IC 耐压以下，能量泄放到地。

## 4. 设计准则（TI SLVA680A）

1. **TVS 紧贴连接器**：ESD 能量入口第一站。
2. **泄放回路面短**：TVS 地直接打过孔到完整地平面，不绕。
3. **被保护 IC 在 TVS 下游**：TVS 在连接器和 IC 之间。
4. **不留分支（stub）**：TVS 之后到 IC 的线不要分叉。
5. **TVS 电容别拖慢高速信号**：USB/以太网选低电容（<1 pF）TVS。

## 5. 完整设计示例

::: example USB 接口 ESD 保护
1. **需求**：USB 2.0 D+/D- 要过接触 ±8kV ESD。
2. **选件**：低电容 TVS 阵列（Cj<1pF，不拖慢 USB 眼图）。
3. **布局**：TVS 紧贴 USB 连接器，D+/D- 先过 TVS 再进 MCU。
4. **地**：TVS 地直接打过孔到 L2 GND，引线 <1mm。
5. **验证**：ESD 枪打连接器，设备不复位、不损坏。
:::

## 6. 检查与仿真

- **ESD 预测试**：用 ESD 模拟器打各接口，看是否复位。
- **布局审查**：确认 TVS 在连接器和 IC 之间、泄放路径短。
- **眼图**：高速口加 TVS 后眼图仍张开（确认电容没拖慢）。

## 扩展与变种电路

### 扩展1：TVS 钳位效果与选型

没保护 vs 有 TVS，电压波形天差地别。

![无 TVS 时 kV 尖峰直击 IC；有 TVS 钳位到 IC 耐压以内](../assets/schematics/esd-tvs-clamp.svg)

::: example 机理与定量
- **反向工作电压 $V_{RWM}$**：要 > 正常信号电压（如 5V 信号选 $V_{RWM}=5.5V$），否则正常导通。
- **钳位电压 $V_C$**：ESD 时 TVS 两端电压，必须 < 被保护 IC 耐压（如 IC 耐 15V，选 $V_C<12V$）。
- **结电容 $C_j$**：高速信号选低电容 TVS，否则信号边沿被拖慢。
- 功率 $P_{PP}$：按 ESD 脉冲能量选，通常几百 W（8/20µs 波形）。
:::

准则对比：

| 参数 | 选大 | 选小 |
|---|---|---|
| $V_{RWM}$ | 不影响信号 | 误动作 |
| $V_C$ | 保护不够 | — |
| $C_j$ | 拖慢高速 | 低速无所谓 |

::: pitfall 高速口用了高电容 TVS
- **现象**：加了 ESD 保护后 USB 枚举失败、眼图闭合。
- **原因**：TVS 结电容几十 pF，把高速信号边沿滤掉。
- **解决**：选低电容（<1pF）专用高速 TVS。
:::

### 扩展2：ESD 测试方法

IEC 61000-4-2 怎么打。

![ESD 模拟器对被测设备做空气放电/接触放电测试](../assets/schematics/esd-test.svg)

::: example 机理与定量
- **接触放电 ±8kV**：放电电极直接戳在金属上，最严酷、最常用。
- **空气放电 ±15kV**：电极靠近绝缘表面直到打火，模拟人手摸塑料外壳。
- 测试点：所有可被人接触到的金属部分、接口引脚、按键、缝隙。
- 判据：测试中及测试后设备不应损坏、不应复位死机（性能可暂时下降后自恢复）。
:::

准则对比：

| 放电方式 | 电压 | 严酷度 |
|---|---|---|
| 接触 | ±8kV | 高（直接注入） |
| 空气 | ±15kV | 中（打火间隙） |

::: pitfall 只测接口不测缝隙
- **现象**：认证时打按键缝隙 fail。
- **原因**：只测了接口，没测人手会摸的塑料缝隙。
- **解决**：按标准覆盖所有可接触点，内部地/屏蔽要连续。
:::

## 7. 常见坑与故障现象

::: pitfall 常见坑
- **TVS 放 IC 旁边而非连接器旁**：ESD 已经跑进板子才被钳位，引线电感让钳位失效。
- **泄放回路绕远**：TVS 地走半天才到平面，能量在板内产生压降。
- **高速口用高电容 TVS**：信号被拖慢。
- **不留 ESD 路径靠"碰运气"**：认证 fail 才补，代价大。
:::

## 8. 自测题

<details><summary>为什么 ESD 保护布局比选 TVS 型号还重要？</summary>

ESD 是 kV、ns 级快脉冲。TVS 引线即使几 mm，寄生电感在 ns 边沿下产生几十伏压降，ESD 已经穿过、IC 已受损，TVS 才反应。所以 TVS 必须紧贴连接器、泄放回路面最短。

</details>

<details><summary>选 TVS 时，V_RWM、V_C、结电容各要满足什么？</summary>

$V_{RWM}$ 要 > 正常信号电压（不误动作）；$V_C$（钳位电压）要 < 被保护 IC 耐压（真正保护）；结电容 $C_j$ 在高速口要小（不拖慢信号）。

</details>

<details><summary>接触放电和空气放电哪个更严酷？为什么？</summary>

**接触放电（±8kV）更严酷**：电极直接接触金属，能量直接注入板子，没有空气间隙衰减。空气放电（±15kV）虽电压高，但要打火击穿空气，实际注入能量不如接触放电直接。

</details>

## 9. 参考资料

- TI SLVA680A *ESD Protection Layout Guide*
- IEC 61000-4-2 Electrostatic Discharge Immunity Test
- onsemi AND8301-D EMC PCB Layout Guidelines
