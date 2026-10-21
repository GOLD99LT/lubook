---
id: supply-rails
title: 供电轨、输出摆幅与 Rail-to-Rail Supply Rails & Output Swing
part: 3
chapter: 运放基础
order: 60
tags: [运放, 供电轨, 输出摆幅, 轨到轨, Headroom]
difficulty: 2
status: published
sources:
  - MT-035 Op Amp Inputs, Outputs, Single-Supply & Rail-to-Rail Issues (ADI Mini Tutorial)
  - https://www.analog.com/en/technical-articles.html
  - Op Amps for Everyone (TI, SLOD006B)
---

# 供电轨、输出摆幅与 Rail-to-Rail

## 1. 定义与物理来源

理想运放被画成一个三角形，旁边从不画电源脚——但真实运放必须接正电源 **+Vs** 和负电源 **−Vs**（单电源时 −Vs 接地）。输出电压不可能凭空高于 +Vs，也不可能低于 −Vs，它被"夹"在两条供电轨之间。

- **输出摆幅（Output Swing）**：运放线性工作时，输出能达到的电压范围。
- **头room（Headroom，裕量）**：输出离最近一条供电轨还差多少伏。普通运放输出离轨还有 1~2V 就推不动了；**轨到轨输出（Rail-to-Rail Output, RRO）** 运放的输出可以逼近到离轨几毫伏。
- **输入共模范围（Input Common-Mode Range, Vcm）**：两个输入端允许同时处于的电压范围，详见 [共模范围、CMRR 与 PSRR](cmrr-psrr.md)。

为什么普通运放输出到不了轨？输出级通常是一对推挽三极管（NMOS/PMOS 或 NPN/PNP），要让它们导通，栅极/基极必须比输出再高出/低出一个驱动电压。当输出想逼近正电源时，上管的驱动电压不够了，输出就停在 +Vs 以下约 1~2V 的位置。

![输出摆幅被供电轨限制，中间蓝色区是线性放大可用区](../assets/schematics/supply-rails.svg)

## 2. 典型数量级

以常见 ±15V 双电源和 5V 单电源为例：

| 运放类型 | 输出到 +Vs | 输出到 −Vs | 输入共模范围 | 典型型号举例 |
|---|---|---|---|---|
| 传统双极型（普通） | −1.5V | +1.5V | 不到负轨，正方向留 2V | μA741、LM358（部分） |
| CMOS 轨到轨输出 RRO | −10 mV | +10 mV | 可到一轨，通常不到另一轨 | OPA340、MCP6001 |
| 轨到轨输入+输出（RRIO） | −10 mV | +10 mV | 两轨之间都可以 | OPA333、MCP6V01 |

注意：**"Rail-to-Rail" 要分清是输入还是输出**。只说 RRO 表示输出能摆到轨，输入可能仍有共模限制；RRIO 才是输入输出都能到轨。

## 3. 在电路中的后果与测量

最常见的后果是 **削波（Clipping）**：信号摆幅超出线性区后，输出顶部/底部被"削平"，波形变成方波，同时产生大量谐波失真。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["理想正弦输出", "实际输出（接近轨被削波）"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 56, "right": 24, "top": 26, "bottom": 58},
  "xAxis": {"type": "category", "name": "角度", "data": [0,30,60,90,120,150,180,210,240,270,300,330,360], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "电压 V", "min": -6, "max": 6, "interval": 2, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "理想正弦输出", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [0,3,5.2,6,5.2,3,0,-3,-5.2,-6,-5.2,-3,0]},
    {"name": "实际输出（接近轨被削波）", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#b5642e"},
     "data": [0,3,4.5,4.5,4.5,3,0,-3,-4.5,-4.5,-4.5,-3,0]}
  ]
}
```

测量方法：给电路加直流输入，慢慢把输出推到正、负两个方向，用万用表/示波器读输出刚要开始非线性（THD 明显上升）时的电压，与供电轨相减即得 Headroom。数据手册里通常用"输出电压摆幅 vs 负载电流"曲线给出。

## 4. 计算示例

::: example 5V 单电源下能放多大信号
1. **需求**：用 5V/0V 单电源运放放大交流信号，希望不失真。
2. **查手册**：普通 LM358 在 5V 供电、10kΩ 负载下，输出高电平 VOH 约 3.4V，输出低电平 VOL 约 0.02V。
3. **线性区**：约 0.02V ~ 3.4V，可用峰峰值只有约 3.4V。
4. **算最大不失真幅度**：若把静态输出偏置在中点 ≈1.7V，则正、负各只能摆约 1.7V，**正弦波峰值约 1.6V（峰峰值 3.2V）**。
5. **换 RRO**：若改用 MCP6001（RRO），输出可到 4.95V~0.05V，中点偏置后峰值可达约 2.4V，摆幅几乎翻倍。
:::

::: advanced 进阶：为什么单电源交流信号要加偏置
单电源运放输出不能为负。放大交流信号时，要先用电阻分压把输出静态点偏置到 Vcc/2（如 2.5V），信号叠加在这个直流上摆动，再用电容隔直耦合到下一级。否则负半周被削到 0V。这部分详见 [单电源电路与电平偏置搬移](../opamp/single-supply-biasing.md)（后续章节）。
:::

## 扩展与变种电路

### 扩展1：电荷泵产生负电源 Charge-Pump Negative Supply

单正电源（如 +5V）供电时，用开关电容把正轨"翻转"出一路负电源，让只能双电源工作的运放电路也能输出负电压。

![电荷泵：CLK 驱动飞跨电容 Cfly，经两只二极管整流得到 −Vout](../assets/schematics/supply-rails-chargepump-neg.svg)

::: example 工作原理与静态分析
- 两相开关：φ1 期间 Cfly 并联在 +Vs 与地之间充电，稳态充到约 $V_s$；φ2 期间 Cfly 被翻转串入输出回路，与 Cout 串联叠加，理想下 $V_{out}\approx -V_s$。
- 带载时受两只二极管正向压降与开关电阻影响，实际约 $V_{out}\approx -(V_s-2V_D)$（二极管整流型）。
- 关键元件：飞跨电容 Cfly（1µF 量级）、输出储能电容 Cout（10µF 量级）、两只整流二极管（或芯片内同步整流 MOS）。
- 输出电流 mA 量级，纹波为开关频率的充电尖峰。
:::

取值数量级：Cfly=1µF、Cout=10µF；与主电路（线性双电源/电感反相）对比：无电感、体积小，但纹波大（几十~几百 mV）、带载能力弱。适用：小信号双极性调理、给运放补一路负轨；不适用：负载大于几十 mA 或要求低纹波的精密基准。

::: pitfall 输出带载后 −Vs 被"拉正"
- **现象**：空载测得 −5V，一接电路就变成 −3V 甚至更接近 0V。
- **原因**：Cfly/Cout 容量不足或二极管压降大，等效输出电阻随负载电流上升。
- **解决**：加大飞跨与输出电容，改选集成电荷泵芯片，后级再加 LDO 或 RC 滤波压低开关纹波。
:::

## 5. 常见坑

::: pitfall 常见坑
- **拿普通运放当 RRO 用**：手册只写"轨到轨"却没说是输入还是输出；单电源 5V 下想输出 4.9V 却只得到 3.4V，信号顶部被削。选器件时同时核对输入共模范围和输出摆幅两张表。
- **负载电流拉低摆幅**：输出摆幅是带负载条件下测的。接 1kΩ 重负载时，CMOS RRO 的输出可能从 10mV 裕量恶化到几百 mV。重负载要查"Output Swing vs Load Current"曲线。
- **误以为供电越高越好**：提高供电电压确实能扩大输出范围，但功耗、发热、压摆率带宽约束、以及后级 ADC 的耐压都要一起考虑。
:::

## 6. 自测题

<details><summary>某 RRO 运放在 5V 单电源下输出可摆到 4.96V ~ 0.04V，把静态点设在 2.5V，最大不失真正弦波峰值约多少？</summary>

正方向余量 4.96−2.5 = 2.46V，负方向 2.5−0.04 = 2.46V，所以**峰值约 2.45V（峰峰值约 4.9V）**。RRO 的优势在低电压供电下最明显。

</details>

<details><summary>示波器看到输出正弦波顶部被削平成一条直线，而供电正常，最可能是什么原因？</summary>

输出**撞到了供电轨（Headroom 用尽）**。要么信号太大，要么供电电压太低，要么运放不是 RRO、输出本来就离轨 1~2V。减小输入幅度或换 RRO/提高供电即可判断。

</details>

## 7. 参考资料

- MT-035 Op Amp Inputs, Outputs, Single-Supply & Rail-to-Rail Issues（ADI Mini Tutorial）
- Op Amps for Everyone（TI, SLOD006B），输出级与摆幅章节
