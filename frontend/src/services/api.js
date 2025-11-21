import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Health check
  healthCheck() {
    return apiClient.get('/health')
  },

  // Analytics endpoints
  getSummary() {
    return apiClient.get('/analytics/summary')
  },

  getTemporalAnalysis() {
    return apiClient.get('/analytics/temporal')
  },

  getCustomerAnalysis() {
    return apiClient.get('/analytics/customers')
  },

  getProductAnalysis() {
    return apiClient.get('/analytics/products')
  },

  getTransactionStats() {
    return apiClient.get('/analytics/transactions')
  },

  getTopCustomers() {
    return apiClient.get('/analytics/top-customers')
  },

  // Recommendations endpoints
  getRecommendationsForCustomer(customerId, topN = 10) {
    return apiClient.get(`/recommendations/customer/${customerId}?top_n=${topN}`)
  },

  getRecommendationsForProduct(productId, topN = 10) {
    return apiClient.get(`/recommendations/product/${productId}?top_n=${topN}`)
  },

  // Reports endpoints
  getImages() {
    return apiClient.get('/reports/images')
  },

  getImageUrl(filename) {
    return `${API_BASE_URL}/reports/images/${filename}`
  },

  getCSVFiles() {
    return apiClient.get('/reports/csv')
  },

  getCSVDownloadUrl(filename) {
    return `${API_BASE_URL}/reports/csv/${filename}`
  }
}
