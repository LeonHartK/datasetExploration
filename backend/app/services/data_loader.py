import pandas as pd
from pathlib import Path
from flask import current_app

class DataLoaderService:
    """Servicio para cargar y procesar datos de los CSVs"""

    def __init__(self):
        self.reports_dir = current_app.config['REPORTS_DIR']

    def load_csv(self, filename, limit=None):
        """
        Carga un archivo CSV y lo convierte a formato JSON

        Args:
            filename (str): Nombre del archivo CSV
            limit (int, optional): Número máximo de filas a retornar

        Returns:
            list: Lista de diccionarios con los datos
        """
        try:
            file_path = self.reports_dir / filename

            if not file_path.exists():
                raise FileNotFoundError(f"El archivo {filename} no existe")

            # Leer CSV
            df = pd.read_csv(file_path)

            # Aplicar límite si se especifica
            if limit:
                df = df.head(limit)

            # Convertir a JSON-friendly format
            data = df.to_dict(orient='records')

            return data

        except Exception as e:
            current_app.logger.error(f"Error cargando {filename}: {str(e)}")
            raise

    def get_csv_info(self, filename):
        """Obtiene información básica de un CSV sin cargarlo completamente"""
        try:
            file_path = self.reports_dir / filename

            if not file_path.exists():
                raise FileNotFoundError(f"El archivo {filename} no existe")

            # Leer solo las primeras filas para obtener info
            df = pd.read_csv(file_path, nrows=5)

            return {
                "filename": filename,
                "columns": df.columns.tolist(),
                "sample_data": df.to_dict(orient='records')
            }

        except Exception as e:
            current_app.logger.error(f"Error obteniendo info de {filename}: {str(e)}")
            raise
