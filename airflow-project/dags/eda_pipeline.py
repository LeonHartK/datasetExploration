from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from utils.analyzer import DatasetAnalyzer
from utils.config import REPORTS_DIR
from utils.customer_analysis import (
    analyze_customer_behavior_summary,
    analyze_customer_frequency,
    analyze_time_between_purchases,
    segment_customers,
)
from utils.data_loader import (
    load_categories,
    load_product_category,
    load_transactions,
)
from utils.data_review import (
    check_data_quality,
    get_data_summary,
)
from utils.data_transformer import (
    transform_transactions_data,
    analyze_products_per_transaction,
    analyze_by_transaction_type,
    get_product_frequency,
)
from utils.product_analysis import (
    analyze_association_rules,
    analyze_product_cooccurrence,
    analyze_top_products,
)
from utils.statistics import descriptive_statistics_numeric
from utils.temporal_analysis import (
    analyze_daily_sales,
    analyze_day_of_week_patterns,
    analyze_hourly_patterns,
    analyze_monthly_sales,
    analyze_trends_and_seasonality,
    analyze_weekly_sales,
)
from utils.visualization import generate_all_visualizations

CACHE_DIR = REPORTS_DIR / "cache"
RAW_TRANSACTIONS_PATH = CACHE_DIR / "transactions.parquet"
TRANSFORMED_TRANSACTIONS_PATH = CACHE_DIR / "transactions_transformed.parquet"
CATEGORIES_PATH = CACHE_DIR / "categories.parquet"
PRODUCT_CATEGORY_PATH = CACHE_DIR / "product_category.parquet"

VENTAS_DIARIAS_PATH = REPORTS_DIR / "ventas_diarias.csv"
VENTAS_SEMANALES_PATH = REPORTS_DIR / "ventas_semanales.csv"
VENTAS_MENSUALES_PATH = REPORTS_DIR / "ventas_mensuales.csv"
VENTAS_DIA_SEMANA_PATH = REPORTS_DIR / "ventas_dia_semana.csv"
VENTAS_POR_HORA_PATH = REPORTS_DIR / "ventas_por_hora.csv"
TRENDS_PATH = REPORTS_DIR / "ventas_mensuales_descomposicion.csv"

ESTADISTICAS_NUMERICAS_PATH = REPORTS_DIR / "estadisticas_numericas.csv"
PRODUCTOS_POR_TRANSACCION_PATH = REPORTS_DIR / "productos_por_transaccion.csv"
TOP_PRODUCTOS_PATH = REPORTS_DIR / "top_productos.csv"
PRODUCTOS_TOP_DETALLADO_PATH = REPORTS_DIR / "productos_top_detallado.csv"
TRANSACCIONES_TIPO_PATH = REPORTS_DIR / "stats_por_tipo_transaccion.csv"
COOCURRENCIA_PATH = REPORTS_DIR / "productos_coocurrencia.csv"
ASOCIACION_PATH = REPORTS_DIR / "reglas_asociacion.csv"

FRECUENCIA_CLIENTES_PATH = REPORTS_DIR / "frecuencia_clientes.csv"
TIEMPO_ENTRE_COMPRAS_PATH = REPORTS_DIR / "tiempo_entre_compras.csv"
SEGMENTACION_CLIENTES_PATH = REPORTS_DIR / "segmentacion_clientes.csv"
CUSTOMER_SUMMARY_PATH = REPORTS_DIR / "customer_behavior_summary.csv"

GRAPHICS_DIR = REPORTS_DIR / "graficas"


def ensure_directories():
    for path in (REPORTS_DIR, CACHE_DIR, GRAPHICS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def _write(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)


def _load_with_analyzer(load_fn: str, attr: str) -> pd.DataFrame:
    analyzer = DatasetAnalyzer()
    getattr(analyzer, load_fn)()
    return getattr(analyzer, attr)


def load_categories_task():
    df = _load_with_analyzer("load_categories", "categories")
    _write(df, CATEGORIES_PATH)


def load_product_category_task():
    df = _load_with_analyzer("load_product_category", "product_category")
    _write(df, PRODUCT_CATEGORY_PATH)


def load_transactions_task():
    df = _load_with_analyzer("load_transactions", "transactions")
    _write(df, RAW_TRANSACTIONS_PATH)


def transform_transactions_task():
    df = pd.read_parquet(RAW_TRANSACTIONS_PATH)
    transformed = transform_transactions_data(df)
    transformed.to_parquet(TRANSFORMED_TRANSACTIONS_PATH, index=False)
    transformed.head(1000).to_csv(
        REPORTS_DIR / "transacciones_transformadas_sample.csv", index=False
    )


def _save_review_outputs(df: pd.DataFrame, dataset_name: str, summary_path: Path):
    summary_df = pd.DataFrame([get_data_summary(df)])
    summary_df.to_csv(summary_path, index=False)
    quality_df = pd.DataFrame([check_data_quality(df, dataset_name)])
    quality_path = summary_path.with_name(summary_path.stem + "_quality.csv")
    quality_df.to_csv(quality_path, index=False)


def review_categories_task():
    df = pd.read_parquet(CATEGORIES_PATH)
    _save_review_outputs(df, "CATEGORIES", REPORTS_DIR / "categories_summary.csv")


def review_product_category_task():
    df = pd.read_parquet(PRODUCT_CATEGORY_PATH)
    _save_review_outputs(
        df, "PRODUCT_CATEGORY", REPORTS_DIR / "product_category_summary.csv"
    )


def review_transactions_task():
    df = pd.read_parquet(RAW_TRANSACTIONS_PATH)
    _save_review_outputs(df, "TRANSACTIONS", REPORTS_DIR / "transactions_summary.csv")


def descriptive_stats_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    stats = descriptive_statistics_numeric(df, name="TRANSACTIONS_TRANSFORMED")
    if stats is not None:
        stats.to_csv(ESTADISTICAS_NUMERICAS_PATH, index=False)


def products_per_transaction_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    stats = analyze_products_per_transaction(df)
    pd.DataFrame([stats]).to_csv(PRODUCTOS_POR_TRANSACCION_PATH, index=False)


def _ensure_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, np.ndarray):
        return value.tolist()
    if pd.isna(value) or value is None:
        return []
    return [value]


def top_products_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    if "productos_list" in df.columns:
        df["productos_list"] = df["productos_list"].apply(_ensure_list)
    top_df = analyze_top_products(df, top_n=50)
    top_df.to_csv(TOP_PRODUCTOS_PATH, index=False)


def transactions_summary_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    stats_df = analyze_by_transaction_type(df).reset_index()
    stats_df.to_csv(TRANSACCIONES_TIPO_PATH, index=False)


def daily_sales_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    analyze_daily_sales(df).to_csv(VENTAS_DIARIAS_PATH, index=False)


def weekly_sales_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    analyze_weekly_sales(df).to_csv(VENTAS_SEMANALES_PATH, index=False)


def monthly_sales_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    analyze_monthly_sales(df).to_csv(VENTAS_MENSUALES_PATH, index=False)


def weekday_patterns_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    analyze_day_of_week_patterns(df).to_csv(VENTAS_DIA_SEMANA_PATH, index=False)


def hourly_patterns_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    analyze_hourly_patterns(df).to_csv(VENTAS_POR_HORA_PATH, index=False)


def trends_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    trends = analyze_trends_and_seasonality(df)
    ventas_mensuales = trends.get("ventas_mensuales", pd.DataFrame())
    if isinstance(ventas_mensuales, pd.DataFrame) and not ventas_mensuales.empty:
        ventas_mensuales.to_csv(TRENDS_PATH, index=False)


def customer_frequency_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    freq = analyze_customer_frequency(df)
    freq.to_csv(FRECUENCIA_CLIENTES_PATH, index=False)


def time_between_purchases_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    time_df = analyze_time_between_purchases(df)
    time_df.to_csv(TIEMPO_ENTRE_COMPRAS_PATH, index=False)


def segment_customers_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    freq = pd.read_csv(FRECUENCIA_CLIENTES_PATH)
    if TIEMPO_ENTRE_COMPRAS_PATH.exists() and TIEMPO_ENTRE_COMPRAS_PATH.stat().st_size > 0:
        tiempo = pd.read_csv(TIEMPO_ENTRE_COMPRAS_PATH)
    else:
        tiempo = pd.DataFrame()
    segments = segment_customers(df, freq, tiempo)
    segments.to_csv(SEGMENTACION_CLIENTES_PATH, index=False)
    summary = analyze_customer_behavior_summary(segments)
    pd.DataFrame([summary]).to_csv(CUSTOMER_SUMMARY_PATH, index=False)


def top_products_detailed_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    if "productos_list" in df.columns:
        df["productos_list"] = df["productos_list"].apply(_ensure_list)
    detailed = get_product_frequency(df, top_n=200)
    detailed.to_csv(PRODUCTOS_TOP_DETALLADO_PATH, index=False)


def cooccurrence_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    cooc = analyze_product_cooccurrence(df, top_n=100)
    cooc.to_csv(COOCURRENCIA_PATH, index=False)


def association_rules_task():
    df = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    rules_df, _ = analyze_association_rules(
        df, min_support=0.01, min_confidence=0.3, top_n=100
    )
    if rules_df is None or rules_df.empty:
        rules_df = pd.DataFrame(
            columns=["antecedente", "consecuente", "soporte", "confianza", "lift", "num_transacciones"]
        )
    rules_df.to_csv(ASOCIACION_PATH, index=False)


def export_global_summary_task():
    analyzer = DatasetAnalyzer()
    analyzer.load_categories()
    analyzer.load_product_category()
    analyzer.load_transactions()
    analyzer.transactions_transformed = pd.read_parquet(TRANSFORMED_TRANSACTIONS_PATH)
    analyzer.export_summary(REPORTS_DIR)


def _safe_read_csv(path: Path, parse_dates: list | None = None) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    return pd.read_csv(path, parse_dates=parse_dates)


def visualization_task():
    ventas_diarias = _safe_read_csv(VENTAS_DIARIAS_PATH, parse_dates=["fecha"])
    ventas_semanales = _safe_read_csv(VENTAS_SEMANALES_PATH)
    ventas_mensuales = _safe_read_csv(VENTAS_MENSUALES_PATH)
    ventas_dia_semana = _safe_read_csv(VENTAS_DIA_SEMANA_PATH)
    ventas_hora = _safe_read_csv(VENTAS_POR_HORA_PATH)
    frecuencia = _safe_read_csv(FRECUENCIA_CLIENTES_PATH)
    tiempo = _safe_read_csv(TIEMPO_ENTRE_COMPRAS_PATH)
    segmentacion = _safe_read_csv(SEGMENTACION_CLIENTES_PATH)
    productos_top = _safe_read_csv(TOP_PRODUCTOS_PATH)
    coocurrencia = _safe_read_csv(COOCURRENCIA_PATH)
    reglas = _safe_read_csv(ASOCIACION_PATH)

    if ventas_diarias.empty or productos_top.empty:
        return

    generate_all_visualizations(
        ventas_diarias,
        ventas_semanales,
        ventas_mensuales,
        ventas_dia_semana,
        ventas_hora,
        frecuencia,
        tiempo,
        segmentacion,
        productos_top,
        coocurrencia,
        reglas,
        output_dir=REPORTS_DIR,
    )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="eda_pipeline_modular",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 2 * * *",
    catchup=False,
    default_args=default_args,
    description="EDA modular para ventas",
    tags=["eda", "ventas"],
) as dag:
    start = PythonOperator(
        task_id="ensure_directories",
        python_callable=ensure_directories,
    )

    with TaskGroup("load_data") as load_group:
        categories = PythonOperator(
            task_id="load_categories",
            python_callable=load_categories_task,
        )
        product_category = PythonOperator(
            task_id="load_product_category",
            python_callable=load_product_category_task,
        )
        transactions = PythonOperator(
            task_id="load_transactions",
            python_callable=load_transactions_task,
        )

    with TaskGroup("transform_data") as transform_group:
        transform = PythonOperator(
            task_id="transform_transactions",
            python_callable=transform_transactions_task,
        )
        stats = PythonOperator(
            task_id="descriptive_stats",
            python_callable=descriptive_stats_task,
        )
        transform >> stats

    with TaskGroup("review_data") as review_group:
        review_cat = PythonOperator(
            task_id="review_categories",
            python_callable=review_categories_task,
        )
        review_product_cat = PythonOperator(
            task_id="review_product_category",
            python_callable=review_product_category_task,
        )
        review_tran = PythonOperator(
            task_id="review_transactions",
            python_callable=review_transactions_task,
        )

    with TaskGroup("product_basic_analysis") as product_basic_group:
        ppt = PythonOperator(
            task_id="products_per_transaction",
            python_callable=products_per_transaction_task,
        )
        top = PythonOperator(
            task_id="top_products",
            python_callable=top_products_task,
        )
        tran_summary = PythonOperator(
            task_id="transactions_summary",
            python_callable=transactions_summary_task,
        )

    with TaskGroup("temporal_analysis") as temporal_group:
        daily = PythonOperator(
            task_id="daily_sales",
            python_callable=daily_sales_task,
        )
        weekly = PythonOperator(
            task_id="weekly_sales",
            python_callable=weekly_sales_task,
        )
        monthly = PythonOperator(
            task_id="monthly_sales",
            python_callable=monthly_sales_task,
        )
        weekday = PythonOperator(
            task_id="weekday_patterns",
            python_callable=weekday_patterns_task,
        )
        hourly = PythonOperator(
            task_id="hourly_patterns",
            python_callable=hourly_patterns_task,
        )
        trends = PythonOperator(
            task_id="trends_seasonality",
            python_callable=trends_task,
        )

        daily >> weekly >> monthly >> weekday >> hourly >> trends   # ejecuta en serie

    with TaskGroup("customer_analysis") as customer_group:
        freq = PythonOperator(
            task_id="customer_frequency",
            python_callable=customer_frequency_task,
        )
        tbc = PythonOperator(
            task_id="time_between_purchases",
            python_callable=time_between_purchases_task,
        )
        segments = PythonOperator(
            task_id="segment_customers",
            python_callable=segment_customers_task,
        )
        freq >> segments
        tbc >> segments

    with TaskGroup("product_advanced_analysis") as product_adv_group:
        top_detailed = PythonOperator(
            task_id="top_products_detailed",
            python_callable=top_products_detailed_task,
        )
        cooc = PythonOperator(
            task_id="product_cooccurrence",
            python_callable=cooccurrence_task,
        )
        rules = PythonOperator(
            task_id="association_rules",
            python_callable=association_rules_task,
        )

    export_summary = PythonOperator(
        task_id="export_global_summary",
        python_callable=export_global_summary_task,
    )

    visualize = PythonOperator(
        task_id="generate_visualizations",
        python_callable=visualization_task,
    )

    end = EmptyOperator(task_id="end")

    start >> load_group >> transform_group
    transform_group >> review_group
    transform_group >> product_basic_group
    product_basic_group >> temporal_group >> customer_group >> product_adv_group
    product_adv_group >> export_summary >> visualize >> end