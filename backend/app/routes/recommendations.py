from flask import Blueprint, jsonify, current_app
from app.services.recommendation_service import RecommendationService

bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

@bp.route('/customer/<int:customer_id>', methods=['GET'])
def recommend_for_customer(customer_id):
    """
    Recomienda productos para un cliente específico basado en su historial de compras

    Args:
        customer_id: ID del cliente

    Query params:
        top_n: Número de recomendaciones (default: 10)
    """
    try:
        from flask import request
        top_n = request.args.get('top_n', 10, type=int)

        service = RecommendationService()
        recommendations = service.recommend_for_customer(customer_id, top_n=top_n)

        return jsonify(recommendations), 200
    except Exception as e:
        current_app.logger.error(f"Error en /customer/{customer_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/product/<int:product_id>', methods=['GET'])
def recommend_for_product(product_id):
    """
    Recomienda productos que suelen comprarse junto con un producto específico

    Args:
        product_id: ID del producto

    Query params:
        top_n: Número de recomendaciones (default: 10)
    """
    try:
        from flask import request
        top_n = request.args.get('top_n', 10, type=int)

        service = RecommendationService()
        recommendations = service.recommend_for_product(product_id, top_n=top_n)

        return jsonify(recommendations), 200
    except Exception as e:
        current_app.logger.error(f"Error en /product/{product_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500
