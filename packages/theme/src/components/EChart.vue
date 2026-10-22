<script setup lang="ts">
// ECharts 按需加载：ECharts 全量约 1MB（gzip ~370KB），而门户与多数章节根本不用图表。
// 历史上它被静态 import 进来，等于每个页面首屏都要下载一个图表库。
// 这里改为首次真正需要绘制时才动态 import —— 静态产物里 ECharts 会独立成 chunk，
// 只有含 ```echarts 围栏的页面才会拉取，门户与纯文字章节不受影响。
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useData } from 'vitepress'

type EChartsModule = typeof import('echarts')

const props = defineProps<{ option: Record<string, any> }>()

const el = ref<HTMLDivElement | null>(null)
let chart: import('echarts').ECharts | null = null
let echartsMod: EChartsModule | null = null
let unmounted = false
const { isDark } = useData()

async function loadECharts(): Promise<EChartsModule> {
  if (!echartsMod) echartsMod = await import('echarts')
  return echartsMod
}

async function render() {
  if (unmounted || !el.value) return
  try {
    const echarts = await loadECharts()
    // 动态 import 是异步的：期间组件可能已卸载或 DOM 已换，必须重新校验
    if (unmounted || !el.value) return
    if (chart) {
      chart.dispose()
      chart = null
    }
    chart = echarts.init(el.value, isDark.value ? 'dark' : undefined)
    chart.setOption(props.option)
  } catch (e) {
    // 图表渲染（或加载）失败不应拖垮整页；错误上抛控制台便于排查
    console.error('[EChart] render failed', e)
  }
}

function resize() {
  chart?.resize()
}

onMounted(() => {
  render()
  window.addEventListener('resize', resize)
})

onBeforeUnmount(() => {
  unmounted = true
  window.removeEventListener('resize', resize)
  chart?.dispose()
  chart = null
})

// 深浅色切换后重绘
watch(isDark, () => render())
</script>

<template>
  <div ref="el" class="hh-chart"></div>
</template>

<style scoped>
.hh-chart {
  width: 100%;
  height: 360px;
  margin: 4px 0;
}
@media (max-width: 768px) {
  .hh-chart {
    height: 300px;
  }
}
</style>
