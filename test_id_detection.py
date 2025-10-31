"""
Script de prueba para demostrar la detección de columnas ID
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Agregar directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.statistics import descriptive_statistics_numeric

print("=" * 70)
print("PRUEBA DE DETECCIÓN DE COLUMNAS ID Y CONSTANTES")
print("=" * 70)

# Crear dataset de prueba con diferentes tipos de columnas
np.random.seed(42)
n = 100

df_test = pd.DataFrame(
    {
        # 1. Variable constante (tipo transacción)
        "102": [102] * n,
        # 2. Variable constante (otro tipo transacción)
        "103": [103] * n,
        # 3. ID secuencial (simula IDs de transacciones)
        "530": np.arange(1, n + 1),
        # 4. ID con huecos (simula customer IDs)
        "customer_id": np.random.choice(range(1, 1000), size=n, replace=False),
        # 5. Variable normal con outliers (precio)
        "precio": np.concatenate(
            [
                np.random.normal(30, 10, 95),  # Precios normales
                [100, 150, 200, 180, 120],  # Outliers
            ]
        ),
        # 6. Variable normal sin outliers (cantidad)
        "cantidad": np.random.randint(1, 10, n),
        # 7. Variable continua normal (rating)
        "rating": np.random.uniform(1, 5, n),
    }
)

print("\nDATASET DE PRUEBA:")
print(f"  • Total registros: {len(df_test)}")
print(f"  • Columnas: {list(df_test.columns)}")
print("\nPrimeras filas:")
print(df_test.head(10))
print("\n" + "=" * 70)

# Ejecutar análisis
stats = descriptive_statistics_numeric(df_test, "TEST")

print("\n" + "=" * 70)
print("RESUMEN FINAL POR TIPO")
print("=" * 70)

if stats is not None:
    # Agrupar por tipo
    for tipo in ["Constante", "ID", "Variable"]:
        tipo_df = stats[stats["Tipo"] == tipo]
        if len(tipo_df) > 0:
            print(f"\n{tipo.upper()}S:")
            print(
                tipo_df[["Variable", "Media", "Desv.Std", "N_Outliers"]].to_string(
                    index=False
                )
            )
