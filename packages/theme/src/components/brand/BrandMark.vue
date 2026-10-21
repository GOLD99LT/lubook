<template>
  <svg
    class="brand-mark"
    :width="width"
    :height="height"
    viewBox="0 0 64 64"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    :aria-label="label"
  >
    <!-- 外框：圆角方形（"书"的容器） -->
    <rect class="frame" x="7" y="7" width="50" height="50" rx="14" />
    <!-- 路径："路"——从左下出发，转折向上，终点为圆点（行程/路线） -->
    <path
      class="route"
      d="M20 44 L20 35 Q20 28 27 28 L36 28 Q43 28 43 21"
    />
    <!-- 起点：空心圆 -->
    <circle class="start" cx="20" cy="44" r="3.4" />
    <!-- 终点：实心圆点 -->
    <circle class="end" cx="43" cy="21" r="3.6" />
  </svg>
</template>

<script setup>
defineProps({
  width: { type: [Number, String], default: 48 },
  height: { type: [Number, String], default: 48 },
  label: { type: String, default: '路书' }
})
</script>

<style scoped>
.brand-mark {
  color: var(--brand, #b5642e);
}
.frame {
  stroke: currentColor;
  stroke-width: 2.6;
}
.route {
  stroke: currentColor;
  stroke-width: 2.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.start {
  stroke: currentColor;
  stroke-width: 2.4;
  fill: none;
}
.end {
  fill: currentColor;
}
</style>
