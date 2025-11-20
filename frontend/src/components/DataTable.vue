<template>
  <div class="table-container">
    <h3 v-if="title" class="table-title">{{ title }}</h3>
    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key">
              {{ column.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in displayData" :key="index">
            <td v-for="column in columns" :key="column.key">
              {{ formatCell(row[column.key], column.format) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="data.length > limit" class="table-footer">
      Mostrando {{ limit }} de {{ data.length }} registros
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  data: {
    type: Array,
    default: () => []
  },
  columns: {
    type: Array,
    required: true
  },
  limit: {
    type: Number,
    default: 10
  }
})

const displayData = computed(() => {
  return props.data.slice(0, props.limit)
})

function formatCell(value, format) {
  if (value === null || value === undefined) return 'N/A'

  switch (format) {
    case 'number':
      return Number(value).toLocaleString('es-ES')
    case 'percent':
      return `${Number(value).toFixed(1)}%`
    case 'decimal':
      return Number(value).toFixed(2)
    default:
      return value
  }
}
</script>

<style scoped>
.table-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.table-title {
  margin: 0 0 1rem;
  font-size: 1.3rem;
  color: #333;
  font-weight: 600;
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.data-table td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid #f0f0f0;
  color: #555;
}

.data-table tbody tr:hover {
  background: #f8f9fa;
}

.table-footer {
  margin-top: 1rem;
  text-align: center;
  color: #999;
  font-size: 0.9rem;
}
</style>
