# Proyecto de Análisis Exploratorio de Datos (EDA)

Análisis de datos de transacciones, productos y categorías.

## Resultados

Esta tarea analiza **1,108,983 transacciones** de productos organizados en **50 categorías**, con un catálogo de **112,010 productos únicos** durante el período **enero-junio 2013**.

### Hallazgos Clave

- **Comportamiento de compra**: 9.55 productos por transacción en promedio (mediana: 6 productos)
- **Outliers de compra**: 8.09% de transacciones con más de 25 productos (89,733 transacciones anormalmente grandes)
- **Rango de compra**: De 1 a 128 productos por transacción
- **Duplicados en catálogo**: 16.49% (18,473 registros) en el catálogo de productos requiere limpieza
- **4 tipos de transacciones**: 102 (28.3%), 103 (36.7%), 107 (23.0%), 110 (12.0%)
- **Catálogo activo**: 449 productos únicos | 10.59 millones de items vendidos
- **Distribución de productos**: Relativamente uniforme, producto más vendido representa solo 2.84% del total

## Análisis de los datos

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
- Columnas: 13 (5 categóricas, 8 numéricas)
- Completitud promedio: 30.77%

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

### 2. Identificadores de Transacción (Variables Categóricas)

**Nota importante**: Las columnas `102`, `103`, `107`, `110`, `530`, `198`, `4235`, `1023` son **identificadores**, no mediciones.

#### Variables Constantes (Tipos de Transacción)

| Variable | Significado | Valores |
|----------|-------------|---------|
| `102`, `103`, `107`, `110` | Tipo de transacción | Constantes (identificadores categóricos) |

**Interpretación**: Representan 4 tipos diferentes de transacciones en el sistema.

#### IDs de Transacción

| Variable | Valores Únicos | % Unicidad | Significado |
|----------|----------------|------------|-------------|
| `530` | 44,592 | 4.02% | ID de transacción tipo 102 |
| `198` | 64,239 | 5.79% | ID de transacción tipo 103 |
| `4235` | 31,437 | 2.83% | ID de transacción tipo 107 |
| `1023` | 18,144 | 1.64% | ID de transacción tipo 110 |

**Interpretación**: Son códigos de referencia, no valores a promediar. Su baja unicidad indica que se repiten (posiblemente clientes recurrentes o ubicaciones).

### 3. Análisis por Tipo de Transacción

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

### 4. Productos Más Vendidos

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
- **449 productos únicos** en el catálogo activo (mucho mayor que los 50 estimados)
- **Patrón de compra muy diversificado**: Sin dependencia crítica de pocos productos
- **Oportunidad comercial**: Múltiples productos con ventas similares, no hay "estrella" única
- **Diferencias mínimas**: Entre el producto #1 y #10 solo hay 1.17 puntos porcentuales de diferencia

### 5. Distribución Temporal

- **Período**: Enero - Junio 2013 (181 días)
- **Total transacciones**: 1,108,983
- **Promedio diario**: 6,127 transacciones/día
- **Estructura**: Datos organizados en archivos por tipo de transacción (102, 103, 107, 110)

## Calidad de Datos

| Dataset | Completitud | Duplicados | Nulos | Calificación |
|---------|-------------|------------|-------|--------------|
| Categorías | 100% | 0% | 0% | Excelente |
| Productos | 100% | 16.49% | 0% | ️ Buena pero requiere limpieza de duplicados |
| Transacciones (raw) | Variable | 0% | Variable | Estructura compleja pero válida |
| Transacciones (transformadas) | 100% | 0% | 0% | Excelente después de transformación |

**Notas importantes:**

- **Categorías**: Datos perfectos, sin problemas
- **Productos**: 18,473 duplicados (16.49%) requieren limpieza antes de análisis avanzado
- **Transacciones**: Estructura en formato ancho (4 tipos por fila) requiere transformación para análisis correcto
- **Después de transformación**: Los datos de transacciones son consistentes y completos

## Estructura del Proyecto

```
proyecto/
├── data/
│   └── DataSet/
│       ├── Products/
│       │   ├── Categories.csv
│       │   └── ProductCategory.csv
│       └── Transactions/
│           ├── 2013-01-01.csv
│           ├── 2013-01-02.csv
│           └── ...
├── notebooks/
│   └── exploratory_analysis.ipynb
├── reports/
│   ├── estadisticas_numericas.csv
│   └── ...
├── scripts/
│   └── run_analysis.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_review.py
│   ├── statistics.py
│   └── analyzer.py
├── requirements.txt
└── README.md
```

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

## Uso

### Script Principal

Ejecutar el análisis completo desde la línea de comandos:

```bash
python scripts/run_analysis.py
```

## Módulos

### `utils/config.py`
Configuración global del proyecto (rutas, constantes, parámetros).

### `utils/data_loader.py`
Funciones para cargar y preparar datasets:
- `load_categories()`: Cargar categorías
- `load_product_category()`: Cargar productos
- `load_transactions()`: Cargar transacciones
- `load_all_data()`: Cargar todos los datasets

### `utils/data_review.py`
Funciones para revisión inicial de datos:
- `initial_review()`: Revisión completa del dataset
- `get_data_summary()`: Resumen rápido
- `check_data_quality()`: Verificación de calidad

### `utils/statistics.py`
Funciones para estadísticas descriptivas:
- `descriptive_statistics_numeric()`: Análisis de variables numéricas
- `descriptive_statistics_categorical()`: Análisis de variables categóricas
- `detect_outliers()`: Detección de valores atípicos
- `correlation_analysis()`: Análisis de correlación

### `utils/analyzer.py`
Clase principal que integra todas las funcionalidades:
- `DatasetAnalyzer`: Clase para análisis exploratorio completo

## Reportes Generados

Los reportes se guardan automáticamente en la carpeta `reports/`:

- **`productos_por_transaccion.csv`**: Estadísticas descriptivas de cantidad de productos por transacción (media, mediana, outliers)
- **`top_productos.csv`**: Ranking de productos más vendidos con frecuencias y porcentajes
- **`stats_por_tipo_transaccion.csv`**: Análisis comparativo entre los 4 tipos de transacción
- **`categories_summary.csv`**: Resumen del dataset de categorías
- **`product_category_summary.csv`**: Resumen del dataset de productos
- **`transacciones_transformadas_sample.csv`**: Muestra de transacciones transformadas al formato correcto

## Configuración

Se debe editar `utils/config.py` en caso de personalizar:
- Rutas de archivos
- Separadores de CSV
- Umbral de detección de outliers
- Número de registros a mostrar en frecuencias

## Transformación de Datos

### Estructura Original (Formato Ancho)

```
fecha|tipo1|id1|productos1|tipo2|id2|productos2|tipo3|id3|productos3|tipo4|id4|productos4
2013-01-01|102|530|20 3 1|103|198|21 5 189...|107|4235|22 16 12...|110|1023|129 53...
```

### Estructura Transformada (Formato Largo)

```
fecha|tipo_transaccion|id_transaccion|productos_str|num_productos
2013-01-01|102|530|20 3 1|3
2013-01-01|103|198|21 5 189 341 60 32 6 3 50|9
2013-01-01|107|4235|22 16 12 31 102 10 3 34 35 9 33|11
2013-01-01|110|1023|129 53 106 4 29 7 6 5 18 230 50 82 11|13
```

**Ventajas de la transformación:**

- Cada fila = 1 transacción (en lugar de 4)
- Permite análisis estadístico correcto de `num_productos`
- Facilita agregaciones por tipo de transacción
- Permite análisis de productos individuales
- Estructura normalizada estándar

## Notas Importantes

### Sobre el Análisis Correcto

- Los archivos de transacciones están en formato CSV con separador `|`
- El script **transforma automáticamente** los datos al formato correcto
- Los análisis estadísticos se aplican a **variables reales** (num_productos, frecuencias)
- Los reportes se generan automáticamente en la carpeta `reports/`
