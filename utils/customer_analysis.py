"""
Módulo para análisis de comportamiento de clientes
Análisis de frecuencia, tiempo entre compras y segmentación
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def analyze_customer_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza la frecuencia de compra por cliente

    Args:
        df: DataFrame transformado con persona_id

    Returns:
        DataFrame con estadísticas de frecuencia por cliente
    """
    print("\nANÁLISIS DE FRECUENCIA DE COMPRA POR CLIENTE")
    print("=" * 70)

    # Preparar datos temporales
    df_temp = df.copy()
    df_temp['fecha'] = pd.to_datetime(df_temp['fecha'])

    # Agrupar por cliente
    frecuencia_clientes = df_temp.groupby('persona_id').agg({
        'fecha': 'count',  # Número de transacciones
        'num_productos': 'sum',  # Total de productos comprados
        'tiene_productos': 'sum'  # Transacciones con productos
    }).reset_index()

    frecuencia_clientes.columns = ['persona_id', 'num_transacciones', 'total_productos', 'transacciones_con_productos']

    # Calcular métricas adicionales
    frecuencia_clientes['promedio_productos_por_transaccion'] = (
        frecuencia_clientes['total_productos'] / frecuencia_clientes['num_transacciones']
    ).round(2)

    frecuencia_clientes['porcentaje_transacciones_con_productos'] = (
        frecuencia_clientes['transacciones_con_productos'] / frecuencia_clientes['num_transacciones'] * 100
    ).round(2)

    # Estadísticas generales
    print(f"\nTotal de clientes únicos: {len(frecuencia_clientes):,}")
    print(f"\nEstadísticas de frecuencia de compra:")
    print(f"  • Promedio de transacciones por cliente: {frecuencia_clientes['num_transacciones'].mean():.2f}")
    print(f"  • Mediana de transacciones por cliente: {frecuencia_clientes['num_transacciones'].median():.2f}")
    print(f"  • Máximo de transacciones por cliente: {frecuencia_clientes['num_transacciones'].max()}")
    print(f"  • Mínimo de transacciones por cliente: {frecuencia_clientes['num_transacciones'].min()}")

    print(f"\n  • Promedio de productos por cliente: {frecuencia_clientes['total_productos'].mean():.2f}")
    print(f"  • Mediana de productos por cliente: {frecuencia_clientes['total_productos'].median():.2f}")
    print(f"  • Máximo de productos por cliente: {frecuencia_clientes['total_productos'].max()}")

    # Distribución de frecuencia
    print(f"\nDistribución de clientes por número de transacciones:")
    distribucion = frecuencia_clientes['num_transacciones'].value_counts().sort_index()
    for num_trans, count in distribucion.head(10).items():
        porcentaje = count / len(frecuencia_clientes) * 100
        print(f"  • {num_trans} transacción(es): {count:,} clientes ({porcentaje:.2f}%)")

    # Top clientes más activos
    print(f"\nTop 20 clientes más activos:")
    top_clientes = frecuencia_clientes.nlargest(20, 'num_transacciones')
    print(top_clientes[['persona_id', 'num_transacciones', 'total_productos', 'promedio_productos_por_transaccion']].to_string(index=False))

    return frecuencia_clientes


def analyze_time_between_purchases(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza el tiempo promedio entre compras por cliente

    Args:
        df: DataFrame transformado con persona_id y fecha

    Returns:
        DataFrame con estadísticas de tiempo entre compras
    """
    print("\nANÁLISIS DE TIEMPO ENTRE COMPRAS")
    print("=" * 70)

    # Preparar datos
    df_temp = df.copy()
    df_temp['fecha'] = pd.to_datetime(df_temp['fecha'])

    # Ordenar por cliente y fecha
    df_temp = df_temp.sort_values(['persona_id', 'fecha'])

    # Calcular diferencia de tiempo entre compras consecutivas
    df_temp['fecha_compra_anterior'] = df_temp.groupby('persona_id')['fecha'].shift(1)
    df_temp['dias_desde_ultima_compra'] = (df_temp['fecha'] - df_temp['fecha_compra_anterior']).dt.total_seconds() / (24 * 3600)

    # Filtrar solo clientes con más de una compra
    clientes_recurrentes = df_temp[df_temp['dias_desde_ultima_compra'].notna()]

    if len(clientes_recurrentes) == 0:
        print("\nNo hay clientes con compras recurrentes en el dataset.")
        return pd.DataFrame()

    # Estadísticas por cliente
    tiempo_entre_compras = clientes_recurrentes.groupby('persona_id').agg({
        'dias_desde_ultima_compra': ['mean', 'median', 'min', 'max', 'count']
    }).reset_index()

    tiempo_entre_compras.columns = ['persona_id', 'promedio_dias', 'mediana_dias', 'min_dias', 'max_dias', 'num_intervalos']
    tiempo_entre_compras = tiempo_entre_compras.round(2)

    print(f"\nClientes con compras recurrentes: {len(tiempo_entre_compras):,}")
    print(f"Total de intervalos analizados: {tiempo_entre_compras['num_intervalos'].sum():.0f}")

    print(f"\nEstadísticas generales de tiempo entre compras:")
    print(f"  • Promedio general: {clientes_recurrentes['dias_desde_ultima_compra'].mean():.2f} días")
    print(f"  • Mediana general: {clientes_recurrentes['dias_desde_ultima_compra'].median():.2f} días")
    print(f"  • Mínimo: {clientes_recurrentes['dias_desde_ultima_compra'].min():.2f} días")
    print(f"  • Máximo: {clientes_recurrentes['dias_desde_ultima_compra'].max():.2f} días")

    # Clasificar clientes por frecuencia
    tiempo_entre_compras['frecuencia_categoria'] = tiempo_entre_compras['promedio_dias'].apply(lambda x:
        'Muy frecuente (< 7 días)' if x < 7 else
        'Frecuente (7-30 días)' if x < 30 else
        'Ocasional (30-90 días)' if x < 90 else
        'Esporádico (> 90 días)'
    )

    print(f"\nClasificación de clientes por frecuencia:")
    clasificacion = tiempo_entre_compras['frecuencia_categoria'].value_counts()
    for categoria, count in clasificacion.items():
        porcentaje = count / len(tiempo_entre_compras) * 100
        print(f"  • {categoria}: {count:,} clientes ({porcentaje:.2f}%)")

    # Clientes más frecuentes
    print(f"\nTop 20 clientes más frecuentes (menor tiempo entre compras):")
    top_frecuentes = tiempo_entre_compras.nsmallest(20, 'promedio_dias')
    print(top_frecuentes[['persona_id', 'promedio_dias', 'mediana_dias', 'num_intervalos']].to_string(index=False))

    return tiempo_entre_compras


def segment_customers(df: pd.DataFrame, frecuencia: pd.DataFrame, tiempo_compras: pd.DataFrame) -> pd.DataFrame:
    """
    Segmenta clientes usando RFM simplificado y otros criterios

    R = Recency (cuán reciente fue la última compra)
    F = Frequency (frecuencia de compras)
    M = Monetary (valor monetario - en este caso, productos comprados)

    Args:
        df: DataFrame transformado original
        frecuencia: DataFrame con frecuencia de compra por cliente
        tiempo_compras: DataFrame con tiempo entre compras

    Returns:
        DataFrame con segmentación de clientes
    """
    print("\nSEGMENTACIÓN DE CLIENTES")
    print("=" * 70)

    # Preparar datos
    df_temp = df.copy()
    df_temp['fecha'] = pd.to_datetime(df_temp['fecha'])

    # Calcular recency (días desde última compra)
    fecha_max = df_temp['fecha'].max()
    recency = df_temp.groupby('persona_id')['fecha'].max().reset_index()
    recency['dias_desde_ultima_compra'] = (fecha_max - recency['fecha']).dt.days
    recency = recency[['persona_id', 'dias_desde_ultima_compra']]

    # Combinar con frecuencia
    segmentacion = frecuencia.merge(recency, on='persona_id', how='left')

    # Añadir promedio de días entre compras si existe
    if len(tiempo_compras) > 0:
        segmentacion = segmentacion.merge(
            tiempo_compras[['persona_id', 'promedio_dias', 'frecuencia_categoria']],
            on='persona_id',
            how='left'
        )
    else:
        segmentacion['promedio_dias'] = np.nan
        segmentacion['frecuencia_categoria'] = 'Cliente único'

    # Calcular percentiles para segmentación
    # Recency: menor es mejor (más reciente)
    try:
        segmentacion['recency_score'] = pd.qcut(segmentacion['dias_desde_ultima_compra'], q=4, labels=[4, 3, 2, 1], duplicates='drop')
    except ValueError:
        # Si no se pueden crear 4 bins, usar menos
        try:
            segmentacion['recency_score'] = pd.qcut(segmentacion['dias_desde_ultima_compra'], q=3, labels=[3, 2, 1], duplicates='drop')
        except:
            segmentacion['recency_score'] = 2  # valor por defecto

    # Frequency: mayor es mejor
    try:
        segmentacion['frequency_score'] = pd.qcut(segmentacion['num_transacciones'], q=4, labels=[1, 2, 3, 4], duplicates='drop')
    except ValueError:
        try:
            segmentacion['frequency_score'] = pd.qcut(segmentacion['num_transacciones'], q=3, labels=[1, 2, 3], duplicates='drop')
        except:
            segmentacion['frequency_score'] = 2  # valor por defecto

    # Monetary: mayor es mejor (más productos = más valor)
    try:
        segmentacion['monetary_score'] = pd.qcut(segmentacion['total_productos'], q=4, labels=[1, 2, 3, 4], duplicates='drop')
    except ValueError:
        try:
            segmentacion['monetary_score'] = pd.qcut(segmentacion['total_productos'], q=3, labels=[1, 2, 3], duplicates='drop')
        except:
            segmentacion['monetary_score'] = 2  # valor por defecto

    # Convertir scores a numérico
    segmentacion['recency_score'] = pd.to_numeric(segmentacion['recency_score'], errors='coerce')
    segmentacion['frequency_score'] = pd.to_numeric(segmentacion['frequency_score'], errors='coerce')
    segmentacion['monetary_score'] = pd.to_numeric(segmentacion['monetary_score'], errors='coerce')

    # Calcular score RFM total
    segmentacion['rfm_score'] = (
        segmentacion['recency_score'] +
        segmentacion['frequency_score'] +
        segmentacion['monetary_score']
    )

    # Segmentar clientes basado en RFM score
    def clasificar_cliente(row):
        score = row['rfm_score']
        r = row['recency_score']
        f = row['frequency_score']
        m = row['monetary_score']

        # Clientes campeones: Alto en todo
        if score >= 10 and r >= 3 and f >= 3:
            return 'Campeones'
        # Clientes leales: Alta frecuencia y valor
        elif f >= 3 and m >= 3:
            return 'Clientes leales'
        # Clientes potenciales: Buena recencia pero baja frecuencia
        elif r >= 3 and f <= 2:
            return 'Clientes potenciales'
        # En riesgo: Buena frecuencia pero baja recencia
        elif f >= 3 and r <= 2:
            return 'En riesgo'
        # Necesitan atención: Bajo en todo
        elif score <= 6:
            return 'Necesitan atención'
        # Prometedores: Score medio
        else:
            return 'Prometedores'

    segmentacion['segmento'] = segmentacion.apply(clasificar_cliente, axis=1)

    # Estadísticas de segmentación
    print(f"\nSegmentación RFM de clientes:")
    segmentos = segmentacion['segmento'].value_counts()
    for segmento, count in segmentos.items():
        porcentaje = count / len(segmentacion) * 100
        print(f"  • {segmento}: {count:,} clientes ({porcentaje:.2f}%)")

    # Características de cada segmento
    print(f"\nCaracterísticas promedio por segmento:")
    caracteristicas = segmentacion.groupby('segmento').agg({
        'num_transacciones': 'mean',
        'total_productos': 'mean',
        'dias_desde_ultima_compra': 'mean',
        'promedio_productos_por_transaccion': 'mean'
    }).round(2)
    print(caracteristicas.to_string())

    # Top clientes por segmento
    print(f"\nTop 10 clientes 'Campeones':")
    campeones = segmentacion[segmentacion['segmento'] == 'Campeones'].nlargest(10, 'rfm_score')
    if len(campeones) > 0:
        print(campeones[['persona_id', 'num_transacciones', 'total_productos', 'dias_desde_ultima_compra', 'rfm_score']].to_string(index=False))
    else:
        print("  No hay clientes en este segmento")

    print(f"\nTop 10 clientes 'En riesgo' (requieren atención):")
    en_riesgo = segmentacion[segmentacion['segmento'] == 'En riesgo'].nlargest(10, 'num_transacciones')
    if len(en_riesgo) > 0:
        print(en_riesgo[['persona_id', 'num_transacciones', 'total_productos', 'dias_desde_ultima_compra']].to_string(index=False))
    else:
        print("  No hay clientes en este segmento")

    return segmentacion


def analyze_customer_behavior_summary(segmentacion: pd.DataFrame) -> Dict:
    """
    Genera un resumen ejecutivo del análisis de clientes

    Args:
        segmentacion: DataFrame con segmentación completa

    Returns:
        Diccionario con resumen de métricas clave
    """
    print("\nRESUMEN EJECUTIVO - ANÁLISIS DE CLIENTES")
    print("=" * 70)

    total_clientes = len(segmentacion)

    # Métricas clave
    promedio_transacciones = segmentacion['num_transacciones'].mean()
    promedio_productos = segmentacion['total_productos'].mean()
    promedio_recency = segmentacion['dias_desde_ultima_compra'].mean()

    print(f"\nMétricas generales:")
    print(f"  • Total de clientes: {total_clientes:,}")
    print(f"  • Promedio de transacciones por cliente: {promedio_transacciones:.2f}")
    print(f"  • Promedio de productos por cliente: {promedio_productos:.2f}")
    print(f"  • Días promedio desde última compra: {promedio_recency:.2f}")

    # Distribución de segmentos
    distribucion_segmentos = segmentacion['segmento'].value_counts().to_dict()

    # Clientes de alto valor (top 20%)
    umbral_alto_valor = segmentacion['total_productos'].quantile(0.8)
    clientes_alto_valor = len(segmentacion[segmentacion['total_productos'] >= umbral_alto_valor])
    productos_alto_valor = segmentacion[segmentacion['total_productos'] >= umbral_alto_valor]['total_productos'].sum()
    total_productos = segmentacion['total_productos'].sum()
    pct_productos_alto_valor = (productos_alto_valor / total_productos * 100) if total_productos > 0 else 0

    print(f"\nClientes de alto valor (top 20%):")
    print(f"  • Número de clientes: {clientes_alto_valor:,} ({clientes_alto_valor/total_clientes*100:.2f}%)")
    print(f"  • Productos comprados: {productos_alto_valor:.0f} ({pct_productos_alto_valor:.2f}% del total)")

    # Clientes en riesgo
    clientes_en_riesgo = len(segmentacion[segmentacion['segmento'] == 'En riesgo'])
    if clientes_en_riesgo > 0:
        print(f"\nAlerta - Clientes en riesgo:")
        print(f"  • {clientes_en_riesgo:,} clientes requieren atención inmediata")
        print(f"  • Representan el {clientes_en_riesgo/total_clientes*100:.2f}% de la base de clientes")

    return {
        'total_clientes': total_clientes,
        'promedio_transacciones': promedio_transacciones,
        'promedio_productos': promedio_productos,
        'promedio_recency': promedio_recency,
        'distribucion_segmentos': distribucion_segmentos,
        'clientes_alto_valor': clientes_alto_valor,
        'porcentaje_productos_alto_valor': pct_productos_alto_valor
    }
