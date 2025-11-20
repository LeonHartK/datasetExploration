<template>
  <div class="temporal-analysis">
    <h2 class="page-title">Análisis Temporal</h2>

    <div v-if="loading" class="loading">Cargando análisis temporal...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else>
      <!-- Gráficas Dinámicas -->
      <ChartContainer title="Tendencia de Ventas Diarias">
        <LineChart v-if="dailyChartData" :data="dailyChartData" />
      </ChartContainer>

      <div class="charts-row">
        <ChartContainer title="Ventas Semanales">
          <BarChart v-if="weeklyChartData" :data="weeklyChartData" />
        </ChartContainer>

        <ChartContainer title="Ventas Mensuales">
          <BarChart v-if="monthlyChartData" :data="monthlyChartData" />
        </ChartContainer>
      </div>

      <ChartContainer title="Ventas por Día de la Semana">
        <BarChart v-if="dayOfWeekChartData" :data="dayOfWeekChartData" />
      </ChartContainer>

      <!-- Data Tables -->
      <DataTable
        v-if="data.ventas_diarias?.length"
        title="Ventas Diarias (Últimos 30 días)"
        :data="data.ventas_diarias.slice(0, 30)"
        :columns="dailyColumns"
        :limit="30"
      />

      <DataTable
        v-if="data.ventas_mensuales?.length"
        title="Ventas Mensuales"
        :data="data.ventas_mensuales"
        :columns="monthlyColumns"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ChartContainer from '@/components/ChartContainer.vue'
import DataTable from '@/components/DataTable.vue'
import LineChart from '@/components/LineChart.vue'
import BarChart from '@/components/BarChart.vue'
import api from '@/services/api'

const loading = ref(true)
const error = ref(null)
const data = ref({})

const dailyColumns = [
  { key: 'Fecha', label: 'Fecha' },
  { key: 'Transacciones', label: 'Transacciones', format: 'number' },
  { key: 'Productos_Vendidos', label: 'Productos Vendidos', format: 'number' }
]

const monthlyColumns = [
  { key: 'Mes', label: 'Mes' },
  { key: 'Transacciones', label: 'Transacciones', format: 'number' },
  { key: 'Productos_Vendidos', label: 'Productos Vendidos', format: 'number' }
]

// Chart Data Computed Properties
const dailyChartData = computed(() => {
  if (!data.value.ventas_diarias) return null

  const labels = data.value.ventas_diarias.map(d => d.Fecha)
  const transactions = data.value.ventas_diarias.map(d => d.Transacciones || 0)

  return {
    labels,
    datasets: [{
      label: 'Transacciones Diarias',
      data: transactions,
      borderColor: 'rgb(102, 126, 234)',
      backgroundColor: 'rgba(102, 126, 234, 0.1)',
      tension: 0.4,
      fill: true
    }]
  }
})

const weeklyChartData = computed(() => {
  if (!data.value.ventas_semanales) return null

  const labels = data.value.ventas_semanales.map(d => `Semana ${d.Semana || d.Week}`)
  const transactions = data.value.ventas_semanales.map(d => d.Transacciones || 0)

  return {
    labels,
    datasets: [{
      label: 'Transacciones Semanales',
      data: transactions,
      backgroundColor: 'rgba(102, 126, 234, 0.7)'
    }]
  }
})

const monthlyChartData = computed(() => {
  if (!data.value.ventas_mensuales) return null

  const labels = data.value.ventas_mensuales.map(d => d.Mes || d.Month)
  const transactions = data.value.ventas_mensuales.map(d => d.Transacciones || 0)

  return {
    labels,
    datasets: [{
      label: 'Transacciones Mensuales',
      data: transactions,
      backgroundColor: 'rgba(118, 75, 162, 0.7)'
    }]
  }
})

const dayOfWeekChartData = computed(() => {
  if (!data.value.ventas_dia_semana) return null

  const labels = data.value.ventas_dia_semana.map(d => d.DiaSemana || d.Day)
  const transactions = data.value.ventas_dia_semana.map(d => d.Transacciones || 0)

  return {
    labels,
    datasets: [{
      label: 'Transacciones por Día',
      data: transactions,
      backgroundColor: [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(199, 199, 199, 0.7)'
      ]
    }]
  }
})

onMounted(async () => {
  try {
    const response = await api.getTemporalAnalysis()
    data.value = response.data
  } catch (err) {
    error.value = 'Error cargando análisis temporal: ' + err.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.loading, .error {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  font-size: 1.2rem;
}

.error {
  color: #e74c3c;
}
</style>
