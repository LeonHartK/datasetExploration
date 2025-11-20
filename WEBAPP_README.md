# EDA Analytics Dashboard - Web Application

Landing page interactiva para visualizar los resultados del análisis exploratorio de datos de transacciones retail.

## Arquitectura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Vue.js    │ ───> │   Flask     │ ───> │  Reports/   │
│  Frontend   │      │   Backend   │      │   (CSVs)    │
│  (Port 5173)│      │  (Port 5000)│      └─────────────┘
└─────────────┘      └─────────────┘
```

## Stack Tecnológico

### Backend
- **Flask 3.0** - Framework web Python
- **Pandas** - Procesamiento de datos
- **Flask-CORS** - Soporte para CORS

### Frontend
- **Vue.js 3** - Framework JavaScript
- **Vite** - Build tool
- **Chart.js** - Visualizaciones
- **Axios** - Cliente HTTP

## Estructura del Proyecto

```
datasetExploration/
├── backend/
│   ├── app/
│   │   ├── routes/          # Endpoints de la API
│   │   ├── services/        # Lógica de negocio
│   │   └── config.py        # Configuración
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── views/           # Páginas
│   │   ├── components/      # Componentes reutilizables
│   │   ├── services/        # API client
│   │   └── router/          # Vue Router
│   ├── package.json
│   └── vite.config.js
│
├── reports/                 # CSVs y gráficas generadas
└── docker-compose.web.yaml  # Docker setup
```

## Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

```bash
# Levantar los servicios
docker-compose -f docker-compose.web.yaml up --build

# Acceder a la aplicación
# Frontend: http://localhost:5173
# Backend API: http://localhost:5000
```

### Opción 2: Desarrollo Local

#### Backend

```bash
# Navegar al backend
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python run.py

# Backend corriendo en http://localhost:5000
```

#### Frontend

```bash
# Navegar al frontend (en otra terminal)
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# Frontend corriendo en http://localhost:5173
```

## API Endpoints

### Analytics

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/analytics/summary` | GET | Resumen ejecutivo con KPIs principales |
| `/api/analytics/temporal` | GET | Análisis temporal (ventas por día/mes/hora) |
| `/api/analytics/customers` | GET | Análisis de clientes (RFM, segmentación) |
| `/api/analytics/products` | GET | Análisis de productos (top, coocurrencia) |
| `/api/analytics/transactions` | GET | Estadísticas de transacciones |

### Reports

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/reports/images` | GET | Lista de gráficas disponibles |
| `/api/reports/images/{filename}` | GET | Descarga una gráfica específica |
| `/api/reports/csv` | GET | Lista de archivos CSV |
| `/api/reports/csv/{filename}` | GET | Descarga un CSV específico |

### Health

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/health` | GET | Health check del servicio |

## Vistas Disponibles

### 1. Dashboard (/)
- Resumen ejecutivo con KPIs principales
- Métricas de clientes y productos
- Visualizaciones destacadas

### 2. Análisis Temporal (/temporal)
- Ventas diarias, semanales y mensuales
- Análisis por día de la semana
- Análisis por hora del día

### 3. Análisis de Clientes (/customers)
- Segmentación RFM
- Distribución de frecuencia
- Tiempo entre compras

### 4. Análisis de Productos (/products)
- Top productos más vendidos
- Coocurrencia de productos
- Reglas de asociación

## Desarrollo

### Agregar un nuevo endpoint

1. Crear la ruta en `backend/app/routes/`
2. Implementar la lógica en `backend/app/services/`
3. Registrar el blueprint en `backend/app/__init__.py`

### Agregar una nueva vista

1. Crear componente en `frontend/src/views/`
2. Agregar ruta en `frontend/src/router/index.js`
3. Agregar link en `frontend/src/components/Navbar.vue`

### Agregar llamada a la API

1. Definir método en `frontend/src/services/api.js`
2. Usar en componente con `import api from '@/services/api'`

## Build para Producción

### Backend
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Frontend
```bash
cd frontend
npm run build
# Los archivos se generan en frontend/dist/
```

## Solución de Problemas

### Error CORS
Si tienes problemas de CORS, verifica que el backend tenga CORS habilitado en `app/__init__.py`:
```python
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173"]}})
```

### Puerto en uso
Si el puerto 5000 o 5173 está en uso:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Datos no cargan
1. Verifica que los archivos CSV estén en `reports/`
2. Verifica que las gráficas estén en `reports/graficas/`
3. Revisa los logs del backend

## Mejoras Futuras

- [ ] Agregar autenticación
- [ ] Implementar caché de datos
- [ ] Agregar filtros por fecha
- [ ] Exportar reportes personalizados
- [ ] Agregar gráficas interactivas con Chart.js
- [ ] Implementar búsqueda de productos/clientes
- [ ] Agregar comparación de períodos

## Licencia

MIT

## Contacto

Para preguntas o sugerencias, contacta al equipo de desarrollo.
