"""
Clase principal para análisis de datasets
Integra todas las funcionalidades de análisis
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict

from .data_loader import (
    load_categories, 
    load_product_category, 
    load_transactions,
    load_all_data
)
from .data_review import initial_review, get_data_summary, check_data_quality
from .statistics import (
    descriptive_statistics_numeric,
    descriptive_statistics_categorical,
    detect_outliers,
    correlation_analysis
)
from .config import PRODUCTS_DIR, TRANSACTIONS_DIR


class DatasetAnalyzer:
    """
    Clase principal para análisis exploratorio de datos
    
    Atributos:
        categories: DataFrame con categorías
        product_category: DataFrame con productos y categorías
        transactions: DataFrame con transacciones
        merged_data: DataFrame con datos combinados
    """
    
    def __init__(self):
        self.categories = None
        self.product_category = None
        self.transactions = None
        self.merged_data = None
        self._stats_cache = {}
    
    def load_categories(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """Cargar archivo de categorías"""
        if file_path is None:
            file_path = PRODUCTS_DIR / 'Categories.csv'
        
        self.categories = load_categories(file_path)
        return self.categories
    
    def load_product_category(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """Cargar archivo de productos y categorías"""
        if file_path is None:
            file_path = PRODUCTS_DIR / 'ProductCategory.csv'
        
        self.product_category = load_product_category(file_path)
        return self.product_category
    
    def load_transactions(
        self, 
        transactions_dir: Optional[Path] = None, 
        sample_size: Optional[int] = None
    ) -> pd.DataFrame:
        """Cargar archivos de transacciones"""
        if transactions_dir is None:
            transactions_dir = TRANSACTIONS_DIR
        
        self.transactions = load_transactions(transactions_dir, sample_size)
        return self.transactions
    
    def load_all(self, sample_transactions: Optional[int] = None) -> Dict[str, pd.DataFrame]:
        """Cargar todos los datasets"""
        data = load_all_data(
            PRODUCTS_DIR / 'Categories.csv',
            PRODUCTS_DIR / 'ProductCategory.csv',
            TRANSACTIONS_DIR,
            sample_transactions
        )
        
        self.categories = data['categories']
        self.product_category = data['product_category']
        self.transactions = data['transactions']
        
        return data
    
    def review_dataset(self, dataset_name: str) -> pd.DataFrame:
        """
        Realizar revisión inicial de un dataset
        
        Args:
            dataset_name: 'categories', 'product_category', o 'transactions'
        """
        df = self._get_dataset(dataset_name)
        return initial_review(df, dataset_name.upper())
    
    def analyze_numeric(self, dataset_name: str) -> pd.DataFrame:
        """
        Análisis de variables numéricas
        
        Args:
            dataset_name: Nombre del dataset a analizar
        """
        df = self._get_dataset(dataset_name)
        return descriptive_statistics_numeric(df, dataset_name.upper())
    
    def analyze_categorical(self, dataset_name: str) -> dict:
        """
        Análisis de variables categóricas
        
        Args:
            dataset_name: Nombre del dataset a analizar
        """
        df = self._get_dataset(dataset_name)
        return descriptive_statistics_categorical(df, dataset_name.upper())
    
    def get_summary(self, dataset_name: str) -> dict:
        """
        Obtener resumen rápido de un dataset
        
        Args:
            dataset_name: Nombre del dataset
        """
        df = self._get_dataset(dataset_name)
        return get_data_summary(df)
    
    def check_quality(self, dataset_name: str) -> dict:
        """
        Verificar calidad de datos
        
        Args:
            dataset_name: Nombre del dataset
        """
        df = self._get_dataset(dataset_name)
        return check_data_quality(df, dataset_name.upper())
    
    def find_outliers(
        self, 
        dataset_name: str, 
        column: str, 
        method: str = 'iqr'
    ) -> pd.DataFrame:
        """
        Detectar outliers en una columna específica
        
        Args:
            dataset_name: Nombre del dataset
            column: Columna a analizar
            method: Método de detección
        """
        df = self._get_dataset(dataset_name)
        return detect_outliers(df, column, method)
    
    def correlations(self, dataset_name: str, method: str = 'pearson') -> pd.DataFrame:
        """
        Calcular correlaciones entre variables numéricas
        
        Args:
            dataset_name: Nombre del dataset
            method: Método de correlación
        """
        df = self._get_dataset(dataset_name)
        return correlation_analysis(df, method)
    
    def merge_data(self) -> pd.DataFrame:
        """
        Combinar todos los datasets
        
        Returns:
            DataFrame con datos combinados
        """
        if self.transactions is None or self.product_category is None or self.categories is None:
            raise ValueError("Debe cargar todos los datasets primero")
        
        # Merge transacciones con producto-categoría
        merged = self.transactions.merge(
            self.product_category,
            on='v.Code_pr',  # Ajustar según columna real
            how='left'
        )
        
        # Merge con categorías
        merged = merged.merge(
            self.categories,
            on='CategoryID',  # Ajustar según columna real
            how='left'
        )
        
        self.merged_data = merged
        
        print("DATOS COMBINADOS")
        print(f"Total registros: {len(merged):,}")
        print(f"Columnas: {list(merged.columns)}")
        
        return merged
    
    def full_analysis(self, dataset_name: str):
        """
        Realizar análisis completo de un dataset
        
        Args:
            dataset_name: Nombre del dataset a analizar
        """
        print(f"ANÁLISIS COMPLETO: {dataset_name.upper()}")
        
        # Revisión inicial
        self.review_dataset(dataset_name)
        
        # Análisis numérico
        print("\n")
        self.analyze_numeric(dataset_name)
        
        # Análisis categórico
        print("\n")
        self.analyze_categorical(dataset_name)
        
        # Calidad de datos
        print("\n")
        quality = self.check_quality(dataset_name)
        print("\nREPORTE DE CALIDAD")
        for key, value in quality.items():
            print(f"  • {key}: {value}")
    
    def _get_dataset(self, name: str) -> pd.DataFrame:
        """Obtener dataset por nombre"""
        datasets = {
            'categories': self.categories,
            'product_category': self.product_category,
            'transactions': self.transactions,
            'merged': self.merged_data
        }
        
        if name not in datasets:
            raise ValueError(f"Dataset '{name}' no válido. Opciones: {list(datasets.keys())}")
        
        df = datasets[name]
        if df is None:
            raise ValueError(f"Dataset '{name}' no ha sido cargado")
        
        return df
    
    def export_summary(self, output_dir: Path):
        """
        Exportar resumen de análisis a archivos
        
        Args:
            output_dir: Directorio de salida
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        datasets = {
            'categories': self.categories,
            'product_category': self.product_category,
            'transactions': self.transactions
        }
        
        for name, df in datasets.items():
            if df is not None:
                # Guardar resumen
                summary = get_data_summary(df)
                summary_df = pd.DataFrame([summary])
                summary_df.to_csv(output_dir / f'{name}_summary.csv', index=False)
                
                print(f"Resumen de {name} exportado")