<template>
  <div class="recommendations">
    <h2 class="page-title">Sistema de Recomendaciones</h2>

    <div class="search-section">
      <!-- Búsqueda por Cliente -->
      <div class="search-card">
        <h3>🔍 Recomendaciones por Cliente</h3>
        <p class="description">Ingrese el ID de un cliente para obtener recomendaciones de productos basadas en su historial de compras</p>

        <div class="search-box">
          <input
            v-model="customerSearch"
            type="number"
            placeholder="ID del cliente (ej: 530)"
            @keyup.enter="searchByCustomer"
            class="search-input"
          />
          <button @click="searchByCustomer" class="search-button" :disabled="loading">
            {{ loading ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>
      </div>

      <!-- Búsqueda por Producto -->
      <div class="search-card">
        <h3>🔍 Productos Relacionados</h3>
        <p class="description">Ingrese el ID de un producto para ver qué otros productos suelen comprarse juntos</p>

        <div class="search-box">
          <input
            v-model="productSearch"
            type="number"
            placeholder="ID del producto (ej: 5)"
            @keyup.enter="searchByProduct"
            class="search-input"
          />
          <button @click="searchByProduct" class="search-button" :disabled="loading">
            {{ loading ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Resultados -->
    <div v-if="results && !loading" class="results-section">
      <!-- Resultados para Cliente -->
      <div v-if="searchType === 'customer'" class="results-container">
        <div class="results-header">
          <h3>Recomendaciones para Cliente #{{ results.customer_id }}</h3>
          <div class="customer-stats" v-if="results.customer_stats">
            <div class="stat">
              <span class="stat-label">Transacciones:</span>
              <span class="stat-value">{{ results.customer_stats.num_transactions }}</span>
            </div>
            <div class="stat">
              <span class="stat-label">Productos comprados:</span>
              <span class="stat-value">{{ results.customer_stats.total_products_bought }}</span>
            </div>
          </div>
        </div>

        <div v-if="results.recommendations && results.recommendations.length > 0" class="recommendations-grid">
          <div v-for="(rec, index) in results.recommendations" :key="index" class="recommendation-card">
            <div class="rec-header">
              <div class="rec-rank">#{{ index + 1 }}</div>
              <div class="rec-product-id">Producto {{ rec.producto_id }}</div>
            </div>
            <div class="rec-metrics">
              <div class="metric">
                <span class="metric-label">Score:</span>
                <span class="metric-value highlight">{{ rec.score.toFixed(3) }}</span>
              </div>
              <div class="metric">
                <span class="metric-label">Lift:</span>
                <span class="metric-value">{{ rec.lift.toFixed(2) }}</span>
              </div>
              <div class="metric">
                <span class="metric-label">Confianza:</span>
                <span class="metric-value">{{ (rec.confianza * 100).toFixed(1) }}%</span>
              </div>
            </div>
            <div class="rec-info">
              <small>Basado en: Producto {{ rec.basado_en_producto }}</small>
            </div>
          </div>
        </div>

        <div v-else class="no-results">
          <p>{{ results.message || 'No se encontraron recomendaciones para este cliente' }}</p>
        </div>
      </div>

      <!-- Resultados para Producto -->
      <div v-if="searchType === 'product'" class="results-container">
        <div class="results-header">
          <h3>Productos Relacionados con Producto #{{ results.product_id }}</h3>
          <div class="product-stats" v-if="results.product_stats && Object.keys(results.product_stats).length > 0">
            <div class="stat">
              <span class="stat-label">Frecuencia de venta:</span>
              <span class="stat-value">{{ results.product_stats.frecuencia?.toLocaleString() }}</span>
            </div>
            <div class="stat">
              <span class="stat-label">% del total:</span>
              <span class="stat-value">{{ results.product_stats.porcentaje?.toFixed(2) }}%</span>
            </div>
          </div>
          <p class="rules-info" v-if="results.based_on_rules">Basado en {{ results.based_on_rules }} reglas de asociación</p>
        </div>

        <div v-if="results.recommendations && results.recommendations.length > 0" class="recommendations-grid">
          <div v-for="(rec, index) in results.recommendations" :key="index" class="recommendation-card">
            <div class="rec-header">
              <div class="rec-rank">#{{ index + 1 }}</div>
              <div class="rec-product-id">Producto {{ rec.producto_id }}</div>
            </div>
            <div class="rec-metrics">
              <div class="metric">
                <span class="metric-label">Score:</span>
                <span class="metric-value highlight">{{ rec.score.toFixed(3) }}</span>
              </div>
              <div class="metric">
                <span class="metric-label">Lift:</span>
                <span class="metric-value">{{ rec.lift.toFixed(2) }}</span>
              </div>
              <div class="metric">
                <span class="metric-label">Confianza:</span>
                <span class="metric-value">{{ (rec.confianza * 100).toFixed(1) }}%</span>
              </div>
            </div>
            <div class="rec-info">
              <small>{{ rec.num_transacciones }} transacciones</small>
            </div>
          </div>
        </div>

        <div v-else class="no-results">
          <p>{{ results.message || 'No se encontraron recomendaciones para este producto' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const customerSearch = ref('')
const productSearch = ref('')
const loading = ref(false)
const error = ref(null)
const results = ref(null)
const searchType = ref(null)

const searchByCustomer = async () => {
  if (!customerSearch.value) {
    error.value = 'Por favor ingrese un ID de cliente'
    return
  }

  loading.value = true
  error.value = null
  results.value = null
  searchType.value = 'customer'

  try {
    const response = await api.getRecommendationsForCustomer(customerSearch.value)
    results.value = response.data

    if (results.value.error) {
      error.value = results.value.error
      results.value = null
    }
  } catch (err) {
    error.value = 'Error al buscar recomendaciones: ' + err.message
    results.value = null
  } finally {
    loading.value = false
  }
}

const searchByProduct = async () => {
  if (!productSearch.value) {
    error.value = 'Por favor ingrese un ID de producto'
    return
  }

  loading.value = true
  error.value = null
  results.value = null
  searchType.value = 'product'

  try {
    const response = await api.getRecommendationsForProduct(productSearch.value)
    results.value = response.data

    if (results.value.error) {
      error.value = results.value.error
      results.value = null
    }
  } catch (err) {
    error.value = 'Error al buscar recomendaciones: ' + err.message
    results.value = null
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-title {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.search-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.search-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.description {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.search-box {
  display: flex;
  gap: 1rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.search-button {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.search-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.search-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border-left: 4px solid #c33;
}

.results-section {
  margin-top: 2rem;
}

.results-container {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.results-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.results-header h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.customer-stats,
.product-stats {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.85rem;
  color: #7f8c8d;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #667eea;
}

.rules-info {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.recommendation-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.recommendation-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.rec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.rec-rank {
  background: #667eea;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
}

.rec-product-id {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
}

.rec-metrics {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric-label {
  color: #7f8c8d;
  font-size: 0.85rem;
}

.metric-value {
  font-weight: 600;
  color: #2c3e50;
}

.metric-value.highlight {
  color: #667eea;
  font-size: 1.1rem;
}

.rec-info {
  padding-top: 0.75rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  color: #7f8c8d;
  font-size: 0.85rem;
}

.no-results {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
  font-size: 1.1rem;
}
</style>
