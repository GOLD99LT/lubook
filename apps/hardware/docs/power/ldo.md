---
id: ldo
title: LDO 原理、选型与功耗计算 Low-Dropout Regulator
part: 6
chapter: 线性电源
order: 15
tags: [LDO, 压差, PSRR, 静态电流, 散热, 线性稳压]
difficulty: 2
status: published
sources:
  - Analog Devices, Low-Dropout Linear Regulator (LDO) Application Tutorial — 压差、调整管结构、环路补偿、PSRR 与热设计 https://www.analog.com/en/resources/technical-articles/lowdropout-linear-regulator-ldo-application-tutorial.html
  - TI, LDO 产品与应用笔记索引 — 线性稳压器拓扑、输出电容稳定性与热设计资料入口 https://www.ti.com/product-category/power-management/linear-ldo-regulators/overview.html
  - Pressman, Billings, Morey, Switching Power Supply Design, 3rd ed.
  - Analog Devices, MT-043 Op Amp Power Supply Rejection Ratio (PSRR) and Supply Voltages — PSRR 的 dB 定义与频率特性 https://www.analog.com/media/en/training-seminars/tutorials/MT-043.pdf
  - TI, LM317 3-Terminal Adjustable Regulator datasheet — Line/Load Regulation、Dropout Voltage 与热设计参数 https://www.ti.com/lit/ds/symlink/lm317.pdf
  - TI, LP5907 250mA Low-Noise LDO datasheet — PSRR、Output Noise 与 Output Capacitor 曲线 https://www.ti.com/lit/ds/symlink/lp5907.pdf
  - Horowitz & Hill, The Art of Electronics, 3rd ed., Chapter 9 Voltage Regulation and Power Conversion — 线性稳压、基准、效率与热设计
---

# LDO 原理、选型与功耗计算 Low-Dropout Regulator

LDO（Low-Dropout Regulator，低压差线性稳压器）是板卡上最不起眼、又最容易翻车的器件之一。它把输入电压“削”到目标值，输出干净、没有开关噪声；代价是压差乘电流全部变成热。选型时只看“输出 1.8V、电流 500mA”远远不够：压差够不够、结温会不会超、输出电容会不会让环路振荡、100kHz 处 PSRR 还剩多少、静态电流会不会把电池耗光、能不能级联或并联，这些都要算。

本章讲 LDO 的**器件级选型与功耗**；调整管结构、环路极点、基准源的精度的完整推导，见[线性稳压与基准源](../opamp/linear-regulator-reference.md)，本章不重复推导，只把口径对齐，并把“3.3V→1.8V/500mA”这个典型场景算完整。线性电源的整流滤波链路见[线性电源：变压、整流、滤波](linear-supply.md)；开关电源的纹波来源见[开关电源原理与 Buck 降压](buck.md)。指标口径见[电源指标：纹波、效率、调整率与时序](power-specs.md)；电池设备的静态电流、待机与充电管理见[电池、充电管理与电量计](battery-charger.md)。

## 1. 设计动机

::: motivation 四个“参数都对、板子不对”的现场
**现场一：3.3V→1.8V/500mA 选了 SOT-23-5。** 功耗 $(3.3-1.8)\times0.5=0.75$ W，SOT-23-5 的结到环境热阻约 250°C/W（典型量级，以数据手册为准），温升 $0.75\times250=187.5^{\circ}\text{C}$，环境 25°C 时结温 212.5°C，远超 125°C。芯片会热关断，或者用寿命换“能用”。

**现场二：Buck 后级 LDO 只看 100Hz 的 PSRR。** 前级 Buck 在 100kHz 有 100mVpp 纹波，LDO 的 100Hz PSRR 是 75dB，看起来输出只有 18µV；实际 100kHz 处 PSRR 只有 30dB，输出是 $100/31.6=3.16$ mV，对 1.8V/12 位 ADC 的 0.44mV LSB 是 7.2 个 LSB。**PSRR 是频率的函数，必须按干扰频率查。**

**现场三：老式 PNP LDO 配 10µF 陶瓷电容。** 陶瓷电容 ESR 只有几毫欧，ESR 零点跑到几百 kHz 之外，环路在穿越频率处没有相位提升，输出出现 100~500kHz 的持续振荡。换“陶瓷稳定”的新一代 PMOS LDO 就好了；但如果是老器件，必须按手册的 ESR 窗口选钽/电解。

**现场四：电池待机三个月就没电。** LDO 的静态电流 1mA，3.7V 电池 2000mAh，理论待机 $2/0.001=2000$ 小时，约 83 天；换成 10µA 的 LDO，理论 22.8 年，实际受电池自放电限制。**$I_Q$ 是电池设备选 LDO 的第一指标，不是 PSRR。**
:::

| 你想确认 | 先查/先算 | 判据（工程经验值，具体以数据手册为准） |
|---|---|---|
| 会不会进 dropout | $V_{in,min}-V_{out}$ 与 $V_{DO}$ | 最坏工况留 0.3~0.5V |
| 会不会过热 | $P_d=(V_{in}-V_{out})I_{out}$ 与 $R_{\theta ja}$ | $T_j\le125^{\circ}\text{C}$（降额后） |
| 环路稳不稳 | $C_{out}$、ESR、$f_c$ | 老 PNP 按 ESR 窗口；新 PMOS 按手册最小 $C_{out}$ |
| 前级纹波剩多少 | 干扰频率处的 PSRR | 折算到输出 <1 LSB |
| 噪声够不够 | 10Hz~100kHz 的 µVrms | 小于 1/2 LSB |
| 电池能撑多久 | $I_Q$ 与关断电流 | 按待机电流算，不按额定电流 |
| 能不能级联 | 总压差、总 IQ、总 PSRR | 每级都留在 dropout 之上 |
| 能不能并联 | 输出电压容差与输出阻抗 | 直接并联会环流，需均流 |

**不算会摔在哪，四个带数字的代价：**

1. **只算压差不算热**：0.75W 在 SOT-23-5 上是 187.5°C 温升，不是“有点热”；换 DFN 带焊盘（约 60°C/W）后温升降到 45.2°C。
2. **用 100Hz PSRR 代替 100kHz**：100mVpp 纹波在 30dB 处剩 3.16mV，是 1.8V/12 位 LSB 的 7.2 倍。
3. **老 PNP 配陶瓷**：ESR 从 0.05Ω 降到 0.005Ω，ESR 零点从 31.8kHz 推到 318kHz，相位裕度从 57.5° 掉到 8.9°，振荡。
4. **忽略 $I_Q$**：1mA 静态电流让 2000mAh 电池的待机从 22.8 年（10µA）掉到 83 天，差 100 倍。

## 2. 定义与直观

### 2.1 一颗 LDO 由什么组成

![LDO = 串联在 Vin/Vout 间的调整管 + 误差放大器采样 FB 与基准比较，输出电容 Cout 稳定环路](../assets/schematics/ldo.svg)

LDO 是一个电压跟随负反馈：

- **调整管（Pass Element）**：串在输入与输出之间，像一个可变电阻；PMOS、PNP 或 NPN 达林顿都有人用。
- **误差放大器（Error Amplifier）**：把反馈电压 $V_{FB}$ 与内部基准 $V_{ref}$ 比较，驱动调整管。
- **反馈分压**：$V_{FB}=V_{out}R_2/(R_1+R_2)$，稳态时 $V_{FB}=V_{ref}$，所以

$$V_{out}=V_{ref}\left(1+\frac{R_1}{R_2}\right)$$

其中 $V_{ref}$ 是内部基准（V）；$R_1$、$R_2$ 是上、下分压电阻（$\Omega$）。固定输出版内部已配好分压，外部看不到。

- **输出电容 $C_{out}$**：既是负载瞬态的能量缓冲，也是环路补偿的一部分。老式 PNP LDO 靠它的 ESR 零点稳定；现代 PMOS LDO 内部补偿，反而要求低 ESR 陶瓷。

### 2.2 压差与调整管：三种结构的代价

**压差（Dropout Voltage，$V_{DO}$）**是维持稳压所需的最小输入输出压差。输入低于 $V_{out}+V_{DO}$ 后，调整管完全导通，输出跟着输入掉，PSRR 和调整率同时失效。

| 结构 | 典型压差 | 输出阻抗 | 环路特点 | 输出电容 | 典型场景 |
|---|---|---|---|---|---|
| NPN 串联（78xx） | 1.5~2.5V | 低（射极跟随） | 单管、易稳定 | 不挑 | 工频整流后级、便宜 |
| PNP LDO | 0.2~0.6V | 高（共射） | 两极点，需 ESR 零点 | 要求 ESR 窗口 | 5V→3.3V、老设计 |
| PMOS/CMOS LDO | 0.1~0.3V | 中（共源） | 片内补偿，可陶瓷稳定 | 低 ESR 陶瓷 | 便携、射频、ADC |

PMOS 的压差是导通电阻上的压降：

$$V_{DO}=I_{out}R_{DS(on)}$$

其中 $I_{out}$ 是负载电流（A）；$R_{DS(on)}$ 是调整管导通电阻（$\Omega$）。例如 $R_{DS(on)}=0.6\,\Omega$、$I_{out}=0.3$ A，$V_{DO}=0.18$ V。NPN 的压差还要叠 $V_{BE}$，达林顿再叠一个 $V_{BE}$，所以 78xx 的压差典型 1.5~2.5V（以数据手册为准）。

**低压制差不是免费的**：同样电流下 $R_{DS(on)}$ 越小，调整管面积越大，栅极电容越大，内部极点越低，补偿越难。低压差、低噪声、高 PSRR 三者往往不能同时最优。

### 2.3 静态电流与效率

**静态电流（Quiescent Current，$I_Q$）**是芯片自身消耗、不流向负载的电流。LDO 的效率：

$$\eta=\frac{V_{out}I_{out}}{V_{in}(I_{out}+I_Q)}$$

其中 $V_{in}$、$V_{out}$ 是输入、输出电压（V）；$I_{out}$ 是负载电流（A）；$I_Q$ 是静态电流（A）。

- 重载时 $I_Q\ll I_{out}$，$\eta\approx V_{out}/V_{in}$；
- 轻载时 $I_Q$ 不能忽略，$\eta$ 迅速下降；
- 空载时 $I_{out}=0$，效率没有定义，只剩 $V_{in}I_Q$ 的待机功耗。

**算一遍**：3.3V→1.8V/0.5A、$I_Q=1$ mA。

$$\eta=\frac{1.8\times0.5}{3.3\times(0.5+0.001)}=\frac{0.9}{1.6533}=54.4\%$$

负载降到 1mA：

$$\eta=\frac{1.8\times0.001}{3.3\times(0.001+0.001)}=\frac{0.0018}{0.0066}=27.3\%$$

**同一个 LDO，满载 54.4%、1mA 时 27.3%。** 电池设备要按实际负载曲线选，不能只看满载效率。

### 2.4 PSRR 的频率特性

**电源抑制比（Power Supply Rejection Ratio，PSRR）**是输入电压变化与输出变化之比，是电压比，所以用 dB：

$$PSRR=\frac{\Delta V_{in}}{\Delta V_{out}},\qquad PSRR(\text{dB})=20\lg\frac{\Delta V_{in}}{\Delta V_{out}}$$

纹波折算：

$$V_{out,ripple}=\frac{V_{in,ripple}}{10^{PSRR(\text{dB})/20}}$$

其中 $V_{in,ripple}$ 是输入纹波（V，峰峰值或有效值，口径要一致）；$V_{out,ripple}$ 是输出纹波（同口径）。

PSRR 随频率下降：低频时环路增益高，能把输入扰动压得很低；到环路增益降到 1 附近，PSRR 靠输出电容分压和片内前馈维持，继续下降。典型量级：

| 频率 | 通用 LDO 的 PSRR | 说明 |
|---|---|---|
| 100Hz | 70~80dB | 工频纹波，环路增益高 |
| 1kHz | 60~70dB | 开始滚降 |
| 10kHz | 45~55dB | 环路增益下降 |
| 100kHz | 30~40dB | 开关电源主频段，最需要看 |
| 1MHz | 15~25dB | 输出电容/前馈主导 |

**这些是典型量级，具体以数据手册曲线为准；不同型号在 100kHz 处能差 20dB。** 高性能低噪声 LDO 在 100kHz 可以做到 45~55dB，但价格、静态电流和输出电容要求也更高。

```echarts
{
  "animation": false,
  "tooltip": {"trigger": "axis"},
  "grid": {"left": 66, "right": 26, "top": 30, "bottom": 50},
  "xAxis": {"type": "log", "name": "频率 Hz", "nameLocation": "middle", "nameGap": 30, "min": 100, "max": 1000000, "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "PSRR dB", "nameLocation": "middle", "nameGap": 44, "min": 0, "max": 90, "interval": 15, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "PSRR（示例）", "type": "line", "showSymbol": true, "symbolSize": 5, "lineStyle": {"width": 2.6, "color": "#1a4f8b"}, "itemStyle": {"color": "#1a4f8b"},
     "data": [[100,75],[1000,65],[10000,45],[100000,30],[1000000,20]]}
  ]
}
```

**PSRR 的测试条件必须一起看**：$V_{in}-V_{out}$、$I_{out}$、$C_{out}$、温度、纹波幅度。手册首页的 75dB 通常是 $V_{in}=V_{out}+1$ V、$I_{out}=100$ mA、$C_{out}=1\,\mu$F 的典型值；实际板子上 $C_{out}$ 更大、压差更大，曲线会变。

### 2.5 输出噪声：LDO 自己产生的扰动

PSRR 描述“输入纹波漏过来多少”；**输出噪声（Output Noise）**描述“LDO 自己产生多少”。单位 µVrms，测试带宽常为 10Hz~100kHz。噪声来源：

- 内部基准的噪声；
- 误差放大器的输入噪声；
- 分压电阻的热噪声；
- 调整管的闪烁噪声。

**噪声与 PSRR 是两件事**：PSRR 再高，也不能消除内部噪声；噪声再低，也不能挡住输入纹波。低噪声 LDO 通常在基准和误差放大器上做文章，并引出 NR/SS 引脚外接电容。

![NR/SS 引脚经 Cn 到地，小电容滤基准噪声并决定上电斜率](../assets/schematics/ldo-nr-ss.svg)

NR/SS 电容的作用：

- **降噪**：对基准分压形成低通，把 µV 级基准噪声再压低；输出噪声可从约 30µVrms 降到约 10µVrms（典型量级，以数据手册为准）。
- **软启动**：上电时引脚电压缓慢爬升，$V_{out}$ 跟随斜升，限制涌入 $C_{out}$ 的浪涌电流 $I_{inrush}=C_{out}\,dV/dt$。
- **取值**：$C_n$ 典型 0.01~0.1µF；越大噪声越低、软启动越慢。太大会超过后级 POR 的等待窗口。

### 2.6 瞬态与输出电容

负载突变时，环路来不及响应，$C_{out}$ 先供电。跌落由两部分组成：

$$\Delta V_{under}\approx\Delta I\left(ESR+\frac{1}{2\pi f_cC_{out}}\right)$$

其中 $\Delta I$ 是负载阶跃（A）；$ESR$ 是输出电容等效串联电阻（$\Omega$）；$f_c$ 是环路穿越频率（Hz）；$C_{out}$ 是输出电容（F）。

- 第一项是 ESR 上的瞬时跳变，$\Delta I\times ESR$；
- 第二项是环路响应时间 $1/(2\pi f_c)$ 内电容放电造成的跌落；
- 环路越快（$f_c$ 越高）、电容越大，跌落越小；但 $f_c$ 太高会牺牲相位裕度。

**算一遍**：$\Delta I=0.5$ A、$ESR=0.05\,\Omega$、$C_{out}=100\,\mu$F、$f_c=50$ kHz。

$$\Delta V_{under}\approx0.5\times\left(0.05+\frac{1}{2\pi\times50\times10^3\times100\times10^{-6}}\right)$$

$$=0.5\times(0.05+0.0318)=0.5\times0.0818=40.9\ \text{mV}$$

### 2.7 ESR 稳定窗口的两代口径

这是 LDO 选型最容易套错经验的地方：

- **老式 PNP LDO**：输出在集电极，输出阻抗高，环路至少两个极点；必须靠 $C_{out}$ 的 ESR 零点在穿越频率附近补相位。ESR 太小（纯陶瓷），零点太高，补偿不足；ESR 太大，零点太低，增益被抬平，穿越频率被推高，第二极点又开始吃相位裕度，同时 ESR 上的纹波和瞬态跌落变大。**ESR 窗口是“相位”和“瞬态”两头夹出来的。**
- **现代 PMOS/CMOS LDO**：片内补偿，输出电容主要做瞬态储能；手册通常要求“低 ESR 陶瓷，$C_{out}$ 在某个最小值以上”，而不是 ESR 区间。给老 PNP 硬配陶瓷会振荡；给现代 PMOS 硬加 1Ω 电解，可能反而让瞬态变差。

**结论：先看器件世代，再看手册的“Output Capacitor”章节，不要套用上一颗器件的经验。**

### 2.8 级联与并联：能，但有条件

**级联（Cascading）**：两级 LDO 串联，例如 5V→3.3V→1.8V。可以，但要满足：

1. **每级都有足够压差**：第一级输出必须高于第二级 $V_{out}+V_{DO}$，包括纹波谷点和负载瞬态；
2. **总压差与总功耗相加**：5V→1.8V 直接一级的功耗是 $(5-1.8)I$，两级串联的总功耗近似相同（忽略 IQ），不会因为“分两段”而变省；
3. **总 PSRR 在 dB 上相加**（近似）：$PSRR_{total}\approx PSRR_1+PSSR_2$，但只在第二级的 PSRR 测试源阻抗与第一级输出阻抗接近时成立；中间电容和 PCB 阻抗可能在高频形成旁路；
4. **总 IQ 相加**，电池设备要算两遍；
5. **每级仍要各自稳定**：第一级的 $C_{out}$ 就是第二级的“输入电容”，要按两级手册分别核对。

**并联（Paralleling）**：两颗 LDO 直接并联，**通常不可以**。两颗器件的输出电压有容差，输出阻抗又低，微小的电压差会产生很大的环流：

$$I_c=\frac{V_1-V_2}{R_{o1}+R_{o2}}$$

其中 $V_1$、$V_2$ 是两颗 LDO 的实际输出电压（V）；$R_{o1}$、$R_{o2}$ 是它们的输出电阻（$\Omega$）；$I_c$ 是环流（A）。1.8V 输出、±1% 容差就是 18mV 偏差；每颗输出电阻 10mΩ，环流 $18\text{mV}/20\text{m\Omega}=0.9$ A，足以让其中一颗限流或过热。

要并联，只有三条路：

- 用**支持均流的 LDO**（带共享引脚或主从配置）；
- 每颗输出串**均流电阻**（ballast），但电阻上的压降会牺牲调整率与效率；
- 改用一颗更大电流的 LDO，或用多相 Buck。

## 3. 定量关系

### 3.1 功耗与结温

$$P_d=(V_{in}-V_{out})I_{out}+V_{in}I_Q$$

其中 $P_d$ 是耗散（W）；$V_{in}$、$V_{out}$ 是输入、输出电压（V）；$I_{out}$ 是负载电流（A）；$I_Q$ 是静态电流（A）。第一项是调整管上的压降乘电流，第二项是芯片自身供电。

$$T_j=T_a+P_dR_{\theta ja}$$

其中 $T_j$ 是结温（°C）；$T_a$ 是环境温度（°C）；$R_{\theta ja}$ 是结到环境热阻（°C/W）。带散热焊盘时，$R_{\theta ja}$ 由封装、铜箔面积、过孔数量决定，数据手册的测试板条件往往比实际板子好，要留 1.5~2 倍余量。

反解允许的最大热阻：

$$R_{\theta ja,max}=\frac{T_{j,max}-T_a}{P_d}$$

**算一遍**：3.3V→1.8V/0.5A、$I_Q=1$ mA。

$$P_d=(3.3-1.8)\times0.5+3.3\times0.001=0.75+0.0033=0.753\ \text{W}$$

SOT-23-5 的 $R_{\theta ja}=250^{\circ}\text{C/W}$：

$$T_j=25+0.753\times250=213.3^{\circ}\text{C}$$

远超 125°C。带裸露焊盘的 DFN，$R_{\theta ja}=60^{\circ}\text{C/W}$：

$$T_j=25+0.753\times60=70.2^{\circ}\text{C}$$

可用。**同一颗芯片、同一个电路，封装和铜箔决定它能不能活。**

### 3.2 效率

$$\eta=\frac{V_{out}I_{out}}{V_{in}(I_{out}+I_Q)}$$

轻载时 $I_Q$ 不能忽略。只有 $I_{out}\ll I_Q$ 时，才能把分母近似为 $I_Q$：

$$\eta\approx\frac{V_{out}I_{out}}{V_{in}I_Q}$$

**算一遍**：1.8V 输出、3.3V 输入、$I_Q=1$ mA。

- 负载 0.5A：$\eta=1.8\times0.5/[3.3\times(0.5+0.001)]=54.4\%$。
- 负载 1mA：$I_{out}$ 与 $I_Q$ 相等，必须用完整式：$\eta=1.8\times0.001/[3.3\times(0.001+0.001)]=27.3\%$。
- 负载 10µA：$\eta=1.8\times10^{-5}/[3.3\times(10^{-5}+10^{-3})]=0.54\%$；此时近似式给 $1.8\times10^{-5}/(3.3\times10^{-3})=0.545\%$，误差很小，因为 $I_{out}\ll I_Q$。

**近似式的条件是 $I_{out}\ll I_Q$，不是“轻载”两个字。** 电池待机时 LDO 的效率通常只有百分之几，这时看的不是效率，而是绝对待机电流。

### 3.3 PSRR 与纹波折算

$$PSRR(\text{dB})=20\lg\frac{\Delta V_{in}}{\Delta V_{out}}$$

$$V_{out,ripple}=\frac{V_{in,ripple}}{10^{PSRR/20}}$$

**算一遍**：输入 100mVpp、100kHz，PSRR 分别为 30dB、40dB、48dB。

$$30\text{dB}\Rightarrow V_{out}=\frac{100}{31.62}=3.16\ \text{mV}$$

$$40\text{dB}\Rightarrow V_{out}=\frac{100}{100}=1.00\ \text{mV}$$

$$48\text{dB}\Rightarrow V_{out}=\frac{100}{251.2}=0.398\ \text{mV}$$

对 1.8V/12 位 ADC，1 LSB $=1.8/4096=0.4395$ mV：

$$3.16/0.4395=7.19\ \text{LSB},\qquad 1.00/0.4395=2.28\ \text{LSB},\qquad 0.398/0.4395=0.91\ \text{LSB}$$

**要把 100kHz 纹波压到 1 LSB 以内，PSRR 至少要 $20\lg(100/0.4395)=47.1$ dB。** 30dB 的通用 LDO 不够，必须选高 PSRR 型号，或在 LDO 前加 LC/磁珠滤波。

### 3.4 输出噪声

噪声密度 $e_n(f)$ 的单位是 µV/√Hz 或 nV/√Hz。总有效值噪声是密度的积分：

$$V_{n,rms}=\sqrt{\int_{f_1}^{f_2}e_n^2(f)\,df}$$

如果 $e_n$ 在带宽内近似白噪声：

$$V_{n,rms}=e_n\sqrt{f_2-f_1}$$

其中 $e_n$ 是噪声密度（V/√Hz）；$f_1$、$f_2$ 是积分下限、上限（Hz）。

**算一遍**：$e_n=20$ nV/√Hz，带宽 10Hz~100kHz。

$$V_{n,rms}=20\times10^{-9}\times\sqrt{10^5-10}=20\times10^{-9}\times316.2=6.32\ \mu\text{Vrms}$$

实际 LDO 的噪声在低频有 1/f 分量，积分值通常比白噪声估算高 1.5~3 倍；数据手册直接给的 10Hz~100kHz 的 µVrms 更可靠。对 1.8V/12 位 ADC，6.32µVrms 只有 $0.00632/0.4395=0.014$ LSB，可忽略；但对 16 位 ADC（1.8V 满量程，1 LSB $=1.8/65536=27.5\,\mu$V），30µVrms 约 $30/27.5=1.09$ LSB，开始进入预算。

### 3.5 瞬态的估算

$$\Delta V_{under}\approx\Delta I\left(ESR+\frac{1}{2\pi f_cC_{out}}\right)$$

符号与单位同 2.6。恢复时间的一阶估算：

$$t_s\approx\frac{4}{2\pi f_c}$$

**算一遍**：$\Delta I=0.5$ A、$ESR=0.05\,\Omega$、$C_{out}=100\,\mu$F、$f_c=50$ kHz。

$$\Delta V_{under}=0.5\times(0.05+0.0318)=40.9\ \text{mV}$$

$$t_s=\frac{4}{2\pi\times50\times10^3}=12.7\ \mu\text{s}$$

若目标跌落 ≤36mV（1.8V 的 ±2%），40.9mV 已经超标；加大 $C_{out}$ 到 220µF：

$$\Delta V_{under}=0.5\times\left(0.05+\frac{1}{2\pi\times50\times10^3\times220\times10^{-6}}\right)=0.5\times(0.05+0.0145)=32.3\ \text{mV}$$

满足 36mV。**电容从 100µF 加到 220µF，跌落从 40.9mV 降到 32.3mV，代价是体积和上电浪涌。**

### 3.6 ESR 窗口

ESR 零点：

$$f_z=\frac{1}{2\pi ESR\,C_{out}}$$

相位裕度的一阶估算：

$$PM\approx\arctan\frac{f_c}{f_z}$$

ESR 下限由 $PM\ge45^{\circ}$（即 $f_z\le f_c$）给出：

$$ESR\ge\frac{1}{2\pi f_cC_{out}}$$

ESR 上限由允许的负载阶跃跌落给出：

$$ESR\le\frac{\Delta V_{allowed}}{\Delta I}$$

**算一遍**：$C_{out}=100\,\mu$F、$f_c=50$ kHz、$\Delta I=0.5$ A、$\Delta V_{allowed}=100$ mV。

$$ESR_{min}=\frac{1}{2\pi\times50\times10^3\times100\times10^{-6}}=0.0318\ \Omega$$

$$ESR_{max}=\frac{0.1}{0.5}=0.2\ \Omega$$

窗口 0.0318~0.2Ω。取 0.05Ω：

$$f_z=\frac{1}{2\pi\times0.05\times100\times10^{-6}}=31.8\ \text{kHz}$$

$$PM\approx\arctan\frac{50}{31.8}=57.5^{\circ}$$

$$V_{ESR}=0.5\times0.05=25\ \text{mV}$$

若用 10µF 陶瓷（ESR 约 0.005Ω）：

$$ESR_{min}=\frac{1}{2\pi\times50\times10^3\times10\times10^{-6}}=0.318\ \Omega$$

而 $ESR_{max}=0.2\,\Omega$，**窗口为空**：这颗老 PNP LDO 在 10µF 下既不稳定，也不满足瞬态。要么把 $C_{out}$ 加到 100µF，要么换陶瓷稳定的 PMOS LDO。

### 3.7 级联的加法

两级串联，总压差、总功耗、总 IQ、总 PSRR：

$$V_{drop,total}=V_{drop1}+V_{drop2}$$

$$P_{d,total}\approx(V_{in1}-V_{out2})I_{out}+V_{in1}I_{Q1}+V_{in2}I_{Q2}$$

$$PSRR_{total}(\text{dB})\approx PSRR_1(\text{dB})+PSRR_2(\text{dB})$$

**算一遍**：5V→3.3V（PSRR 40dB @100kHz）→1.8V（PSRR 48dB @100kHz）。

$$PSRR_{total}\approx40+48=88\ \text{dB}$$

$$V_{out,ripple}=\frac{100\ \text{mV}}{10^{88/20}}=\frac{100}{25119}=3.98\ \mu\text{V}$$

总效率（忽略 IQ）：

$$\eta\approx\frac{1.8}{5}=36.0\%$$

总压差：

$$V_{drop,total}=(5-3.3)+(3.3-1.8)=1.7+1.5=3.2\ \text{V}$$

**级联能把 PSRR 叠到 88dB，但效率只有 36%，而且两级都要散热。** 只有在“前级纹波极大、后级要求极干净”时才值得。

### 3.8 并联的环流

$$I_c=\frac{V_1-V_2}{R_{o1}+R_{o2}}$$

**算一遍**：两颗 1.8V LDO，±1% 容差，最坏偏差 18mV；每颗输出电阻 10mΩ。

$$I_c=\frac{18\ \text{mV}}{20\ \text{m\Omega}}=0.9\ \text{A}$$

如果每颗额定 1A，环流已经吃掉 90% 的余量；如果额定 0.5A，直接过流。加 0.1Ω 均流电阻：

$$I_c=\frac{18\ \text{mV}}{2\times0.1+0.02}=\frac{18}{220}=81.8\ \text{mA}$$

环流降到 82mA，但 0.5A 负载时每颗电阻压降 $0.5\times0.1=50$ mV，输出调整率变差。加 0.5Ω：

$$I_c=\frac{18}{1.02}=17.6\ \text{mA}$$

环流可接受，但 1A 时压降 0.5V，LDO 的压差余量被吃掉。**并联不是“加颗电阻”就能解决，优先选支持均流的器件或单颗大电流 LDO。**

### 3.9 适用条件与失效边界

- **压差**：$V_{in,min}$ 必须高于 $V_{out}+V_{DO}$，包括纹波谷点、负载瞬态、电池末端。
- **热**：$P_d$ 按最坏 $V_{in}$、最大 $I_{out}$、最高 $T_a$ 算；$R_{\theta ja}$ 按实际铜箔，不按手册测试板。
- **稳定性**：老 PNP 看 ESR 窗口；现代 PMOS 看最小/最大 $C_{out}$ 与 ESR 上限；不要跨世代套经验。
- **PSRR**：按干扰频率查，不按 100Hz 值；注意测试条件。
- **噪声**：按 10Hz~100kHz 的 µVrms 查，不按噪声密度峰值。
- **反向电流**：输入掉电比输出快时，输出电容会通过调整管/体二极管向输入倒灌；要选带反向保护或加肖特基。
- **输入瞬态**：热插拔、浪涌可能超过绝对最大值；加 TVS/限流。

## 4. 典型计算

### 4.1 3.3V→1.8V/500mA 完整设计

**需求与假设**：

| 项目 | 数值/假设 |
|---|---|
| 输入 | 3.3V ±5%（3.135~3.465V） |
| 输出 | 1.8V/0.5A |
| 环境 | 25°C，目标 $T_j\le125^{\circ}\text{C}$ |
| 前级纹波 | 100kHz 处 100mVpp |
| ADC | 12 位、1.8V，1 LSB=0.4395mV |
| 目标输出纹波 | <1 LSB（0.4395mV） |
| 瞬态目标 | 0.5A 阶跃，跌落 ≤36mV（1.8V 的 ±2%） |
| 封装候选 | SOT-23-5（250°C/W）、DFN 带焊盘（60°C/W） |
| LDO 静态电流 | 1mA（示例值） |
| 环路 | $f_c\approx50$ kHz（示例值） |

**第 1 步：压差。** 最低输入 3.135V，输出 1.8V，压差 1.335V。所选 PMOS LDO 在 0.5A 时 $V_{DO}\approx0.2$ V（示例值，以数据手册为准），余量 $1.335-0.2=1.135$ V，全程不会进 dropout。

**第 2 步：功耗。** 名义：

$$P_d=(3.3-1.8)\times0.5+3.3\times0.001=0.75+0.0033=0.753\ \text{W}$$

最坏输入 3.465V：

$$P_d=(3.465-1.8)\times0.5+3.465\times0.001=0.8325+0.0035=0.836\ \text{W}$$

**第 3 步：结温。** SOT-23-5：

$$T_j=25+0.753\times250=213.3^{\circ}\text{C}>125^{\circ}\text{C}$$

不可用。DFN 带焊盘：

$$T_j=25+0.753\times60=70.2^{\circ}\text{C}$$

最坏输入：

$$T_j=25+0.836\times60=75.2^{\circ}\text{C}$$

环境升到 60°C 时：

$$T_j=60+0.836\times60=110.2^{\circ}\text{C}$$

留 14.8°C 余量。允许的最大热阻：

$$R_{\theta ja,max}=\frac{125-60}{0.836}=77.8^{\circ}\text{C/W}$$

选 60°C/W 的 DFN + 铺铜，满足。

**第 4 步：PSRR。** 目标输出纹波 <1 LSB = 0.4395mV，输入 100mVpp：

$$PSRR_{min}=20\lg\frac{100}{0.4395}=20\lg227.6=47.1\ \text{dB}$$

通用 LDO 在 100kHz 只有 30~40dB，不够；选 100kHz ≥48dB 的高 PSRR 型号：

$$V_{out,ripple}=\frac{100}{10^{48/20}}=\frac{100}{251.2}=0.398\ \text{mV}=0.91\ \text{LSB}$$

满足。若只能选 45dB 的器件：

$$V_{out,ripple}=\frac{100}{177.8}=0.562\ \text{mV}=1.28\ \text{LSB}$$

不满足，需要在 LDO 前加 LC/磁珠，或把 ADC 基准单独滤波。

**第 5 步：输出电容。** 分两种情况：

- **现代 PMOS LDO（陶瓷稳定）**：按手册选 10µF X5R + 0.1µF，ESR 几毫欧；手册通常要求 $C_{out}\ge1\sim10\,\mu$F，且 ESR 在某个上限以下。10µF 在 1.8V 偏置下容值可能掉 20%，实际 8µF；瞬态跌落：

$$\Delta V_{under}=0.5\times\left(0.005+\frac{1}{2\pi\times50\times10^3\times8\times10^{-6}}\right)=0.5\times(0.005+0.398)=0.201\ \text{V}$$

201mV 远超 36mV，说明 10µF 单独不够，需要加 100µF  bulk 或提高 $f_c$。加上 100µF 后总容值约 110µF：

$$\Delta V_{under}=0.5\times\left(0.005+\frac{1}{2\pi\times50\times10^3\times110\times10^{-6}}\right)=0.5\times(0.005+0.0289)=17.0\ \text{mV}$$

满足 36mV。**“陶瓷稳定”不等于“10µF 就能满足瞬态”，要按负载阶跃算。**

- **老式 PNP LDO（ESR 窗口）**：$C_{out}=100\,\mu$F、$f_c=50$ kHz，ESR 窗口 0.0318~0.2Ω，取 0.05Ω：

$$f_z=\frac{1}{2\pi\times0.05\times100\times10^{-6}}=31.8\ \text{kHz},\qquad PM\approx57.5^{\circ}$$

$$\Delta V_{under}=0.5\times(0.05+0.0318)=40.9\ \text{mV}$$

40.9mV 略高于 36mV；把 $C_{out}$ 加到 220µF：

$$\Delta V_{under}=0.5\times(0.05+0.0145)=32.3\ \text{mV}$$

满足。但 220µF 钽/电解的体积和成本要接受。**如果不想用大电容，就选陶瓷稳定的新 PMOS LDO，并加 100µF  bulk 解决瞬态。**

**第 6 步：级联与并联的取舍。**

- 如果输入是 5V，可以先 5V→3.3V（PSRR 40dB），再 3.3V→1.8V（PSRR 48dB），总 PSRR 约 88dB，输出纹波 3.98µV；但总效率只有 36%，两级都要散热。只有在 5V 前级纹波极大、且 1.8V 要求极干净时才值得。
- 如果 1.8V 需要 1A，不要用两颗 0.5A LDO 并联：1% 容差、10mΩ 输出电阻会产生 0.9A 环流；用一颗 1A LDO，或支持均流的器件。

**第 7 步：验证。**

- 压差：输入从 3.465V 降到 3.0V，测输出何时开始跌落；
- 结温：热电偶贴 DFN 焊盘，稳定 30min 后读；按 $T_j=T_a+P_dR_{\theta ja}$ 反算；
- PSRR：在 100kHz 注入 100mVpp，测输出纹波；
- 瞬态：0.5A 阶跃（0.1↔0.6A，1A/µs），测跌落与恢复；
- 输出电容：按手册的 $C_{out}$ 范围与 ESR 范围核对，不要只看容值。

### 4.2 5V→3.3V/300mA 的封装对比

同样 0.3A、$I_Q=1$ mA：

$$P_d=(5-3.3)\times0.3+5\times0.001=0.51+0.005=0.515\ \text{W}$$

SOT-23-5（250°C/W）：

$$T_j=25+0.515\times250=153.8^{\circ}\text{C}$$

DFN（60°C/W）：

$$T_j=25+0.515\times60=55.9^{\circ}\text{C}$$

**0.515W 在 SOT-23-5 上就是 128.8°C 温升**；同样的芯片换 DFN + 铺铜，结温降 98°C。选型时先算 $P_d$，再选封装，不要反过来。

### 4.3 级联与并联的数值对比

| 方案 | 总压差 | 总效率 | 100kHz 总 PSRR | 主要代价 |
|---|---|---|---|---|
| 5V→1.8V 单级 | 3.2V | 36.0% | 48dB | 功耗 1.6W @0.5A，散热大 |
| 5V→3.3V→1.8V 两级 | 3.2V | 36.0% | 88dB | 两颗器件、两级散热、总 IQ 加倍 |
| 两颗 1.8V LDO 并联 | 1.5V | 54.4% | 48dB | 环流 0.9A，需均流 |
| 5V→3.3V Buck + 3.3V→1.8V LDO | — | 约 80%~85% | 48dB（LDO 级） | 开关噪声、电感、成本 |

**单级 LDO 的效率由 $V_{out}/V_{in}$ 决定，级联不会改变这个比值；级联只买 PSRR，不买效率。** 要大电流、大压差，先用 Buck 预稳压，再用 LDO 后级，见[开关电源原理与 Buck 降压](buck.md)。

## 5. 工程含义

### 5.1 数量级：先有直觉，再查手册

| 指标 | 78xx（NPN） | 老式 PNP LDO | 现代 PMOS LDO | 单位 |
|---|---|---|---|---|
| 压差 | 1.5~2.5 | 0.2~0.6 | 0.1~0.3 | V |
| 静态电流 | 3~8 | 0.5~5 | 0.01~1 | mA |
| 100Hz PSRR | 60~75 | 60~80 | 60~80 | dB |
| 100kHz PSRR | 20~30 | 25~40 | 30~45 | dB |
| 输出噪声（10Hz~100kHz） | 50~100 | 20~50 | 5~30 | µVrms |
| 输出电容 | 不挑 | 需 ESR 窗口 | 陶瓷 1~10µF | — |
| 热阻（SOT-23-5） | — | 200~250 | 200~250 | °C/W |
| 热阻（DFN+焊盘） | — | 50~80 | 50~80 | °C/W |

**这些是典型量级，具体以数据手册为准。** 不同厂商、不同修调等级可以差一个数量级。

### 5.2 选型顺序

1. **定压差**：$V_{in,min}-V_{out}\ge V_{DO}+0.3$ V；否则进 dropout，PSRR 和调整率全部失效。
2. **算热**：按最坏 $V_{in}$、最大 $I_{out}$、最高 $T_a$ 算 $T_j$；封装热阻按实际铜箔。
3. **查稳定性**：老 PNP 看 ESR 窗口；陶瓷稳定型看最小/最大 $C_{out}$ 与 ESR 上限。
4. **查 PSRR**：按前级开关频率查曲线；不够就加 LC/磁珠或换器件。
5. **查噪声**：按 10Hz~100kHz 的 µVrms 与 ADC 的 LSB 比。
6. **查 IQ**：电池设备按待机电流算，不按满载效率。
7. **定封装与布局**：DFN 焊盘、过孔、铜箔面积；FB 走线远离功率节点。

### 5.3 布局与热设计

- **输入/输出电容就近**：输入电容紧贴 $V_{in}$ 与地，输出电容紧贴 $V_{out}$ 与地；电容到芯片的回路面积越小，高频阻抗越低。
- **FB 走线**：从输出电容正端开尔文接回 FB，不要从负载端随便引；FB 是高阻节点，远离 SW 节点、电感和时钟线。
- **热焊盘**：DFN/QFN 的裸露焊盘必须焊到铺铜，过孔阵列到内层地；没有散热焊盘时，$R_{\theta ja}$ 可能比手册高 1.5~2 倍。
- **地**：输入电容地、输出电容地、负载地单点汇合，避免负载电流在公共地阻抗上产生压降，把噪声“抬”到 FB。
- **反向保护**：输入掉电比输出快时，加肖特基或选带反向电流保护的 LDO。
- **EN 引脚**：不能悬空；不用时上拉到 $V_{in}$ 或下拉到地，按手册定义。

### 5.4 什么时候不该用 LDO

- **大压差**：12V→3.3V/1A 耗散 8.7W，物理上扛不住；先用 Buck 降到 4~5V，再用 LDO。
- **大电流**：5A 级 LDO 又贵又大，多相 Buck 更合适。
- **效率敏感**：电池设备、绿色能源；LDO 的效率上限就是 $V_{out}/V_{in}$。
- **需要升压**：LDO 只能降压，不能升压；用 Boost 或 Buck-Boost。
- **需要隔离**：LDO 不隔离；用隔离电源或变压器。

## 6. 常见坑

::: pitfall 常见坑
- **现象**：LDO 烫手、输出周期性掉电。**原因**：只算压差够不够，没算 $P_d=(V_{in}-V_{out})I_{out}$ 与结温；SOT-23-5 的 250°C/W 在 0.75W 下就是 187.5°C 温升。**解决**：按最坏 $V_{in}$、最大 $I_{out}$ 算 $T_j$；换 DFN 带焊盘、铺铜、打过孔；必要时降电流或改用 Buck。
- **现象**：老 PNP LDO 配 10µF 陶瓷，输出叠 100~500kHz 振荡。**原因**：陶瓷 ESR 太低，ESR 零点跑到穿越频率之外，相位裕度不足；10µF 时 ESR 窗口甚至是空的。**解决**：按手册 ESR 窗口选钽/电解，或把 $C_{out}$ 加到 100µF 以上；要陶瓷电容就换“陶瓷稳定”的 PMOS LDO。
- **现象**：100Hz PSRR 有 75dB，ADC 仍随 Buck 负载跳。**原因**：Buck 的 100kHz 纹波处 PSRR 只有 30dB，100mV 变成 3.16mV（7.2 LSB）；或纹波从基准/分压网络绕过环路。**解决**：按开关频率查 PSRR；选 100kHz ≥48dB 的器件；加 LC/磁珠；基准单独滤波，FB 远离功率节点。
- **现象**：两级 LDO 级联后，第二级输出掉出稳压。**原因**：只算了自己的压差，没算第一级的纹波谷点和负载瞬态；总压差是两级之和，第二级的 $V_{in,min}$ 可能低于 $V_{out}+V_{DO}$。**解决**：按最低输入、最大负载、纹波谷点逐级核算；每级留 0.3~0.5V；必要时降低第一级输出或加大中间电容。
- **现象**：两颗 LDO 并联，一颗烫、一颗凉，输出电流不均。**原因**：两颗输出电压有容差，输出阻抗又低，微小偏差产生大环流；1.8V/±1%、10mΩ 时环流可达 0.9A。**解决**：不要直接并联；用支持均流的 LDO，或每颗串均流电阻，或改用一颗大电流 LDO。
- **现象**：电池设备待机几天就没电。**原因**：只看了满载效率，忽略 $I_Q$；1mA 静态电流对 2000mAh 电池就是 83 天。**解决**：按待机电流算；选 µA 级 $I_Q$ 的 LDO；不用时用 EN 关断，关断电流可到 nA 级。
- **现象**：输入掉电后，输出电容把 LDO 或前级倒灌坏。**原因**：$V_{out}>V_{in}$ 时，输出电容通过调整管/体二极管向输入放电。**解决**：选带反向电流保护的 LDO；输入串肖特基；或用理想二极管做 ORing。
:::

## 7. 自测题

<details><summary>3.3V→1.8V/500mA、$I_Q=1$mA。功耗多少？SOT-23-5（250°C/W）与 DFN（60°C/W）在 25°C 下结温各多少？</summary>

$$P_d=(3.3-1.8)\times0.5+3.3\times0.001=0.753\ \text{W}$$

SOT-23-5：

$$T_j=25+0.753\times250=213.3^{\circ}\text{C}>125^{\circ}\text{C}$$

DFN：

$$T_j=25+0.753\times60=70.2^{\circ}\text{C}$$

**同一颗芯片，封装决定生死。** 最坏输入 3.465V 时 $P_d=0.836$W，DFN 结温 75.2°C。

</details>

<details><summary>输入 100mVpp、100kHz，PSRR 分别为 30dB、40dB、48dB。输出纹波各多少？对 1.8V/12 位 ADC 是几个 LSB？</summary>

1 LSB $=1.8/4096=0.4395$mV。

30dB：$100/31.62=3.16$mV，$3.16/0.4395=7.19$ LSB。

40dB：$100/100=1.00$mV，$1.00/0.4395=2.28$ LSB。

48dB：$100/251.2=0.398$mV，$0.398/0.4395=0.91$ LSB。

**要 <1 LSB，PSRR 至少 $20\lg(100/0.4395)=47.1$dB。**

</details>

<details><summary>$C_{out}=100\mu$F、$f_c=50$kHz、ESR=0.05Ω、0.5A 阶跃、允许 100mV。ESR 窗口、零点、相位裕度、跌落各多少？</summary>

$$ESR_{min}=\frac{1}{2\pi\times50\times10^3\times100\times10^{-6}}=0.0318\ \Omega$$

$$ESR_{max}=\frac{0.1}{0.5}=0.2\ \Omega$$

$$f_z=\frac{1}{2\pi\times0.05\times100\times10^{-6}}=31.8\ \text{kHz}$$

$$PM\approx\arctan\frac{50}{31.8}=57.5^{\circ}$$

$$\Delta V_{under}=0.5\times(0.05+0.0318)=40.9\ \text{mV}$$

窗口 0.0318~0.2Ω；取 0.05Ω 时 PM 57.5°、跌落 40.9mV。

</details>

<details><summary>5V→3.3V→1.8V 两级 LDO，PSRR 各 40dB 与 48dB（100kHz）。总 PSRR、100mV 输入下的输出纹波、总效率各多少？</summary>

$$PSRR_{total}\approx40+48=88\ \text{dB}$$

$$V_{out,ripple}=\frac{100}{10^{88/20}}=\frac{100}{25119}=3.98\ \mu\text{V}$$

$$\eta\approx\frac{1.8}{5}=36.0\%$$

总压差 $(5-3.3)+(3.3-1.8)=3.2$V。**级联买 PSRR，不买效率。**

</details>

<details><summary>两颗 1.8V LDO 直接并联，±1% 容差、每颗输出电阻 10mΩ。最坏环流多少？加 0.1Ω 均流电阻后呢？</summary>

最坏偏差 $1.8\times1\%=18$mV：

$$I_c=\frac{18\ \text{mV}}{10\ \text{m}\Omega+10\ \text{m}\Omega}=0.9\ \text{A}$$

加 0.1Ω：

$$I_c=\frac{18}{2\times0.1+0.02}=81.8\ \text{mA}$$

环流仍占 0.5A 的 16%，且 0.5A 时每颗电阻压降 50mV。**直接并联不可取；用均流 LDO 或单颗大电流器件。**

</details>

<details><summary>LDO 的 $I_Q=1$mA 与 10µA，2000mAh 电池、3.7V，理论待机各多少？为什么实际更短？</summary>

1mA：

$$t=\frac{2\ \text{Ah}}{0.001\ \text{A}}=2000\ \text{h}=83.3\ \text{天}$$

10µA：

$$t=\frac{2}{0.00001}=200000\ \text{h}=22.8\ \text{年}$$

实际受电池自放电（典型 2%~3%/月）、保护板静态电流、负载待机电流、温度影响，通常远短于理论值。**$I_Q$ 是电池设备的第一指标。**

</details>

<details><summary>为什么 12V→3.3V/1A 不适合用 LDO？算一下功耗与结温。</summary>

$$P_d=(12-3.3)\times1=8.7\ \text{W}$$

即使 DFN 60°C/W：

$$T_j=25+8.7\times60=547^{\circ}\text{C}$$

远超 125°C。必须先用 Buck 把 12V 降到 4~5V，再用 LDO 后级；或者全用 Buck。**LDO 只适合小压差、小电流、低噪声的场合。**

</details>

## 8. 参考资料

- **Analog Devices, *Low-Dropout Linear Regulator (LDO) Application Tutorial***：压差、调整管结构、环路补偿、PSRR 与热设计；本章 2.2、2.7、3.1 的结构与 ESR 窗口按该文。<https://www.analog.com/en/resources/technical-articles/lowdropout-linear-regulator-ldo-application-tutorial.html>
- **Analog Devices, MT-043 *Op Amp Power Supply Rejection Ratio (PSRR) and Supply Voltages***：PSRR 的 dB 定义、正负电源分别给值与频率特性；本章 2.4、3.3 的 $20\lg$ 口径按该文。<https://www.analog.com/media/en/training-seminars/tutorials/MT-043.pdf>
- **TI, LM317 数据手册**：Line/Load Regulation、Dropout Voltage 与热设计参数；本章 3.1 的功耗/结温核算与 4.2 的封装对比参考该表。<https://www.ti.com/lit/ds/symlink/lm317.pdf>
- **TI, LP5907 250mA 低噪声 LDO 数据手册**：PSRR、Output Noise 与 Output Capacitor 曲线；本章 2.4、2.5、3.6 的量级参照该手册（具体型号以数据手册为准）。<https://www.ti.com/lit/ds/symlink/lp5907.pdf>
- **Horowitz & Hill, *The Art of Electronics*, 3rd ed., Chapter 9 *Voltage Regulation and Power Conversion***：线性稳压、基准、效率与热设计的工程讲法；本章 2.3 与 5.1 的量级参照该章。
- **TI, LDO 产品与应用笔记索引**：线性稳压器拓扑、输出电容稳定性与热设计资料入口；本章 5.2 的选型顺序参考该索引。<https://www.ti.com/product-category/power-management/linear-ldo-regulators/overview.html>
