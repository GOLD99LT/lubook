<script setup lang="ts">
// 首页学习面板：整体进度、我的收藏、JSON 导出/导入。
// 持久化失败时不显示成功提示：依据仓储 saveState 给出失败横幅、重试与导出兜底（ADR-0007 §5）。
import { computed, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'
import { useLearning } from './store'

const learning = useLearning()
const s = computed(() => learning.stats())
const saveState = computed(() => learning.saveState)
// 静态构建期没有 localStorage，仓储会如实标记不可持久化；但那份状态不属于用户浏览器。
// 等 mounted 后再展示，避免 SSG 产物把"仅本次会话"写进 HTML 并与客户端水合结果冲突。
const mounted = ref(false)
onMounted(() => {
  mounted.value = true
})
const persistFailed = computed(() => mounted.value && !saveState.value.ok)
// persistent=false：内存降级，读写仍可用，但必须显示"仅本次会话有效"（ADR-0007 §5 补充）。
const persistUnavailable = computed(() => mounted.value && !saveState.value.persistent)

// catalog 里的 link 是站点根相对路径（如 /basics/foo），不含部署 base。
// 部署在 /lubook/hardware/ 这类子路径下时必须过 withBase，否则点收藏会 404/回首页。
const favList = computed(() =>
  learning.favorites().map((f) => ({ path: f.id, title: f.title, link: withBase(f.link) }))
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
// 先读入文件文本但不立即导入：merge/replace 的语义差异很大，必须让用户明确选择；
// replace 还会二次确认，避免默认整体覆盖造成不可撤销的数据丢失。
const importText = ref('')
const importName = ref('')

function onImportClick() {
  fileInput.value?.click()
}
function onFileChange(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (!f) return
  const reader = new FileReader()
  reader.onload = () => {
    importText.value = String(reader.result || '')
    importName.value = f.name
  }
  reader.readAsText(f)
  ;(e.target as HTMLInputElement).value = ''
}

function runImport(mode: 'merge' | 'replace') {
  if (!importText.value) return
  if (mode === 'replace' && !window.confirm('将覆盖当前全部学习数据且不可撤销。确定继续？')) return
  const text = importText.value
  importText.value = ''
  importName.value = ''
  const r = learning.importJSON(text, mode)
  // 导入失败（校验不通过或持久化未成功）时按错误提示，不显示成功 toast。
  showToast(r.message, !r.ok)
}

function cancelImport() {
  importText.value = ''
  importName.value = ''
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

    <div v-if="importText" class="hh-hp-import-choice">
      <span class="hh-hp-import-name">已选择「{{ importName }}」，请选择导入方式：</span>
      <button type="button" @click="runImport('merge')">合并导入（保留现有数据）</button>
      <button type="button" @click="runImport('replace')">覆盖导入（清空现有数据）</button>
      <button type="button" class="is-plain" @click="cancelImport">取消</button>
    </div>

    <div v-if="persistFailed" class="hh-hp-unsaved">
      <span v-if="persistUnavailable" class="hh-hp-unsaved-msg">
        仅本次会话有效：浏览器存储不可用，学习数据刷新后会丢失，可先导出备份。
      </span>
      <span v-else class="hh-hp-unsaved-msg">
        本地保存失败（{{ saveState.error || '存储不可用' }}），当前会话内数据仍保留。
      </span>
      <button v-if="!persistUnavailable" type="button" @click="retrySave">重试保存</button>
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

    <div class="hh-hp-tip" v-if="!persistUnavailable">数据仅保存在你当前浏览器（localStorage），换设备请先「导出数据」再到新设备「导入数据」。</div>
    <div class="hh-hp-tip" v-else>浏览器未提供可用的本地存储，本次会话的数据不会跨刷新保留，请及时「导出数据」。</div>
    <div class="hh-hp-toast" :class="{ 'is-error': toastError }" v-if="toast">{{ toast }}</div>
  </div>
</template>
