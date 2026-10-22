<script setup lang="ts">
// 章末学习工具：已学/在学切换、收藏、我的笔记（按章自动保存到 localStorage）。
// 仅在内容页渲染（首页 index.md 不渲染）。
// 持久化失败时不提示"已保存"：依据仓储 saveState 显示"未保存"，提供重试与导出兜底（ADR-0007 §5）。
import { computed, ref, watch } from 'vue'
import { useData } from 'vitepress'
import { useLearning } from './store'

const { page } = useData()
const learning = useLearning()

const currentPath = computed(() => page.value.relativePath)
const isHome = computed(() => currentPath.value === 'index.md' || page.value.frontmatter?.layout === 'home')

const status = computed(() => learning.getStatus(currentPath.value))
const fav = computed(() => learning.isFavorite(currentPath.value))
const note = ref(learning.getNote(currentPath.value))
const savedHint = ref('')
const persistFailed = computed(() => !learning.saveState.ok)

// SPA 切章时刷新笔记内容
watch(currentPath, (p) => {
  note.value = learning.getNote(p)
  savedHint.value = ''
})

let saveTimer: any = null
function flashSaved() {
  savedHint.value = '已保存'
  clearTimeout(saveTimer)
  saveTimer = setTimeout(() => (savedHint.value = ''), 1200)
}

function setStatus(s: 'done' | 'learning') {
  // 再点同一状态 -> 取消（回到未学）；返回值决定是否需要提示未保存。
  learning.setStatus(currentPath.value, status.value === s ? null : s)
}
function toggleFav() {
  learning.toggleFavorite(currentPath.value)
}

function onNoteInput() {
  const r = learning.setNote(currentPath.value, note.value)
  if (r.ok) {
    flashSaved()
  } else {
    // 写入失败：内存状态仍保留，提示未保存，不自动消失（等待重试或导出兜底）。
    savedHint.value = '未保存'
    clearTimeout(saveTimer)
  }
}

function retrySave() {
  const r = learning.retrySave()
  if (r.ok) flashSaved()
  else savedHint.value = '未保存'
}

// 启动期数据损坏时的唯一出口：明确告知会丢弃本地数据，用户确认后才重置。
function resetLocal() {
  if (!window.confirm('将删除本浏览器中无法解析的学习数据（进度/收藏/笔记），且不可恢复。建议先"立即导出备份"。确定继续？')) return
  const r = learning.resetLocalData()
  savedHint.value = r.ok ? '已重置' : '未保存'
}

// 本地写不进去时的兜底：把当前会话内存数据导出成文件。
function exportBackup() {
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
}
</script>

<template>
  <div v-if="!isHome" class="hh-learning-chapter">
    <div class="hh-learning-status" :class="{ 'is-unsaved': persistFailed }">
      <button
        type="button"
        class="hh-ls-btn"
        :class="{ active: status === 'learning' }"
        :aria-pressed="status === 'learning' ? 'true' : 'false'"
        @click="setStatus('learning')"
      >在学</button>
      <button
        type="button"
        class="hh-ls-btn"
        :class="{ active: status === 'done' }"
        :aria-pressed="status === 'done' ? 'true' : 'false'"
        @click="setStatus('done')"
      >已学</button>
      <button
        type="button"
        class="hh-ls-btn hh-ls-fav"
        :class="{ active: fav }"
        :aria-pressed="fav ? 'true' : 'false'"
        @click="toggleFav"
      >
      <svg class="hh-ls-star" viewBox="0 0 24 24" :fill="fav ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.5 9.7l5.9-.9L12 3.5z"/></svg>
      {{ fav ? '已收藏' : '收藏本章' }}</button>
    </div>

    <div v-if="persistFailed" class="hh-ls-unsaved" role="status" aria-live="polite">
      <span class="hh-ls-unsaved-msg">
        本地保存失败（{{ learning.saveState.error || '存储不可用' }}），当前会话内数据仍保留。
      </span>
      <button v-if="!learning.saveState.bootFailed" type="button" class="hh-ls-unsaved-btn" @click="retrySave">重试保存</button>
      <button type="button" class="hh-ls-unsaved-btn" @click="exportBackup">立即导出备份</button>
      <button v-if="learning.saveState.bootFailed" type="button" class="hh-ls-unsaved-btn" @click="resetLocal">
        丢弃本地数据并重新开始
      </button>
    </div>

    <div class="hh-learning-notes">
      <div class="hh-ln-head">
        <label class="hh-ln-title" for="hh-note-input">我的笔记</label>
        <span class="hh-ln-hint" :class="{ 'is-error': savedHint === '未保存' }" role="status" aria-live="polite">{{ savedHint || '自动保存到本地浏览器' }}</span>
      </div>
      <textarea
        id="hh-note-input"
        v-model="note"
        rows="5"
        placeholder="按本章记录要点、坑、待办…（仅保存在你当前浏览器）"
        @input="onNoteInput"
      ></textarea>
    </div>
  </div>
</template>
