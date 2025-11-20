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
          title="Hora Pico"
          :value="summary.temporal_metrics?.peak_hour"
          icon="⏰"
          format="none"
          iconColor="linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
        />
      </div>

      <!-- Images Grid -->
      <h3 class="section-title">Visualizaciones Principales</h3>
      <div class="images-grid">
        <ChartContainer
          v-for="image in featuredImages"
          :key="image"
          :title="getImageTitle(image)"
        >
          <img :src="getImageUrl(image)" :alt="image" class="chart-image" />
        </ChartContainer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import KPICard from '@/components/KPICard.vue'
import ChartContainer from '@/components/ChartContainer.vue'
import api from '@/services/api'

const loading = ref(true)
const error = ref(null)
const summary = ref({})
const featuredImages = ref([
  'grafica_ventas_diarias.png',
  'grafica_segmentacion_clientes.png',
  'grafica_top_productos.png',
  'grafica_reglas_asociacion.png'
])

onMounted(async () => {
  try {
    const response = await api.getSummary()
    summary.value = response.data
  } catch (err) {
    error.value = 'Error cargando el resumen: ' + err.message
  } finally {
    loading.value = false
  }
})

function getImageUrl(filename) {
  return api.getImageUrl(filename)
}

function getImageTitle(filename) {
  const titles = {
    'grafica_ventas_diarias.png': 'Tendencia de Ventas Diarias',
    'grafica_segmentacion_clientes.png': 'Segmentación RFM de Clientes',
    'grafica_top_productos.png': 'Top Productos Más Vendidos',
    'grafica_reglas_asociacion.png': 'Reglas de Asociación de Productos'
  }
  return titles[filename] || filename
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
