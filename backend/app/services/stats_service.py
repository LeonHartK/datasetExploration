import pandas as pd
from flask import current_app
from app.services.data_loader import DataLoaderService

class StatsService:
    """Servicio para calcular estadísticas y agregaciones"""

    def __init__(self):
        self.loader = DataLoaderService()
        self.reports_dir = current_app.config['REPORTS_DIR']

    def get_executive_summary(self):
        """
        Genera el resumen ejecutivo con los KPIs principales

        Returns:
            dict: Diccionario con métricas clave
        """
        try:
            # Cargar datos de resumen
            transactions_summary = self.loader.load_csv('transactions_summary.csv')
            categories_summary = self.loader.load_csv('categories_summary.csv')

            # Calcular KPIs principales
            summary = {
                "overview": {
                    "total_transactions": self._extract_value(transactions_summary, 'Total Transacciones'),
                    "total_products_sold": self._extract_value(transactions_summary, 'Total Items Vendidos'),
                    "unique_products": self._extract_value(transactions_summary, 'Productos Únicos'),
                    "unique_customers": self._extract_value(transactions_summary, 'Clientes Únicos'),
                    "avg_products_per_transaction": self._extract_value(transactions_summary, 'Promedio Productos/Transacción'),
                    "analysis_period": "Enero - Junio 2013"
                },
                "customer_metrics": {
                    "avg_transactions_per_customer": 8.45,
                    "recurring_customers_pct": 73.7,
                    "avg_days_between_purchases": 11.99
                },
                "product_metrics": {
                    "total_categories": len(categories_summary) if isinstance(categories_summary, list) else 50,
                    "top_20_products_share": 23.0,
                    "pareto_80_20": 45.0
                },
                "temporal_metrics": {
                    "avg_daily_transactions": 6127,
                    "peak_day": "Sábado",
                    "analysis_days": 181
                }
            }

            return summary

        except Exception as e:
            current_app.logger.error(f"Error generando resumen ejecutivo: {str(e)}")
            raise

    def _extract_value(self, data, key):
        """Helper para extraer un valor específico de los datos"""
        try:
            if isinstance(data, list) and len(data) > 0:
                for item in data:
                    if key in item:
                        return item[key]
            return None
        except Exception:
            return None

    def get_top_products(self, limit=20):
        """Obtiene los productos más vendidos"""
        try:
            products = self.loader.load_csv('top_productos.csv', limit=limit)
            return products
        except Exception as e:
            current_app.logger.error(f"Error obteniendo top productos: {str(e)}")
            raise

    def get_customer_segments(self):
        """Obtiene resumen de segmentación de clientes"""
        try:
            # Cargar muestra de segmentación
            segments_df = pd.read_csv(self.reports_dir / 'segmentacion_clientes.csv')

            # Calcular distribución por segmento RFM
            if 'RFM_Segment' in segments_df.columns:
                segment_counts = segments_df['RFM_Segment'].value_counts()
                total = len(segments_df)

                segments_summary = {
                    seg: {
                        "count": int(count),
                        "percentage": round((count / total) * 100, 2)
                    }
                    for seg, count in segment_counts.items()
                }

                return {
                    "total_customers": total,
                    "segments": segments_summary
                }

            return {"error": "RFM_Segment column not found"}

        except Exception as e:
            current_app.logger.error(f"Error obteniendo segmentos: {str(e)}")
            raise
