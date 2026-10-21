---
id: capacitor-parameters
title: 电容参数：耐压、ESR、ESL 与失效模式 Capacitor Parameters
part: 2
chapter: 电容器与电感器
order: 25
tags: [ESR, ESL, 自谐振频率, 纹波电流, 降额, 失效模式]
difficulty: 2
status: published
sources:
  - The Circuit Designer's Companion (P. Wilson)
  - The Art of Electronics (Horowitz & Hill, 3rd ed.)
  - https://www.ibiblio.org/kuphaldt/electricCircuits/
---

# 电容参数：耐压、ESR、ESL 与失效模式 Capacitor Parameters

上一章按材质选电容类型，这一章深入电容的"非理想模型"。真实电容不是理想的 $C$，它内部还串联着电阻和电感（ESR、ESL）。理解它们，才能解释"为什么同样 10µF，在高频下一个管用一个不管用"。

## 1. 设计动机：为什么要关心 ESR 和 ESL

::: motivation 理想电容 vs 真实电容
理想电容的阻抗随频率升高无限下降，随便多大频率都能滤。但真实电容在某个频率以上阻抗反而上升——因为它寄生了串联电感 ESL。超过自谐振频率（Self-Resonant Frequency, SRF）后，电容表现得像电感，去耦作用消失。选电容时不仅要看容量，还要看它在你关心的频段阻抗够不够低。
:::

## 2. 等效电路与阻抗曲线

真实电容的串联等效模型：理想电容 $C$ + 等效串联电阻 ESR + 等效串联电感 ESL。

$$Z = ESR + j\!\left(\omega L_{ESL} - \frac{1}{\omega C}\right)$$

![真实电容串联等效模型：C 串联 ESR 与 ESL](../assets/schematics/capacitor-parameters.svg)

- **低于 SRF**：容抗 $1/\omega C$ 主导，阻抗随频率升高下降。
- **在 SRF 处**：容抗与感抗抵消，阻抗最小 ≈ ESR。
- **高于 SRF**：感抗 $\omega L_{ESL}$ 主导，阻抗随频率升高上升，电容"变成电感"。

自谐振频率：

$$f_{SRF}=\frac{1}{2\pi\sqrt{L_{ESL}\,C}}$$

下面是一颗 10µF/0805 MLCC 的典型阻抗-频率曲线（对数坐标），谷底就是 SRF：

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["|Z| 阻抗"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 60, "right": 30, "top": 30, "bottom": 56},
  "xAxis": {"type": "category", "name": "频率 Hz", "data": ["1k","3k","10k","30k","100k","300k","1M","3M","10M","30M","100M"], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "log", "name": "|Z| Ω", "min": 0.01, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "|Z| 阻抗", "type": "line", "smooth": true, "showSymbol": false,
     "lineStyle": {"width": 2.6, "color": "#1a4f8b"},
     "data": [16, 5.3, 1.6, 0.53, 0.18, 0.08, 0.06, 0.11, 0.35, 1.1, 3.5]}
  ]
}
```

## 3. 关键参数详解

| 参数 | 英文 | 含义 | 工程影响 |
|---|---|---|---|
| 等效串联电阻 | ESR | 电容内部串联损耗电阻 | 纹波电流流过 ESR 发热 $P=I_{rms}^2 R_{ESR}$；LDO/电源环路中 ESR 影响稳定性 |
| 等效串联电感 | ESL | 引脚与极板寄生电感 | 决定 SRF 上限；封装越小 ESL 越低，高频去耦越好 |
| 纹波电流 | Ripple Current | 允许长期通过的交流电流有效值 | 超限则 ESR 发热超温，寿命骤减 |
| 额定电压 | Rated Voltage | 最大工作电压 | 直流工作电压建议 ≤ 额定 50%~70% 留裕量 |
| 介质吸收 | Dielectric Absorption (DA) | 放电后电容"回弹"出残余电压 | 影响采样保持、ADC、积分器精度 |
| 寿命 | Lifetime | 电解电容在最高额定温度下的保证时间 | 温度每降 10℃，寿命约翻倍 |

::: analogy 直觉类比：阻抗曲线像一口锅的剖面
把电容阻抗画出来，形状像一口锅：左边（低频）是高高的锅壁（容抗大），中间锅底最薄（≈ESR），右边（高频）锅壁又高起来（感抗大）。你希望工作频率正好落在"锅底"附近——这时阻抗最低、去耦最有效。频率太高，锅壁又厚了，等于没用。
:::

## 4. 选型要点与工程权衡

- **按目标频段选电容**：芯片瞬态噪声在几十 MHz，就要选 SRF 落在该频段的小封装 MLCC（0402/0603，ESL 低）。大容量电解 SRF 只有几十 kHz，指望它滤 MHz 噪声是徒劳。
- **ESR 与纹波发热**：开关电源输出电容要选低 ESR、允许大纹波电流的型号（聚合物/POSCAP 或低 ESR 电解）。ESR 高会发热、并在输出纹波上叠加尖峰。
- **LDO 稳定性对 ESR 敏感**：某些 LDO 需要输出电容 ESR 落在特定范围才能稳定，太低反而振荡——必须按数据手册选电容，不能盲目用超低 ESR 陶瓷。
- **电压降额**：陶瓷电容按工作电压的 2~3 倍选耐压（抵消直流偏置降额）；电解按 ≤70% 额定电压；钽按 ≤50%。
- **介质吸收影响精密电路**：采样保持、电荷积分器要选低 DA 的 C0G/薄膜电容，别用 X7R。

## 5. 典型应用：Buck 输出电容

::: example Buck 开关电源输出电容取值
1. **需求**：Buck 输出 5V/2A，要求输出纹波 < 50mV。
2. **选容量**：按纹波与瞬态响应估算，需 22~47µF 有效容量。
3. **选低 ESR**：开关频率 400kHz，纹波电流约 2A，ESR 产生的纹波 $\Delta V=I_{ripple}\times ESR$，要 < 20mV 则 ESR < 10mΩ。选几颗 22µF/0805 X7R 并联（并联降 ESR 也降 ESL）。
4. **核算直流偏置**：5V 工作，选 10V 以上耐压以减少 X7R 偏置降额；必要时多颗并联补足有效容量。
5. **布置**：电容尽量靠近电感/输出脚，走线短粗，降低回路电感。
:::

## 6. 失效模式与常见坑

::: pitfall 常见坑
- **过压/浪涌致介质击穿短路**：现象——电源输入电容击穿、保险丝烧断。原因——工作电压超出电容耐压，或开关浪涌/反峰电压超过耐压。解决——按 2~3 倍裕量选耐压，电解/钽特别注意浪涌，必要时加压敏/TVS。
- **电解电容干涸开路**：现象——容量变小、ESR 变大、电源纹波增大、输出掉压。原因——电解液长期高温蒸发。解决——选 105℃ 长寿命型号、远离热源、留纹波裕量，定期更换。
- **误用高 ESR 电容致电源环路振荡**：现象——LDO/Buck 输出出现高频振荡。原因——输出电容 ESR 不在数据手册要求范围。解决——严格按数据手册推荐的电容类型/ESR 范围选型。
- **陶瓷电容直流偏置降额被忽略**：现象——设计 22µF 去耦，实际有效只有 8µF，瞬态响应差。原因——X7R/X5R 在直流偏压下容量暴跌。解决——选高耐压/优化材质，多颗并联，按偏压后容量复核。
:::

## 7. 自测题

<details><summary>一颗电容的自谐振频率 SRF 由什么决定？频率远高于 SRF 时它表现为什么？</summary>

$f_{SRF}=1/(2\pi\sqrt{L_{ESL}C})$，由 ESL 和 C 共同决定。频率远高于 SRF 时，感抗 $\omega L$ 超过容抗，电容整体表现为**电感**，阻抗随频率升高而上升，去耦失效。
</details>

<details><summary>纹波电流为什么会让电解电容发热？怎么选？</summary>

纹波电流流过 ESR，产生 $P=I_{rms}^2 R_{ESR}$ 的损耗并发热。发热加速电解液蒸发、缩短寿命。应选允许纹波电流（Ripple Current）足够大、ESR 低的型号，必要时多颗电容并联分摊，并远离热源。
</details>

<details><summary>为什么小封装（0402）比大封装（1206）更适合高频去耦？</summary>

小封装引脚短、极板回路小，ESL 更低，SRF 更高，能在更高频率保持低阻抗。1206 ESL 大，SRF 低，高频下早已变成电感。因此高频去耦优先用 0402/0603。
</details>

## 8. 参考资料

- The Circuit Designer's Companion (P. Wilson) — 电容 ESR/ESR 与电源去耦
- The Art of Electronics (Horowitz & Hill, 3rd ed.) — 非理想电容与频率特性
- Lessons In Electric Circuits (Kuphaldt) — 容抗与阻抗基础
