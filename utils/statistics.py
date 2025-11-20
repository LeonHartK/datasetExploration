"""
Módulo para estadísticas descriptivas
Análisis de variables numéricas y categóricas
"""

import pandas as pd
import numpy as np
from typing import Optional, List
from .config import DISPLAY_TOP_N, OUTLIER_THRESHOLD


def _is_id_column(series: pd.Series, col_name: str) -> bool:
    """
    Detectar si una columna es un identificador (ID)

    Criterios:
    - Alta cardinalidad (>80% de valores únicos)
    - Valores secuenciales o uniformemente distribuidos
    - Nombre sugiere ID

    Args:
        series: Serie de pandas a evaluar
        col_name: Nombre de la columna

    Returns:
        True si parece ser un ID, False en caso contrario
    """
    # Evitar división por cero
    if len(series) == 0:
        return False

    # 1. Criterio de cardinalidad: >80% de valores únicos
    cardinality = series.nunique() / len(series)

    # 2. Criterio de nombre: contiene palabras clave de ID
    name_lower = str(col_name).lower()
    id_keywords = ["id", "code", "key", "number", "num", "ref", "sku"]
    has_id_name = any(keyword in name_lower for keyword in id_keywords)

    # 3. Criterio de secuencialidad: valores parecen secuenciales
    # Verificar si los valores son principalmente enteros consecutivos o uniformes
    is_sequential = False
    try:
        # Si todos son enteros y el rango es similar al número de valores únicos
        if series.dropna().apply(lambda x: float(x).is_integer()).all():
            value_range = series.max() - series.min()
            unique_count = series.nunique()
            # Si el rango es similar al número de valores únicos, es secuencial
            is_sequential = abs(value_range - unique_count) < unique_count * 0.2
    except:
        pass

    # Decisión: es ID si cumple alta cardinalidad Y (tiene nombre de ID O es secuencial)
    return cardinality > 0.8 and (has_id_name or is_sequential)


def descriptive_statistics_numeric(
    df: pd.DataFrame, name: str = "Dataset", columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Estadísticas descriptivas para variables numéricas

    Incluye:
    - Medidas de tendencia central (media, mediana, moda)
    - Medidas de dispersión (desviación estándar, varianza, rango)
    - Percentiles (Q1, Q2, Q3)
    - Detección de valores atípicos (outliers)

    Args:
        df: DataFrame a analizar
        name: Nombre del dataset
        columns: Lista de columnas específicas a analizar (None = todas)

    Returns:
        DataFrame con resumen estadístico
    """
    print(f"ESTADÍSTICAS DESCRIPTIVAS NUMÉRICAS: {name}")

    # Seleccionar columnas numéricas
    if columns:
        numeric_cols = [
            col
            for col in columns
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col])
        ]
    else:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) == 0:
        print("No hay columnas numéricas en este dataset")
        return None

    # Detectar y clasificar columnas
    constant_vars = []
    id_like_cols = []
    analysis_cols = []

    for col in numeric_cols:
        # 1. Detectar variables constantes (sin variación)
        if df[col].std() == 0 or df[col].nunique() == 1:
            constant_vars.append(col)
        # 2. Detectar columnas tipo ID (alta cardinalidad, valores únicos)
        elif _is_id_column(df[col], col):
            id_like_cols.append(col)
        # 3. Variables normales para análisis
        else:
            analysis_cols.append(col)

    print(f"\nColumnas numéricas encontradas: {len(numeric_cols)}")
    print(f"{list(numeric_cols)}\n")

    # Advertencias
    if constant_vars:
        print(f"️ADVERTENCIA: Variables constantes detectadas (sin variación)")
        print(f"   Estas variables probablemente son identificadores categóricos:")
        print(f"   {constant_vars}")
        print(f"   Se excluirán del análisis estadístico detallado.\n")

    if id_like_cols:
        print(f"️  INFORMACIÓN: Columnas tipo ID detectadas")
        print(f"   Estas columnas parecen ser identificadores únicos:")
        print(f"   {id_like_cols}")
        print(
            f"   Se excluirán del análisis de outliers (no tiene sentido buscar outliers en IDs).\n"
        )

    if analysis_cols:
        print(f"Variables para análisis estadístico: {len(analysis_cols)}")
        print(f"  {analysis_cols}\n")
    else:
        print(f"️  No hay variables numéricas válidas para análisis estadístico.\n")

    stats_list = []

    for col in numeric_cols:
        # Clasificar tipo de variable
        is_constant = col in constant_vars
        is_id = col in id_like_cols

        # Etiqueta visual
        if is_constant:
            print(f"Variable: {col} [CONSTANTE - Posible identificador categórico]")
        elif is_id:
            print(f"Variable: {col} [ID - Identificador único]")
        else:
            print(f"Variable: {col}")

        # Estadísticas básicas
        mean_val = df[col].mean()
        median_val = df[col].median()
        mode_val = df[col].mode().values[0] if len(df[col].mode()) > 0 else np.nan

        print(f"\nMEDIDAS DE TENDENCIA CENTRAL")
        print(f"  • Media:    {mean_val:.2f}")
        print(f"  • Mediana:  {median_val:.2f}")
        print(f"  • Moda:     {mode_val if not pd.isna(mode_val) else 'N/A'}")

        # Medidas de dispersión
        std_val = df[col].std()
        var_val = df[col].var()
        min_val = df[col].min()
        max_val = df[col].max()
        range_val = max_val - min_val

        print(f"\nMEDIDAS DE DISPERSIÓN")
        print(f"  • Desviación estándar: {std_val:.2f}")
        print(f"  • Varianza:            {var_val:.2f}")
        print(f"  • Rango:               {range_val:.2f}")
        print(f"  • Mínimo:              {min_val:.2f}")
        print(f"  • Máximo:              {max_val:.2f}")

        # Percentiles
        print(f"\nPERCENTILES")
        percentiles = df[col].quantile([0.25, 0.50, 0.75])
        Q1 = percentiles[0.25]
        Q2 = percentiles[0.50]
        Q3 = percentiles[0.75]
        IQR = Q3 - Q1

        print(f"  • P25 (Q1): {Q1:.2f}")
        print(f"  • P50 (Q2): {Q2:.2f}")
        print(f"  • P75 (Q3): {Q3:.2f}")
        print(f"  • IQR:      {IQR:.2f}")

        # Detección de outliers (solo para variables normales, no para IDs ni constantes)
        print(f"\nVALORES ATÍPICOS (Método IQR)")

        if is_constant:
            # Variable constante: no tiene sentido buscar outliers
            print(
                f"  ️  No se pueden detectar outliers: variable sin variación (IQR = 0)"
            )
            print(f"  • Todos los valores son: {Q1:.2f}")
            print(f"  • Interpretación: Variable constante (identificador categórico)")
            n_outliers = 0
            pct_outliers = 0.0
            lower_bound = Q1
            upper_bound = Q1
        elif is_id:
            # Variable tipo ID: no tiene sentido buscar outliers en identificadores
            print(
                f"  Análisis de outliers omitido: esta columna es un identificador único"
            )
            print(f"  • Los IDs son valores de referencia, no mediciones")
            print(f"  • Buscar outliers en IDs no tiene sentido estadístico")
            print(
                f"  • Rango de IDs: {min_val:.0f} - {max_val:.0f} ({df[col].nunique():,} valores únicos)"
            )
            n_outliers = 0
            pct_outliers = 0.0
            lower_bound = np.nan
            upper_bound = np.nan
        else:
            # Variable normal: calcular outliers
            lower_bound = Q1 - OUTLIER_THRESHOLD * IQR
            upper_bound = Q3 + OUTLIER_THRESHOLD * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            n_outliers = len(outliers)
            pct_outliers = n_outliers / len(df) * 100

            print(f"  • Límite inferior: {lower_bound:.2f}")
            print(f"  • Límite superior: {upper_bound:.2f}")
            print(f"  • Outliers detectados: {n_outliers:,} ({pct_outliers:.2f}%)")

        # Clasificar tipo de variable
        var_type = "Constante" if is_constant else ("ID" if is_id else "Variable")

        # Guardar estadísticas
        stats_list.append(
            {
                "Variable": col,
                "Tipo": var_type,
                "Media": mean_val,
                "Mediana": median_val,
                "Moda": mode_val,
                "Desv.Std": std_val,
                "Varianza": var_val,
                "Min": min_val,
                "Max": max_val,
                "Rango": range_val,
                "Q1": Q1,
                "Q2": Q2,
                "Q3": Q3,
                "IQR": IQR,
                "N_Outliers": n_outliers,
                "%_Outliers": pct_outliers,
            }
        )

    # Resumen consolidado
    stats_df = pd.DataFrame(stats_list)
    print("RESUMEN CONSOLIDADO - VARIABLES NUMÉRICAS")
    print(stats_df.to_string(index=False))

    return stats_df


def descriptive_statistics_categorical(
    df: pd.DataFrame,
    name: str = "Dataset",
    columns: Optional[List[str]] = None,
    top_n: int = DISPLAY_TOP_N,
) -> dict:
    """
    Estadísticas descriptivas para variables categóricas

    Incluye:
    - Valores únicos
    - Frecuencias absolutas y relativas
    - Distribución por categorías

    Args:
        df: DataFrame a analizar
        name: Nombre del dataset
        columns: Lista de columnas específicas a analizar (None = todas)
        top_n: Número de categorías más frecuentes a mostrar

    Returns:
        Diccionario con estadísticas por columna
    """
    print(f"ESTADÍSTICAS DESCRIPTIVAS CATEGÓRICAS: {name}")

    # Seleccionar columnas categóricas
    if columns:
        categorical_cols = [col for col in columns if col in df.columns]
    else:
        categorical_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

    if len(categorical_cols) == 0:
        print("No hay columnas categóricas en este dataset")
        return None

    print(f"\nColumnas categóricas encontradas: {len(categorical_cols)}")
    print(f"{list(categorical_cols)}\n")

    results = {}

    for col in categorical_cols:
        print(f"Variable: {col}")

        # Valores únicos
        n_unique = df[col].nunique()
        n_nulls = df[col].isnull().sum()

        print(f"\nINFORMACIÓN GENERAL")
        print(f"  • Valores únicos: {n_unique:,}")
        print(f"  • Valores nulos:  {n_nulls:,}")

        # Frecuencias
        freq = df[col].value_counts()
        freq_rel = df[col].value_counts(normalize=True) * 100

        freq_df = pd.DataFrame({"Frecuencia": freq, "Porcentaje": freq_rel.round(2)})

        print(f"\nFRECUENCIAS (Top {top_n})")
        print(freq_df.head(top_n).to_string())

        # Categoría más frecuente
        print(f"\nMÁS FRECUENTE")
        print(f"  • Categoría: {freq.index[0]}")
        print(f"  • Frecuencia: {freq.values[0]:,} ({freq_rel.values[0]:.2f}%)")

        # Guardar resultados
        results[col] = {
            "n_unique": n_unique,
            "n_nulls": n_nulls,
            "frequencies": freq_df,
            "most_frequent": freq.index[0],
            "most_frequent_count": freq.values[0],
            "most_frequent_pct": freq_rel.values[0],
        }

    return results


def detect_outliers(
    df: pd.DataFrame,
    column: str,
    method: str = "iqr",
    threshold: float = OUTLIER_THRESHOLD,
) -> pd.DataFrame:
    """
    Detectar valores atípicos en una columna específica

    Args:
        df: DataFrame
        column: Nombre de la columna
        method: Método de detección ('iqr' o 'zscore')
        threshold: Umbral para detección

    Returns:
        DataFrame con los outliers detectados
    """
    if method == "iqr":
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    elif method == "zscore":
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        outliers = df[z_scores > threshold]
    else:
        raise ValueError("Método debe ser 'iqr' o 'zscore'")

    return outliers


def correlation_analysis(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """
    Análisis de correlación entre variables numéricas

    Args:
        df: DataFrame
        method: Método de correlación ('pearson', 'spearman', 'kendall')

    Returns:
        Matriz de correlación
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) < 2:
        print("Se necesitan al menos 2 variables numéricas para correlación")
        return None

    corr_matrix = df[numeric_cols].corr(method=method)

    print(f"MATRIZ DE CORRELACIÓN ({method.upper()})")
    print(corr_matrix)

    return corr_matrix
