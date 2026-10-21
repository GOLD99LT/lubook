---
id: power-monitoring-loadswitch
title: 电源监控、POR 与负载开关 Supervisors, POR & Load Switches
part: 6
chapter: 电池与电源管理
order: 50
tags: [电源监控, 复位IC, POR, 负载开关, 热插拔, 浪涌电流]
difficulty: 2
status: published
sources:
  - TI Power Management IC Selection Guides
  - Analog Devices (Maxim) Supervisor & Load Switch Design Notes
---

# 电源监控、POR 与负载开关 Supervisors, POR & Load Switches

电源本身稳了还不够。系统还需要：**监测电源是否正常**（电压掉了要复位 MCU）、**上电时延时**（等电源稳定再让 MCU 跑程序）、**受控地给各负载上电**（避免浪涌）。这一章讲这三类"电源周边"电路。

## 1. 设计动机

::: motivation 为什么需要这些周边电路
MCU 对供电有要求：电压掉到一定程度，CPU 内部逻辑就可能跑飞、把 Flash 写坏。如果电源刚上电还没稳定 MCU 就开始执行程序，会跑飞、卡死、误动作。

而且各路电源（内核 1.2V、IO 3.3V、外设 5V）需要按顺序上下电，直接同时给大电容负载上电，瞬间浪涌电流会把电源拉垮。**电源监控 IC（Supervisor）、上电复位 POR、负载开关（Load Switch）**就是解决这些问题的小电路。
:::

## 2. 原理图

一个完整的电源周边：负载开关受控给负载供电，监控 IC 检测电压、输出复位信号给 MCU。

![负载开关 + 监控复位 IC：EN 控制上电、检测 VOUT、输出 RESET](../assets/schematics/power-monitoring-loadswitch.svg)

## 3. 静态分析（DC）

- **监控 IC（如 MAX809/RT9818）**：内部带精密基准和比较器，监测某一路电压。电压正常时 RESET# 为高；电压跌到门槛 $V_{TH}$ 以下时拉低 RESET#。
- **门槛设置**：3.3V 系统常选 3.08V 门槛（跌约 6.6%），带迟滞 $\Delta V\approx 0.05V_{TH}$ 防抖动。
- **复位延时**：IC 内部或外部电容设定释放复位的超时时间 $t_{RP}$，典型 100ms。
- **负载开关**：一只高侧 MOSFET，EN 控制导通；导通时压降 $V_{drop}=I_{load}R_{ds(on)}$，功耗 $P=I^2R_{ds(on)}$。

## 4. 动态分析（AC / 瞬态）

电源电压跌落→复位的过程：电压越过门槛→内部延迟→RESET# 拉低；电压恢复→越过门槛+迟滞→再延时 $t_{RP}$→RESET# 释放。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["VCC (V)", "RESET#"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 56, "right": 60, "top": 26, "bottom": 56},
  "xAxis": {"type": "category", "name": "时间 ms", "data": ["0","20","40","60","80","100","120","140","160"], "axisLabel": {"fontSize": 11}},
  "yAxis": [
    {"type": "value", "name": "V", "min": 0, "max": 3.6, "axisLabel": {"fontSize": 11}},
    {"type": "value", "name": "RESET", "min": -0.2, "max": 3.6, "axisLabel": {"fontSize": 11}}
  ],
  "series": [
    {"name": "VCC (V)", "type": "line", "smooth": true, "showSymbol": false, "lineStyle": {"width": 2.6, "color": "#1a4f8b"},
     "data": [0,1.5,2.8,3.3,3.3,3.3,3.3,3.3,3.3]},
    {"name": "RESET#", "type": "line", "step": "end", "showSymbol": false, "yAxisIndex": 1, "lineStyle": {"width": 2.2, "color": "#b5642e"},
     "data": [0,0,0,0,0,0,3.3,3.3,3.3]}
  ]
}
```

VCC 上电上升，RESET# 保持低直到 VCC 稳定后约延时 100ms 才释放为高。

## 5. 环路分析

监控电路本身是个带迟滞的比较器，不是闭环；关键参数是门槛精度（±1%~2%）和复位延时。负载开关是开环受控开关，重点在**导通斜率 dV/dt**——它决定浪涌电流 $I_{inrush}=C_{load}\dfrac{dV}{dt}$。

::: advanced 进阶：POR 时间常数与负载开关浪涌
**RC 上电复位**：VCC 经 R 给 C 充电，节点电压 $V(t)=V_{CC}(1-e^{-t/RC})$，升到施密特门槛的时间近似 $t\approx RC\cdot\ln\dfrac{V_{CC}}{V_{CC}-V_{TH}}$。取 R=100kΩ、C=1µF，$\tau=RC=100\text{ms}$，留出足够上电等待。

**负载开关浪涌**：开通斜率由栅极电容/外部 dVdt 电容设定。若直接硬开关，输出电容 $C_{load}=100\mu\text{F}$ 瞬间接到电源，浪涌电流可达数安培，可能触发电源限流。dV/dt 限制在例如 1ms 内升到 3.3V，则 $I_{inrush}=C_{load}\Delta V/\Delta t=100\mu\text{F}\times3.3\text{V}/1\text{ms}=0.33\text{A}$，可接受。
:::

## 6. 元件取值与工程权衡

- **监控门槛**：选比标称低 5%~10% 的门槛，既不误触发、又在 MCU 失控前复位。
- **复位延时电容**：RC 取值保证电源稳定（一般 50~200ms）即可，过长拖慢启动。
- **负载开关 $R_{ds(on)}$**：大电流选低导通电阻降功耗，但芯片体积/成本上升；dVdt 电容大则浪涌小但上电慢。
- **手动复位**：接按键到 RESET# 脚，加去抖。

## 7. 完整设计示例

::: example 3.3V 系统的监控与上电
1. **需求**：3.3V MCU 系统，电压跌过低要复位，上电延时 100ms 再跑。
2. **监控 IC**：选门槛 3.08V 的复位 IC，接 3.3V。
3. **RC POR**：R=100kΩ、C=1µF，τ=100ms。
4. **负载开关**：外设 500mA，选 $R_{ds(on)}<100\text{m}\Omega$ 的负载开关，dVdt 电容设 1ms 软启动。
5. **验证**：示波器看 VCC 上升后 RESET# 延迟约 100ms 释放；拉低 VCC 到 3.0V 以下 RESET# 应立即拉低。
:::

## 8. 仿真与实验

用可调电源缓慢上升/下降给监控 IC 供电，示波器同时测 VCC 与 RESET#：确认门槛电压、迟滞宽度、复位延时。负载开关测试：电子负载模拟大电容负载，测开通时输入电流峰值是否被 dV/dt 限制在设计值内。

## 扩展与变种电路

### 扩展1：RC 上电复位 POR

最省钱的 POR：一只电阻一只电容加施密特反相器。

![VCC 经 R 给 C 充电，节点过施密特门槛后释放 RESET#](../assets/schematics/power-monitoring-loadswitch-por-rc.svg)

::: example 工作原理
- 上电时 C 上电压从 0 指数上升，$V(t)=V_{CC}(1-e^{-t/RC})$。
- 越过施密特门槛后 RESET# 释放，延时约 RC 保证电源稳定。
- 优点零成本；缺点门槛不精确、抗扰差。
:::

取值对比：RC POR 几毛钱但门槛随温度飘；专用监控 IC 门槛 ±1% 精确。适用：低成本、电源干净；不适用：门槛要求准的工业/医疗。

::: pitfall RC POR 的 R 太大拾取噪声误复位
- **现象**：系统偶发莫名复位。
- **原因**：高阻节点拾取噪声，电容电压被扰动越过门槛。
- **解决**：R 不宜过大（百 kΩ 内），或直接用带迟滞的监控 IC。
:::

### 扩展2：热插拔/理想二极管 Hot-swap

板卡带电插入背板时，用受控 MOSFET 软启动限制浪涌，并防电流倒灌。

![背板经 Rsns + 受控 N-MOS 接板载负载，控制器检测电流缓开](../assets/schematics/power-monitoring-loadswitch-hotswap.svg)

::: example 工作原理
- 插入瞬间栅极缓慢开启，给输出电容预充电，浪涌电流受控。
- 控制器检测 Rsns 压降，过流快速关断保护背板。
- 理想二极管模式：MOSFET 正向导通、反向阻断，替代肖特基降损耗。
:::

取值对比：普通负载开关只管软启动；热插拔控制器还做过流短路保护。适用：背板/服务器板卡带电插拔；不适用：固定上电的普通产品。

::: pitfall 热插拔 MOS 选小了插入时炸管
- **现象**：插入瞬间 MOSFET 烧损。
- **原因**：MOSFET 未工作在安全区（SOA），浪涌能量超限。
- **解决**：选满足 SOA 的热插拔专用 MOS，栅极斜率按浪涌能量设计。
:::

## 9. 常见坑与故障现象

::: pitfall 常见坑
- **上电就跑飞/卡死**：没有 POR 或延时太短，电源未稳定 MCU 已取指。解决：加复位 IC，延时 ≥100ms。
- **电压微跌就误复位**：监控门槛选太高或无迟滞，电源正常纹波就触发复位。解决：门槛留 5%~10% 裕量、选带迟滞型号。
- **负载开关开通浪涌拉垮电源**：硬开通大电容负载，瞬间过流。解决：设 dV/dt 软启动。
- **RESET# 引脚悬空**：像天线拾取噪声，MCU 随机复位。解决：RESET# 用上拉电阻可靠拉高。
:::

## 10. 自测题

<details><summary>3.3V 系统选 3.08V 复位门槛，为什么不选 3.2V 那么灵敏？</summary>
要在 MCU 失控（通常 2.7~3.0V 以下才不正常）之前复位，但又要躲开正常的电源纹波和瞬态跌落。选 3.08V（跌约 6.6%）是在"早保护"与"不误触发"间折中。
</details>

<details><summary>RC POR 取 R=100kΩ、C=1µF，时间常数是多少？</summary>
$\tau=RC=100\text{k}\times1\mu=100\text{ms}$，上电后约 100ms 节点电压升到门槛、释放复位。
</details>

<details><summary>负载开关为什么要软启动（限制 dV/dt）？</summary>
输出端有大电容，硬开通瞬间 $I=C_{load}\,dV/dt$ 会产生数安培浪涌，可能触发电源限流或损坏开关。软启动把 dV/dt 压下来，浪涌电流受控。
</details>

<details><summary>RESET# 引脚悬空会怎样？</summary>
悬空引脚像天线拾取噪声，RESET# 随机抖动导致 MCU 莫名复位。必须用上拉电阻可靠拉高。
</details>

## 11. 参考资料

- TI Power Management IC Selection Guides（Supervisor / Load Switch）
- Analog Devices (Maxim) 复位 IC 与热插拔设计笔记
