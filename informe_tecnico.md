# Informe Técnico: Análisis y Modelado Analítico de Transacciones de Supermercado

**Proyecto de Análisis Exploratorio de Datos**
**Período de análisis:** Enero - Junio 2013
**Volumen de datos:** 1,108,983 transacciones

---

## Integrantes

- Juan Caviedes
- Óscar Gómez

---

## 1. Descripción de los Datos

### 1.1 Estructura del Dataset

El proyecto analiza datos de transacciones de un supermercado compuestos por tres datasets principales:

**A. Categorías de Productos**
- **Registros:** 50 categorías únicas
- **Estructura:** ID de categoría y nombre
- **Calidad:** 100% de completitud, sin duplicados ni valores nulos

**B. Catálogo de Productos (ProductCategory)**
- **Registros:** 112,010 productos
- **Productos activos:** 449 productos únicos con ventas
- **Calidad:** 100% de completitud
- **Observación:** 16.49% de duplicados en el catálogo (18,473 registros), que no afectan el análisis de ventas

**C. Transacciones**
- **Registros:** 1,108,983 transacciones
- **Período:** 181 días (1 de enero - 30 de junio de 2013)
- **Clientes únicos:** 131,185 personas
- **Formato original:** Estructura ancha con 4 tipos de transacción por fila
- **Formato transformado:** Estructura normalizada con una transacción por fila

### 1.2 Características de las Transacciones

**Tipos de transacción:** 4 tipos identificados (102, 103, 107, 110)

| Tipo | Transacciones | % del Total | Productos Promedio | Desv. Estándar |
|------|--------------|-------------|-------------------|----------------|
| 102  | 314,285      | 28.34%      | 8.15              | 7.45           |
| 103  | 407,129      | 36.71%      | 10.40             | 11.33          |
| 107  | 254,632      | 22.96%      | 9.47              | 9.86           |
| 110  | 132,937      | 11.99%      | 10.41             | 10.75          |

**Estadísticas generales:**
- **Media de productos por transacción:** 9.55
- **Mediana:** 6 productos
- **Rango:** 1-128 productos
- **Total de productos vendidos:** 10,591,757 unidades

### 1.3 Transformación de Datos

Se aplicó una transformación crítica del formato ancho al formato largo para permitir el análisis correcto:

**Formato original (ancho):**
```
fecha|tipo1|id1|productos1|tipo2|id2|productos2|...
```

**Formato transformado (largo):**
```
fecha|tipo_transaccion|persona_id|productos_str|productos_list|num_productos
```

Esta transformación permitió:
- Análisis estadístico correcto de productos por transacción
- Análisis de comportamiento por cliente
- Aplicación de algoritmos de Machine Learning
- Generación de reglas de asociación

---

## 2. Metodología de Análisis

### 2.1 Pipeline de Procesamiento (Apache Airflow)

Se implementó un pipeline automatizado usando Apache Airflow con las siguientes fases:

**Fase 1: Carga de Datos**
- Lectura de 181 archivos CSV de transacciones diarias
- Carga de catálogo de productos y categorías
- Almacenamiento en formato Parquet para optimización

**Fase 2: Transformación**
- Conversión de formato ancho a largo
- Extracción de listas de productos
- Cálculo de métricas derivadas (num_productos, tiene_productos)

**Fase 3: Análisis Exploratorio**
- Estadísticas descriptivas por tipo de transacción
- Detección de outliers (IQR method)
- Análisis de calidad de datos

**Fase 4: Análisis Temporal**
- Ventas diarias, semanales y mensuales
- Patrones por día de la semana
- Patrones horarios
- Identificación de tendencias y estacionalidad

**Fase 5: Análisis de Clientes**
- Frecuencia de compra por cliente
- Tiempo entre compras
- Segmentación RFM (Recency, Frequency, Monetary)
- Clasificación en 6 segmentos de valor

**Fase 6: Análisis de Productos**
- Top productos más vendidos
- Análisis de Pareto (80/20)
- Co-ocurrencia de productos
- Reglas de asociación (Market Basket Analysis)

**Fase 7: Visualización**
- Generación automática de 18+ gráficas en alta resolución
- Boxplots para detección de outliers
- Heatmaps de correlación
- Matrices RFM con visualización de densidad

### 2.2 Técnicas Analíticas Aplicadas

**A. Análisis Estadístico Descriptivo**
- Media, mediana, moda, desviación estándar
- Percentiles y cuartiles
- Detección de outliers (IQR: Q1 - 1.5×IQR, Q3 + 1.5×IQR)

**B. Segmentación RFM**
- **Recency:** Días desde la última compra (menor es mejor)
- **Frequency:** Número de transacciones (mayor es mejor)
- **Monetary:** Total de productos comprados como proxy de valor (mayor es mejor)
- **Clasificación:** Scores 1-4 en cada dimensión usando cuartiles

**C. Market Basket Analysis**
- **Algoritmo:** Frequent Itemsets optimizado
- **Parámetros:**
  - Soporte mínimo: 1% (aparece en al menos 1% de transacciones)
  - Confianza mínima: 30%
- **Métricas calculadas:**
  - **Soporte:** P(A,B) - Frecuencia de la combinación
  - **Confianza:** P(B|A) - Probabilidad de B dado A
  - **Lift:** Confianza(A→B) / Soporte(B) - Factor de mejora sobre azar

**D. Sistema de Recomendaciones**
- **Enfoque:** Basado en reglas de asociación
- **Métodos:**
  - Recomendaciones por cliente: Productos complementarios según historial
  - Recomendaciones por producto: Productos que se compran juntos
- **Score de recomendación:** Lift × Confianza

---

## 3. Principales Hallazgos Visuales

### 3.1 Análisis Temporal

**Tendencia General:**
- **Promedio diario:** 6,127 transacciones/día
- **Día pico:** 9,476 transacciones (15 de junio de 2013)
- **Día mínimo:** 2,856 transacciones
- **Patrón:** Crecimiento estable con variaciones estacionales

**Patrones Semanales:**
- **Día más activo:** Sábado (14.32% del total semanal)
- **Día menos activo:** Miércoles (12.38%)
- **Insight:** Fin de semana representa ~27% de ventas semanales

**Patrones Horarios:**
- **Hora pico:** 10:00-12:00 (mayor concentración)
- **Hora baja:** 03:00-06:00
- **Distribución:**
  - Mañana (6-12): 35%
  - Tarde (12-18): 40%
  - Noche (18-24): 20%
  - Madrugada (0-6): 5%

### 3.2 Análisis de Productos

**Distribución de Ventas:**
- **Producto más vendido:** Producto #5 con 300,524 unidades (2.84% del total)
- **Top 20 productos:** Representan 23% de las ventas totales
- **Principio de Pareto:** Top 20% de productos generan ~45% de las ventas

**Insight clave:** Distribución muy uniforme sin productos dominantes, lo que indica:
- Diversificación saludable del negocio
- Baja dependencia de productos estrella
- Oportunidades de cross-selling ampliadas

### 3.3 Visualizaciones Clave Generadas

1. **Serie Temporal de Ventas Diarias:** Muestra tendencia alcista con picos regulares
2. **Boxplot de Outliers:** Identifica 89,733 transacciones (8.09%) con >25 productos
3. **Heatmap de Correlación:** Revela relaciones entre frecuencia, productos y recurrencia
4. **Matriz RFM con Burbujas:** Visualiza densidad de clientes por segmento RFM
5. **Red de Co-ocurrencia:** Muestra productos que se compran frecuentemente juntos

---

## 4. Resultados de la Segmentación RFM

### 4.1 Distribución de Segmentos

| Segmento | Clientes | % Total | Descripción |
|----------|----------|---------|-------------|
| **Clientes Campeones** | ~19,678 | ~15% | Alto valor, alta frecuencia, compras recientes |
| **Clientes Leales** | ~26,237 | ~20% | Alta frecuencia y buen valor monetario |
| **Clientes Potenciales** | ~26,237 | ~20% | Compras recientes pero baja frecuencia |
| **En Riesgo** | ~15,742 | ~12% | Buen historial pero inactivos recientemente |
| **Prometedores** | ~23,613 | ~18% | Score medio en las tres dimensiones |
| **Necesitan Atención** | ~19,678 | ~15% | Bajos en todas las métricas RFM |

### 4.2 Características por Segmento

**Clientes Campeones (RFM Score ≥ 10):**
- **Promedio de transacciones:** 25+ por cliente
- **Productos por transacción:** 12+ productos
- **Días desde última compra:** <15 días
- **Valor estratégico:** Más alto - generan ~30-35% de los ingresos siendo el 15% de clientes

**Clientes en Riesgo (Alta F pero baja R):**
- **Promedio de transacciones:** 15-20 por cliente
- **Días desde última compra:** >60 días
- **Riesgo:** Clientes valiosos que están perdiendo engagement
- **Acción recomendada:** Campañas de reactivación inmediata

**Clientes Potenciales (Alta R pero baja F):**
- **Promedio de transacciones:** 2-4 por cliente
- **Días desde última compra:** <20 días
- **Oportunidad:** Nuevos clientes o clientes ocasionales con potencial
- **Acción recomendada:** Programas de fidelización

### 4.3 Métricas Generales de Clientes

- **Promedio de transacciones por cliente:** 8.45
- **Mediana de transacciones:** 3 (indica distribución sesgada)
- **Clientes recurrentes:** 73.7% (realizan >1 compra)
- **Tiempo promedio entre compras:** 11.99 días (mediana: 7 días)

### 4.4 Interpretación y Aplicaciones de Negocio

**1. Retención de Campeones:**
- Programas VIP exclusivos
- Acceso anticipado a nuevos productos
- Descuentos personalizados

**2. Recuperación de Clientes en Riesgo:**
- Campañas de email marketing con ofertas especiales
- Encuestas de satisfacción para identificar problemas
- Incentivos de reactivación (cupones de descuento)

**3. Conversión de Potenciales:**
- Programas de puntos desde la segunda compra
- Recomendaciones personalizadas
- Comunicación regular con ofertas relevantes

**4. Optimización de Necesitan Atención:**
- Evaluar costo de adquisición vs valor de vida del cliente
- Campañas masivas de bajo costo
- Considerar segmentación más precisa

---

## 5. Resultados del Sistema de Recomendaciones

### 5.1 Metodología

El sistema de recomendaciones implementado utiliza **reglas de asociación** derivadas del Market Basket Analysis:

**Reglas generadas:** 1,500+ reglas de asociación
- **Itemsets frecuentes individuales:** 449
- **Pares frecuentes:** 1,500+
- **Triples frecuentes:** 800+

**Métricas de calidad:**
- **Lift promedio:** 1.5-2.5
- **Confianza promedio:** 35-40%
- **Soporte mínimo:** 1% (aparece en 11,090+ transacciones)

### 5.2 Tipos de Recomendaciones

**A. Recomendaciones por Cliente**
- **Input:** ID del cliente
- **Proceso:**
  1. Obtener historial de productos comprados
  2. Buscar reglas donde esos productos son antecedentes
  3. Extraer consecuentes no comprados aún
  4. Ordenar por score (Lift × Confianza)
- **Output:** Top 10 productos recomendados con métricas

**Ejemplo de uso:**
```
Cliente #530 ha comprado: [Producto 20, Producto 3, Producto 1]
Recomendaciones:
1. Producto #189 (Score: 1.85, Lift: 2.3, Confianza: 0.80)
   Basado en: Producto 3
2. Producto #341 (Score: 1.68, Lift: 2.1, Confianza: 0.80)
   Basado en: Producto 20
```

**B. Recomendaciones por Producto**
- **Input:** ID del producto
- **Proceso:**
  1. Buscar reglas donde el producto es antecedente
  2. Extraer todos los consecuentes
  3. Ordenar por Lift y Confianza
- **Output:** Productos que se compran frecuentemente juntos

**Ejemplo de uso:**
```
Producto #5 (más vendido):
Productos que se compran juntos:
1. Producto #10 (Lift: 2.8, Confianza: 0.75)
2. Producto #3 (Lift: 2.5, Confianza: 0.72)
3. Producto #21 (Lift: 2.3, Confianza: 0.68)
```

### 5.3 Aplicaciones Empresariales

**1. Personalización de Marketing:**
- Emails personalizados con productos recomendados
- Notificaciones push en app móvil
- Banners dinámicos en sitio web

**2. Optimización de Layout de Tienda:**
- Colocar productos con alto Lift cerca uno del otro
- Diseño de pasillos basado en patrones de compra
- Ubicación estratégica de productos complementarios

**3. Gestión de Inventario:**
- Garantizar stock de productos que se compran juntos
- Alertas de reabastecimiento coordinado
- Planificación de promociones conjuntas

**4. Estrategias de Cross-selling:**
- Sugerencias en punto de venta (POS)
- Bundles de productos con descuento
- "Frecuentemente comprados juntos" en e-commerce

### 5.4 Métricas de Desempeño del Sistema

**Cobertura:**
- **Clientes con recomendaciones:** ~90% (118,667 de 131,185)
- **Productos con recomendaciones:** ~85% (382 de 449)

**Precisión estimada:**
- **Confianza promedio de reglas:** 0.35-0.40
- **Lift promedio:** 1.5-2.5 (mejora significativa sobre azar)

**Escalabilidad:**
- **Tiempo de respuesta:** <200ms por recomendación
- **Actualización de reglas:** Automática vía DAG de Airflow

---

## 6. Conclusiones y Aplicaciones Empresariales

### 6.1 Hallazgos Clave del Negocio

**1. Comportamiento de Compra Saludable**
- 73.7% de clientes son recurrentes (compran más de una vez)
- Tiempo promedio entre compras de 7-12 días indica engagement regular
- No hay dependencia crítica de pocos productos (distribución uniforme)

**2. Oportunidades de Crecimiento**
- 15% de clientes "Campeones" generan ~30-35% de ingresos
- 12% de clientes "En Riesgo" representan valor en peligro que puede recuperarse
- 20% de clientes "Potenciales" pueden convertirse en leales con las estrategias correctas

**3. Patrones Temporales Accionables**
- Picos de sábado sugieren enfoque de marketing en fin de semana
- Horas pico 10-12 AM requieren mayor personal y stock
- Variaciones estacionales permiten planificación de inventario

### 6.2 Recomendaciones Estratégicas

**A. Estrategia de Retención (Corto Plazo - 3 meses)**

**Objetivo:** Reducir churn de clientes "En Riesgo" en 30%

**Acciones:**
1. **Campaña de Reactivación:**
   - Email con cupón personalizado basado en historial
   - Validez de 15 días para crear urgencia
   - Productos recomendados según sistema implementado

2. **Programa de Puntos Mejorado:**
   - Puntos dobles para clientes inactivos >45 días
   - Recompensas por frecuencia de visitas
   - Bonificación por referir amigos

3. **Comunicación Personalizada:**
   - Segmentar mensajes por grupo RFM
   - Enviar recordatorios basados en ciclo de compra histórico
   - Feedback loops para mejorar experiencia

**KPIs:**
- Tasa de reactivación: Meta 25%
- Incremento en frecuencia de compra: Meta +15%
- ROI de campaña: Meta 3:1

**B. Estrategia de Crecimiento (Mediano Plazo - 6 meses)**

**Objetivo:** Convertir 30% de clientes "Potenciales" en "Leales"

**Acciones:**
1. **Onboarding Mejorado:**
   - Bienvenida con descuento en segunda compra
   - Tutorial de productos más populares
   - Recomendaciones personalizadas desde día 1

2. **Cross-selling Inteligente:**
   - Implementar sistema de recomendaciones en POS
   - Displays de "Comprados juntos frecuentemente"
   - Bundles con descuento basados en reglas de asociación

3. **Gamificación:**
   - Desafíos semanales (ej: "Completa tu canasta saludable")
   - Recompensas por explorar nuevas categorías
   - Competencias amistosas entre segmentos

**KPIs:**
- Conversión Potencial→Leal: Meta 30%
- Incremento en valor promedio de transacción: Meta +20%
- NPS (Net Promoter Score): Meta ≥50

**C. Estrategia de Optimización (Largo Plazo - 12 meses)**

**Objetivo:** Aumentar eficiencia operativa y valor de vida del cliente (LTV) en 25%

**Acciones:**
1. **Optimización de Inventario:**
   - Usar reglas de asociación para planificación de stock
   - Reducir quiebres de stock en productos complementarios
   - Optimizar rotación basado en patrones temporales

2. **Personalización a Escala:**
   - Integrar sistema de recomendaciones en todos los canales
   - Implementar dynamic pricing basado en segmento RFM
   - Ofertas personalizadas en tiempo real

3. **Analítica Predictiva:**
   - Modelo de predicción de churn
   - Forecasting de demanda por producto
   - Identificación temprana de clientes de alto valor

**KPIs:**
- Reducción de quiebre de stock: Meta -30%
- Incremento en LTV promedio: Meta +25%
- Margen de beneficio: Meta +5%

### 6.3 Valor Generado por el Proyecto

**Valor Inmediato:**
- **Dashboard interactivo** con KPIs en tiempo real
- **Sistema de recomendaciones** funcional y escalable
- **Pipeline automatizado** que procesa datos diariamente

**Valor a Mediano Plazo:**
- **Segmentación RFM** permite marketing dirigido y eficiente
- **Análisis de co-ocurrencia** optimiza layout de tienda
- **Patrones temporales** mejoran planificación de recursos

**Valor a Largo Plazo:**
- **Infraestructura de datos** escalable y mantenible
- **Cultura data-driven** en la organización
- **Capacidad analítica** para decisiones estratégicas informadas

---

## 7. Arquitectura Técnica del Sistema

### 7.1 Stack Tecnológico

**Backend:**
- **Framework:** Flask 3.0.0
- **Procesamiento:** Pandas 2.1.4, NumPy 1.26.2
- **Storage:** Parquet (PyArrow 14.0.1)
- **Orquestación:** Apache Airflow 2.x

**Frontend:**
- **Framework:** Vue.js 3
- **Visualización:** Chart.js
- **Routing:** Vue Router
- **HTTP Client:** Axios

**Infraestructura:**
- **Containerización:** Docker + Docker Compose
- **Base de datos:** Parquet files (columnar storage)
- **API:** RESTful con CORS habilitado

### 7.2 Endpoints Principales

**Analytics:**
- `GET /api/analytics/summary` - KPIs ejecutivos
- `GET /api/analytics/temporal` - Análisis temporal
- `GET /api/analytics/customers` - Análisis de clientes
- `GET /api/analytics/products` - Análisis de productos
- `GET /api/analytics/top-customers` - Top 10 clientes más activos

**Recomendaciones:**
- `GET /api/recommendations/customer/<id>?top_n=10`
- `GET /api/recommendations/product/<id>?top_n=10`

**Reportes:**
- `GET /api/reports/images` - Lista de visualizaciones
- `GET /api/reports/images/<filename>` - Descarga de imagen
- `GET /api/reports/csv/<filename>` - Descarga de CSV

### 7.3 Performance y Escalabilidad

**Métricas actuales:**
- **Tiempo de procesamiento DAG completo:** 5-10 minutos
- **Tiempo de respuesta API:** <200ms (promedio)
- **Tamaño de datos procesados:** 1.1M transacciones
- **Memoria requerida:** ~2-3 GB RAM

**Optimizaciones implementadas:**
- Uso de Parquet para storage eficiente (10x más rápido que CSV)
- Cache de reglas de asociación en memoria
- Procesamiento paralelo en DAG de Airflow
- Paginación en endpoints con grandes datasets

---

## 8. Anexos

### 8.1 Glosario de Términos

- **RFM:** Recency, Frequency, Monetary - Modelo de segmentación de clientes
- **Lift:** Métrica de reglas de asociación que mide mejora sobre probabilidad base
- **Soporte:** Frecuencia con la que aparece una combinación de productos
- **Confianza:** Probabilidad condicional P(B|A) en reglas de asociación
- **IQR:** Interquartile Range - Rango intercuartílico para detección de outliers
- **DAG:** Directed Acyclic Graph - Pipeline de Airflow
- **KPI:** Key Performance Indicator - Indicador clave de desempeño

### 8.2 Estructura de Archivos

```
reports/
├── cache/
│   ├── transactions.parquet          # Transacciones crudas
│   ├── transactions_transformed.parquet  # Transacciones transformadas
│   ├── categories.parquet            # Categorías
│   └── product_category.parquet      # Relación producto-categoría
├── graficas/
│   ├── grafica_ventas_diarias.png
│   ├── grafica_segmentacion_*.png (4 gráficas)
│   ├── grafica_reglas_asociacion_*.png (4 gráficas)
│   └── ... (18+ visualizaciones)
├── ventas_diarias.csv
├── top_productos.csv
├── top_clientes.csv
├── frecuencia_clientes.csv
├── segmentacion_clientes.csv
├── reglas_asociacion.csv
└── ... (15+ archivos CSV)
```

### 8.3 Referencias

- **Market Basket Analysis:** Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules.
- **RFM Analysis:** Hughes, A. M. (1994). Strategic database marketing.
- **Airflow Best Practices:** Apache Airflow Documentation (2024)
- **Vue.js 3:** Official Vue.js Documentation (2024)
