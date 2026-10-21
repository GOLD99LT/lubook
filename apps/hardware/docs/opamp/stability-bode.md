---
id: stability-bode
title: 稳定性：伯德图、相位裕度与补偿 Stability, Bode Plots & Compensation
part: 3
chapter: 运放基础
order: 55
tags: [稳定性, 伯德图, 相位裕度, 增益裕度, 频率补偿, 自激]
difficulty: 3
status: published
sources:
  - Sergio Franco, Design with Operational Amplifiers 4e, Stability & Compensation 章
  - Robert A. Pease, Troubleshooting Analog Circuits
  - ADI, A Deeper Look into Difference Amplifiers (Analog Dialogue)
---

# 稳定性：伯德图、相位裕度与补偿 Stability, Bode Plots & Compensation

负反馈能稳定增益，但它有个代价：**高频处环路相位滞后累积，可能让反馈"变正"，电路开始自激振荡**。本章是运放理论的收官——用伯德图（Bode Plot）判断一个反馈电路稳不稳，以及怎么加补偿把它救回来。

## 1. 设计动机

::: motivation 为什么要学稳定性
你有没有遇到过：面包板电路接好后，输出什么都没输入却在几 MHz 上吱吱振荡？这就是负反馈在高频"翻脸成正反馈"。仿真不出问题、一上板就振荡，多半是相位裕度不够。学会看伯德图，你就能在设计阶段预判并消除它。
:::

## 2. 原理图

![并联补偿：反馈电阻 Rf 上并联小电容 Cf，在高频引入零点把相位"拉回"](../assets/schematics/stability-bode.svg)

## 3. 伯德图：幅频与相频

环路增益 $T(f)=A(f)\beta$ 随频率变化，画成伯德图：幅频看 $|T|$ 怎么滚降，相频看相位怎么滞后。

- **增益交界频率 $f_c$**：$|T|=1$（0dB）处。
- **相位裕度 PM（Phase Margin）**：在 $f_c$ 处，相位 $\phi$ 距离 −180° 还有多少：$\text{PM}=180^{\circ}+\phi(f_c)$。
- **判据**：PM ≥ 45° 稳定；PM < 30° 输出有明显过冲/振铃；PM ≤ 0 自激振荡。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["环路增益 |T| dB", "相位 φ(°)"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 60, "right": 60, "top": 30, "bottom": 56},
  "xAxis": {"type": "category", "name": "频率 Hz（对数）", "data": ["1","10","100","1k","10k","100k","1M","10M"], "axisLabel": {"fontSize": 11}},
  "yAxis": [
    {"type": "value", "name": "|T| dB", "min": -20, "max": 80, "axisLabel": {"fontSize": 11}},
    {"type": "value", "name": "相位", "min": -200, "max": 0, "axisLabel": {"fontSize": 11}}
  ],
  "series": [
    {"name": "环路增益 |T| dB", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.6, "color": "#1a4f8b"},
     "data": [70,70,69,60,40,20,0,-20]},
    {"name": "相位 φ(°)", "type": "line", "smooth": true, "showSymbol": false, "yAxisIndex": 1, "lineStyle": {"width": 2.4, "color": "#b5642e"},
     "data": [-5,-10,-20,-45,-90,-130,-135,-150]}
  ]
}
```

在上图中，$|T|$ 过 0dB 处（1MHz）相位约 −135°，相位裕度 $\text{PM}=180-135=45^{\circ}$——刚好及格，稳定但余量不大。

::: analogy 相位裕度像打方向盘的余量
高速开车（高频）时方向盘有延迟（相位滞后）。如果打方向后车过 180° 才反应过来，你就会来回画龙（振荡）。相位裕度就是"反应还差多少到 180°"的安全距离——余量越大，车越稳。
:::

## 4. 自激的本质

负反馈在中频是负的；但每个极点贡献 90° 滞后，两个极点后总滞后 180°——原本的负反馈在高频变成了正反馈。若此时 $|T|\ge1$，信号绕环路一圈不仅没被衰减还被同相放大，就开始振荡。

## 5. 频率补偿怎么救

- **主极点补偿（Dominant Pole）**：把第一个极点前移，让 $|T|$ 在相位变差前就降到 0dB，换稳定牺牲带宽。
- **密勒补偿**：在运放内部跨增益级加电容，利用密勒倍增把主极点压得更低。
- **外部滞后补偿**：如上图，在反馈电阻 Rf 上并一个小电容 Cf（几 pF），引入一个零点把相位拉回，抬高 PM。

::: advanced 进阶：相位裕度定量推导
设运放开环单极点模型 $A(s)=A_0/(1+s/\omega_1)$，反馈系数 β。环路增益 $T(s)=A(s)\beta$。增益交界满足 $|T(j\omega_c)|=1$。单极点系统相位最多到 −90°，PM 永远 >90°，无条件稳定。实际运放是多极点（两级以上），第二个极点 $\omega_2$ 再贡献 90°。若 $|T|$ 在过 $\omega_2$ 后才到 0dB，相位已接近 −180°，PM 很小。补偿的目标就是让 0dB 交界频率落在 $\omega_2$ 之前——在相位还没恶化前把增益压下来。
:::

## 6. 元件取值与权衡

- **Cf 取值**：几 pF~几十 pF，太大带宽损失，太小补偿不足。按目标 PM（≥45°）反推。
- **负载电容**：容性负载会引入额外极点，最容易让电路振荡——必要时在输出串小电阻隔离。
- **LDO 的 ESR 要求**：本质也是频率补偿，电容 ESR 不对就振荡。

## 7. 仿真与实验

LTspice：

- 搭反相放大，做 AC 扫描看闭环频响；若在高频出现"尖峰"，说明 PM 不足。
- 在 Rf 上并 Cf，观察尖峰消失、带宽略降。
- 逐步加大容性负载，看输出从干净→振铃→振荡的渐变。

## 扩展与变种电路

### 扩展1：容性负载隔离补偿 Capacitive-Load Isolation

**定位**：输出串一颗小电阻把容性负载与运放输出隔开，消除容性负载引入的附加极点——解决"带大电容就振荡"。

![容性负载隔离](../assets/schematics/stability-bode-capload-iso.svg)

::: example 工作原理 / 静态分析
$R_s$（几十 $\Omega$）串在输出与 $C_L$ 之间，反馈取在 $R_s$ 前的运放输出脚。$C_L$ 与运放输出阻抗形成的极点被 $R_s$ 隔开，相位裕度恢复：

$$f_p\approx \frac{1}{2\pi(R_s+R_{out})C_L}$$

代价是 $R_s$ 上有微小压降。
:::

设计要点：$R_s=10\Omega\sim 100\Omega$；反馈必须取 $R_s$ 前，否则隔离失效。

::: pitfall 容性负载专属坑
- **反馈取在隔离电阻后**：把反馈接到 $C_L$ 端，$R_s$ 被反馈环包围，隔离作用消失、照样振荡。反馈要取 $R_s$ 前的运放脚。
:::

### 扩展2：反馈超前补偿 Lead Compensation

**定位**：在反馈网络用 $R_{lead}$-$C_{lead}$ 与 $R_f$ 并联，引入零点把相位拉回——抬相位裕度、压自激。

![反馈超前补偿](../assets/schematics/stability-bode-lead-comp.svg)

::: example 工作原理 / 静态分析
$R_{lead}$-$C_{lead}$ 支路在高频提供超前相位，反馈网络引入一个零点

$$f_z=\frac{1}{2\pi R_{lead}C_{lead}}$$

零点抵消一个极点的滞后，相位裕度 $\text{PM}$ 提升到 $>45^{\circ}$。
:::

设计要点：$C_{lead}$ 几 pF~几十 pF；太大带宽损失，太小补偿不足。

::: pitfall 超前补偿专属坑
- **凭感觉取电容**：仿真看闭环频响，高频出现尖峰就是 PM 不足，逐步加大 $C_{lead}$ 直到尖峰消失、带宽略降。
:::

## 8. 常见坑

::: pitfall 常见坑
- **输出带大电容负载振荡**：容性负载与输出阻抗形成附加极点，高频啸叫。串小电阻（几十Ω）隔离或加补偿电容。
- **面包板寄生电感引发振荡**：高频下长线变电感，和运放输出阻抗形成谐振。缩短走线、就近加去耦。
- **为图快省略补偿电容**：在实验室好好的产品，量产温漂后批次性振荡。补偿要按最恶劣条件留余量。
- **以为振荡是噪声**：输出上叠的固定频率正弦波不是外界干扰，是电路自激——靠滤波没用，要改环路。
:::

## 9. 自测题

<details><summary>增益交界处相位 −120°，相位裕度多少？电路稳定吗？</summary>

$\text{PM}=180-120=60^{\circ}$，大于 45°，稳定且余量充足。
</details>

<details><summary>为什么容性负载容易让运放振荡？</summary>
负载电容与运放输出阻抗构成一个额外极点，在环路中再贡献 90° 相位滞后，把相位裕度吃掉。串小电阻或加补偿电容可解。
</details>

<details><summary>主极点补偿为什么牺牲带宽？</summary>
把主极点前移，意味着环路增益在更低频率就开始滚降、更早降到 0dB——交界频率降低，可用闭环带宽变小，换稳定。
</details>

## 10. 参考资料

- Sergio Franco《Design with Operational Amplifiers》4e，Stability & Compensation 章
- Robert A. Pease《Troubleshooting Analog Circuits》
- ADI《A Deeper Look into Difference Amplifiers》——输入间接电容致振荡的量产案例
