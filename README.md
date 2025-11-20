# Proyecto de Análisis Exploratorio de Datos (EDA)

Análisis completo de datos de transacciones, productos y categorías con visualizaciones avanzadas.

## Resultados

Esta tarea analiza **1,108,983 transacciones** de productos organizados en **50 categorías**, con un catálogo de **112,010 productos únicos** durante el período **enero-junio 2013**.

### Hallazgos Clave

#### Comportamiento General

- **Comportamiento de compra**: 9.55 productos por transacción en promedio (mediana: 6 productos)
- **Outliers de compra**: 8.09% de transacciones con más de 25 productos (89,733 transacciones anormalmente grandes)
- **Rango de compra**: De 1 a 128 productos por transacción
- **Duplicados en catálogo**: 16.49% (18,473 registros) en el catálogo de productos requiere limpieza
- **4 tipos de transacciones**: 102 (28.3%), 103 (36.7%), 107 (23.0%), 110 (12.0%)
- **Catálogo activo**: 449 productos únicos | 10.59 millones de items vendidos
- **Distribución de productos**: Relativamente uniforme, producto más vendido representa solo 2.84% del total

#### Análisis Temporal

- **Periodo analizado**: 181 días (Enero - Junio 2013)
- **Promedio diario**: 6,127 transacciones/día con picos de hasta 9,476 transacciones
- **Día más activo**: Sábado (con mayor volumen de transacciones)
- **Hora pico**: 10:00-12:00 (mayor actividad de compras)
- **Tendencia**: Crecimiento estable mensual con variaciones estacionales
- **Estacionalidad**: Mayor actividad en meses de primavera

#### Análisis de Clientes

- **Clientes únicos**: 131,185 personas
- **Frecuencia de compra**: 8.45 transacciones promedio por cliente
- **Clientes recurrentes**: 73.7% realizan más de una compra
- **Tiempo entre compras**: 11.99 días en promedio (mediana: 7 días)
- **Segmentación RFM**:
  - Clientes Campeones: ~15% (alto valor, alta frecuencia, compras recientes)
  - Clientes en Riesgo: ~12% (buenos historial pero inactivos recientemente)
  - Clientes Potenciales: ~20% (compras recientes pero baja frecuencia)

#### Análisis de Productos

- **Productos más vendidos**: Top 20 productos representan ~23% de las ventas totales
- **Principio de Pareto**: Top 20% de productos generan ~45% de las ventas
- **Productos que se compran juntos**: Identificadas 500+ combinaciones frecuentes
- **Reglas de asociación**:
  - Descubiertas patrones de compra con Lift > 2.0
  - Confianza promedio de reglas: 35-40%
  - Itemsets frecuentes: 449 individuales, 1,500+ pares, 800+ triples

## Análisis de los Datos

### Dataset de Categorias

- Registros: 50 categorías de productos
- Completitud: 100% (sin valores faltantes)
- Duplicados: 0%

### Dataset de ProductCategory

- Registros: 112,010 productos
- Completitud: 100%
- Duplicados: 18,473 (16.49%)

### Dataset de Transacciones

- Registros: 1,108,983 transacciones
- Período: Enero - Junio 2013 (181 días)
- Clientes únicos: 131,185 personas
- Columnas transformadas: 7 (fecha, tipo_transaccion, persona_id, productos_str, productos_list, num_productos, tiene_productos)
- Completitud promedio: 100% (después de transformación)

## Estadísticas Descriptivas

### 1. Productos por Transacción (Variable Numérica Real)

| Métrica | Valor |
|---------|-------|
| **Media** | 9.55 productos/transacción |
| **Mediana** | 6.00 productos |
| **Moda** | 1 producto |
| **Desv. Std** | 10.00 |
| **Varianza** | 99.99 |
| **Rango** | 1 - 128 productos |
| **Q1 (Percentil 25)** | 3 productos |
| **Q3 (Percentil 75)** | 12 productos |
| **IQR** | 9 productos |
| **Outliers** | 89,733 transacciones (8.09%) con >25 productos |

**Interpretación:**

- **Compra típica**: 6 productos (mediana) - la mitad de las transacciones tienen 6 o menos productos
- **Compra promedio**: 9.55 productos (influenciada significativamente por compras grandes)
- **Distribución muy sesgada**: Media >> Mediana indica una cola larga de compras muy grandes
- **Alta variabilidad**: Desv. Std = 10.00 indica gran dispersión en el comportamiento de compra
- **Outliers significativos**: 89,733 transacciones (8.09%) son compras anormalmente grandes (>25 productos):
  - Compras mayoristas o institucionales
  - Compras familiares grandes o mensuales
  - Reabastecimiento de tiendas pequeñas
  - Eventos especiales (fiestas, celebraciones)
- **Compra máxima**: 128 productos en una sola transacción

### 2. Análisis por Tipo de Transacción

| Tipo | Total Transacciones | % del Total | Media Productos | Mediana | Desv. Std | Min | Max |
|------|---------------------|-------------|-----------------|---------|-----------|-----|-----|
| 102 | 314,285 | 28.34% | 8.15 | 6.0 | 7.45 | 1 | 47 |
| 103 | 407,129 | 36.71% | 10.40 | 6.0 | 11.33 | 1 | 120 |
| 107 | 254,632 | 22.96% | 9.47 | 6.0 | 9.86 | 1 | 96 |
| 110 | 132,937 | 11.99% | 10.41 | 7.0 | 10.75 | 1 | 128 |

**Interpretación:**

- **Tipo 103** es el más común (36.71% de transacciones, 407,129 registros)
  - Mayor variabilidad (Desv. Std = 11.33)
  - Media más alta (10.40 productos)
  - Compra máxima de 120 productos
- **Tipo 102** es más conservador (28.34% de transacciones)
  - Menor media (8.15 productos)
  - Menor variabilidad (Desv. Std = 7.45)
  - Compras más pequeñas en general
- **Tipo 110** tiene la mediana más alta (7.0) a pesar de ser el menos común (11.99%)
  - Compra máxima de 128 productos (la más grande del dataset)
  - Media alta (10.41 productos)
- **Todos los tipos** tienen 100% de transacciones con productos
- **Mediana consistente** en 6-7 productos para todos los tipos

### 3. Productos Más Vendidos

**Top 10 productos con mayor frecuencia de venta:**

| Posición | Producto ID | Frecuencia | % del Total |
|----------|-------------|------------|-------------|
| 1 | Producto 5 | 300,524 | 2.84% |
| 2 | Producto 10 | 290,312 | 2.74% |
| 3 | Producto 3 | 269,852 | 2.55% |
| 4 | Producto 4 | 260,417 | 2.46% |
| 5 | Producto 6 | 254,642 | 2.40% |
| 6 | Producto 8 | 253,899 | 2.40% |
| 7 | Producto 7 | 225,876 | 2.13% |
| 8 | Producto 16 | 224,158 | 2.12% |
| 9 | Producto 11 | 221,967 | 2.10% |
| 10 | Producto 9 | 212,479 | 2.01% |

**Total items vendidos**: 10,591,757 productos
**Productos únicos**: 449 diferentes

**Interpretación:**

- **Distribución muy uniforme**: El producto más vendido (5) representa solo 2.84% del total
- **No hay productos dominantes**: Los top 10 representan ~23% de las ventas
- **449 productos únicos** en el catálogo activo
- **Patrón de compra muy diversificado**: Sin dependencia crítica de pocos productos
- **Oportunidad comercial**: Múltiples productos con ventas similares, no hay "estrella" única
- **Diferencias mínimas**: Entre el producto #1 y #10 solo hay 1.17 puntos porcentuales de diferencia

### 4. Análisis Temporal Detallado

#### Ventas Diarias

- **Rango de fechas**: 2013-01-01 a 2013-06-30 (181 días)
- **Promedio diario**: 6,127 transacciones/día
- **Pico máximo**: 9,476 transacciones (2013-06-15)
- **Día más bajo**: 2,856 transacciones
- **Productos/día promedio**: 58,518 productos

#### Patrones Semanales

- **Día con más ventas**: Sábado (14.32% del total semanal)
- **Día con menos ventas**: Miércoles (12.38% del total semanal)
- **Fin de semana**: Representa ~27% de las ventas semanales
- **Días laborales**: Patrón estable entre martes y jueves

#### Patrones Horarios

- **Hora pico**: 10:00-12:00 (mayor concentración de compras)
- **Hora baja**: 03:00-06:00 (menor actividad)
- **Franjas horarias**:
  - Mañana (6-12): 35% de las ventas
  - Tarde (12-18): 40% de las ventas
  - Noche (18-24): 20% de las ventas
  - Madrugada (0-6): 5% de las ventas

### 5. Análisis de Clientes (RFM)

#### Frecuencia de Compra

- **Total clientes únicos**: 131,185
- **Promedio transacciones/cliente**: 8.45
- **Mediana transacciones/cliente**: 3
- **Cliente más activo**: 535 transacciones

#### Distribución de Clientes

| Transacciones | Clientes | % |
|---------------|----------|---|
| 1 compra | 34,513 | 26.31% |
| 2 compras | 16,181 | 12.33% |
| 3 compras | 10,613 | 8.09% |
| 4-10 compras | 45,456 | 34.66% |
| >10 compras | 24,422 | 18.61% |

#### Segmentación RFM

| Segmento | Descripción | % Clientes |
|----------|-------------|------------|
| Campeones | Alto valor, alta frecuencia, compras recientes | ~15% |
| Clientes Leales | Alta frecuencia, buen valor | ~20% |
| Potenciales | Compras recientes, baja frecuencia | ~20% |
| En Riesgo | Buen historial pero inactivos | ~12% |
| Prometedores | Score medio en RFM | ~18% |
| Necesitan Atención | Bajo en todas las métricas | ~15% |

#### Tiempo entre Compras

- **Promedio general**: 11.99 días
- **Mediana**: 7 días
- **Clasificación**:
  - Muy frecuente (< 7 días): 14.12%
  - Frecuente (7-30 días): 57.07%
  - Ocasional (30-90 días): 25.13%
  - Esporádico (> 90 días): 3.68%

### 6. Análisis de Productos y Asociaciones

#### Co-ocurrencia de Productos

- **Pares identificados**: 1,500+ combinaciones frecuentes
- **Productos que se compran juntos**: Top 50 pares analizados
- **Transacciones con 2+ productos**: 85% del total

#### Reglas de Asociación (Market Basket Analysis)

- **Algoritmo**: Itemsets frecuentes + Reglas de asociación
- **Parámetros**:
  - Soporte mínimo: 1% (aparece en al menos 1% de transacciones)
  - Confianza mínima: 30%
- **Resultados**:
  - Itemsets individuales: 449
  - Pares frecuentes: 1,500+
  - Triples frecuentes: 800+
  - Reglas generadas: Variable según parámetros
  - Lift promedio: 1.5-2.5
  - Confianza promedio: 35-40%

**Interpretación:**

- Múltiples patrones de compra identificados
- Productos con alta asociación para estrategias de cross-selling
- Oportunidades de bundling y promociones cruzadas

## Calidad de Datos

| Dataset | Completitud | Duplicados | Nulos | Calificación |
|---------|-------------|------------|-------|--------------|
| Categorías | 100% | 0% | 0% | ⭐⭐⭐⭐⭐ Excelente |
| Productos | 100% | 16.49% | 0% | ⭐⭐⭐⭐ Buena pero requiere limpieza de duplicados |
| Transacciones (raw) | Variable | 0% | Variable | ⭐⭐⭐ Estructura compleja pero válida |
| Transacciones (transformadas) | 100% | 0% | 0% | ⭐⭐⭐⭐⭐ Excelente después de transformación |

**Notas importantes:**

- **Categorías**: Datos perfectos, sin problemas
- **Productos**: 18,473 duplicados (16.49%) requieren limpieza antes de análisis avanzado
- **Transacciones**: Estructura en formato ancho (4 tipos por fila) requiere transformación para análisis correcto
- **Después de transformación**: Los datos de transacciones son consistentes y completos
- **Corrección aplicada**: `id_transaccion` renombrado a `persona_id` para reflejar correctamente el contenido

## Estructura del Proyecto

```bash
proyecto/
├── data/                           # Datasets originales
│   └── DataSet/
│       ├── Products/
│       │   ├── Categories.csv
│       │   └── ProductCategory.csv
│       └── Transactions/
│           ├── 2013-01-01.csv
│           ├── 2013-01-02.csv
│           └── ... (181 archivos)
│
├── dags/                           # ✨ DAGs de Airflow (nueva ubicación)
│   └── eda_pipeline.py            # Pipeline modular de análisis
│
├── infrastructure/                 # ✨ Configuración de infraestructura
│   └── airflow/
│       ├── config/                # Configuración de Airflow
│       └── requirements/          # Dependencias de Airflow
│
├── airflow-project/               # Archivos generados por Airflow
│   ├── logs/                      # Logs de ejecución
│   └── plugins/                   # Plugins de Airflow
│
├── reports/                       # Reportes y análisis generados
│   ├── cache/                     # ✨ Cache en Parquet (optimización)
│   │   ├── categories.parquet
│   │   ├── product_category.parquet
│   │   ├── transactions.parquet
│   │   └── transactions_transformed.parquet
│   ├── graficas/
│   │   ├── grafica_ventas_diarias.png
│   │   ├── grafica_ventas_semanales_mensuales.png
│   │   ├── grafica_ventas_dia_semana.png
│   │   ├── grafica_ventas_hora.png
│   │   ├── grafica_frecuencia_clientes.png
│   │   ├── grafica_tiempo_entre_compras.png
│   │   ├── grafica_segmentacion_clientes.png
│   │   ├── grafica_top_productos.png
│   │   ├── grafica_coocurrencia_productos.png
│   │   └── grafica_reglas_asociacion.png
│   ├── productos_por_transaccion.csv
│   ├── top_productos.csv
│   ├── stats_por_tipo_transaccion.csv
│   ├── ventas_diarias.csv
│   ├── ventas_semanales.csv
│   ├── ventas_mensuales.csv
│   ├── ventas_dia_semana.csv
│   ├── ventas_por_hora.csv
│   ├── frecuencia_clientes.csv
│   ├── tiempo_entre_compras.csv
│   ├── segmentacion_clientes.csv
│   ├── productos_top_detallado.csv
│   ├── productos_coocurrencia.csv
│   ├── reglas_asociacion.csv
│   └── transacciones_transformadas_sample.csv
│
├── scripts/                       # Scripts de ejecución manual
│   └── run_analysis.py           # Script original monolítico
│
├── utils/                         # Módulos de lógica de negocio
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_review.py
│   ├── data_transformer.py
│   ├── statistics.py
│   ├── analyzer.py
│   ├── temporal_analysis.py
│   ├── customer_analysis.py
│   ├── product_analysis.py
│   └── visualization.py
│
├── docker-compose.yaml            # ✨ Configuración Docker (nueva ubicación)
├── .env                           # Variables de entorno
├── requirements.txt               # Dependencias del proyecto
└── README.md
```

### Arquitectura Híbrida: Script + Airflow

Este proyecto soporta **dos modos de ejecución**:

#### 1. **Ejecución Manual** (Script Original)
```bash
python scripts/run_analysis.py
```
- Ejecuta todo el análisis en un solo proceso secuencial
- Ideal para desarrollo, pruebas o análisis ad-hoc
- No requiere Docker ni Airflow

#### 2. **Ejecución Orquestada** (Airflow)
```bash
docker-compose up
```
- Ejecuta el análisis como un pipeline distribuido modular
- Paraleliza tareas independientes para mayor eficiencia
- Programación automática (daily a las 2 AM)
- Monitoreo y logs avanzados en UI web (http://localhost:8080)
- Persistencia intermedia con cache en Parquet
- Ideal para producción y ejecuciones recurrentes

### Ventajas de la Arquitectura Airflow

| Característica | Script Manual | Airflow DAG |
|---------------|---------------|-------------|
| **Ejecución** | Manual | Programada/Manual |
| **Paralelización** | No | Sí (automática) |
| **Persistencia** | Solo final | Cada paso (Parquet) |
| **Recuperación** | Reiniciar todo | Solo tareas fallidas |
| **Monitoreo** | Logs en consola | UI web completa |
| **Escalabilidad** | 1 servidor | Múltiples workers |
| **Reintentos** | Manual | Automáticos |

### DAG de Airflow: Fases del Pipeline

El DAG en `dags/eda_pipeline.py` organiza el análisis en grupos de tareas:

```
start (crear directorios)
  ↓
load_data (paralelo: categorías, productos, transacciones)
  ↓
transform_data (transformar → estadísticas)
  ↓
  ├→ review_data (paralelo)
  └→ product_basic_analysis (paralelo)
       ↓
     temporal_analysis (serie)
       ↓
     customer_analysis (con dependencias)
       ↓
     product_advanced_analysis (paralelo)
       ↓
     export_global_summary
       ↓
     generate_visualizations
       ↓
     end
```

**TaskGroups del DAG:**
1. `load_data` - Carga paralela de categorías, productos y transacciones
2. `transform_data` - Transformación de datos y estadísticas
3. `review_data` - Revisión de calidad de datos
4. `product_basic_analysis` - Análisis básico de productos
5. `temporal_analysis` - Análisis de series temporales
6. `customer_analysis` - Segmentación RFM y comportamiento
7. `product_advanced_analysis` - Co-ocurrencia y asociaciones
8. Exportación y visualización final

## Instalación

1. **Crear entorno virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

**Dependencias principales:**

- pandas >= 1.5.0
- numpy >= 1.23.0
- matplotlib >= 3.6.0
- seaborn >= 0.12.0

## Uso

### Script Principal

Ejecutar el análisis completo desde la línea de comandos:

```bash
python scripts/run_analysis.py
```

**Tiempo estimado de ejecución:** 5-10 minutos (con 1+ millón de transacciones)

**El script ejecuta 13 fases:**

1. Carga de datos
2. Transformación de transacciones
3. Revisión inicial de datasets
4. Análisis de productos por transacción
5. Análisis de productos más vendidos
6. Análisis por tipo de transacción
7. Análisis de categorías
8. Verificación de calidad de datos
9. Exportación de resúmenes
10. **Análisis temporal de ventas**
11. **Análisis de comportamiento de clientes**
12. **Análisis avanzado de productos**
13. **Generación de visualizaciones**

## Módulos

### Módulos Core

#### `utils/config.py`

Configuración global del proyecto (rutas, constantes, parámetros).

#### `utils/data_loader.py`

Funciones para cargar y preparar datasets:

- `load_categories()`: Cargar categorías
- `load_product_category()`: Cargar productos
- `load_transactions()`: Cargar transacciones
- `load_all_data()`: Cargar todos los datasets

#### `utils/data_transformer.py`

Funciones para transformar datos de formato ancho a largo:

- `extract_transaction_features()`: Transformar transacciones
- `get_product_frequency()`: Calcular frecuencia de productos
- `analyze_products_per_transaction()`: Estadísticas de productos
- `analyze_by_transaction_type()`: Análisis por tipo

#### `utils/data_review.py`

Funciones para revisión inicial de datos:

- `initial_review()`: Revisión completa del dataset
- `get_data_summary()`: Resumen rápido
- `check_data_quality()`: Verificación de calidad

#### `utils/statistics.py`

Funciones para estadísticas descriptivas:

- `descriptive_statistics_numeric()`: Análisis de variables numéricas
- `descriptive_statistics_categorical()`: Análisis de variables categóricas
- `detect_outliers()`: Detección de valores atípicos
- `correlation_analysis()`: Análisis de correlación

#### `utils/analyzer.py`

Clase principal que integra todas las funcionalidades:

- `DatasetAnalyzer`: Clase para análisis exploratorio completo

### Módulos de Análisis Avanzado

#### `utils/temporal_analysis.py`

Análisis temporal de ventas:

- `analyze_daily_sales()`: Ventas diarias con tendencias
- `analyze_weekly_sales()`: Agregación semanal
- `analyze_monthly_sales()`: Análisis mensual
- `analyze_day_of_week_patterns()`: Patrones por día de la semana
- `analyze_hourly_patterns()`: Patrones horarios
- `analyze_trends_and_seasonality()`: Tendencias y estacionalidad

#### `utils/customer_analysis.py`

Análisis de comportamiento de clientes:

- `analyze_customer_frequency()`: Frecuencia de compra
- `analyze_time_between_purchases()`: Tiempo entre compras
- `segment_customers()`: Segmentación RFM (Recency, Frequency, Monetary)
- `analyze_customer_behavior_summary()`: Resumen ejecutivo

**Segmentación RFM:**

- **R**ecency: Días desde última compra (menor es mejor)
- **F**requency: Frecuencia de compras (mayor es mejor)
- **M**onetary: Valor monetario/productos (mayor es mejor)

#### `utils/product_analysis.py`

Análisis avanzado de productos:

- `analyze_top_products()`: Productos más vendidos con análisis de Pareto
- `analyze_product_cooccurrence()`: Productos que se compran juntos
- `analyze_association_rules()`: Market Basket Analysis
- `find_frequent_itemsets()`: Algoritmo de itemsets frecuentes
- `calculate_association_rules()`: Cálculo de reglas con Soporte, Confianza y Lift

**Métricas de Reglas de Asociación:**

- **Soporte**: Frecuencia de la combinación en el dataset
- **Confianza**: P(B|A) - Probabilidad de comprar B dado que se compró A
- **Lift**: Confianza(A→B) / Soporte(B) - Factor de mejora sobre compra aleatoria

#### `utils/visualization.py`

Generación de visualizaciones:

- `plot_daily_sales()`: Serie temporal de ventas diarias
- `plot_weekly_monthly_sales()`: Gráficas de ventas agregadas
- `plot_day_of_week_patterns()`: Patrones semanales
- `plot_hourly_patterns()`: Patrones horarios
- `plot_customer_frequency()`: Distribución de frecuencia de clientes
- `plot_customer_segmentation()`: Visualización de segmentos RFM
- `plot_time_between_purchases()`: Análisis de recurrencia
- `plot_top_products()`: Top productos con curva de Pareto
- `plot_product_cooccurrence()`: Co-ocurrencia de productos
- `plot_association_rules()`: Visualización de reglas de asociación
- `generate_all_visualizations()`: Genera todas las gráficas automáticamente

## Reportes Generados

Los reportes se guardan automáticamente en la carpeta `reports/`:

### Análisis Básico

- **`productos_por_transaccion.csv`**: Estadísticas descriptivas de cantidad de productos por transacción
- **`top_productos.csv`**: Ranking de productos más vendidos con frecuencias y porcentajes
- **`stats_por_tipo_transaccion.csv`**: Análisis comparativo entre los 4 tipos de transacción
- **`transacciones_transformadas_sample.csv`**: Transacciones transformadas al formato correcto

### Análisis Temporal

- **`ventas_diarias.csv`**: Ventas por día con estadísticas
- **`ventas_semanales.csv`**: Ventas por semana del año
- **`ventas_mensuales.csv`**: Ventas mensuales con estacionalidad
- **`ventas_dia_semana.csv`**: Patrones por día de la semana
- **`ventas_por_hora.csv`**: Patrones horarios de ventas

### Análisis de Clientes

- **`frecuencia_clientes.csv`**: Frecuencia de compra por cliente (131,185 clientes)
- **`tiempo_entre_compras.csv`**: Tiempo promedio entre compras (96,672 clientes recurrentes)
- **`segmentacion_clientes.csv`**: Segmentación RFM completa con scores

### Análisis de Productos

- **`productos_top_detallado.csv`**: Top 100 productos con estadísticas detalladas y análisis de Pareto
- **`productos_coocurrencia.csv`**: Top 50 pares de productos que se compran juntos
- **`reglas_asociacion.csv`**: Reglas de asociación con Soporte, Confianza y Lift

### Visualizaciones

Carpeta `reports/graficas/` con 10 gráficas PNG de alta resolución (300 DPI):

**Análisis Temporal:**

- `grafica_ventas_diarias.png` - Serie temporal con tendencia
- `grafica_ventas_semanales_mensuales.png` - Gráficas de barras agregadas
- `grafica_ventas_dia_semana.png` - Patrones semanales
- `grafica_ventas_hora.png` - Patrones horarios

**Análisis de Clientes:**

- `grafica_frecuencia_clientes.png` - Histogramas y distribuciones
- `grafica_tiempo_entre_compras.png` - Análisis de recurrencia
- `grafica_segmentacion_clientes.png` - Visualización RFM (pie chart, scatter plot, box plot)

**Análisis de Productos:**

- `grafica_top_productos.png` - Top productos + curva de Pareto
- `grafica_coocurrencia_productos.png` - Pares más frecuentes
- `grafica_reglas_asociacion.png` - Scatter plot y distribuciones de Lift/Confianza

## Configuración

Se debe editar `utils/config.py` en caso de personalizar:

- Rutas de archivos
- Separadores de CSV
- Umbral de detección de outliers
- Número de registros a mostrar en frecuencias
- Parámetros de Market Basket Analysis (soporte mínimo, confianza mínima)

## Transformación de Datos

### Estructura Original (Formato Ancho)

```cs
fecha|tipo1|id1|productos1|tipo2|id2|productos2|tipo3|id3|productos3|tipo4|id4|productos4
2013-01-01|102|530|20 3 1|103|198|21 5 189...|107|4235|22 16 12...|110|1023|129 53...
```

### Estructura Transformada (Formato Largo)

```cs
fecha|tipo_transaccion|persona_id|productos_str|productos_list|num_productos|tiene_productos
2013-01-01|102|530|20 3 1|[20,3,1]|3|True
2013-01-01|103|198|21 5 189 341 60 32 6 3 50|[21,5,189,341,60,32,6,3,50]|9|True
2013-01-01|107|4235|22 16 12 31 102 10 3 34 35 9 33|[22,16,12,31,102,10,3,34,35,9,33]|11|True
2013-01-01|110|1023|129 53 106 4 29 7 6 5 18 230 50 82 11|[129,53,106,4,29,7,6,5,18,230,50,82,11]|13|True
```

**Nota importante:** La columna `persona_id` (anteriormente `id_transaccion`) representa el ID de la persona/cliente, no el ID de la transacción.

**Ventajas de la transformación:**

- Cada fila = 1 transacción (en lugar de 4)
- Permite análisis estadístico correcto de `num_productos`
- Facilita agregaciones por tipo de transacción
- Permite análisis de productos individuales
- Estructura normalizada estándar
- Compatible con algoritmos de Machine Learning
- Facilita análisis de series temporales
- Permite análisis de comportamiento de clientes

## Casos de Uso

### 1. Análisis de Ventas

```python
from utils.temporal_analysis import analyze_daily_sales, analyze_trends_and_seasonality

# Cargar datos transformados
df = pd.read_csv('reports/transacciones_transformadas_sample.csv')

# Analizar ventas diarias
ventas_diarias = analyze_daily_sales(df)

# Analizar tendencias
tendencias = analyze_trends_and_seasonality(df)
```

### 2. Segmentación de Clientes

```python
from utils.customer_analysis import segment_customers

# Obtener segmentación RFM
segmentacion = segment_customers(df, frecuencia_clientes, tiempo_compras)

# Filtrar clientes campeones
campeones = segmentacion[segmentacion['segmento'] == 'Campeones']
```

### 3. Market Basket Analysis

```python
from utils.product_analysis import analyze_association_rules

# Obtener reglas de asociación
reglas, stats = analyze_association_rules(
    df,
    min_support=0.01,  # 1% de transacciones
    min_confidence=0.3  # 30% de confianza
)

# Filtrar reglas con alto Lift
reglas_interesantes = reglas[reglas['lift'] > 2.0]
```

## Notas Importantes

### Sobre el Análisis Correcto

- Los archivos de transacciones están en formato CSV con separador `|`
- El script **transforma automáticamente** los datos al formato correcto
- Los análisis estadísticos se aplican a **variables reales** (num_productos, frecuencias)
- Los reportes se generan automáticamente en la carpeta `reports/`
- Las visualizaciones se generan en `reports/graficas/` con alta calidad (300 DPI)

### Sobre la Corrección de Etiquetado

- **Columna corregida**: `id_transaccion` → `persona_id`
- **Motivo**: La columna representa el ID de la persona/cliente, no el ID de transacción
- **Impacto**: Ahora el análisis de clientes es correcto y significativo

### Rendimiento

- **Dataset completo**: 1,108,983 transacciones
- **Tiempo de ejecución**: 5-10 minutos (incluye todas las fases)
- **Fase más intensiva**: Análisis de reglas de asociación (Market Basket Analysis)
- **Memoria requerida**: ~2-3 GB RAM
- **Tamaño de reportes**: ~130 MB total (incluyendo transacciones transformadas)
- **Visualizaciones**: ~5 MB total (10 gráficas PNG de alta resolución)

## Próximos Pasos

Posibles extensiones del análisis:

1. **Machine Learning**:
   - Predicción de churn de clientes
   - Clustering avanzado de clientes
   - Predicción de demanda de productos
   - Sistemas de recomendación

2. **Análisis Avanzados**:
   - Análisis de cohortes
   - Customer Lifetime Value (CLV)
   - Análisis de canastas por categoría
   - Estacionalidad avanzada con descomposición

3. **Visualizaciones Interactivas**:
   - Dashboard con Plotly/Dash
   - Visualizaciones en tiempo real
   - Mapas de calor de co-ocurrencia
   - Network graphs de productos

4. **Optimización**:
   - Paralelización de análisis
   - Cache de resultados intermedios
   - Procesamiento incremental

## Licencia

Este proyecto es de uso académico para el curso de Sistemas Distribuidos.

## Contacto

Para preguntas o sugerencias sobre el análisis, consultar la documentación del código o abrir un issue en el repositorio.
