from flask import Flask
from flask_cors import CORS

def create_app():
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)

    # Configuración
    app.config.from_object('app.config.Config')

    # Habilitar CORS para el frontend
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:3000"]}})

    # Registrar blueprints (rutas)
    from app.routes import analytics, reports, health
    app.register_blueprint(analytics.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(health.bp)

    @app.route('/')
    def index():
        return {
            "message": "EDA Analytics API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/api/health",
                "analytics": "/api/analytics",
                "reports": "/api/reports"
            }
        }

    return app
