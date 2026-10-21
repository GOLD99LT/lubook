<script setup>
import { withBase } from 'vitepress'
import BrandMark from './BrandMark.vue'
import BookIcon from './BookIcon.vue'

const props = defineProps({
  cards: { type: Array, required: true },
  tagline: { type: String, default: '路先生知识手册' },
  intro: { type: String, default: '' }
})

function href(card) {
  if (card.type === 'external') return card.url
  return withBase((card.slug || '') + '/')
}
</script>

<template>
  <div class="portal-home">
    <header class="hero">
      <BrandMark :width="76" :height="76" />
      <h1 class="wordmark">路书</h1>
      <p class="tagline">{{ tagline }}</p>
      <p v-if="intro" class="intro">{{ intro }}</p>
    </header>

    <nav class="cards" aria-label="手册分册">
      <template v-for="card in cards" :key="card.title">
        <!-- 可进入：内部 / 外部 -->
        <a
          v-if="card.available !== false"
          class="card"
          :href="href(card)"
          :target="card.type === 'external' ? '_blank' : undefined"
          :rel="card.type === 'external' ? 'noopener' : undefined"
        >
          <span class="card-icon"><BookIcon :name="card.icon" /></span>
          <span class="card-body">
            <span class="card-title">{{ card.title }}</span>
            <span class="card-desc">{{ card.desc }}</span>
          </span>
          <span class="card-arrow">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="1.8"
                stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </span>
        </a>
        <!-- 占位：即将上线（非链接，不做僵尸按钮） -->
        <div v-else class="card is-pending" aria-disabled="true">
          <span class="card-icon"><BookIcon :name="card.icon" /></span>
          <span class="card-body">
            <span class="card-title">{{ card.title }}</span>
            <span class="card-desc">{{ card.desc }}</span>
          </span>
          <span class="soon">即将上线</span>
        </div>
      </template>
    </nav>
  </div>
</template>

<style scoped>
.portal-home {
  max-width: 920px;
  margin: 0 auto;
  padding: 64px 24px 80px;
}

/* ---- Hero ---- */
.hero {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.wordmark {
  margin: 18px 0 10px;
  line-height: 1.15;
  font-size: 46px;
  font-weight: 800;
  letter-spacing: 6px;
  color: var(--vp-c-text-1);
}
.tagline {
  margin: 0;
  line-height: 1.6;
  font-size: 16px;
  letter-spacing: 2px;
  color: var(--vp-c-text-2);
}
.intro {
  margin: 16px 0 0;
  font-size: 14px;
  color: var(--vp-c-text-3);
  max-width: 560px;
}

/* ---- Cards ---- */
.cards {
  margin-top: 52px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
.card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 20px 18px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  text-decoration: none;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}
.card:not(.is-pending):hover {
  border-color: var(--brand, #b5642e);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}
.card-icon {
  flex: none;
  display: flex;
  color: var(--brand, #b5642e);
}
.card-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}
.card-title {
  font-size: 16px;
  font-weight: 700;
}
.card-desc {
  font-size: 13px;
  line-height: 1.6;
  color: var(--vp-c-text-2);
}
.card-arrow {
  margin-left: auto;
  flex: none;
  color: var(--vp-c-text-3);
  align-self: center;
}
.card:not(.is-pending):hover .card-arrow {
  color: var(--brand, #b5642e);
}

/* pending 占位 */
.card.is-pending {
  opacity: 0.62;
}
.soon {
  margin-left: auto;
  flex: none;
  align-self: center;
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--vp-c-text-3);
  border: 1px solid var(--vp-c-divider);
  border-radius: 20px;
  padding: 3px 10px;
  white-space: nowrap;
}

/* 响应式：避免 2+1 孤儿行——宽屏 3 列，窄屏直接 1 列 */
@media (max-width: 760px) {
  .cards {
    grid-template-columns: 1fr;
  }
  .portal-home {
    padding: 40px 18px 60px;
  }
}
</style>
