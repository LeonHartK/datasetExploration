"""
Módulo para carga de datos
Funciones para cargar y preparar datasets
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List
from .config import SEPARATOR, ENCODING


def load_categories(file_path: Path) -> pd.DataFrame:
    """
    Cargar archivo de categorías
    
    Args:
        file_path: Ruta al archivo de categorías
        
    Returns:
        DataFrame con categorías
    """
    print("CARGANDO CATEGORÍAS")
    
    df = pd.read_csv(
        file_path, 
        sep=SEPARATOR, 
        names=['CategoryID', 'CategoryName'],
        encoding=ENCODING
    )
    
    print(f"Categorías cargadas: {len(df)} registros")
    print(f"\nPrimeras categorías:")
    print(df.head(10))
    
    return df


def load_product_category(file_path: Path) -> pd.DataFrame:
    """
    Cargar archivo de productos y categorías
    
    Args:
        file_path: Ruta al archivo de producto-categoría
        
    Returns:
        DataFrame con productos y categorías
    """
    print("CARGANDO PRODUCTO-CATEGORÍA")
    
    df = pd.read_csv(file_path, sep=SEPARATOR)
    
    print(f"Productos cargados: {len(df)} registros")
    print(f"\nColumnas: {list(df.columns)}")
    print(f"\nPrimeros registros:")
    print(df.head())
    
    return df


def load_transactions(
    transactions_dir: Path, 
    sample_size: Optional[int] = None,
    file_pattern: str = '*.csv'
) -> pd.DataFrame:
    """
    Cargar todos los archivos de transacciones
    
    Args:
        transactions_dir: Directorio con archivos de transacciones
        sample_size: Número de archivos a cargar (None = todos)
        file_pattern: Patrón de archivos a buscar
        
    Returns:
        DataFrame con todas las transacciones
    """
    print("CARGANDO TRANSACCIONES")
    
    transaction_files = sorted(Path(transactions_dir).glob(file_pattern))
    
    if sample_size:
        transaction_files = transaction_files[:sample_size]
    
    print(f"Archivos encontrados: {len(transaction_files)}")
    
    dfs = []
    errors = []
    
    for i, file in enumerate(transaction_files, 1):
        try:
            df = pd.read_csv(file, sep=SEPARATOR)
            dfs.append(df)
            if i % 50 == 0:
                print(f"  Procesados: {i}/{len(transaction_files)}")
        except Exception as e:
            error_msg = f"Error en {file.name}: {e}"
            errors.append(error_msg)
            print(f"  {error_msg}")
    
    if not dfs:
        raise ValueError("No se pudieron cargar transacciones")
    
    result = pd.concat(dfs, ignore_index=True)
    
    print(f"\nTotal transacciones cargadas: {len(result):,}")
    print(f"Columnas: {list(result.columns)}")
    
    if errors:
        print(f"\nArchivos con errores: {len(errors)}")
    
    return result


def load_all_data(
    categories_path: Path,
    product_category_path: Path,
    transactions_dir: Path,
    sample_transactions: Optional[int] = None
) -> dict:
    """
    Cargar todos los datasets del proyecto
    
    Args:
        categories_path: Ruta al archivo de categorías
        product_category_path: Ruta al archivo de producto-categoría
        transactions_dir: Directorio con transacciones
        sample_transactions: Número de archivos de transacciones a cargar
        
    Returns:
        Diccionario con todos los DataFrames cargados
    """
    return {
        'categories': load_categories(categories_path),
        'product_category': load_product_category(product_category_path),
        'transactions': load_transactions(transactions_dir, sample_transactions)
    }