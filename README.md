# Proyecto de Análisis Exploratorio de Datos (EDA)

Análisis de datos de transacciones, productos y categorías.

## Resultados

Esta tarea analiza 1,108,983 transacciones de productos organizados en 50 categorías, con un catálogo de 112,010 productos únicos durante el período enero-junio 2013.

### Hallazgos

- Alta fragmentación de datos: 69.2% de completitud promedio en transacciones
- Duplicados significativos: 16.49% en el catálogo de productos
- Distribución temporal: Pico máximo el 15 de junio de 2013 (9,476 transacciones)
- Estructura compleja: 5 tipos de transacciones con diferentes niveles de detalle

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

### Variables Numéricas 

#### Variables constantes

Variables: 102, 103, 107, 110

- Desviación estándar: 0.00
- Varianza: 0.00
- Interpretación: Identificadores categóricos mal tipificados

#### Variables con Distribución

| Variable | Media | Mediana | Desv. Std | Rango | Outliers |
|----------|-------|---------|-----------|-------|----------|
| `530` | 505,465 | 501,800 | 290,959 | 1,009,509 | 0% |
| `198` | 500,854 | 498,747 | 291,346 | 1,009,491 | 0% |
| `4235` | 496,342 | 490,240 | 290,027 | 1,009,496 | 0% |
| `1023` | 505,306 | 504,414 | 295,122 | 1,009,453 | 0% |

- Distribución uniforme: Media ≈ Mediana indica distribución simétrica
- Sin outliers detectados: Datos limpios sin valores extremos
- Rango amplio: IDs secuenciales de 0 a ~1 millón
- Alta desviación estándar: Cobertura completa del rango de IDs

### Variables Categóricas Con Patrones Identificados

#### Distribución temporal

- Días analizados: 181 días únicos
- Promedio diario: 6,127 transacciones/día
- Día pico: 2013-06-15 (9,476 transacciones) - 54.7% sobre la media
- Día mínimo: ~2,000 transacciones (estimado)

#### Productos por Transacción:

| Nivel | Valores Únicos | Completitud | Avg. Productos |
|-------|----------------|-------------|----------------|
| Nivel 1 (`20 3 1`) | 227,538 | 28.34% | 1-3 items |
| Nivel 2 (`21 5...`) | 336,053 | 36.71% | 5-10 items |
| Nivel 3 (`22 16...`) | 207,242 | 22.96% | 8-11 items |
| Nivel 4 (`129 53...`) | 116,534 | 11.99% | 10-13 items |

- Jerarquía de transacciones por tamaño de canasta
- Mayor completitud en transacciones medianas (nivel 2)
- Menor completitud en transacciones grandes (nivel 4)

### Top Productos Más Vendidos:

```
Nivel 1: Producto 49 (3,434 transacciones - 1.09%)
Nivel 2: Producto 125 (1,239 transacciones - 0.30%)
Nivel 3: Producto 4 (913 transacciones - 0.36%)
Nivel 4: Producto 36 (434 transacciones - 0.33%)
```

## Calidad de Datos

| Dataset | Completitud | Duplicados | Nulos | Calificación |
|---------|-------------|------------|-------|--------------|
| Categorías | 100% | 0% | 0% | Excelente |
| Productos | 100% | 16.49% | 0% | Buena pero requiere limpieza |
| Transacciones | 30.77% | 0.00% | 69.23% | Regular con estructura fragmentada

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

Los reportes se guardan en la carpeta `reports/`:
- `estadisticas_numericas.csv`: Estadísticas de variables numéricas
- `categories_summary.csv`: Resumen del dataset de categorías
- `product_category_summary.csv`: Resumen del dataset de productos
- `transactions_summary.csv`: Resumen del dataset de transacciones

## Configuración

Editar `utils/config.py` para personalizar:
- Rutas de archivos
- Separadores de CSV
- Umbral de detección de outliers
- Número de registros a mostrar en frecuencias

## Notas

- Los archivos de transacciones deben estar en formato CSV con separador `|`
- El script puede procesar todos los archivos de transacciones o una muestra
- Los reportes se generan automáticamente en la carpeta `reports/`