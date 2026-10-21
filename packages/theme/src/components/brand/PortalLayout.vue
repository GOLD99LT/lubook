<script setup>
import DefaultTheme from 'vitepress/theme'
import BrandMark from './BrandMark.vue'
</script>

<template>
  <DefaultTheme.Layout>
    <!-- 导航栏：路书品牌标识 + 站点标题（无侧边栏：门户无章节目录） -->
    <template #nav-bar-title-before>
      <BrandMark class="nav-brand" :width="28" :height="28" />
    </template>
  </DefaultTheme.Layout>
</template>

<style>
.nav-brand {
  flex: none;
  margin-right: 6px;
}
</style>
