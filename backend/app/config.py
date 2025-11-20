import os
from pathlib import Path

class Config:
    """Configuración de la aplicación Flask"""

    # Paths
    # En Docker, el working directory es /app, así que usamos rutas absolutas
    BASE_DIR = Path('/app') if Path('/app/reports').exists() else Path(__file__).parent.parent.parent
    REPORTS_DIR = BASE_DIR / 'reports'
    GRAPHICS_DIR = REPORTS_DIR / 'graficas'
    DATA_DIR = BASE_DIR / 'data'

    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    # API config
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

    # Cache config (opcional para futuro)
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

    @staticmethod
    def init_app(app):
        """Inicialización adicional si es necesaria"""
        pass
