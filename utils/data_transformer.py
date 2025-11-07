"""
Módulo para transformar datos de transacciones al formato correcto
Extrae métricas reales desde las columnas de productos
"""

import pandas as pd
import numpy as np
from typing import List


def extract_transaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae características reales de las transacciones

    Args:
        df: DataFrame con estructura:
           [fecha|tipo1|id1|productos1|tipo2|id2|productos2|...]

    Returns:
        DataFrame transformado con métricas calculadas
    """
    print("TRANSFORMANDO DATOS DE TRANSACCIONES")
    print("=" * 70)

    # Identificar estructura
    print(f"\nColumnas originales: {len(df.columns)}")
    print(f"Primeras columnas: {list(df.columns[:5])}")

    # Las columnas impares (después de fecha) son IDs
    # Las columnas pares son listas de productos

    transactions = []

    for idx, row in df.iterrows():
        # Obtener fecha (primera columna)
        fecha = row.iloc[0]

        # Procesar cada tipo de transacción (cada 3 columnas después de fecha)
        # Estructura: tipo|id|productos|tipo|id|productos|...
        for i in range(1, len(row), 3):
            if i + 2 >= len(row):
                break

            tipo = row.iloc[i]
            trans_id = row.iloc[i + 1]
            productos_str = row.iloc[i + 2]

            # Verificar que haya datos
            if pd.isna(tipo) or pd.isna(trans_id):
                continue

            # Parsear productos (si existen)
            productos = []
            num_productos = 0

            if pd.notna(productos_str):
                productos = str(productos_str).strip().split()
                num_productos = len(productos)

            transactions.append(
                {
                    "fecha": fecha,
                    "tipo_transaccion": int(tipo) if not pd.isna(tipo) else None,
                    "persona_id": int(trans_id) if not pd.isna(trans_id) else None,
                    "productos_str": productos_str,
                    "productos_list": productos,
                    "num_productos": num_productos,
                    "tiene_productos": num_productos > 0,
                }
            )

    df_transformed = pd.DataFrame(transactions)

    print(f"\n✓ Transacciones procesadas: {len(df_transformed):,}")
    print(f"\nColumnas transformadas:")
    for col in df_transformed.columns:
        print(f"  • {col}")

    return df_transformed


def get_product_frequency(
    df_transformed: pd.DataFrame, top_n: int = 20
) -> pd.DataFrame:
    """
    Calcula frecuencia de productos

    Args:
        df_transformed: DataFrame transformado con columna 'productos_list'
        top_n: Número de productos top a retornar

    Returns:
        DataFrame con productos y sus frecuencias
    """
    print(f"\nCALCULANDO FRECUENCIA DE PRODUCTOS (Top {top_n})")
    print("=" * 70)

    # Expandir listas de productos
    all_products = []
    for productos_list in df_transformed["productos_list"]:
        if productos_list:
            all_products.extend(productos_list)

    # Contar frecuencias
    product_counts = pd.Series(all_products).value_counts()

    # Crear DataFrame
    freq_df = pd.DataFrame(
        {
            "producto_id": product_counts.index,
            "frecuencia": product_counts.values,
            "porcentaje": (product_counts.values / product_counts.sum() * 100).round(2),
        }
    )

    print(f"\n✓ Productos únicos encontrados: {len(freq_df):,}")
    print(f"✓ Total de items vendidos: {product_counts.sum():,}")
    print(f"\nTop {top_n} productos más vendidos:")
    print(freq_df.head(top_n).to_string(index=False))

    return freq_df


def analyze_products_per_transaction(df_transformed: pd.DataFrame) -> dict:
    """
    Analiza estadísticas de productos por transacción

    Args:
        df_transformed: DataFrame transformado

    Returns:
        Diccionario con estadísticas
    """
    print("\nESTADÍSTICAS: PRODUCTOS POR TRANSACCIÓN")
    print("=" * 70)

    # Filtrar solo transacciones con productos
    df_with_products = df_transformed[df_transformed["tiene_productos"]]

    num_productos = df_with_products["num_productos"]

    stats = {
        "total_transacciones": len(df_transformed),
        "transacciones_con_productos": len(df_with_products),
        "pct_con_productos": len(df_with_products) / len(df_transformed) * 100,
        "media": num_productos.mean(),
        "mediana": num_productos.median(),
        "moda": (
            num_productos.mode().values[0] if len(num_productos.mode()) > 0 else None
        ),
        "desv_std": num_productos.std(),
        "min": num_productos.min(),
        "max": num_productos.max(),
        "Q1": num_productos.quantile(0.25),
        "Q3": num_productos.quantile(0.75),
        "IQR": num_productos.quantile(0.75) - num_productos.quantile(0.25),
    }

    # Detectar outliers
    IQR = stats["IQR"]
    lower_bound = stats["Q1"] - 1.5 * IQR
    upper_bound = stats["Q3"] + 1.5 * IQR

    outliers = df_with_products[
        (num_productos < lower_bound) | (num_productos > upper_bound)
    ]

    stats["outliers_count"] = len(outliers)
    stats["outliers_pct"] = len(outliers) / len(df_with_products) * 100
    stats["outlier_lower_bound"] = lower_bound
    stats["outlier_upper_bound"] = upper_bound

    # Imprimir resultados
    print("\nMEDIDAS DE TENDENCIA CENTRAL")
    print(f"  • Media:    {stats['media']:.2f} productos/transacción")
    print(f"  • Mediana:  {stats['mediana']:.2f} productos/transacción")
    print(f"  • Moda:     {stats['moda']} productos")

    print("\nMEDIDAS DE DISPERSIÓN")
    print(f"  • Desviación estándar: {stats['desv_std']:.2f}")
    print(f"  • Rango: {stats['min']:.0f} - {stats['max']:.0f} productos")
    print(f"  • Q1: {stats['Q1']:.2f}")
    print(f"  • Q3: {stats['Q3']:.2f}")
    print(f"  • IQR: {stats['IQR']:.2f}")

    print("\nOUTLIERS (Transacciones anormales)")
    print(f"  • Límite inferior: {stats['outlier_lower_bound']:.2f}")
    print(f"  • Límite superior: {stats['outlier_upper_bound']:.2f}")
    print(
        f"  • Outliers detectados: {stats['outliers_count']:,} ({stats['outliers_pct']:.2f}%)"
    )

    if stats["outliers_count"] > 0:
        print(f"\n  Ejemplos de transacciones outliers:")
        print(
            outliers[["tipo_transaccion", "persona_id", "num_productos"]]
            .head(10)
            .to_string(index=False)
        )

    return stats


def analyze_by_transaction_type(df_transformed: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza métricas por tipo de transacción

    Args:
        df_transformed: DataFrame transformado

    Returns:
        DataFrame con estadísticas por tipo
    """
    print("\nESTADÍSTICAS POR TIPO DE TRANSACCIÓN")
    print("=" * 70)

    # Agrupar por tipo
    stats_by_type = (
        df_transformed.groupby("tipo_transaccion")
        .agg(
            {
                "persona_id": "count",
                "num_productos": ["mean", "median", "std", "min", "max"],
                "tiene_productos": "sum",
            }
        )
        .round(2)
    )

    stats_by_type.columns = [
        "_".join(col).strip() for col in stats_by_type.columns.values
    ]
    stats_by_type = stats_by_type.rename(
        columns={
            "persona_id_count": "total_transacciones",
            "num_productos_mean": "media_productos",
            "num_productos_median": "mediana_productos",
            "num_productos_std": "std_productos",
            "num_productos_min": "min_productos",
            "num_productos_max": "max_productos",
            "tiene_productos_sum": "con_productos",
        }
    )

    stats_by_type["pct_con_productos"] = (
        stats_by_type["con_productos"] / stats_by_type["total_transacciones"] * 100
    ).round(2)

    print(stats_by_type.to_string())

    return stats_by_type


# Alias para compatibilidad
transform_transactions_data = extract_transaction_features
