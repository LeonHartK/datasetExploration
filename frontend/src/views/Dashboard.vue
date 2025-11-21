<template>
  <div class="dashboard">
    <h2 class="page-title">Resumen Ejecutivo</h2>

    <!-- Loading state -->
    <div v-if="loading" class="loading">Cargando datos...</div>

    <!-- Error state -->
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- Dashboard content -->
    <div v-else>
      <!-- KPIs Grid -->
      <div class="kpi-grid">
        <KPICard
          title="Total Transacciones"
          :value="summary.overview?.total_transactions"
          icon="🛒"
          format="number"
        />
        <KPICard
          title="Productos Vendidos"
          :value="summary.overview?.total_products_sold"
          icon="📦"
          format="number"
        />
        <KPICard
          title="Clientes Únicos"
          :value="summary.overview?.unique_customers"
          icon="👥"
          format="number"
        />
        <KPICard
          title="Productos/Transacción"
          :value="summary.overview?.avg_products_per_transaction"
          icon="📊"
          format="decimal"
        />
      </div>

      <!-- Secondary KPIs -->
      <h3 class="section-title">Métricas de Clientes</h3>
      <div class="kpi-grid">
        <KPICard
          title="Compras/Cliente"
          :value="summary.customer_metrics?.avg_transactions_per_customer"
          icon="🔄"
          format="decimal"
          iconColor="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        />
        <KPICard
          title="Clientes Recurrentes"
          :value="summary.customer_metrics?.recurring_customers_pct"
          icon="⭐"
          format="percent"
          iconColor="linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        />
        <KPICard
          title="Días entre Compras"
          :value="summary.customer_metrics?.avg_days_between_purchases"
          icon="📅"
          format="decimal"
          iconColor="linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
        />
      </div>

      <!-- Temporal KPIs -->
      <h3 class="section-title">Métricas Temporales</h3>
      <div class="kpi-grid">
        <KPICard
          title="Transacciones Diarias"
          :value="summary.temporal_metrics?.avg_daily_transactions"
          subtitle="Promedio"
          icon="📈"
          format="number"
          iconColor="linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
        />
        <KPICard
          title="Día Pico"
          :value="summary.temporal_metrics?.peak_day"
          icon="🎯"
          format="none"
          iconColor="linear-gradient(135deg, #30cfd0 0%, #330867 100%)"
        />
        <KPICard
          title="Días de Análisis"
          :value="summary.temporal_metrics?.analysis_days"
          icon="📆"
          format="number"
          iconColor="linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
        />
      </div>

      <!-- Dynamic Charts -->
      <h3 class="section-title">Visualizaciones Principales</h3>

      <!-- Ventas Diarias - Dynamic Chart -->
      <ChartContainer title="Tendencia de Ventas Diarias (Últimos 30 días)">
        <LineChart v-if="dailySalesChartData" :data="dailySalesChartData" />
      </ChartContainer>

      <!-- Top Productos - Dynamic Chart -->
      <ChartContainer title="Top 20 Productos Más Vendidos">
        <BarChart v-if="topProductsChartData" :data="topProductsChartData" :horizontal="true" />
      </ChartContainer>

      <!-- Top Clientes - Dynamic Chart -->
      <ChartContainer title="Top 10 Clientes Más Activos">
        <BarChart v-if="topCustomersChartData" :data="topCustomersChartData" :horizontal="true" />
      </ChartContainer>

      <!-- Segmentación RFM - 4 gráficas separadas -->
      <h3 class="section-title">Segmentación RFM de Clientes</h3>
      <div class="images-grid">
        <ChartContainer
          v-for="image in segmentationImages"
          :key="image.file"
          :title="image.title"
        >
          <img :src="getImageUrl(image.file)" :alt="image.title" class="chart-image" />
        </ChartContainer>
      </div>

      <!-- Reglas de Asociación - 4 gráficas separadas -->
      <h3 class="section-title">Reglas de Asociación de Productos</h3>
      <div class="images-grid">
        <ChartContainer
          v-for="image in associationImages"
          :key="image.file"
          :title="image.title"
        >
          <img :src="getImageUrl(image.file)" :alt="image.title" class="chart-image" />
        </ChartContainer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import KPICard from '@/components/KPICard.vue'
import ChartContainer from '@/components/ChartContainer.vue'
import LineChart from '@/components/LineChart.vue'
import BarChart from '@/components/BarChart.vue'
import api from '@/services/api'

const loading = ref(true)
const error = ref(null)
const summary = ref({})
const topCustomers = ref([])

// Imágenes de segmentación RFM
const segmentationImages = ref([
  { file: 'grafica_segmentacion_distribucion.png', title: 'Distribución de Segmentos' },
  { file: 'grafica_segmentacion_barras.png', title: 'Clientes por Segmento' },
  { file: 'grafica_segmentacion_matriz_rfm.png', title: 'Matriz RFM' },
  { file: 'grafica_segmentacion_boxplot.png', title: 'Distribución RFM Score' }
])

// Imágenes de reglas de asociación
const associationImages = ref([
  { file: 'grafica_reglas_asociacion_lift.png', title: 'Top Reglas por Lift' },
  { file: 'grafica_reglas_asociacion_scatter.png', title: 'Soporte vs Confianza' },
  { file: 'grafica_reglas_asociacion_dist_lift.png', title: 'Distribución de Lift' },
  { file: 'grafica_reglas_asociacion_dist_confianza.png', title: 'Distribución de Confianza' }
])

// Computed property for daily sales chart
const dailySalesChartData = computed(() => {
  const chartData = summary.value.chart_data
  if (!chartData || !chartData.ventas_diarias) return null

  const data = chartData.ventas_diarias
  const labels = data.map(d => d.fecha)
  const transactions = data.map(d => d.total_transacciones || 0)

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

// Computed property for top products chart
const topProductsChartData = computed(() => {
  const chartData = summary.value.chart_data
  if (!chartData || !chartData.top_productos) return null

  const data = chartData.top_productos
  const labels = data.map(d => `Producto ${d.producto_id}`)
  const frequencies = data.map(d => d.frecuencia || 0)

  return {
    labels,
    datasets: [{
      label: 'Frecuencia de Venta',
      data: frequencies,
      backgroundColor: 'rgba(102, 126, 234, 0.7)',
      borderColor: 'rgb(102, 126, 234)',
      borderWidth: 1
    }]
  }
})

// Computed property for top customers chart
const topCustomersChartData = computed(() => {
  if (!topCustomers.value || topCustomers.value.length === 0) return null

  const labels = topCustomers.value.map(c => `Cliente ${c.persona_id}`)
  const transactions = topCustomers.value.map(c => c.num_transacciones || 0)

  return {
    labels,
    datasets: [{
      label: 'Número de Transacciones',
      data: transactions,
      backgroundColor: 'rgba(255, 99, 132, 0.7)',
      borderColor: 'rgb(255, 99, 132)',
      borderWidth: 1
    }]
  }
})

onMounted(async () => {
  try {
    const [summaryResponse, topCustomersResponse] = await Promise.all([
      api.getSummary(),
      api.getTopCustomers()
    ])
    summary.value = summaryResponse.data
    topCustomers.value = topCustomersResponse.data
  } catch (err) {
    error.value = 'Error cargando el resumen: ' + err.message
  } finally {
    loading.value = false
  }
})

function getImageUrl(filename) {
  return api.getImageUrl(filename)
}
</script>

<style scoped>
.page-title {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.section-title {
  color: white;
  font-size: 1.5rem;
  margin: 2rem 0 1rem;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
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
