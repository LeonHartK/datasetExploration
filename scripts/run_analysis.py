
"""
Script principal para ejecutar análisis exploratorio de datos
Ejecutar desde la raíz del proyecto: python scripts/run_analysis.py
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.analyzer import DatasetAnalyzer
from utils.config import REPORTS_DIR
import warnings
warnings.filterwarnings('ignore')


def main():
    """Función principal"""
    
    print("ANÁLISIS EXPLORATORIO DE DATOS")
    print("Proyecto: Procesamiento de Transacciones y Productos")
    
    # Inicializar analizador
    analyzer = DatasetAnalyzer()
    
    try:
        # ============================================================
        # 1. CARGAR DATOS
        # ============================================================
        print("FASE 1: CARGA DE DATOS")
        
        # Cargar categorías
        analyzer.load_categories()
        
        # Cargar producto-categoría
        analyzer.load_product_category()
        
        # Cargar transacciones (todas las disponibles)
        # Si quieres probar con una muestra primero, usa: sample_size=50
        analyzer.load_transactions()  # sample_size=None carga todas
        
        # ============================================================
        # 2. REVISIÓN INICIAL
        # ============================================================
        print("FASE 2: REVISIÓN INICIAL DE DATASETS")
        
        # Revisar categorías
        analyzer.review_dataset('categories')
        
        # Revisar producto-categoría
        analyzer.review_dataset('product_category')
        
        # Revisar transacciones
        analyzer.review_dataset('transactions')
        
        # ============================================================
        # 3. ESTADÍSTICAS DESCRIPTIVAS - NUMÉRICAS
        # ============================================================
        print("FASE 3: ESTADÍSTICAS DESCRIPTIVAS NUMÉRICAS")
        
        # Análisis numérico de transacciones
        stats_numeric = analyzer.analyze_numeric('transactions')
        
        # Guardar estadísticas numéricas
        if stats_numeric is not None:
            stats_numeric.to_csv(REPORTS_DIR / 'estadisticas_numericas.csv', index=False)
            print(f"\n✓ Estadísticas numéricas guardadas en: {REPORTS_DIR / 'estadisticas_numericas.csv'}")
        
        # ============================================================
        # 4. ESTADÍSTICAS DESCRIPTIVAS - CATEGÓRICAS
        # ============================================================
        print("FASE 4: ESTADÍSTICAS DESCRIPTIVAS CATEGÓRICAS")
        
        # Análisis categórico de transacciones
        stats_categorical = analyzer.analyze_categorical('transactions')
        
        # Análisis de categorías
        analyzer.analyze_categorical('categories')
        
        # ============================================================
        # 5. CALIDAD DE DATOS
        # ============================================================
        print("FASE 5: VERIFICACIÓN DE CALIDAD DE DATOS")
        
        # Calidad de cada dataset
        for dataset in ['categories', 'product_category', 'transactions']:
            quality = analyzer.check_quality(dataset)
            print(f"\nCALIDAD: {dataset.upper()}")
            for key, value in quality.items():
                print(f"  • {key}: {value}")
        
        # ============================================================
        # 6. EXPORTAR RESÚMENES
        # ============================================================
        print("FASE 6: EXPORTACIÓN DE RESÚMENES")
        
        analyzer.export_summary(REPORTS_DIR)
        
        # ============================================================
        # RESUMEN FINAL
        # ============================================================
        print("ANÁLISIS COMPLETADO EXITOSAMENTE")
        print(f"\nReportes generados en: {REPORTS_DIR}")
        print("\nDatasets cargados:")
        print(f"  • Categorías: {len(analyzer.categories):,} registros")
        print(f"  • Productos: {len(analyzer.product_category):,} registros")
        print(f"  • Transacciones: {len(analyzer.transactions):,} registros")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())