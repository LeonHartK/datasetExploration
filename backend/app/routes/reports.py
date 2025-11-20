from flask import Blueprint, jsonify, send_file, current_app
from pathlib import Path
import os

bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@bp.route('/images', methods=['GET'])
def list_images():
    """Lista todas las gráficas disponibles"""
    try:
        graphics_dir = current_app.config['GRAPHICS_DIR']
        images = [f.name for f in graphics_dir.glob('*.png')]
        return jsonify({
            "images": images,
            "count": len(images)
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error en /images: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    """Descarga una gráfica específica"""
    try:
        graphics_dir = current_app.config['GRAPHICS_DIR']
        file_path = graphics_dir / filename

        if not file_path.exists():
            return jsonify({"error": "Image not found"}), 404

        return send_file(file_path, mimetype='image/png')
    except Exception as e:
        current_app.logger.error(f"Error en /images/{filename}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/csv', methods=['GET'])
def list_csv_files():
    """Lista todos los archivos CSV disponibles"""
    try:
        reports_dir = current_app.config['REPORTS_DIR']
        csv_files = [f.name for f in reports_dir.glob('*.csv')]
        return jsonify({
            "files": csv_files,
            "count": len(csv_files)
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error en /csv: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/csv/<filename>', methods=['GET'])
def download_csv(filename):
    """Descarga un archivo CSV específico"""
    try:
        reports_dir = current_app.config['REPORTS_DIR']
        file_path = reports_dir / filename

        if not file_path.exists():
            return jsonify({"error": "File not found"}), 404

        return send_file(file_path, mimetype='text/csv', as_attachment=True)
    except Exception as e:
        current_app.logger.error(f"Error en /csv/{filename}: {str(e)}")
        return jsonify({"error": str(e)}), 500
