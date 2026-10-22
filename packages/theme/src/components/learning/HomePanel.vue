<script setup lang="ts">
// 首页学习面板：整体进度、我的收藏、JSON 导出/导入。
// 持久化失败时不显示成功提示：依据仓储 saveState 给出失败横幅、重试与导出兜底（ADR-0007 §5）。
import { computed, ref } from 'vue'
import { useLearning } from './store'

const learning = useLearning()
const s = computed(() => learning.stats())
const saveState = computed(() => learning.saveState)
const persistFailed = computed(() => !saveState.value.ok)

const favList = computed(() =>
  learning.favorites().map((f) => ({ path: f.id, title: f.title, link: f.link }))
)

const toast = ref('')
const toastError = ref(false)
function showToast(msg: string, isError = false) {
  toast.value = msg
  toastError.value = isError
  setTimeout(() => (toast.value = ''), 2600)
}

function onExport() {
  const json = learning.exportJSON()
  let appId = 'book'
  try {
    appId = JSON.parse(json).appId || 'book'
  } catch {
    /* 用默认值 */
  }
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  const d = new Date()
  const stamp =
    `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`
  a.href = url
  a.download = `${appId}-learning-${stamp}.json`
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
  showToast('已导出 JSON 备份')
}

function retrySave() {
  const r = learning.retrySave()
  showToast(r.ok ? '重试保存成功' : `重试保存失败：${r.error ?? '存储不可用'}`, !r.ok)
}

const fileInput = ref<HTMLInputElement | null>(null)
function onImportClick() {
  fileInput.value?.click()
}
function onFileChange(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (!f) return
  const reader = new FileReader()
  reader.onload = () => {
    const r = learning.importJSON(String(reader.result || ''))
    // 导入失败（校验不通过或持久化未成功）时按错误提示，不显示成功 toast。
    showToast(r.message, !r.ok)
  }
  reader.readAsText(f)
  ;(e.target as HTMLInputElement).value = ''
}
</script>

<template>
  <div class="hh-home-panel">
    <div class="hh-hp-row">
      <div class="hh-hp-progress">
        <div class="hh-hp-pct">{{ s.pct }}%</div>
        <div class="hh-hp-bar"><div class="hh-hp-fill" :style="{ width: s.pct + '%' }"></div></div>
        <div class="hh-hp-count">已学 {{ s.done }} / {{ s.total }} 章 · 在学 {{ s.learning }} · 收藏 {{ s.favCount }}</div>
      </div>
      <div class="hh-hp-actions">
        <button type="button" @click="onExport">导出数据</button>
        <button type="button" @click="onImportClick">导入数据</button>
        <input
          ref="fileInput"
          type="file"
          accept="application/json,.json"
          style="display: none"
          @change="onFileChange"
        />
      </div>
    </div>

    <div v-if="persistFailed" class="hh-hp-unsaved">
      <span class="hh-hp-unsaved-msg">
        本地保存失败（{{ saveState.error || '存储不可用' }}），当前会话内数据仍保留。
      </span>
      <button type="button" @click="retrySave">重试保存</button>
      <button type="button" @click="onExport">立即导出备份</button>
    </div>

    <div class="hh-hp-favs" v-if="favList.length">
      <div class="hh-hp-favs-title">我的收藏（{{ favList.length }}）</div>
      <ul>
        <li v-for="f in favList" :key="f.path"><a :href="f.link">{{ f.title }}</a></li>
      </ul>
    </div>
    <div class="hh-hp-empty" v-else>
      暂无收藏 —— 打开任意章节，点「收藏本章」即可在此快速进入。
    </div>

    <div class="hh-hp-tip">数据仅保存在你当前浏览器（localStorage），换设备请先「导出数据」再到新设备「导入数据」。</div>
    <div class="hh-hp-toast" :class="{ 'is-error': toastError }" v-if="toast">{{ toast }}</div>
  </div>
</template>
