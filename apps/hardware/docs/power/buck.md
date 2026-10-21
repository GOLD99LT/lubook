---
id: buck
title: 开关电源原理与 Buck 降压 Switch-Mode Power Supply & Buck Converter
part: 6
chapter: 开关电源
order: 20
tags: [开关电源, Buck, CCM, 伏秒平衡, 电感纹波, 占空比, 效率]
difficulty: 3
status: published
sources:
  - TI SLVA477A Basic Calculation of a Buck Converter's Power Stage
  - Erickson & Maksimovic, Fundamentals of Power Electronics, 2nd ed.
  - Maniktala, Switching Power Supplies A–Z, 2nd ed.
  - ADI AN-149 Modeling and Loop Compensation of SMPS
---

# 开关电源原理与 Buck 降压 Switch-Mode Power Supply & Buck Converter

## 1. 设计动机

::: motivation 为什么需要开关电源
线性电源效率 ≈ Vout/Vin，12V→5V 只有 ~42%，大半功耗变成热。**开关电源（Switch-Mode Power Supply, SMPS）**让功率管在"全开（低阻）"和"全关（无电流）"之间高速切换，管子本身功耗极小，效率可达 85~95%。**Buck（降压变换器）**是最基础的拓扑：把较高的输入电压降到较低的输出，12V→5V、锂电池→3.3V 都用它。代价是输出有开关纹波、电路更复杂。
:::

核心思想：用一个开关高速通断，把能量"打包"送进电感/电容，再靠反馈调节每个包的大小（占空比），把输出稳住。

## 2. 原理图

![异步 Buck：Vin 经高侧开关 Q1 接到 SW 节点，续流二极管在 Q1 关断时维持电感电流，电感 L 滤波后接 Cout 输出，R1/R2 分压反馈](../assets/schematics/buck.svg)

三个能量元件各司其职：**Q1**（高侧开关）把 Vin 接到 SW；**D**（续流二极管）在 Q1 关断时给电感电流一条回路；**L**（电感）平滑电流；**Cout**（输出电容）平滑电压。SW 节点是"方波"，经 L、Cout 低通后变成平滑直流。

## 3. 静态分析（DC）

稳态 CCM（连续导通模式，电感电流始终 > 0）下：

- **输出与输入关系（理想）**：$V_{out}=D\cdot V_{in}$，D 为占空比（高侧开通时间占开关周期比例）。考虑效率 $\eta$ 后工程用 $D=V_{out}/(\eta V_{in})$。
- **电感平均电流**：等于输出电流 $I_L=I_{out}$（直流分量全部流向负载）。
- **开关管应力**：Q1 关断时承受的电压 = $V_{in(max)}$；峰值电流 $I_{SW(peak)}=I_{out}+\Delta I_L/2$。
- **二极管应力**：反向电压 = $V_{in(max)}$；平均电流 $I_F=I_{out}(1-D)$。

## 4. 动态分析（AC / 瞬态）

电感电流是三角波：Q1 开通（SW=Vin）时线性上升、关断（SW≈0）时线性下降。下图中 IL 上升段严格落在 SW=12V 区间、下降段落在 SW=0 区间（占空比为示意，本设计标称 D≈0.46）。输出纹波由电容充放电与 ESR 共同产生。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["SW 节点电压", "电感电流 IL"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 60, "right": 60, "top": 26, "bottom": 56},
  "xAxis": {"type": "category", "name": "时间 µs", "data": [0,0.5,1,1.5,2,2.5,3,3.5,4], "axisLabel": {"fontSize": 11}},
  "yAxis": [
    {"type": "value", "name": "SW V", "min": 0, "max": 14, "axisLabel": {"fontSize": 11}},
    {"type": "value", "name": "IL A", "min": 0.8, "max": 1.2, "axisLabel": {"fontSize": 11}}
  ],
  "series": [
    {"name": "SW 节点电压", "type": "line", "step": "end", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#b5642e"},
     "data": [12, 12, 12, 12, 0, 0, 0, 0, 0]},
    {"name": "电感电流 IL", "type": "line", "showSymbol": false, "yAxisIndex": 1, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [0.86, 0.94, 1.02, 1.10, 1.13, 1.04, 0.96, 0.90, 0.86]}
  ]
}
```

## 5. 环路分析

Buck 是电压/电流模式负反馈：采样输出分压 → 误差放大器 → PWM 比较器调占空比。

- 结论：功率级含一个 LC 双极点（在 $f_0=1/(2\pi\sqrt{LC})$）和 ESR 零点，相位在 LC 谐振处骤降，必须用补偿网络把相位裕度拉到 >45°。
- 环路穿越频率建议 ≤ fs/10~fs/5；太快易振荡，太慢瞬态差。

::: advanced 进阶：CCM 伏秒平衡与小信号
**伏秒平衡（Volt-Second Balance）**：稳态下电感两端伏秒积一周内正负相消，否则电流单向漂移。
- Q1 开通 $D\cdot T$：电感电压 $V_L=V_{in}-V_{out}$，伏秒积 $(V_{in}-V_{out})D T$；
- Q1 关断 $(1-D)T$：续流二极管导通，SW≈0，$V_L=-V_{out}$，伏秒积 $-V_{out}(1-D)T$；
- 相加为零：$(V_{in}-V_{out})D = V_{out}(1-D)\Rightarrow V_{out}=D V_{in}$。
**电感纹波**：开通期电流上升 $\Delta I_L=\dfrac{(V_{in}-V_{out})D T}{L}=\dfrac{V_{in}-V_{out}}{f_s L}D$。
**小信号**：CCM Buck 功率级控制-输出传递函数近似 $G_{vd}(s)=G_{dc}\dfrac{1+s/(\omega_{ESR})}{1+s/(Q\omega_0)+(s/\omega_0)^2}$，其中 $G_{dc}=V_{in}$，$\omega_0=1/\sqrt{LC}$。补偿网络（Type II/III）在 LC 双极点处提供相位提升，保证相位裕度 >45°。
:::

## 6. 元件取值与工程权衡

- **电感 L**：由目标纹波电流反推。工程取 $\Delta I_L=(0.2\sim0.4)I_{out(max)}$（常 30%）。L 大→纹波小、峰值电流低，但体积大、瞬态慢；L 小→体积小但纹波大、峰值应力高。
- **输出电容 Cout**：由目标输出纹波反推 $C_{out}=\Delta I_L/(8 f_s \Delta V_{out})$；ESR 额外贡献 $\Delta V_{ESR}=ESR\cdot\Delta I_L$。首选低 ESR 陶瓷（X5R/X7R）。
- **占空比**：按最差输入（最低 Vin）算最大 D。
- **反馈分压**：支路电流 ≥ 100×FB 偏置电流，电阻取 1%。

## 7. 完整设计示例

::: example 12V→5V/1A Buck 完整设计（CCM）
1. **需求**：Vin=12V（范围 10.8~13.2V），Vout=5V，Iout=1A，fs=500kHz，预估 η=0.9。
2. **算占空比（最差 Vin=10.8V）**：$D=V_{out}/(\eta V_{in})=5/(0.9\times10.8)=0.514$。
3. **定纹波电流**：取 $\Delta I_L=0.3\times1A=0.3A$。
4. **算电感**：$L=\dfrac{V_{out}(V_{in}-V_{out})}{\Delta I_L f_s V_{in}}=\dfrac{5\times7}{0.3\times500k\times12}\approx19.4\mu H$，取标准值 **22µH**。
5. **验算纹波**：$\Delta I_L=(12-5)\times0.463/(500k\times22\mu H)\approx0.295A\approx0.3A$ ✓（D 按标称 12V 取 0.463）。
6. **峰值开关电流**：$I_{SW(peak)}=1+0.295/2\approx1.15A$，选电感饱和电流 ≥1.5A（降额）。
7. **算输出电容**：目标纹波 50mV，$C_{out}=\Delta I_L/(8 f_s\Delta V)=0.295/(8\times500k\times0.05)\approx1.5\mu F$；计入 DC bias 降额，取 **2×22µF X5R**。
8. **反馈分压**：VFB=0.8V，取支路电流 10µA，$R_2=0.8V/10\muA=80k$（取 80.6k），$R_1=80.6k\times(5/0.8-1)=422k$。
9. **续流二极管（异步）**：$I_F=1\times(1-0.463)=0.537A$，选肖特基 VF=0.5V，$P_D=0.27W$。
10. **效率与损耗**：Q1 导通损 $I^2R_{DSon}D\approx1^2\times0.1\times0.46=0.046W$；二极管 0.27W；电感 DCR 0.05W；开关/栅损 ~0.2W。Pout=5W，总损 ≈0.57W，η≈5/5.57≈90%。
:::

## 8. 仿真与实验

LTspice 用 Buck 控制器/开关管模型：

- `.tran 200u`：观察 SW 节点方波、电感电流三角波、输出纹波；
- 扫 Vin 从 10.8→13.2V：验证 D 变化、输出稳定；
- 负载 0.2A↔1A 阶跃：看输出坑深与恢复，对照环路设计；
- 改 L 从 10µH→47µH：看纹波电流与峰值电流变化；
- 用 ADI LTpowerCAD 先"纸面设计"再导出 LTspice 网表核对。

## 扩展与变种电路

### 扩展1：自举 Bootstrap（高侧 N-MOS 驱动）

高侧开关用 N-MOS 时，栅极要比源极（SW）还高 10V 才能完全导通；而 SW 在 0~Vin 间摆动。用一只自举二极管 + 自举电容"泵"出一个比 SW 高的电压驱动栅极。

![Vin 经 Dboot 给 Cboot 充电，Cboot 跨在 BST-SW 之间，作为栅驱动电源](../assets/schematics/buck-bootstrap.svg)

::: example 工作原理与静态
- Q2（低侧同步管）导通、SW≈0 时，Vin 经 Dboot 给 Cboot 充到 ≈Vin−0.7V。
- Q1 导通时 SW 升到 Vin，Cboot 上的电荷把栅极抬到 Vin+Cboot，保证 N-MOS 充分导通。
- Cboot 典型 0.1~1µF 陶瓷；Dboot 用快恢复/肖特基。
:::

取值对比：自举 N-MOS 对比 P-MOS 高侧：N-MOS RDSon 小、便宜，但需要自举；P-MOS 驱动简单但 RDSon 大、贵。占空比不能 100%（否则自举电容没机会充电）。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["BST-SW 驱动电压"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 60, "right": 30, "top": 26, "bottom": 50},
  "xAxis": {"type": "category", "name": "µs", "data": [0,1,2,3,4], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "V", "min": 9, "max": 11, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "BST-SW 驱动电压", "type": "line", "step": "end", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [10, 9.9, 9.8, 9.9, 10]}
  ]
}
```

::: pitfall 占空比过大致使自举电容亏电
- **现象**：高占空比下高侧 MOS 半导通、发热。
- **原因**：SW 长时间为高，自举电容无续充机会，驱动电压被放低。
- **解决**：限制最大占空比（如 <90%），或用内置电荷泵的驱动器；Cboot 别取太小。
:::

### 扩展2：同步整流（低侧 MOS 替代二极管）Synchronous Rectification

把续流二极管换成低侧同步 MOS（Q2），用其极低 RDSon 替代肖特基的 0.5V 压降，大幅提升效率。

![续流位置由 Q2 同步 MOS 承担，与 Q1 互补导通](../assets/schematics/buck-sync.svg)

::: example 工作原理与静态
- Q1、Q2 互补开关（加死防直通）。Q2 导通时压降 = $I_{out}\cdot R_{DSon}$（几十 mV），远小于二极管 0.5V。
- 本例二极管耗 0.27W → 同步后 $1^2\times0.05=0.05W$，效率提升约 4 个百分点。
- 轻载时 Q2 仍导通会反向倒灌，需进入二极管仿真/PFM 模式。
:::

取值对比：同步 Buck 对比异步（二极管）：效率高、发热小，但需栅驱动和死区控制、IC 更贵。低压大电流（如 5V→3.3V）几乎都用同步。

::: pitfall Q1/Q2 直通 shoot-through
- **现象**：管子炸、电流尖峰。
- **原因**：两管同时导通把 Vin 对地短路。
- **解决**：硬件死区时间（dead-time）由控制器保证，绝不外加强行同时开。
:::

### 扩展3：PFM 节能模式（轻载降频）PFM / Auto Mode

重载时用固定 fs 的 PWM 保证低纹波；轻载时跳脉冲降频，牺牲纹波规整性换轻载效率。

![轻载自动跳脉冲、重载固定频率 PWM 的控制块](../assets/schematics/buck-pfm.svg)

::: example 工作原理与静态
- 轻载时开关损耗占主导，降频减少开关次数；电感电流进入 DCM（断续）。
- 静态：输出仍稳压，但开关频率随负载变化。
- 电池设备多数时间轻载，PFM 显著延长续航。
:::

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["效率：强制PWM", "效率：Auto/PFM"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 60, "right": 30, "top": 26, "bottom": 50},
  "xAxis": {"type": "category", "name": "负载比例", "data": ["1%", "10%", "30%", "60%", "100%"], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "效率 %", "min": 60, "max": 95, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "效率：强制PWM", "type": "line", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#b5642e"},
     "data": [62, 78, 87, 90, 89]},
    {"name": "效率：Auto/PFM", "type": "line", "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [85, 89, 91, 91, 89]}
  ]
}
```

取值对比：PFM/Auto 对比强制 PWM：轻载效率高、但纹波频率不固定（射频更敏感）。适用：电池便携；不适用：对固定开关频率敏感（如射频、时钟耦合）的场合。

::: pitfall PFM 纹波干扰射频
- **现象**：PFM 模式下收音机/接收机出现杂散。
- **原因**：跳脉冲频率分散，落在射频带内。
- **解决**：射频附近改强制 PWM 或固定频率，靠 LDO 后级净化。
:::

### 扩展4：反馈前馈电容 Cff Feedforward Compensation

在反馈上电阻 R1 上并联一只小电容，超前相位、改善负载瞬态。

![Cff 与 R1 并联，高频旁路 R1 加快反馈响应](../assets/schematics/buck-ffcomp.svg)

::: example 工作原理与静态
- Cff 在中高频把 R1 旁路，相当于随频率提高反馈系数，引入一个零点提升相位裕度。
- 典型 Cff = 几十 pF~几百 pF，与 R1 构成零点 $f_z=1/(2\pi R_1 C_{ff})$。
- 静态 DC 不受影响（电容直流开路）。
:::

取值对比：加 Cff 对比纯电阻分压：瞬态恢复更快、相位裕度更好；过大则噪声增益抬高。适用：要求快瞬态的负载阶跃；不适用：内部已补偿 IC（勿乱加）。

::: pitfall 内部补偿 IC 乱加 Cff 致振荡
- **现象**：加 Cff 后输出振荡。
- **原因**：内部补偿已固定，外加零点破坏相位裕度。
- **解决**：只有外部补偿型 IC 才按推荐加 Cff/补偿网络。
:::

### 扩展5：多相并联 Buck Multiphase

多相交错并联，每相电感电流相位错开，输入输出纹波相互抵消，等效频率倍增、电流能力倍增。

![两相开关相位错开 180°，电感电流相加，纹波部分抵消](../assets/schematics/buck-multiphase.svg)

::: example 工作原理与静态
- N 相交错，每相只承担 $I_{out}/N$，热分散；输入纹波电流因相位抵消而减小。
- 等效开关频率 ×N，可用更小单相电感，动态更快。
- 静态总输出 = 各相电流之和，靠均流控制。
:::

取值对比：多相对比单相大电流：电流大（10A+）、纹波小、热好；但需多相控制器、成本高。适用：CPU/GPU 大电流 core 供电；不适用：小电流。

::: pitfall 相间不均流
- **现象**：某相过热。
- **原因**：电感 DCR 或阈值不匹配导致电流分配不均。
- **解决**：选均流控制好的多相控制器，电感配对。
:::

## 9. 常见坑与故障现象

::: pitfall 常见坑
- **只算电感量不算饱和电流**：选了够 µH 但饱和电流 < 峰值电流的电感，重载时电感饱和、电流尖峰烧管。$I_{sat}$ 必须 > $I_{SW(peak)}$ 并留量。
- **陶瓷电容 DC bias 降额没算**：22µF/10V X5R 在 5V 偏置下实际可能只剩 ~10µF，纹波比设计大一倍。按 DC bias 曲线选容量。
- **输入电容 ESR/纹波电流不够**：Buck 输入电容承受脉冲方波电流，ESR 发热炸电容。选低 ESR、纹波电流额定足够的陶瓷。
- **PCB 高 di/dt 环路没收紧**：Vin-高侧管-输入电容回路面积大，辐射尖峰。详见 [EMI/EMC 布局](../pcb/emi-emc.md)。
:::

## 10. 自测题

<details><summary>Buck：Vin=12V、Vout=5V、理想效率，占空比 D 是多少？</summary>

理想 $D=V_{out}/V_{in}=5/12\approx0.417$。工程按 η=0.9 和最低 Vin=10.8V 取 D≈0.51 留余量。

</details>

<details><summary>伏秒平衡：Q1 开通时电感电压多少？为什么稳态一周内伏秒积必须为零？</summary>

开通期 $V_L=V_{in}-V_{out}=7V$。若一周内伏秒积不为零，电感电流会单向逐周期累加或衰减，无法稳态平衡；稳态必须正负伏秒相消，从而推得 $V_{out}=D V_{in}$。

</details>

<details><summary>$I_{out}=1A$、$\Delta I_L=0.3A$，开关管峰值电流多少？选电感饱和电流至少多大？</summary>

$I_{SW(peak)}=I_{out}+\Delta I_L/2=1+0.15=1.15A$。电感饱和电流须 >1.15A，按降额取 ≥1.5A。

</details>

## 11. 参考资料

- [TI SLVA477A — Basic Calculation of a Buck Converter's Power Stage](https://www.ti.com/lit/an/slva477a/slva477a.pdf)
- [ADI AN-149 — Modeling and Loop Compensation Design of SMPS](https://www.analog.com/media/en/technical-documentation/application-notes/an149fa.pdf)
- Maniktala, *Switching Power Supplies A–Z*, 2nd ed.
- Erickson & Maksimovic, *Fundamentals of Power Electronics*, 2nd ed.
- [ADI LTpowerCAD 设计工具](https://www.analog.com/en/design-center/design-tools-and-calculators.html)
