<template>
  <div class="product-analysis">
    <h2 class="page-title">Análisis de Productos</h2>

    <div v-if="loading" class="loading">Cargando análisis de productos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else>
      <!-- Product Images -->
      <div class="images-grid">
        <ChartContainer title="Top Productos Más Vendidos">
          <img :src="getImageUrl('grafica_top_productos.png')" alt="Top Productos" class="chart-image" />
        </ChartContainer>

        <ChartContainer title="Coocurrencia de Productos">
          <img :src="getImageUrl('grafica_coocurrencia_productos.png')" alt="Coocurrencia" class="chart-image" />
        </ChartContainer>

        <ChartContainer title="Reglas de Asociación">
          <img :src="getImageUrl('grafica_reglas_asociacion.png')" alt="Reglas Asociación" class="chart-image" />
        </ChartContainer>
      </div>

      <!-- Data Tables -->
      <DataTable
        v-if="data.top_productos?.length"
        title="Top 20 Productos Más Vendidos"
        :data="data.top_productos"
        :columns="topProductsColumns"
        :limit="20"
      />

      <DataTable
        v-if="data.reglas_asociacion?.length"
        title="Reglas de Asociación (Muestra)"
        :data="data.reglas_asociacion"
        :columns="rulesColumns"
        :limit="20"
      />

      <DataTable
        v-if="data.product_category_summary?.length"
        title="Resumen por Categoría"
        :data="data.product_category_summary"
        :columns="categoryColumns"
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

const topProductsColumns = [
  { key: 'Product', label: 'Producto' },
  { key: 'Cantidad', label: 'Cantidad Vendida', format: 'number' },
  { key: 'Porcentaje', label: 'Porcentaje', format: 'percent' }
]

const rulesColumns = [
  { key: 'antecedents', label: 'Antecedentes' },
  { key: 'consequents', label: 'Consecuentes' },
  { key: 'support', label: 'Soporte', format: 'decimal' },
  { key: 'confidence', label: 'Confianza', format: 'decimal' },
  { key: 'lift', label: 'Lift', format: 'decimal' }
]

const categoryColumns = [
  { key: 'Category', label: 'Categoría' },
  { key: 'Productos', label: 'Productos', format: 'number' },
  { key: 'Transacciones', label: 'Transacciones', format: 'number' }
]

onMounted(async () => {
  try {
    const response = await api.getProductAnalysis()
    data.value = response.data
  } catch (err) {
    error.value = 'Error cargando análisis de productos: ' + err.message
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
