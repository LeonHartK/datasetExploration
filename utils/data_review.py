"""
Módulo para revisión inicial de datasets
Funciones para inspección básica de datos
"""

import pandas as pd
import numpy as np


def initial_review(df: pd.DataFrame, name: str = "Dataset") -> pd.DataFrame:
    """
    Revisión inicial del dataset
    
    Incluye:
    - Estructura básica
    - Número de registros y columnas
    - Tipos de datos
    - Valores faltantes
    - Duplicados
    
    Args:
        df: DataFrame a analizar
        name: Nombre del dataset para mostrar
        
    Returns:
        DataFrame con información detallada por columna
    """
    print(f"REVISIÓN INICIAL: {name}")
    
    # Estructura básica
    print(f"\nESTRUCTURA")
    print(f"  • Registros: {len(df):,}")
    print(f"  • Columnas: {len(df.columns)}")
    print(f"  • Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Tipos de datos
    print(f"\nTIPOS DE DATOS")
    tipo_counts = df.dtypes.value_counts()
    for dtype, count in tipo_counts.items():
        print(f"  • {dtype}: {count} columnas")
    
    print(f"\nDetalle por columna:")
    info_df = pd.DataFrame({
        'Tipo': df.dtypes,
        'No Nulos': df.count(),
        'Nulos': df.isnull().sum(),
        '% Nulos': (df.isnull().sum() / len(df) * 100).round(2)
    })
    print(info_df)
    
    # Duplicados
    print(f"\nDUPLICADOS")
    duplicates = df.duplicated().sum()
    print(f"  • Filas duplicadas: {duplicates:,} ({duplicates/len(df)*100:.2f}%)")
    
    # Primeras filas
    print(f"\nMUESTRA DE DATOS")
    print(df.head())
    
    return info_df


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Obtener resumen rápido del dataset
    
    Args:
        df: DataFrame a resumir
        
    Returns:
        Diccionario con métricas básicas
    """
    return {
        'n_rows': len(df),
        'n_columns': len(df.columns),
        'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'n_duplicates': df.duplicated().sum(),
        'pct_duplicates': (df.duplicated().sum() / len(df) * 100),
        'n_nulls': df.isnull().sum().sum(),
        'pct_nulls': (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100),
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict()
    }


def check_data_quality(df: pd.DataFrame, name: str = "Dataset") -> dict:
    """
    Verificar calidad de datos
    
    Args:
        df: DataFrame a verificar
        name: Nombre del dataset
        
    Returns:
        Diccionario con indicadores de calidad
    """
    quality_report = {
        'dataset_name': name,
        'total_records': len(df),
        'total_columns': len(df.columns),
        'columns_with_nulls': (df.isnull().sum() > 0).sum(),
        'pct_complete': ((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100),
        'has_duplicates': df.duplicated().any(),
        'n_duplicates': df.duplicated().sum()
    }
    
    # Columnas con alta proporción de nulos
    high_null_cols = df.columns[df.isnull().sum() / len(df) > 0.5].tolist()
    quality_report['high_null_columns'] = high_null_cols
    
    return quality_report