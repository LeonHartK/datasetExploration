"""
Script para verificar la unicidad de las columnas numéricas
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.data_loader import load_transactions
from utils.config import TRANSACTIONS_DIR

print("Cargando transacciones (muestra)...")
df = load_transactions(TRANSACTIONS_DIR, sample_size=4)  # Solo 4 archivos

print(f"\nTotal de registros: {len(df):,}")
print(f"Columnas: {list(df.columns)}\n")

# Verificar unicidad de columnas numéricas
numeric_cols = df.select_dtypes(include=["number"]).columns

print("ANÁLISIS DE UNICIDAD:")
print("=" * 70)
for col in numeric_cols:
    n_unique = df[col].nunique()
    n_total = len(df)
    unique_pct = n_unique / n_total * 100

    print(f"\nColumna: {col}")
    print(f"  • Total valores: {n_total:,}")
    print(f"  • Valores únicos: {n_unique:,}")
    print(f"  • Porcentaje único: {unique_pct:.2f}%")

    # Determinar tipo
    if df[col].std() == 0:
        tipo = "CONSTANTE"
    elif unique_pct > 95:
        tipo = "ID (alta unicidad)"
    elif unique_pct > 50:
        tipo = "CATEGÓRICA (media unicidad)"
    else:
        tipo = "VARIABLE (baja unicidad)"

    print(f"  • Clasificación sugerida: {tipo}")

    # Mostrar algunos valores
    print(f"  • Muestra valores: {df[col].head(5).tolist()}")
