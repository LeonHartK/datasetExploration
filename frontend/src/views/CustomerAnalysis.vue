<template>
  <div class="customer-analysis">
    <h2 class="page-title">Análisis de Clientes</h2>

    <div v-if="loading" class="loading">Cargando análisis de clientes...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else>
      <!-- Customer Images -->
      <div class="images-grid">
        <ChartContainer title="Segmentación RFM de Clientes">
          <img :src="getImageUrl('grafica_segmentacion_clientes.png')" alt="Segmentación" class="chart-image" />
        </ChartContainer>

        <ChartContainer title="Distribución de Frecuencia de Clientes">
          <img :src="getImageUrl('grafica_frecuencia_clientes.png')" alt="Frecuencia" class="chart-image" />
        </ChartContainer>

        <ChartContainer title="Tiempo entre Compras">
          <img :src="getImageUrl('grafica_tiempo_entre_compras.png')" alt="Tiempo entre compras" class="chart-image" />
        </ChartContainer>
      </div>

      <!-- Data Tables -->
      <DataTable
        v-if="data.segmentacion_clientes?.length"
        title="Segmentación de Clientes (Muestra Top 100)"
        :data="data.segmentacion_clientes"
        :columns="segmentColumns"
        :limit="100"
      />

      <DataTable
        v-if="data.frecuencia_clientes?.length"
        title="Frecuencia de Clientes (Muestra)"
        :data="data.frecuencia_clientes"
        :columns="frequencyColumns"
        :limit="20"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChartContainer from '@/components/ChartContainer.vue'
import DataTable from '@/components/DataTable.vue'
import api from '@/services/api'

const loading = ref(true)
const error = ref(null)
const data = ref({})

const segmentColumns = [
  { key: 'Customer', label: 'Cliente' },
  { key: 'Recency', label: 'Recencia (días)', format: 'number' },
  { key: 'Frequency', label: 'Frecuencia', format: 'number' },
  { key: 'Monetary', label: 'Valor Monetario', format: 'number' },
  { key: 'RFM_Segment', label: 'Segmento RFM' }
]

const frequencyColumns = [
  { key: 'Customer', label: 'Cliente' },
  { key: 'Frecuencia', label: 'Número de Compras', format: 'number' }
]

onMounted(async () => {
  try {
    const response = await api.getCustomerAnalysis()
    data.value = response.data
  } catch (err) {
    error.value = 'Error cargando análisis de clientes: ' + err.message
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
