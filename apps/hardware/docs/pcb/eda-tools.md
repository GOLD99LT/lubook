---
id: eda-tools
title: EDA 工具：KiCad / Altium 工作流 EDA Design Flow
part: 7
chapter: PCB 基础
order: 10
tags: [EDA, KiCad, Altium, 工作流, Gerber]
difficulty: 1
status: published
sources:
  - https://github.com/KiCad/kicad-source-mirror
  - https://github.com/kitspace/awesome-electronics
---

# EDA 工具：KiCad / Altium 工作流 EDA Design Flow

画 PCB 不靠手画，而靠 EDA（Electronic Design Automation，电子设计自动化）工具。这一章讲清楚一套板子从脑子里的想法，怎么一步步变成发给板厂的制造文件。

## 1. 设计动机

::: motivation 为什么需要标准工作流
没有工具，你得手工算每个元件位置、手工连几千根线、手工核对每个引脚有没有接错——这在现代板子上不可能完成。EDA 工具把"原理图逻辑"和"物理布线"绑定，改一处自动联动，还能自动查错（DRC）。工作流就是这套"先逻辑、后物理、再验证"的固定套路。
:::

## 2. 图示：EDA 工作流六步

![EDA 工作流：原理图→网表→布局→布线→DRC→输出制造文件，问题回溯回到原理图](../assets/schematics/eda-tools.svg)

## 3. 关键概念

- **原理图（Schematic）**：用符号表达"谁接谁"的逻辑连接，不关心物理位置。
- **网表（Netlist）**：从原理图导出的"元件清单 + 引脚连接关系"，是原理图与 PCB 之间的桥梁。现代工具（KiCad、Altium）实现原理图-PCB 双向同步，不再手工导出网表。
- **布局（Placement）**：把元件从网表里一个个搬到板子上、定方向。
- **布线（Routing）**：按电气规则把引脚用铜线连起来。
- **DRC（Design Rule Check，设计规则检查）**：自动查线间距、线宽、过孔、焊盘是否违反工艺规则。
- **制造输出（Manufacturing Output）**：导出 Gerber 等文件给板厂。

## 4. 常用工具对比

| 工具 | 性质 | 适用 |
|---|---|---|
| KiCad | 开源免费、跨平台 | 个人/小团队，功能已足够专业 |
| Altium Designer | 商业、Windows | 中大型企业，生态最全 |
| 立创 EDA | 在线/免费、国产 | 快速打样、对接嘉立创 |
| Allegro / Cadence | 商业、高端 | 高速/大规模板 |

## 5. 完整设计示例

::: example 用 KiCad 走一遍最小流程
1. **建工程**：新建 `.kicad_pro`，设好板子参数。
2. **画原理图**：放 MCU、晶振、电容，连线，分配位号（U1、C1…）。
3. **标注封装**：每个符号指定对应 PCB 封装（如 0805、QFP-48）。
4. **更新到 PCB**：原理图一键同步，元件以飞絮（ratsnest）形式出现在 PCB 画布。
5. **布局**：按功能模块摆放，MCU 居中、接口靠边。
6. **布线**：先电源线、后信号线，关键线手工控。
7. **跑 DRC**：0 errors 才算完。
8. **输出**：Gerber + 钻孔 + BOM + 坐标，打包发板厂。
:::

## 6. 检查与仿真

- **ERC（Electrical Rule Check）**：原理图阶段查未连接引脚、电源短路、重复位号。
- **DRC**：PCB 阶段查间距、线宽、过孔、丝印上焊盘。
- **网表一致性**：原理图改了没同步到 PCB，工具会报差异（netlist compare）。

## 扩展与变种电路

### 扩展：制造输出文件清单（Gerber / ODB++ / BOM）

画板的终点不是"线连完"，而是"板厂能照着做出来"。

![交付板厂的四类文件：Gerber、钻孔、BOM、贴片坐标](../assets/schematics/eda-tools-output.svg)

::: example 机理与定量
- **Gerber（RS-274X）**：铜箔（顶/底层）、阻焊、丝印每层一张图（均为 .gbr），板厂据此曝光制板；钻孔**不是** Gerber，而是独立的 Excellon 文件。
- **钻孔文件（Excellon）**：孔的位置与孔径，区分金属化孔 PTH 与非金属化 NPTH。
- **BOM**：物料清单，贴片厂据此备料。
- **坐标文件（Pick & Place）**：每个元件的 XY 位置与旋转角，贴片机据此摆件。
- 现代趋势：导出 **ODB++** 单一压缩包，把上述全部打包，比散件 Gerber 更少出错。
:::

准则对比：

| 输出 | 给谁 | 关键注意 |
|---|---|---|
| Gerber/ODB++ | 板厂 | 附叠层与表面处理要求 |
| 钻孔文件 | 板厂 | 孔壁金属化选项要写明 |
| BOM + 坐标 | 贴片厂 | 位号与封装必须一致 |

::: pitfall 把工程源文件当制造文件发给板厂
- **现象**：把 `.kicad_pro` 直接发过去，板厂没法用。
- **原因**：工程文件是给 EDA 软件读的，不是制造格式。
- **解决**：必须导出 Gerber/ODB++；工程文件自己留档做版本管理。
:::

## 7. 常见坑与故障现象

::: pitfall 常见坑
- **在 PCB 里直接改连接而不回原理图**：PCB 与原理图不一致，下次同步被覆盖，逻辑混乱。**改逻辑一定回原理图**。
- **忘了跑 DRC 就发板**：线间距不够导致板厂短路，板子回来连不上。DRC 必须 0 error。
- **封装没对应上**：原理图符号是 0805，PCB 封装画成 0603，焊盘对不上实物。
- **叠层说明漏给板厂**：自己设了四层，板厂按双层做出来。制造文件里必须附叠层。
:::

## 8. 自测题

<details><summary>原理图和 PCB 之间靠什么衔接？为什么现代工具不用手工导网表了？</summary>

靠**网表（Netlist）**——元件清单加引脚连接关系。KiCad/Altium 实现了原理图与 PCB 的**双向实时同步**，改任一边另一边自动更新，所以不用手工导出导入网表。

</details>

<details><summary>发给板厂的"制造文件"主要是哪几类？</summary>

Gerber（各层图形）、钻孔文件、BOM（物料）、贴片坐标。现代可打包成 ODB++。工程源文件（.kicad_pro 等）自己留档，不发给板厂。

</details>

## 9. 参考资料

- KiCad 官方文档与源码镜像：https://github.com/KiCad/kicad-source-mirror
- awesome-electronics（EDA 与制造资源入口）：https://github.com/kitspace/awesome-electronics
- 立创 EDA / Altium 官方文档
