"""
Script principal para ejecutar análisis exploratorio de datos
Ejecutar desde la raíz del proyecto: python scripts/run_analysis.py
"""

import sys
import warnings
from pathlib import Path

# Agregar directorio raíz al path ANTES de los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from utils.analyzer import DatasetAnalyzer
from utils.config import REPORTS_DIR
from utils.data_transformer import transform_transactions_data
from utils.statistics import descriptive_statistics_numeric
from utils.temporal_analysis import (
    analyze_daily_sales,
    analyze_weekly_sales,
    analyze_monthly_sales,
    analyze_day_of_week_patterns,
    analyze_hourly_patterns,
    analyze_trends_and_seasonality,
)
from utils.customer_analysis import (
    analyze_customer_frequency,
    analyze_time_between_purchases,
    segment_customers,
    analyze_customer_behavior_summary,
)
from utils.product_analysis import (
    analyze_top_products,
    analyze_association_rules,
    analyze_product_cooccurrence,
)
from utils.visualization import generate_all_visualizations

warnings.filterwarnings("ignore")


def main():
    """Función principal"""

    print("=" * 70)
    print("ANÁLISIS EXPLORATORIO DE DATOS")
    print("Proyecto: Procesamiento de Transacciones y Productos")
    print("=" * 70)

    # Inicializar analizador
    analyzer: DatasetAnalyzer = DatasetAnalyzer()

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
                    "persona_id": "count",
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
        # 10. ANÁLISIS TEMPORAL
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 10: ANÁLISIS TEMPORAL DE VENTAS")
        print("=" * 70)

        print("\n10.1 Análisis de ventas diarias:")
        ventas_diarias = analyze_daily_sales(df_transformed)
        ventas_diarias.to_csv(REPORTS_DIR / "ventas_diarias.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'ventas_diarias.csv'}")

        print("\n10.2 Análisis de ventas semanales:")
        ventas_semanales = analyze_weekly_sales(df_transformed)
        ventas_semanales.to_csv(REPORTS_DIR / "ventas_semanales.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'ventas_semanales.csv'}")

        print("\n10.3 Análisis de ventas mensuales:")
        ventas_mensuales = analyze_monthly_sales(df_transformed)
        ventas_mensuales.to_csv(REPORTS_DIR / "ventas_mensuales.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'ventas_mensuales.csv'}")

        print("\n10.4 Patrones por día de la semana:")
        ventas_dia_semana = analyze_day_of_week_patterns(df_transformed)
        ventas_dia_semana.to_csv(REPORTS_DIR / "ventas_dia_semana.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'ventas_dia_semana.csv'}")

        print("\n10.5 Patrones por hora del día:")
        ventas_hora = analyze_hourly_patterns(df_transformed)
        ventas_hora.to_csv(REPORTS_DIR / "ventas_por_hora.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'ventas_por_hora.csv'}")

        print("\n10.6 Análisis de tendencias y estacionalidad:")
        tendencias = analyze_trends_and_seasonality(df_transformed)

        # ============================================================
        # 11. ANÁLISIS POR CLIENTE
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 11: ANÁLISIS DE COMPORTAMIENTO DE CLIENTES")
        print("=" * 70)

        print("\n11.1 Frecuencia de compra por cliente:")
        frecuencia_clientes = analyze_customer_frequency(df_transformed)
        frecuencia_clientes.to_csv(REPORTS_DIR / "frecuencia_clientes.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'frecuencia_clientes.csv'}")

        print("\n11.2 Tiempo entre compras:")
        tiempo_compras = analyze_time_between_purchases(df_transformed)
        if len(tiempo_compras) > 0:
            tiempo_compras.to_csv(
                REPORTS_DIR / "tiempo_entre_compras.csv", index=False
            )
            print(f"\n✓ Guardado en: {REPORTS_DIR / 'tiempo_entre_compras.csv'}")

        print("\n11.3 Segmentación de clientes:")
        segmentacion = segment_customers(df_transformed, frecuencia_clientes, tiempo_compras)
        segmentacion.to_csv(REPORTS_DIR / "segmentacion_clientes.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'segmentacion_clientes.csv'}")

        print("\n11.4 Resumen ejecutivo de clientes:")
        resumen_clientes = analyze_customer_behavior_summary(segmentacion)

        # ============================================================
        # 12. ANÁLISIS AVANZADO DE PRODUCTOS
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 12: ANÁLISIS AVANZADO DE PRODUCTOS")
        print("=" * 70)

        print("\n12.1 Análisis detallado de productos más vendidos:")
        productos_top = analyze_top_products(df_transformed, top_n=100)
        productos_top.to_csv(REPORTS_DIR / "productos_top_detallado.csv", index=False)
        print(f"\n✓ Guardado en: {REPORTS_DIR / 'productos_top_detallado.csv'}")

        print("\n12.2 Co-ocurrencia de productos:")
        coocurrencia = analyze_product_cooccurrence(df_transformed, top_n=50)
        if len(coocurrencia) > 0:
            coocurrencia.to_csv(REPORTS_DIR / "productos_coocurrencia.csv", index=False)
            print(f"\n✓ Guardado en: {REPORTS_DIR / 'productos_coocurrencia.csv'}")

        print("\n12.3 Reglas de asociación (Market Basket Analysis):")
        reglas, stats_reglas = analyze_association_rules(
            df_transformed, min_support=0.01, min_confidence=0.3, top_n=50
        )
        if len(reglas) > 0:
            reglas.to_csv(REPORTS_DIR / "reglas_asociacion.csv", index=False)
            print(f"\n✓ Guardado en: {REPORTS_DIR / 'reglas_asociacion.csv'}")

        # ============================================================
        # 13. GENERACIÓN DE VISUALIZACIONES
        # ============================================================
        print("\n" + "=" * 70)
        print("FASE 13: GENERACIÓN DE VISUALIZACIONES")
        print("=" * 70)

        generate_all_visualizations(
            ventas_diarias=ventas_diarias,
            ventas_semanales=ventas_semanales,
            ventas_mensuales=ventas_mensuales,
            ventas_dia_semana=ventas_dia_semana,
            ventas_hora=ventas_hora,
            frecuencia_clientes=frecuencia_clientes,
            tiempo_compras=tiempo_compras,
            segmentacion=segmentacion,
            productos_top=productos_top,
            coocurrencia=coocurrencia,
            reglas=reglas,
            output_dir=REPORTS_DIR
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
        print("\n  ANÁLISIS BÁSICO:")
        print("    • productos_por_transaccion.csv - Estadísticas de cantidad de productos")
        print("    • top_productos.csv - Productos más vendidos")
        print("    • stats_por_tipo_transaccion.csv - Análisis por tipo")
        print("    • transacciones_transformadas_sample.csv - Datos transformados")

        print("\n  ANÁLISIS TEMPORAL:")
        print("    • ventas_diarias.csv - Ventas por día")
        print("    • ventas_semanales.csv - Ventas por semana")
        print("    • ventas_mensuales.csv - Ventas por mes")
        print("    • ventas_dia_semana.csv - Patrones por día de la semana")
        print("    • ventas_por_hora.csv - Patrones por hora del día")

        print("\n  ANÁLISIS DE CLIENTES:")
        print("    • frecuencia_clientes.csv - Frecuencia de compra por cliente")
        print("    • tiempo_entre_compras.csv - Tiempo promedio entre compras")
        print("    • segmentacion_clientes.csv - Segmentación RFM de clientes")

        print("\n  ANÁLISIS DE PRODUCTOS:")
        print("    • productos_top_detallado.csv - Top productos con estadísticas")
        print("    • productos_coocurrencia.csv - Productos que se compran juntos")
        print("    • reglas_asociacion.csv - Reglas de asociación (Market Basket)")

        print("\n  VISUALIZACIONES (en carpeta graficas/):")
        print("    • grafica_ventas_diarias.png - Evolución temporal de ventas")
        print("    • grafica_ventas_semanales_mensuales.png - Ventas agregadas")
        print("    • grafica_ventas_dia_semana.png - Patrones semanales")
        print("    • grafica_ventas_hora.png - Patrones horarios")
        print("    • grafica_frecuencia_clientes.png - Distribución de clientes")
        print("    • grafica_tiempo_entre_compras.png - Análisis de recurrencia")
        print("    • grafica_segmentacion_clientes.png - Segmentación RFM")
        print("    • grafica_top_productos.png - Productos más vendidos")
        print("    • grafica_coocurrencia_productos.png - Co-ocurrencia")
        print("    • grafica_reglas_asociacion.png - Market Basket Analysis")

        print("\n" + "=" * 70)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
