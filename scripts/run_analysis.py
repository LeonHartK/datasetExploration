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
from utils.data_transformer import transform_transactions_data
from utils.statistics import descriptive_statistics_numeric
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def main():
    """Función principal"""

    print("=" * 70)
    print("ANÁLISIS EXPLORATORIO DE DATOS")
    print("Proyecto: Procesamiento de Transacciones y Productos")
    print("=" * 70)

    # Inicializar analizador
    analyzer = DatasetAnalyzer()

    try:
        # ============================================================
        # 1. CARGAR DATOS
        # ============================================================
        print("\nFASE 1: CARGA DE DATOS")
        print("=" * 70)

        # Cargar categorías
        print("\n1.1 Cargando categorías...")
        analyzer.load_categories()

        # Cargar producto-categoría
        print("1.2 Cargando productos...")
        analyzer.load_product_category()

        # Cargar transacciones (todas las disponibles)
        # Si quieres probar con una muestra primero, usa: sample_size=50
        print("1.3 Cargando transacciones...")
        analyzer.load_transactions()  # sample_size=None carga todas

        # ============================================================
        # 2. TRANSFORMAR TRANSACCIONES
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 2: TRANSFORMACIÓN DE DATOS")
        print("=" * 70)

        print("\n2.1 Transformando estructura de transacciones...")
        df_transformed = transform_transactions_data(analyzer.transactions)

        # Guardar datos transformados
        analyzer.transactions_transformed = df_transformed

        print(f"\n✓ Transacciones transformadas: {len(df_transformed):,} registros")
        print(f"✓ Columnas generadas: {list(df_transformed.columns)}")

        # ============================================================
        # 3. REVISIÓN INICIAL
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 3: REVISIÓN INICIAL DE DATASETS")
        print("=" * 70)

        # Revisar categorías
        print("\n3.1 Categorías:")
        analyzer.review_dataset("categories")

        # Revisar producto-categoría
        print("\n3.2 Productos:")
        analyzer.review_dataset("product_category")

        # ============================================================
        # 4. ANÁLISIS DE PRODUCTOS POR TRANSACCIÓN
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 4: ANÁLISIS DE PRODUCTOS POR TRANSACCIÓN")
        print("=" * 70)

        # Analizar cantidad de productos por transacción
        print("\n4.1 Estadísticas de productos por transacción:")
        stats_productos = descriptive_statistics_numeric(
            df_transformed[["num_productos"]], "PRODUCTOS POR TRANSACCIÓN"
        )

        if stats_productos is not None:
            stats_productos.to_csv(
                REPORTS_DIR / "productos_por_transaccion.csv", index=False
            )
            print(f"\n✓ Guardado en: {REPORTS_DIR / 'productos_por_transaccion.csv'}")

        # ============================================================
        # 5. ANÁLISIS DE PRODUCTOS MÁS VENDIDOS
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 5: ANÁLISIS DE PRODUCTOS MÁS VENDIDOS")
        print("=" * 70)

        print("\n5.1 Calculando frecuencia de productos...")

        # Expandir lista de productos
        all_products = []
        for products in df_transformed["productos_list"]:
            if products:
                all_products.extend(products)

        # Contar frecuencias
        product_freq = pd.Series(all_products).value_counts()
        product_freq_df = pd.DataFrame(
            {
                "producto_id": product_freq.index,
                "frecuencia": product_freq.values,
                "porcentaje": (product_freq.values / product_freq.sum() * 100).round(2),
            }
        )

        print(f"\n✓ Total productos únicos: {len(product_freq)}")
        print(f"✓ Total items vendidos: {len(all_products):,}")
        print("\nTop 10 productos más vendidos:")
        print(product_freq_df.head(10).to_string(index=False))

        # Guardar
        product_freq_df.to_csv(REPORTS_DIR / "top_productos.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'top_productos.csv'}")

        # ============================================================
        # 6. ANÁLISIS POR TIPO DE TRANSACCIÓN
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 6: ANÁLISIS POR TIPO DE TRANSACCIÓN")
        print("=" * 70)

        print("\n6.1 Estadísticas por tipo de transacción:")
        stats_por_tipo = (
            df_transformed.groupby("tipo_transaccion")
            .agg(
                {
                    "id_transaccion": "count",
                    "num_productos": ["mean", "median", "std", "min", "max"],
                    "tiene_productos": "sum",
                }
            )
            .round(2)
        )

        stats_por_tipo.columns = [
            "total_transacciones",
            "media_productos",
            "mediana_productos",
            "std_productos",
            "min_productos",
            "max_productos",
            "con_productos",
        ]
        stats_por_tipo["pct_con_productos"] = (
            stats_por_tipo["con_productos"]
            / stats_por_tipo["total_transacciones"]
            * 100
        ).round(2)

        print("\n" + stats_por_tipo.to_string())

        # Guardar
        stats_por_tipo.to_csv(REPORTS_DIR / "stats_por_tipo_transaccion.csv")
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'stats_por_tipo_transaccion.csv'}")

        # ============================================================
        # 7. ESTADÍSTICAS DESCRIPTIVAS - CATEGÓRICAS
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 7: ANÁLISIS DE CATEGORÍAS")
        print("=" * 70)

        # Análisis de categorías
        print("\n7.1 Análisis de categorías:")
        analyzer.analyze_categorical("categories")

        # ============================================================
        # 8. CALIDAD DE DATOS
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 8: VERIFICACIÓN DE CALIDAD DE DATOS")
        print("=" * 70)

        # Calidad de cada dataset
        for dataset in ["categories", "product_category"]:
            quality = analyzer.check_quality(dataset)
            print(f"\nCALIDAD: {dataset.upper()}")
            for key, value in quality.items():
                print(f"  • {key}: {value}")

        # ============================================================
        # 9. EXPORTAR RESÚMENES
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 9: EXPORTACIÓN DE RESÚMENES")
        print("=" * 70)

        analyzer.export_summary(REPORTS_DIR)

        # Guardar también transacciones transformadas
        df_transformed.to_csv(
            REPORTS_DIR / "transacciones_transformadas_sample.csv", index=False
        )
        print(
            f"\n✓ Transacciones transformadas guardadas: {REPORTS_DIR / 'transacciones_transformadas_sample.csv'}"
        )

        # ============================================================
        # RESUMEN FINAL
        # ============================================================
        print("\n" + "=" * 70)
        print("ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        print(f"\nReportes generados en: {REPORTS_DIR}")
        print("\nDatasets cargados:")
        if analyzer.categories is not None:
            print(f"  • Categorías: {len(analyzer.categories):,} registros")
        if analyzer.product_category is not None:
            print(f"  • Productos: {len(analyzer.product_category):,} registros")
        if analyzer.transactions is not None:
            print(f"  • Transacciones: {len(analyzer.transactions):,} registros")
        print(f"  • Transacciones transformadas: {len(df_transformed):,} registros")

        print("\nArchivos generados:")
        print(
            "  • productos_por_transaccion.csv - Estadísticas de cantidad de productos"
        )
        print("  • top_productos.csv - Productos más vendidos")
        print("  • stats_por_tipo_transaccion.csv - Análisis por tipo")
        print("  • transacciones_transformadas_sample.csv - Datos transformados")
        print("\n" + "=" * 70)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
