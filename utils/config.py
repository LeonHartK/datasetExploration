"""
Configuración global del proyecto
Rutas, constantes y parámetros de configuración
"""

from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'DataSet'
PRODUCTS_DIR = DATA_DIR / 'Products'
TRANSACTIONS_DIR = DATA_DIR / 'Transactions'
REPORTS_DIR = BASE_DIR / 'reports'
NOTEBOOKS_DIR = BASE_DIR / 'notebooks'
SCRIPTS_DIR = BASE_DIR / 'scripts'
UTILS_DIR = BASE_DIR / 'utils'

# Crear directorios si no existen
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Configuración de archivos
FILES_CONFIG = {
    'categories': 'Categories.csv',
    'product_category': 'ProductCategory.csv'
}

# Configuración de separadores
SEPARATOR = '|'

# Configuración de encoding
ENCODING = 'utf-8'

# Configuración de visualización
DISPLAY_TOP_N = 20  # Número de registros a mostrar en frecuencias

# Configuración de análisis
OUTLIER_THRESHOLD = 1.5  # Factor para detección de outliers (IQR)