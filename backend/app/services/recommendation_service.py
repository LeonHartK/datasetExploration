"""
Servicio de recomendaciones de productos basado en reglas de asociación
"""
import pandas as pd
from pathlib import Path
from flask import current_app


class RecommendationService:
    def __init__(self):
        self.reports_dir = Path(current_app.config['REPORTS_DIR'])
        self.reglas = None
        self.frecuencia_clientes = None
        self.transacciones = None
        self._load_data()

    def _load_data(self):
        """Carga las reglas de asociación y frecuencia de clientes"""
        try:
            # Cargar reglas de asociación
            reglas_path = self.reports_dir / 'reglas_asociacion.csv'
            if reglas_path.exists():
                self.reglas = pd.read_csv(reglas_path)
                current_app.logger.info(f"Reglas de asociación cargadas: {len(self.reglas)} reglas")

            # Cargar frecuencia de clientes con historial de compras
            freq_path = self.reports_dir / 'frecuencia_clientes.csv'
            if freq_path.exists():
                self.frecuencia_clientes = pd.read_csv(freq_path)
                current_app.logger.info(f"Frecuencia de clientes cargada: {len(self.frecuencia_clientes)} clientes")

            # Cargar transacciones para obtener historial de clientes
            trans_path = self.reports_dir / 'cache' / 'transactions_transformed.parquet'
            if trans_path.exists():
                self.transacciones = pd.read_parquet(trans_path)
                # Convertir productos_str a lista si existe
                if 'productos_str' in self.transacciones.columns:
                    self.transacciones['productos_list'] = self.transacciones['productos_str'].apply(
                        lambda x: [int(p) for p in str(x).split()] if pd.notna(x) and str(x).strip() else []
                    )
                current_app.logger.info(f"Transacciones cargadas: {len(self.transacciones)} registros")
        except Exception as e:
            current_app.logger.error(f"Error cargando datos para recomendaciones: {str(e)}")

    def recommend_for_customer(self, customer_id: int, top_n: int = 10):
        """
        Recomienda productos para un cliente específico basado en su historial de compras

        Args:
            customer_id: ID del cliente
            top_n: Número de productos a recomendar

        Returns:
            dict con recomendaciones y metadata
        """
        try:
            customer_id = int(customer_id)

            # Verificar si el cliente existe
            if self.transacciones is None or 'productos_list' not in self.transacciones.columns:
                return {"error": "Datos de transacciones no disponibles"}

            customer_transactions = self.transacciones[self.transacciones['persona_id'] == customer_id]

            if len(customer_transactions) == 0:
                return {
                    "customer_id": customer_id,
                    "message": "Cliente no encontrado",
                    "recommendations": []
                }

            # Obtener todos los productos que el cliente ha comprado
            customer_products = set()
            for products_list in customer_transactions['productos_list']:
                if isinstance(products_list, list):
                    customer_products.update(products_list)

            # Obtener estadísticas del cliente
            num_transactions = len(customer_transactions)
            total_products = len(customer_products)

            # Buscar recomendaciones en las reglas de asociación
            recommendations = []

            if self.reglas is not None and len(self.reglas) > 0:
                for product in customer_products:
                    product_str = str(product)

                    # Buscar reglas donde el producto es antecedente
                    matching_rules = self.reglas[
                        self.reglas['antecedente'].str.contains(product_str, na=False)
                    ]

                    for _, rule in matching_rules.iterrows():
                        # Extraer productos del consecuente
                        consequents = [int(p.strip()) for p in str(rule['consecuente']).split(',')]

                        # Filtrar productos que el cliente ya compró
                        new_products = [p for p in consequents if p not in customer_products]

                        for rec_product in new_products:
                            recommendations.append({
                                'producto_id': rec_product,
                                'lift': float(rule['lift']),
                                'confianza': float(rule['confianza']),
                                'soporte': float(rule['soporte']),
                                'basado_en_producto': product,
                                'score': float(rule['lift']) * float(rule['confianza'])  # Score compuesto
                            })

            # Ordenar por score y eliminar duplicados
            if recommendations:
                recommendations_df = pd.DataFrame(recommendations)
                recommendations_df = recommendations_df.sort_values('score', ascending=False)
                recommendations_df = recommendations_df.drop_duplicates('producto_id')
                recommendations = recommendations_df.head(top_n).to_dict('records')

            return {
                "customer_id": customer_id,
                "customer_stats": {
                    "num_transactions": int(num_transactions),
                    "total_products_bought": int(total_products),
                    "unique_products": list(customer_products)[:20]  # Limitar para no saturar
                },
                "recommendations": recommendations[:top_n],
                "total_recommendations": len(recommendations)
            }

        except Exception as e:
            current_app.logger.error(f"Error generando recomendaciones para cliente {customer_id}: {str(e)}")
            return {"error": str(e)}

    def recommend_for_product(self, product_id: int, top_n: int = 10):
        """
        Recomienda productos que suelen comprarse junto con un producto específico

        Args:
            product_id: ID del producto
            top_n: Número de productos a recomendar

        Returns:
            dict con recomendaciones y metadata
        """
        try:
            product_id = int(product_id)
            product_str = str(product_id)

            if self.reglas is None:
                return {"error": "Reglas de asociación no disponibles"}

            # Buscar reglas donde el producto es antecedente
            matching_rules = self.reglas[
                self.reglas['antecedente'].str.contains(product_str, na=False, regex=False)
            ].copy()

            if len(matching_rules) == 0:
                return {
                    "product_id": product_id,
                    "message": "No se encontraron recomendaciones para este producto",
                    "recommendations": []
                }

            # Extraer recomendaciones
            recommendations = []
            for _, rule in matching_rules.iterrows():
                consequents = [p.strip() for p in str(rule['consecuente']).split(',')]

                for rec_product in consequents:
                    try:
                        rec_product_id = int(rec_product)
                        if rec_product_id != product_id:  # No recomendar el mismo producto
                            recommendations.append({
                                'producto_id': rec_product_id,
                                'lift': float(rule['lift']),
                                'confianza': float(rule['confianza']),
                                'soporte': float(rule['soporte']),
                                'num_transacciones': int(rule.get('num_transacciones', 0)),
                                'score': float(rule['lift']) * float(rule['confianza'])
                            })
                    except (ValueError, TypeError):
                        continue

            # Ordenar y eliminar duplicados
            if recommendations:
                recommendations_df = pd.DataFrame(recommendations)
                recommendations_df = recommendations_df.sort_values('score', ascending=False)
                recommendations_df = recommendations_df.drop_duplicates('producto_id')
                recommendations = recommendations_df.head(top_n).to_dict('records')

            # Obtener estadísticas del producto
            product_stats = self._get_product_stats(product_id)

            return {
                "product_id": product_id,
                "product_stats": product_stats,
                "recommendations": recommendations[:top_n],
                "total_recommendations": len(recommendations),
                "based_on_rules": len(matching_rules)
            }

        except Exception as e:
            current_app.logger.error(f"Error generando recomendaciones para producto {product_id}: {str(e)}")
            return {"error": str(e)}

    def _get_product_stats(self, product_id: int):
        """Obtiene estadísticas de un producto"""
        try:
            # Buscar en top productos
            top_productos_path = self.reports_dir / 'top_productos.csv'
            if top_productos_path.exists():
                top_productos = pd.read_csv(top_productos_path)
                product_info = top_productos[top_productos['producto_id'] == product_id]

                if len(product_info) > 0:
                    product_row = product_info.iloc[0]
                    return {
                        "frecuencia": int(product_row.get('frecuencia', 0)),
                        "porcentaje": float(product_row.get('porcentaje', 0)),
                        "ranking": int(product_row.name + 1) if hasattr(product_row, 'name') else None
                    }

            return {}
        except Exception as e:
            current_app.logger.error(f"Error obteniendo stats del producto {product_id}: {str(e)}")
            return {}
