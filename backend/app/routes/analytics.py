from flask import Blueprint, jsonify, current_app
from app.services.data_loader import DataLoaderService
from app.services.stats_service import StatsService

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route('/summary', methods=['GET'])
def get_summary():
    """Obtiene el resumen ejecutivo con KPIs principales"""
    try:
        stats_service = StatsService()
        summary = stats_service.get_executive_summary()
        return jsonify(summary), 200
    except Exception as e:
        current_app.logger.error(f"Error en /summary: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/temporal', methods=['GET'])
def get_temporal_analysis():
    """Obtiene análisis temporal (ventas diarias, semanales, mensuales)"""
    try:
        loader = DataLoaderService()
        data = {
            "ventas_diarias": loader.load_csv('ventas_diarias.csv'),
            "ventas_semanales": loader.load_csv('ventas_semanales.csv'),
            "ventas_mensuales": loader.load_csv('ventas_mensuales.csv'),
            "ventas_dia_semana": loader.load_csv('ventas_dia_semana.csv')
        }
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error en /temporal: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/customers', methods=['GET'])
def get_customer_analysis():
    """Obtiene análisis de clientes (RFM, segmentación, frecuencia)"""
    try:
        loader = DataLoaderService()
        data = {
            "segmentacion_clientes": loader.load_csv('segmentacion_clientes.csv', limit=1000),
            "frecuencia_clientes": loader.load_csv('frecuencia_clientes.csv', limit=1000),
            "tiempo_entre_compras": loader.load_csv('tiempo_entre_compras.csv', limit=1000)
        }
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error en /customers: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/products', methods=['GET'])
def get_product_analysis():
    """Obtiene análisis de productos (top productos, coocurrencia, reglas)"""
    try:
        loader = DataLoaderService()

        # Generar resumen de categorías dinámicamente
        categories_summary = generate_category_summary()

        data = {
            "top_productos": loader.load_csv('top_productos.csv'),
            "productos_top_detallado": loader.load_csv('productos_top_detallado.csv', limit=50),
            "productos_coocurrencia": loader.load_csv('productos_coocurrencia.csv', limit=100),
            "reglas_asociacion": loader.load_csv('reglas_asociacion.csv', limit=100),
            "product_category_summary": categories_summary
        }
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error en /products: {str(e)}")
        return jsonify({"error": str(e)}), 500

def generate_category_summary():
    """Genera resumen de productos por categoría"""
    try:
        data_dir = current_app.config['DATA_DIR']

        # Leer archivos de datos
        categories_df = pd.read_csv(
            data_dir / 'DataSet' / 'Products' / 'Categories.csv',
            sep='|',
            names=['categoria_id', 'categoria_nombre'],
            header=None
        )

        product_category_df = pd.read_csv(
            data_dir / 'DataSet' / 'Products' / 'ProductCategory.csv',
            sep='|',
            names=['producto_id', 'categoria_id'],
            skiprows=1
        )

        # Contar productos por categoría
        category_counts = product_category_df.groupby('categoria_id').size().reset_index(name='total_productos')

        # Unir con nombres de categorías
        summary = categories_df.merge(category_counts, on='categoria_id', how='left')
        summary['total_productos'] = summary['total_productos'].fillna(0).astype(int)

        # Ordenar por total de productos descendente
        summary = summary.sort_values('total_productos', ascending=False)

        return summary.to_dict('records')
    except Exception as e:
        current_app.logger.error(f"Error generando resumen de categorías: {str(e)}")
        return []

@bp.route('/transactions', methods=['GET'])
def get_transaction_stats():
    """Obtiene estadísticas de transacciones"""
    try:
        loader = DataLoaderService()
        data = {
            "transactions_summary": loader.load_csv('transactions_summary.csv'),
            "stats_por_tipo_transaccion": loader.load_csv('stats_por_tipo_transaccion.csv'),
            "productos_por_transaccion": loader.load_csv('productos_por_transaccion.csv')
        }
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error en /transactions: {str(e)}")
        return jsonify({"error": str(e)}), 500
