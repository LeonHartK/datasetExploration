<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <h1>EDA Analytics Dashboard</h1>
      <p>Análisis Exploratorio de Datos - Retail 2013</p>
    </div>
    <div class="navbar-menu">
      <router-link to="/" class="nav-item" active-class="active">Dashboard</router-link>
      <router-link to="/temporal" class="nav-item" active-class="active">Análisis Temporal</router-link>
      <router-link to="/customers" class="nav-item" active-class="active">Clientes</router-link>
      <router-link to="/products" class="nav-item" active-class="active">Productos</router-link>
      <router-link to="/recommendations" class="nav-item" active-class="active">Recomendaciones</router-link>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.navbar-brand h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
  font-weight: 700;
}

.navbar-brand p {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  color: #666;
}

.navbar-menu {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.nav-item {
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  text-decoration: none;
  color: #555;
  font-weight: 500;
  transition: all 0.3s ease;
  background: transparent;
}

.nav-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
</style>
