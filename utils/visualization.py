"""
Módulo para visualización de datos
Genera gráficas para análisis temporal, de clientes y de productos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def setup_plot_style():
    """Configura el estilo general de las gráficas"""
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9


# ============================================================
# GRÁFICAS DE ANÁLISIS TEMPORAL
# ============================================================

def plot_daily_sales(ventas_diarias: pd.DataFrame, output_dir: Path):
    """
    Gráfica de ventas diarias (serie temporal)

    Args:
        ventas_diarias: DataFrame con ventas por día
        output_dir: Directorio de salida
    """
    print("\n  Generando gráfica: ventas diarias...")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Gráfica 1: Transacciones por día
    ax1.plot(ventas_diarias['fecha'], ventas_diarias['total_transacciones'],
             color='#2E86AB', linewidth=1.5, marker='o', markersize=3)
    ax1.set_title('Evolución de Transacciones Diarias', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Total de Transacciones')
    ax1.grid(True, alpha=0.3)

    # Añadir línea de tendencia
    z = np.polyfit(range(len(ventas_diarias)), ventas_diarias['total_transacciones'], 1)
    p = np.poly1d(z)
    ax1.plot(ventas_diarias['fecha'], p(range(len(ventas_diarias))),
             "--", color='red', linewidth=2, alpha=0.7, label='Tendencia')
    ax1.legend()

    # Gráfica 2: Productos vendidos por día
    ax2.plot(ventas_diarias['fecha'], ventas_diarias['total_productos'],
             color='#A23B72', linewidth=1.5, marker='o', markersize=3)
    ax2.set_title('Evolución de Productos Vendidos Diarios', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Fecha')
    ax2.set_ylabel('Total de Productos')
    ax2.grid(True, alpha=0.3)

    # Añadir línea de tendencia
    z2 = np.polyfit(range(len(ventas_diarias)), ventas_diarias['total_productos'], 1)
    p2 = np.poly1d(z2)
    ax2.plot(ventas_diarias['fecha'], p2(range(len(ventas_diarias))),
             "--", color='red', linewidth=2, alpha=0.7, label='Tendencia')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_ventas_diarias.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_weekly_monthly_sales(ventas_semanales: pd.DataFrame, ventas_mensuales: pd.DataFrame, output_dir: Path):
    """
    Gráfica de ventas semanales y mensuales

    Args:
        ventas_semanales: DataFrame con ventas por semana
        ventas_mensuales: DataFrame con ventas por mes
        output_dir: Directorio de salida
    """
    print("\n  Generando gráfica: ventas semanales y mensuales...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfica 1: Ventas semanales
    semanas_label = [f"S{row['semana']}" for _, row in ventas_semanales.iterrows()]
    ax1.bar(semanas_label, ventas_semanales['total_transacciones'],
            color='#06A77D', alpha=0.7, edgecolor='black')
    ax1.set_title('Transacciones por Semana', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Semana del Año')
    ax1.set_ylabel('Total de Transacciones')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')

    # Gráfica 2: Ventas mensuales
    ax2.bar(ventas_mensuales['mes_nombre'], ventas_mensuales['total_transacciones'],
            color='#F18F01', alpha=0.7, edgecolor='black')
    ax2.set_title('Transacciones por Mes', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Mes')
    ax2.set_ylabel('Total de Transacciones')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_ventas_semanales_mensuales.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_day_of_week_patterns(ventas_dia_semana: pd.DataFrame, output_dir: Path):
    """
    Gráfica de patrones por día de la semana

    Args:
        ventas_dia_semana: DataFrame con ventas por día de la semana
        output_dir: Directorio de salida
    """
    print("\n  Generando gráfica: patrones por día de la semana...")

    fig, ax = plt.subplots(figsize=(12, 6))

    # Crear gráfica de barras con colores degradados
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(ventas_dia_semana)))
    bars = ax.bar(ventas_dia_semana['dia_semana'],
                   ventas_dia_semana['total_transacciones'],
                   color=colors, alpha=0.8, edgecolor='black')

    ax.set_title('Transacciones por Día de la Semana', fontsize=16, fontweight='bold')
    ax.set_xlabel('Día de la Semana')
    ax.set_ylabel('Total de Transacciones')
    ax.grid(True, alpha=0.3, axis='y')

    # Añadir valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_ventas_dia_semana.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_hourly_patterns(ventas_hora: pd.DataFrame, output_dir: Path):
    """
    Gráfica de patrones por hora del día

    Args:
        ventas_hora: DataFrame con ventas por hora
        output_dir: Directorio de salida
    """
    print("\n  Generando gráfica: patrones por hora...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfica 1: Transacciones por hora
    ax1.plot(ventas_hora['hora'], ventas_hora['total_transacciones'],
             marker='o', linewidth=2, markersize=8, color='#D62828')
    ax1.fill_between(ventas_hora['hora'], ventas_hora['total_transacciones'],
                     alpha=0.3, color='#D62828')
    ax1.set_title('Transacciones por Hora del Día', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Hora del Día')
    ax1.set_ylabel('Total de Transacciones')
    ax1.set_xticks(range(0, 24, 2))
    ax1.grid(True, alpha=0.3)

    # Gráfica 2: Productos por hora
    ax2.plot(ventas_hora['hora'], ventas_hora['total_productos'],
             marker='s', linewidth=2, markersize=8, color='#003049')
    ax2.fill_between(ventas_hora['hora'], ventas_hora['total_productos'],
                     alpha=0.3, color='#003049')
    ax2.set_title('Productos Vendidos por Hora del Día', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Hora del Día')
    ax2.set_ylabel('Total de Productos')
    ax2.set_xticks(range(0, 24, 2))
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_ventas_hora.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================
# GRÁFICAS DE ANÁLISIS DE CLIENTES
# ============================================================

def plot_customer_frequency(frecuencia_clientes: pd.DataFrame, output_dir: Path):
    """
    Gráficas de frecuencia de compra de clientes

    Args:
        frecuencia_clientes: DataFrame con frecuencia de clientes
        output_dir: Directorio de salida
    """
    print("\n  Generando gráfica: frecuencia de clientes...")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    # Gráfica 1: Histograma de número de transacciones
    ax1.hist(frecuencia_clientes['num_transacciones'], bins=50,
             color='#06A77D', alpha=0.7, edgecolor='black')
    ax1.set_title('Distribución de Transacciones por Cliente', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Número de Transacciones')
    ax1.set_ylabel('Número de Clientes')
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3)

    # Gráfica 2: Histograma de productos por cliente
    ax2.hist(frecuencia_clientes['total_productos'], bins=50,
             color='#F18F01', alpha=0.7, edgecolor='black')
    ax2.set_title('Distribución de Productos por Cliente', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Número de Productos')
    ax2.set_ylabel('Número de Clientes')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)

    # Gráfica 3: Top 20 clientes más activos
    top_20 = frecuencia_clientes.nlargest(20, 'num_transacciones')
    ax3.barh(range(len(top_20)), top_20['num_transacciones'], color='#2E86AB', alpha=0.7)
    ax3.set_yticks(range(len(top_20)))
    ax3.set_yticklabels([f"Cliente {pid}" for pid in top_20['persona_id']], fontsize=8)
    ax3.set_title('Top 20 Clientes Más Activos', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Número de Transacciones')
    ax3.invert_yaxis()
    ax3.grid(True, alpha=0.3, axis='x')

    # Gráfica 4: Scatter plot transacciones vs productos
    ax4.scatter(frecuencia_clientes['num_transacciones'],
               frecuencia_clientes['total_productos'],
               alpha=0.5, s=20, color='#A23B72')
    ax4.set_title('Relación: Transacciones vs Productos', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Número de Transacciones')
    ax4.set_ylabel('Total de Productos')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_frecuencia_clientes.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_customer_segmentation(segmentacion: pd.DataFrame, output_dir: Path):
    """
    Gráficas de segmentación de clientes

    Args:
        segmentacion: DataFrame con segmentación RFM
        output_dir: Directorio de salida
    """
    print("\n  Generando gráfica: segmentación de clientes...")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    # Gráfica 1: Distribución de segmentos
    segmentos_count = segmentacion['segmento'].value_counts()
    colors_segmentos = plt.cm.Set3(range(len(segmentos_count)))
    ax1.pie(segmentos_count.values, labels=segmentos_count.index, autopct='%1.1f%%',
            startangle=90, colors=colors_segmentos)
    ax1.set_title('Distribución de Segmentos de Clientes', fontsize=14, fontweight='bold')

    # Gráfica 2: Segmentos por número de clientes
    ax2.barh(segmentos_count.index, segmentos_count.values, color=colors_segmentos, alpha=0.7)
    ax2.set_title('Clientes por Segmento', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Número de Clientes')
    ax2.grid(True, alpha=0.3, axis='x')

    # Añadir valores en las barras
    for i, v in enumerate(segmentos_count.values):
        ax2.text(v, i, f' {v:,}', va='center', fontsize=9)

    # Gráfica 3: Scatter RFM (Recency vs Frequency)
    scatter = ax3.scatter(segmentacion['recency_score'],
                         segmentacion['frequency_score'],
                         c=segmentacion['monetary_score'],
                         cmap='viridis', s=30, alpha=0.6)
    ax3.set_title('Matriz RFM: Recency vs Frequency (color=Monetary)',
                  fontsize=14, fontweight='bold')
    ax3.set_xlabel('Recency Score')
    ax3.set_ylabel('Frequency Score')
    plt.colorbar(scatter, ax=ax3, label='Monetary Score')
    ax3.grid(True, alpha=0.3)

    # Gráfica 4: Box plot de RFM score por segmento
    segmentos_para_box = segmentacion.groupby('segmento')['rfm_score'].apply(list)
    ax4.boxplot([segmentos_para_box[seg] for seg in segmentos_count.index],
                labels=segmentos_count.index, patch_artist=True)
    ax4.set_title('Distribución de RFM Score por Segmento', fontsize=14, fontweight='bold')
    ax4.set_ylabel('RFM Score')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_segmentacion_clientes.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_time_between_purchases(tiempo_compras: pd.DataFrame, output_dir: Path):
    """
    Gráficas de tiempo entre compras

    Args:
        tiempo_compras: DataFrame con tiempo entre compras
        output_dir: Directorio de salida
    """
    print("\n  Generando gráfica: tiempo entre compras...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfica 1: Histograma de días promedio entre compras
    ax1.hist(tiempo_compras['promedio_dias'], bins=50,
             color='#06A77D', alpha=0.7, edgecolor='black')
    ax1.set_title('Distribución de Días Promedio entre Compras', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Días Promedio')
    ax1.set_ylabel('Número de Clientes')
    ax1.axvline(tiempo_compras['promedio_dias'].median(), color='red',
                linestyle='--', linewidth=2, label=f'Mediana: {tiempo_compras["promedio_dias"].median():.1f} días')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfica 2: Distribución por categoría de frecuencia
    if 'frecuencia_categoria' in tiempo_compras.columns:
        categorias_count = tiempo_compras['frecuencia_categoria'].value_counts()
        colors_cat = plt.cm.Pastel1(range(len(categorias_count)))
        ax2.pie(categorias_count.values, labels=categorias_count.index, autopct='%1.1f%%',
                startangle=90, colors=colors_cat)
        ax2.set_title('Clasificación de Clientes por Frecuencia', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_tiempo_entre_compras.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================
# GRÁFICAS DE ANÁLISIS DE PRODUCTOS
# ============================================================

def plot_top_products(productos_top: pd.DataFrame, output_dir: Path, top_n: int = 20):
    """
    Gráficas de productos más vendidos

    Args:
        productos_top: DataFrame con productos y frecuencias
        output_dir: Directorio de salida
        top_n: Número de productos top a mostrar
    """
    print(f"\n  Generando gráfica: top {top_n} productos...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Gráfica 1: Top N productos
    top_n_products = productos_top.head(top_n)
    colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(top_n_products)))

    ax1.barh(range(len(top_n_products)), top_n_products['frecuencia'], color=colors, alpha=0.8)
    ax1.set_yticks(range(len(top_n_products)))
    ax1.set_yticklabels([f"Prod {pid}" for pid in top_n_products['producto_id']], fontsize=9)
    ax1.set_title(f'Top {top_n} Productos Más Vendidos', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Frecuencia de Venta')
    ax1.invert_yaxis()
    ax1.grid(True, alpha=0.3, axis='x')

    # Añadir valores en las barras
    for i, (freq, pct) in enumerate(zip(top_n_products['frecuencia'], top_n_products['porcentaje'])):
        ax1.text(freq, i, f' {freq:,} ({pct}%)', va='center', fontsize=8)

    # Gráfica 2: Curva de Pareto
    productos_top_sorted = productos_top.sort_values('frecuencia', ascending=False).reset_index(drop=True)
    productos_top_sorted['porcentaje_acumulado'] = productos_top_sorted['porcentaje'].cumsum()

    ax2_twin = ax2.twinx()
    ax2.bar(range(len(productos_top_sorted[:50])), productos_top_sorted['frecuencia'][:50],
            color='#2E86AB', alpha=0.6, label='Frecuencia')
    ax2_twin.plot(range(len(productos_top_sorted[:50])), productos_top_sorted['porcentaje_acumulado'][:50],
                  color='red', linewidth=2, marker='o', markersize=4, label='% Acumulado')

    ax2.set_title('Análisis de Pareto - Top 50 Productos', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Ranking de Productos')
    ax2.set_ylabel('Frecuencia', color='#2E86AB')
    ax2_twin.set_ylabel('Porcentaje Acumulado (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='#2E86AB')
    ax2_twin.tick_params(axis='y', labelcolor='red')
    ax2.grid(True, alpha=0.3)

    # Añadir línea del 80%
    ax2_twin.axhline(y=80, color='green', linestyle='--', linewidth=2, alpha=0.7, label='80%')
    ax2_twin.legend(loc='center right')

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_top_productos.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_product_cooccurrence(coocurrencia: pd.DataFrame, output_dir: Path, top_n: int = 20):
    """
    Gráfica de co-ocurrencia de productos

    Args:
        coocurrencia: DataFrame con pares de productos
        output_dir: Directorio de salida
        top_n: Número de pares top a mostrar
    """
    if len(coocurrencia) == 0:
        print("\n  Saltando gráfica de co-ocurrencia: no hay datos")
        return

    print(f"\n  Generando gráfica: co-ocurrencia de productos (top {top_n})...")

    fig, ax = plt.subplots(figsize=(12, 10))

    top_pairs = coocurrencia.head(top_n)
    labels = [f"({p1}, {p2})" for p1, p2 in zip(top_pairs['producto_1'], top_pairs['producto_2'])]

    colors = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(top_pairs)))
    bars = ax.barh(range(len(top_pairs)), top_pairs['frecuencia'], color=colors, alpha=0.8)

    ax.set_yticks(range(len(top_pairs)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_title(f'Top {top_n} Pares de Productos que se Compran Juntos', fontsize=14, fontweight='bold')
    ax.set_xlabel('Frecuencia de Co-ocurrencia')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis='x')

    # Añadir valores en las barras
    for i, (freq, pct) in enumerate(zip(top_pairs['frecuencia'], top_pairs['porcentaje'])):
        ax.text(freq, i, f' {freq:,} ({pct}%)', va='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_coocurrencia_productos.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_association_rules(reglas: pd.DataFrame, output_dir: Path, top_n: int = 20):
    """
    Gráficas de reglas de asociación

    Args:
        reglas: DataFrame con reglas de asociación
        output_dir: Directorio de salida
        top_n: Número de reglas top a mostrar
    """
    if len(reglas) == 0:
        print("\n  Saltando gráfica de reglas de asociación: no hay datos")
        return

    print(f"\n  Generando gráfica: reglas de asociación (top {top_n})...")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    top_rules = reglas.head(top_n)

    # Gráfica 1: Top reglas por Lift
    labels = [f"{ant} → {cons}" for ant, cons in zip(top_rules['antecedente'], top_rules['consecuente'])]
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top_rules)))

    ax1.barh(range(len(top_rules)), top_rules['lift'], color=colors, alpha=0.8)
    ax1.set_yticks(range(len(top_rules)))
    ax1.set_yticklabels(labels, fontsize=8)
    ax1.set_title(f'Top {top_n} Reglas por Lift', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Lift')
    ax1.invert_yaxis()
    ax1.grid(True, alpha=0.3, axis='x')

    # Gráfica 2: Scatter Soporte vs Confianza (color = Lift)
    scatter = ax2.scatter(reglas['soporte'], reglas['confianza'],
                         c=reglas['lift'], cmap='viridis', s=100, alpha=0.6)
    ax2.set_title('Reglas: Soporte vs Confianza (color=Lift)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Soporte')
    ax2.set_ylabel('Confianza')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax2, label='Lift')

    # Gráfica 3: Histograma de Lift
    ax3.hist(reglas['lift'], bins=30, color='#06A77D', alpha=0.7, edgecolor='black')
    ax3.set_title('Distribución de Lift en las Reglas', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Lift')
    ax3.set_ylabel('Frecuencia')
    ax3.axvline(reglas['lift'].median(), color='red', linestyle='--',
                linewidth=2, label=f'Mediana: {reglas["lift"].median():.2f}')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Gráfica 4: Histograma de Confianza
    ax4.hist(reglas['confianza'], bins=30, color='#F18F01', alpha=0.7, edgecolor='black')
    ax4.set_title('Distribución de Confianza en las Reglas', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Confianza')
    ax4.set_ylabel('Frecuencia')
    ax4.axvline(reglas['confianza'].median(), color='red', linestyle='--',
                linewidth=2, label=f'Mediana: {reglas["confianza"].median():.4f}')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'grafica_reglas_asociacion.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================
# FUNCIÓN PRINCIPAL PARA GENERAR TODAS LAS GRÁFICAS
# ============================================================

def plot_boxplot_analysis(df_transactions, df_customers, graficas_dir):
    """
    Genera boxplots para detectar outliers en distribuciones

    Args:
        df_transactions: DataFrame con datos de transacciones
        df_customers: DataFrame con frecuencia de clientes
        graficas_dir: Directorio donde guardar las gráficas
    """
    print("Generando boxplots de análisis...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Análisis de Distribuciones - Detección de Outliers',
                 fontsize=16, fontweight='bold', y=0.995)

    # 1. Boxplot de productos por transacción
    ax1 = axes[0, 0]
    if 'num_productos' in df_transactions.columns:
        data_to_plot = df_transactions['num_productos'].dropna()
        ax1.boxplot(data_to_plot, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightblue', alpha=0.7),
                   medianprops=dict(color='red', linewidth=2))
        ax1.set_ylabel('Número de Productos', fontsize=12)
        ax1.set_title('Productos por Transacción', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')

        # Estadísticas
        q1 = data_to_plot.quantile(0.25)
        q3 = data_to_plot.quantile(0.75)
        iqr = q3 - q1
        outliers = len(data_to_plot[(data_to_plot < q1 - 1.5*iqr) | (data_to_plot > q3 + 1.5*iqr)])
        ax1.text(0.02, 0.98, f'Outliers: {outliers:,} ({outliers/len(data_to_plot)*100:.1f}%)',
                transform=ax1.transAxes, va='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 2. Boxplot de transacciones por cliente
    ax2 = axes[0, 1]
    if 'num_transacciones' in df_customers.columns:
        data_to_plot = df_customers['num_transacciones'].dropna()
        ax2.boxplot(data_to_plot, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightgreen', alpha=0.7),
                   medianprops=dict(color='red', linewidth=2))
        ax2.set_ylabel('Número de Transacciones', fontsize=12)
        ax2.set_title('Transacciones por Cliente', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')

        # Estadísticas
        q1 = data_to_plot.quantile(0.25)
        q3 = data_to_plot.quantile(0.75)
        iqr = q3 - q1
        outliers = len(data_to_plot[(data_to_plot < q1 - 1.5*iqr) | (data_to_plot > q3 + 1.5*iqr)])
        ax2.text(0.02, 0.98, f'Outliers: {outliers:,} ({outliers/len(data_to_plot)*100:.1f}%)',
                transform=ax2.transAxes, va='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 3. Boxplot de productos totales por cliente
    ax3 = axes[1, 0]
    if 'total_productos' in df_customers.columns:
        data_to_plot = df_customers['total_productos'].dropna()
        ax3.boxplot(data_to_plot, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightcoral', alpha=0.7),
                   medianprops=dict(color='red', linewidth=2))
        ax3.set_ylabel('Total de Productos', fontsize=12)
        ax3.set_title('Volumen Total por Cliente', fontsize=13, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')

        # Estadísticas
        q1 = data_to_plot.quantile(0.25)
        q3 = data_to_plot.quantile(0.75)
        iqr = q3 - q1
        outliers = len(data_to_plot[(data_to_plot < q1 - 1.5*iqr) | (data_to_plot > q3 + 1.5*iqr)])
        ax3.text(0.02, 0.98, f'Outliers: {outliers:,} ({outliers/len(data_to_plot)*100:.1f}%)',
                transform=ax3.transAxes, va='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 4. Boxplot de promedio de productos por transacción por cliente
    ax4 = axes[1, 1]
    if 'promedio_productos_por_transaccion' in df_customers.columns:
        data_to_plot = df_customers['promedio_productos_por_transaccion'].dropna()
        ax4.boxplot(data_to_plot, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightyellow', alpha=0.7),
                   medianprops=dict(color='red', linewidth=2))
        ax4.set_ylabel('Promedio de Productos/Transacción', fontsize=12)
        ax4.set_title('Promedio de Productos por Transacción', fontsize=13, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')

        # Estadísticas
        q1 = data_to_plot.quantile(0.25)
        q3 = data_to_plot.quantile(0.75)
        iqr = q3 - q1
        outliers = len(data_to_plot[(data_to_plot < q1 - 1.5*iqr) | (data_to_plot > q3 + 1.5*iqr)])
        ax4.text(0.02, 0.98, f'Outliers: {outliers:,} ({outliers/len(data_to_plot)*100:.1f}%)',
                transform=ax4.transAxes, va='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    output_path = graficas_dir / 'grafica_boxplot_outliers.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Boxplot guardado: {output_path.name}")


def plot_correlation_heatmap(df_customers, df_time_between, graficas_dir):
    """
    Genera heatmap de correlación entre variables numéricas

    Args:
        df_customers: DataFrame con datos de clientes
        df_time_between: DataFrame con tiempo entre compras
        graficas_dir: Directorio donde guardar las gráficas
    """
    print("Generando heatmap de correlación...")

    # Seleccionar variables numéricas relevantes
    customer_vars = ['num_transacciones', 'total_productos', 'promedio_productos_por_transaccion']

    # Crear DataFrame para análisis
    df_analysis = df_customers[customer_vars].copy()

    # Agregar promedio de días entre compras si está disponible
    if not df_time_between.empty and 'promedio_dias' in df_time_between.columns:
        # Agregar como nueva columna
        avg_days_by_customer = df_time_between.groupby('persona_id')['promedio_dias'].mean()
        df_analysis = df_analysis.merge(
            avg_days_by_customer.to_frame('dias_entre_compras'),
            left_index=True,
            right_index=True,
            how='left'
        )

    # Renombrar columnas para mejor visualización
    column_names = {
        'num_transacciones': 'Frecuencia\nCompras',
        'total_productos': 'Volumen\nTotal',
        'promedio_productos_por_transaccion': 'Productos/\nTransacción',
        'dias_entre_compras': 'Días entre\nCompras'
    }
    df_analysis = df_analysis.rename(columns=column_names)

    # Calcular matriz de correlación
    corr_matrix = df_analysis.corr()

    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # Generar heatmap
    im = ax.imshow(corr_matrix, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)

    # Configurar ejes
    ax.set_xticks(np.arange(len(corr_matrix.columns)))
    ax.set_yticks(np.arange(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, fontsize=11)
    ax.set_yticklabels(corr_matrix.columns, fontsize=11)

    # Rotar etiquetas del eje x
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

    # Agregar valores de correlación en cada celda
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            value = corr_matrix.iloc[i, j]
            color = 'white' if abs(value) > 0.5 else 'black'
            text = ax.text(j, i, f'{value:.2f}',
                          ha="center", va="center", color=color,
                          fontsize=12, fontweight='bold')

    # Título y colorbar
    ax.set_title('Matriz de Correlación - Variables de Comportamiento de Clientes',
                fontsize=14, fontweight='bold', pad=20)
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Coeficiente de Correlación', fontsize=12)

    # Agregar interpretación
    interpretation = (
        "Interpretación:\n"
        "• Valores cercanos a +1: Correlación positiva fuerte\n"
        "• Valores cercanos a 0: Sin correlación\n"
        "• Valores cercanos a -1: Correlación negativa fuerte"
    )
    plt.figtext(0.5, -0.05, interpretation, ha='center', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

    plt.tight_layout()
    output_path = graficas_dir / 'grafica_correlacion_heatmap.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Heatmap guardado: {output_path.name}")


def generate_all_visualizations(
    ventas_diarias: pd.DataFrame,
    ventas_semanales: pd.DataFrame,
    ventas_mensuales: pd.DataFrame,
    ventas_dia_semana: pd.DataFrame,
    ventas_hora: pd.DataFrame,
    frecuencia_clientes: pd.DataFrame,
    tiempo_compras: pd.DataFrame,
    segmentacion: pd.DataFrame,
    productos_top: pd.DataFrame,
    coocurrencia: pd.DataFrame,
    reglas: pd.DataFrame,
    output_dir: Path,
    df_transactions: Optional[pd.DataFrame] = None
):
    """
    Genera todas las visualizaciones del análisis

    Args:
        Varios DataFrames con los resultados de análisis
        output_dir: Directorio de salida para las gráficas
        df_transactions: DataFrame con transacciones transformadas (opcional, para boxplot)
    """
    print("\n" + "=" * 70)
    print("GENERANDO VISUALIZACIONES")
    print("=" * 70)

    setup_plot_style()

    # Crear subdirectorio para gráficas
    graficas_dir = output_dir / "graficas"
    graficas_dir.mkdir(exist_ok=True)

    print("\nGenerando gráficas de análisis temporal...")
    plot_daily_sales(ventas_diarias, graficas_dir)
    plot_weekly_monthly_sales(ventas_semanales, ventas_mensuales, graficas_dir)
    plot_day_of_week_patterns(ventas_dia_semana, graficas_dir)
    plot_hourly_patterns(ventas_hora, graficas_dir)

    print("\nGenerando gráficas de análisis de clientes...")
    plot_customer_frequency(frecuencia_clientes, graficas_dir)
    if len(tiempo_compras) > 0:
        plot_time_between_purchases(tiempo_compras, graficas_dir)
    plot_customer_segmentation(segmentacion, graficas_dir)

    print("\nGenerando gráficas de análisis de productos...")
    plot_top_products(productos_top, graficas_dir, top_n=20)
    if len(coocurrencia) > 0:
        plot_product_cooccurrence(coocurrencia, graficas_dir, top_n=20)
    if len(reglas) > 0:
        plot_association_rules(reglas, graficas_dir, top_n=20)

    print("\nGenerando visualizaciones analíticas avanzadas...")
    # Boxplot de outliers
    if df_transactions is not None and not frecuencia_clientes.empty:
        plot_boxplot_analysis(df_transactions, frecuencia_clientes, graficas_dir)

    # Heatmap de correlación
    if not frecuencia_clientes.empty:
        plot_correlation_heatmap(frecuencia_clientes, tiempo_compras, graficas_dir)

    print(f"\n✓ Todas las gráficas generadas en: {graficas_dir}")
    print(f"  Total de gráficas generadas: {len(list(graficas_dir.glob('*.png')))}")
