"""
Script de prueba: Análisis CORRECTO de transacciones
Demuestra cómo se deben extraer y analizar las métricas reales
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.data_loader import load_transactions
from utils.data_transformer import (
    extract_transaction_features,
    get_product_frequency,
    analyze_products_per_transaction,
    analyze_by_transaction_type,
)
from utils.config import TRANSACTIONS_DIR

print("=" * 70)
print("ANÁLISIS CORRECTO DE TRANSACCIONES")
print("=" * 70)

# 1. Cargar datos originales (muestra MUY pequeña - solo 1 archivo)
print("\n1. CARGANDO DATOS ORIGINALES (MUESTRA PEQUEÑA)...")
df_original = load_transactions(TRANSACTIONS_DIR, sample_size=1)

# Tomar solo las primeras 1000 filas para rapidez
df_original = df_original.head(1000)

print(f"\nDatos originales:")
print(f"  • Registros: {len(df_original):,}")
print(f"  • Columnas: {len(df_original.columns)}")
print(f"\n  Ejemplo de fila:")
print(df_original.head(1).to_string())

# 2. Transformar datos
print("\n\n2. TRANSFORMANDO DATOS...")
df_transformed = extract_transaction_features(df_original)

print(f"\n  Datos transformados (primeras 10 filas):")
print(
    df_transformed[["fecha", "tipo_transaccion", "id_transaccion", "num_productos"]]
    .head(10)
    .to_string(index=False)
)

# 3. Analizar productos por transacción (¡LO QUE REALMENTE IMPORTA!)
print("\n\n3. ANÁLISIS DE PRODUCTOS POR TRANSACCIÓN")
print("=" * 70)
stats = analyze_products_per_transaction(df_transformed)

# 4. Productos más vendidos
print("\n\n4. PRODUCTOS MÁS VENDIDOS")
print("=" * 70)
product_freq = get_product_frequency(df_transformed, top_n=10)

# 5. Análisis por tipo de transacción
print("\n\n5. ANÁLISIS POR TIPO DE TRANSACCIÓN")
print("=" * 70)
stats_by_type = analyze_by_transaction_type(df_transformed)

# 6. COMPARACIÓN: Lo que estabas haciendo vs lo correcto
print("\n\n" + "=" * 70)
print("COMPARACIÓN: ANÁLISIS INCORRECTO vs CORRECTO")
print("=" * 70)

print("\n❌ LO QUE ESTABAS ANALIZANDO (INCORRECTO):")
print("   Variable: 530 (ID de transacción)")
print("   Media: 505,465")
print("   → Esto NO tiene sentido, es solo un número de referencia")

print("\n✅ LO QUE DEBERÍAS ANALIZAR (CORRECTO):")
print("   Variable: num_productos (cantidad de productos por transacción)")
print(f"   Media: {stats['media']:.2f} productos/transacción")
print(f"   Mediana: {stats['mediana']:.2f} productos/transacción")
print(f"   Outliers: {stats['outliers_count']:,} transacciones anormales")
print("   → ¡Esto SÍ tiene sentido estadístico!")

print("\n" + "=" * 70)
print("CONCLUSIÓN")
print("=" * 70)
print(
    """
El análisis correcto debe enfocarse en:
1. ✅ Cantidad de productos por transacción (variable numérica real)
2. ✅ Productos más vendidos (frecuencia de IDs de productos)
3. ✅ Distribución por tipo de transacción
4. ✅ Patrones temporales

NO en:
❌ Promedios de IDs de transacción
❌ Outliers de números de referencia
❌ Estadísticas de columnas constantes
"""
)
