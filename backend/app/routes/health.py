from flask import Blueprint, jsonify
import os

bp = Blueprint('health', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        "status": "healthy",
        "service": "EDA Analytics API",
        "version": "1.0.0"
    }), 200
