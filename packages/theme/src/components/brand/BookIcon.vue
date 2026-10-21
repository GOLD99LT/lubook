<template>
  <svg
    class="book-icon"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <!-- 硬件：电路板 -->
    <template v-if="name === 'hardware'">
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <path d="M9 4v3M15 4v3M9 17v3M15 17v3M4 9h3M4 15h3M17 9h3M17 15h3" />
      <rect x="9.5" y="9.5" width="5" height="5" rx="1" />
    </template>
    <!-- 嵌入式 MCU：芯片 -->
    <template v-else-if="name === 'embedded'">
      <rect x="7" y="7" width="10" height="10" rx="1.5" />
      <path d="M10 1v3M14 1v3M10 20v3M14 20v3M1 10h3M1 14h3M20 10h3M20 14h3" />
      <path d="M10.5 12h3M12 10.5v3" />
    </template>
    <!-- 嵌入式 Linux：终端窗口 -->
    <template v-else-if="name === 'linux'">
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <path d="M3 8.5h18" />
      <path d="M7 12l3 2.5L7 17" />
      <path d="M12.5 17H16" />
    </template>
    <!-- 外部：外链箭头 -->
    <template v-else>
      <path d="M14 4h6v6" />
      <path d="M20 4l-9 9" />
      <path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" />
    </template>
  </svg>
</template>

<script setup>
defineProps({
  name: { type: String, default: 'external' },
  size: { type: [Number, String], default: 26 }
})
</script>

<style scoped>
.book-icon {
  color: currentColor;
}
.book-icon :is(rect, path, line, circle) {
  stroke: currentColor;
  stroke-width: 1.7;
  stroke-linecap: round;
  stroke-linejoin: round;
}
</style>
