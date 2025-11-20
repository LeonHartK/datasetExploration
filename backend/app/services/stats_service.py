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
            # Cargar datos desde archivos CSV
            ventas_diarias = pd.read_csv(self.reports_dir / 'ventas_diarias.csv')
            ventas_dia_semana = pd.read_csv(self.reports_dir / 'ventas_dia_semana.csv')
            top_productos = pd.read_csv(self.reports_dir / 'top_productos.csv')
            customer_behavior = pd.read_csv(self.reports_dir / 'customer_behavior_summary.csv')
            tiempo_entre_compras = pd.read_csv(self.reports_dir / 'tiempo_entre_compras.csv')
            frecuencia_clientes = pd.read_csv(self.reports_dir / 'frecuencia_clientes.csv')

            # Calcular totales
            total_transactions = int(ventas_diarias['total_transacciones'].sum())
            total_products_sold = int(ventas_diarias['total_productos'].sum())
            unique_products = len(top_productos)
            avg_products_per_transaction = round(total_products_sold / total_transactions, 2)

            # Métricas de clientes
            customer_data = customer_behavior.to_dict('records')[0] if len(customer_behavior) > 0 else {}
            unique_customers = int(customer_data.get('total_clientes', 0))
            avg_transactions = round(customer_data.get('promedio_transacciones', 0), 2)

            # Calcular clientes recurrentes (más de 1 transacción)
            clientes_recurrentes = len(frecuencia_clientes[frecuencia_clientes['num_transacciones'] > 1])
            recurring_pct = round((clientes_recurrentes / unique_customers) * 100, 1) if unique_customers > 0 else 0

            # Promedio de días entre compras
            avg_days_between = round(tiempo_entre_compras['promedio_dias'].mean(), 2)

            # Métricas temporales
            avg_daily_trans = int(ventas_diarias['total_transacciones'].mean())
            peak_day_row = ventas_dia_semana.loc[ventas_dia_semana['total_transacciones'].idxmax()]
            peak_day = peak_day_row['dia_semana']
            analysis_days = len(ventas_diarias)

            # Métricas de productos
            top_20_share = round(top_productos.head(20)['porcentaje'].sum(), 1)

            # Encontrar cuántos productos representan el 80%
            cumsum = 0
            pareto_count = 0
            for _, row in top_productos.iterrows():
                cumsum += row['porcentaje']
                pareto_count += 1
                if cumsum >= 80:
                    break
            pareto_pct = round((pareto_count / len(top_productos)) * 100, 1)

            summary = {
                "overview": {
                    "total_transactions": total_transactions,
                    "total_products_sold": total_products_sold,
                    "unique_products": unique_products,
                    "unique_customers": unique_customers,
                    "avg_products_per_transaction": avg_products_per_transaction,
                    "analysis_period": "Enero - Junio 2013"
                },
                "customer_metrics": {
                    "avg_transactions_per_customer": avg_transactions,
                    "recurring_customers_pct": recurring_pct,
                    "avg_days_between_purchases": avg_days_between
                },
                "product_metrics": {
                    "total_categories": unique_products,
                    "top_20_products_share": top_20_share,
                    "pareto_80_20": pareto_pct
                },
                "temporal_metrics": {
                    "avg_daily_transactions": avg_daily_trans,
                    "peak_day": peak_day,
                    "analysis_days": analysis_days
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
