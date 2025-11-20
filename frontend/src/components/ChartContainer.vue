<template>
  <div class="chart-container">
    <h3 v-if="title" class="chart-title">{{ title }}</h3>
    <div class="chart-wrapper">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String
})
</script>

<style scoped>
.chart-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.chart-title {
  margin: 0 0 1.5rem;
  font-size: 1.3rem;
  color: #333;
  font-weight: 600;
}

.chart-wrapper {
  position: relative;
  min-height: 300px;
}
</style>
