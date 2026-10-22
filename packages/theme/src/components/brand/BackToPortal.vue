<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'
import BrandMark from './BrandMark.vue'

// 分册 base = VP_BASE + '<slug>/'；门户在 VP_BASE。剥掉末尾的 '<slug>/' 即门户。
const { site } = useData()
const portalHref = computed(() => site.value.base.replace(/[^/]+\/$/, ''))
</script>

<template>
  <!--
    跨 app 边界（分册→门户）：VitePress 客户端路由的 click 拦截在 window 捕获阶段，
    其路由清单解释不了门户路径。target="_self" 让路由拦截跳过（命中 hasAttribute('target')），
    浏览器按同标签页整页加载回门户。
  -->
  <a
    class="back-to-portal"
    :href="portalHref"
    target="_self"
    title="返回路书门户"
  >
    <BrandMark :width="20" :height="20" />
    <span class="bp-text">路书</span>
  </a>
</template>

<style scoped>
.back-to-portal {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  margin-right: 14px;
  padding: 4px 10px 4px 6px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 20px;
  color: var(--vp-c-text-2);
  text-decoration: none;
  font-size: 13px;
  letter-spacing: 1px;
  transition: color 0.2s, border-color 0.2s;
}
.back-to-portal:hover {
  color: var(--brand, #b5642e);
  border-color: var(--brand, #b5642e);
}
.bp-text {
  line-height: 1;
}
</style>
