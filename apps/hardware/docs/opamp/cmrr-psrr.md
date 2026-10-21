---
id: cmrr-psrr
title: 共模范围、CMRR 与 PSRR Common-Mode Range, CMRR & PSRR
part: 3
chapter: 运放基础
order: 65
tags: [运放, CMRR, PSRR, 共模抑制, 电源抑制]
difficulty: 2
status: published
sources:
  - MT-035 Op Amp Inputs, Outputs, Single-Supply & Rail-to-Rail Issues (ADI)
  - A Deeper Look into Difference Amplifiers (ADI Analog Dialogue)
  - https://www.analog.com/en/resources/analog-dialogue/articles/deeper-look-into-difference-amplifiers.html
---

# 共模范围、CMRR 与 PSRR

## 1. 定义与物理来源

运放的输出只应该响应两个输入端的**电压差**。但真实运放会同时响应"两个输入端共同被抬升的那部分电压"，这就是**共模信号（Common-Mode Voltage, Vcm）**。

- **共模抑制比（CMRR, Common-Mode Rejection Ratio）**：运放对差模信号的增益除以它对共模信号的增益，通常用分贝表示 $CMRR = 20\log_{10}(A_d/A_c)$。理想 CMRR 无穷大。
- **电源抑制比（PSRR, Power Supply Rejection Ratio）**：电源上的波动（纹波、噪声）折算到输入端、再被输出放大的反向指标。$PSRR$ 表示电源变化 1V 相当于输入端多大的失调变化。PSRR 越高，电源纹波越难泄漏到输出。

物理来源：输入差分对两个管子不可能完全对称，电源电压变化会不对称地改变它们的工作点，于是共模/电源变化被"误读"成差模信号。

![把两个输入端短接到同一个共模电压 Vcm，理想运放输出应保持不变](../assets/schematics/cmrr-psrr.svg)

## 2. 典型数量级

| 指标 | 通用运放 | 精密运放 | 说明 |
|---|---|---|---|
| CMRR（直流） | 70~90 dB | 110~140 dB | 80 dB 表示共模被衰减到差模的 1/10000 |
| CMRR（1kHz） | 下降到 60~80 dB | 90~110 dB | 随频率升高明显恶化 |
| PSRR（直流） | 80~100 dB | 100~130 dB | 对 +Vs/−Vs 分别给出 |
| PSRR（10kHz） | 降到 50~70 dB | 80~100 dB | 高频电源纹波抑制变差 |

关键直觉：**CMRR 和 PSRR 都随频率升高而快速下降**。直流时 120dB 很惊人，到 10kHz 可能只剩 80dB，到 MHz 级甚至不到 60dB。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["CMRR", "PSRR"], "bottom": 0, "textStyle": {"fontSize": 12}},
  "grid": {"left": 56, "right": 24, "top": 26, "bottom": 58},
  "xAxis": {"type": "category", "name": "频率 Hz（对数示意）", "data": ["1","10","100","1k","10k","100k","1M"], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "dB", "min": 40, "max": 130, "interval": 15, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "CMRR", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#1a4f8b"},
     "data": [120,118,112,95,78,62,50]},
    {"name": "PSRR", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.4, "color": "#b5642e"},
     "data": [115,112,105,88,72,58,46]}
  ]
}
```

## 3. 在电路中的后果与测量

- **测量 CMRR**：两输入端短接，加一个已知直流共模电压（比如从 0V 扫到 4V），测输出变化，除以闭环增益得到等效输入失调变化，再与共模变化量之比即为 CMRR。
- **后果**：在 [差分放大器](differential-amplifier.md) 和 [仪表放大器](instrumentation-amplifier.md) 里，我们希望只放大差分信号、抑制两根线上的共模干扰（如 50Hz 工频）。CMRR 不够时，共模干扰会按 $1/CMRR$ 的比例混进输出。
- **PSRR 后果**：电源上的开关纹波（如 DC-DC 的几百 kHz）因为 PSRR 在高频已经很差，会直接泄漏到模拟输出，污染 ADC 采样。

## 4. 计算示例

::: example 共模工频干扰有多少变成误差
1. **场景**：差分放大器拾取两根线上的 50Hz 共模工频干扰 $V_{cm}=1\text{V}$。
2. **查 CMRR**：该运放在 50Hz 时 CMRR = 80dB。
3. **换算**：$80\text{dB} = 10^{80/20}=10000$，即共模被衰减 10000 倍。
4. **等效输入误差**：$V_{cm}/CMRR = 1\text{V}/10000 = 100\,\mu\text{V}$。
5. **结论**：1V 的工频共模最终只表现为 100µV 的输入等效误差。若电路分辨率是 1mV，这就是 10% 的误差；选 CMRR=120dB 的精密运放，误差降到 1µV。
:::

::: advanced 进阶：CMRR、电阻匹配与差分电路
注意区分两个层面的"共模抑制"：运放自身的 CMRR，和外部分立四电阻差分网络的电阻匹配。后者常常才是瓶颈——即使运放 CMRR=120dB，四个电阻差 0.1%，整个电路的 CMRR 也可能被压到 60dB 左右。详见 [差分放大器与电阻匹配](differential-amplifier.md) 的定量推导。
:::

## 扩展与变种电路

### 扩展1：远距传感器共模抑制 Remote-Sensor CMR

传感器在现场、电路在控制室，两根长线上既传差分信号，又拾取同样的 50Hz 共模干扰；用屏蔽双绞 + 差分前端把共模压住。

![远距双绞传感器线拾取共模 Vcm，进差分放大；外层屏蔽单端接地](../assets/schematics/cmrr-psrr-remote-cmr.svg)

::: example 工作原理与静态分析
- 两根传输线对地点电压分别为 $V_{cm}\pm V_d/2$，差分前端只取差值：$V_{out}=G(V_{+}-V_{-})$。
- 共模部分按 $1/CMRR$ 折算到输入，等效输入误差 $V_{e}=V_{cm}/CMRR$。
- 关键：线对绞合减小环路面积，屏蔽层单端接地切断地环路；前端用高 CMRR 差分/仪表放大器。
- 匹配电阻 R1=R2、Rf=Rg 时，电路 CMRR 由电阻精度与运放 CMRR 共同决定（见 [差分放大器](differential-amplifier.md)）。
:::

取值数量级：R1/Rf 取 10kΩ 量级；与单端放大对比：多走一根线、需要差分前端，但能把几伏的工频共模压到 µV 级。适用：远传热电偶、桥式传感器、工业 4~20mA；不适用：极短连线、共模本就很小的板内信号。

::: pitfall 屏蔽层两端接地反而引入工频
- **现象**：加了屏蔽线后 50Hz 干扰反而变大。
- **原因**：屏蔽层两端接机壳地，两地电位差驱动工频环流，屏蔽层成了拾取天线。
- **解决**：屏蔽层在接收端单端接地；现场侧屏蔽悬空或经小电容接机壳，避免地环路。
:::

## 5. 常见坑

::: pitfall 常见坑
- **只看直流 CMRR 选型**：数据手册首页写 CMRR=120dB，实际电路工作在几十 kHz，CMRR 已掉到 70dB。要看 CMRR-频率曲线，按工作频段取值。
- **忽略 PSRR 直接用开关电源供电**：开关电源纹波几十 mV、频率几百 kHz，PSRR 在该频率很差，纹波几乎原样进输出。模拟前级供电应加 LC/π 型滤波或用 LDO。
- **共模电压超出范围**：即使 CMRR 很高，输入共模电压一旦超出规定范围（普通运放共模到不了负轨），电路会失真甚至输出锁死。RRO 输入运放可解决，见 [供电轨与输出摆幅](supply-rails.md)。
:::

## 6. 自测题

<details><summary>CMRR = 100dB 时，1V 的共模干扰等效为多大输入误差？</summary>

$100\text{dB}=10^{5}=100000$，等效误差 $=1\text{V}/10^5 =$ **10µV**。

</details>

<details><summary>为什么同一块运放，直流时 CMRR 很高，处理音频（20kHz）时共模抑制却变差？</summary>

CMRR 随频率升高而下降：差分对内部的寄生电容、补偿网络在高频引入相移和不对称，共模到差模的泄漏增大。数据手册的 CMRR-频率曲线才是高频设计依据。

</details>

## 7. 参考资料

- MT-035 Op Amp Inputs, Outputs, Single-Supply & Rail-to-Rail Issues（ADI）
- A Deeper Look into Difference Amplifiers（ADI Analog Dialogue, Harry Holt）
