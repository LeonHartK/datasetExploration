<template>
  <div class="kpi-card">
    <div class="kpi-icon" :style="{ background: iconColor }">
      {{ icon }}
    </div>
    <div class="kpi-content">
      <h3 class="kpi-title">{{ title }}</h3>
      <p class="kpi-value">{{ formattedValue }}</p>
      <p v-if="subtitle" class="kpi-subtitle">{{ subtitle }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  value: [String, Number],
  subtitle: String,
  icon: {
    type: String,
    default: '📊'
  },
  iconColor: {
    type: String,
    default: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  format: {
    type: String,
    default: 'number' // 'number', 'percent', 'currency', 'none'
  }
})

const formattedValue = computed(() => {
  if (props.value === null || props.value === undefined) return 'N/A'

  switch (props.format) {
    case 'number':
      return Number(props.value).toLocaleString('es-ES')
    case 'percent':
      return `${Number(props.value).toFixed(1)}%`
    case 'currency':
      return `$${Number(props.value).toLocaleString('es-ES')}`
    case 'decimal':
      return Number(props.value).toFixed(2)
    default:
      return props.value
  }
})
</script>

<style scoped>
.kpi-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.kpi-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.kpi-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  flex-shrink: 0;
}

.kpi-content {
  flex: 1;
}

.kpi-title {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.kpi-value {
  margin: 0.5rem 0 0;
  font-size: 2rem;
  color: #333;
  font-weight: 700;
  line-height: 1;
}

.kpi-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #999;
}
</style>
