"""
Módulo para análisis temporal de transacciones
Análisis de ventas por tiempo, tendencias y estacionalidad
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def prepare_temporal_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara datos para análisis temporal

    Args:
        df: DataFrame con columna 'fecha'

    Returns:
        DataFrame con columnas de tiempo adicionales
    """
    df = df.copy()

    # Convertir fecha a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Extraer componentes temporales
    df['año'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month
    df['dia'] = df['fecha'].dt.day
    df['dia_semana'] = df['fecha'].dt.dayofweek  # 0=Lunes, 6=Domingo
    df['dia_semana_nombre'] = df['fecha'].dt.day_name()
    df['hora'] = df['fecha'].dt.hour
    df['fecha_solo'] = df['fecha'].dt.date
    df['semana_año'] = df['fecha'].dt.isocalendar().week
    df['año_mes'] = df['fecha'].dt.to_period('M')

    return df


def analyze_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza ventas diarias

    Args:
        df: DataFrame transformado con fecha

    Returns:
        DataFrame con estadísticas de ventas diarias
    """
    print("\nANÁLISIS DE VENTAS DIARIAS")
    print("=" * 70)

    df_temp = prepare_temporal_data(df)

    # Agrupar por fecha
    ventas_diarias = df_temp.groupby('fecha_solo').agg({
        'persona_id': 'count',  # Total de transacciones
        'num_productos': 'sum',  # Total de productos vendidos
        'tiene_productos': 'sum'  # Transacciones con productos
    }).reset_index()

    ventas_diarias.columns = ['fecha', 'total_transacciones', 'total_productos', 'transacciones_con_productos']
    ventas_diarias['promedio_productos_por_transaccion'] = (
        ventas_diarias['total_productos'] / ventas_diarias['total_transacciones']
    ).round(2)

    print(f"\nRango de fechas: {ventas_diarias['fecha'].min()} a {ventas_diarias['fecha'].max()}")
    print(f"Total de días con datos: {len(ventas_diarias)}")
    print(f"\nEstadísticas de ventas diarias:")
    print(f"  • Promedio transacciones/día: {ventas_diarias['total_transacciones'].mean():.2f}")
    print(f"  • Mediana transacciones/día: {ventas_diarias['total_transacciones'].median():.2f}")
    print(f"  • Máximo transacciones/día: {ventas_diarias['total_transacciones'].max()}")
    print(f"  • Mínimo transacciones/día: {ventas_diarias['total_transacciones'].min()}")

    print(f"\n  • Promedio productos/día: {ventas_diarias['total_productos'].mean():.2f}")
    print(f"  • Máximo productos/día: {ventas_diarias['total_productos'].max()}")

    # Mostrar días con más ventas
    print("\nTop 10 días con más transacciones:")
    print(ventas_diarias.nlargest(10, 'total_transacciones')[
        ['fecha', 'total_transacciones', 'total_productos']
    ].to_string(index=False))

    return ventas_diarias


def analyze_weekly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza ventas semanales

    Args:
        df: DataFrame transformado con fecha

    Returns:
        DataFrame con estadísticas de ventas semanales
    """
    print("\nANÁLISIS DE VENTAS SEMANALES")
    print("=" * 70)

    df_temp = prepare_temporal_data(df)

    # Agrupar por año y semana
    ventas_semanales = df_temp.groupby(['año', 'semana_año']).agg({
        'persona_id': 'count',
        'num_productos': 'sum',
        'tiene_productos': 'sum'
    }).reset_index()

    ventas_semanales.columns = ['año', 'semana', 'total_transacciones', 'total_productos', 'transacciones_con_productos']
    ventas_semanales['promedio_productos_por_transaccion'] = (
        ventas_semanales['total_productos'] / ventas_semanales['total_transacciones']
    ).round(2)

    print(f"\nTotal de semanas con datos: {len(ventas_semanales)}")
    print(f"\nEstadísticas de ventas semanales:")
    print(f"  • Promedio transacciones/semana: {ventas_semanales['total_transacciones'].mean():.2f}")
    print(f"  • Mediana transacciones/semana: {ventas_semanales['total_transacciones'].median():.2f}")
    print(f"  • Máximo transacciones/semana: {ventas_semanales['total_transacciones'].max()}")
    print(f"  • Mínimo transacciones/semana: {ventas_semanales['total_transacciones'].min()}")

    print(f"\n  • Promedio productos/semana: {ventas_semanales['total_productos'].mean():.2f}")
    print(f"  • Máximo productos/semana: {ventas_semanales['total_productos'].max()}")

    # Mostrar semanas con más ventas
    print("\nTop 10 semanas con más transacciones:")
    print(ventas_semanales.nlargest(10, 'total_transacciones')[
        ['año', 'semana', 'total_transacciones', 'total_productos']
    ].to_string(index=False))

    return ventas_semanales


def analyze_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza ventas mensuales

    Args:
        df: DataFrame transformado con fecha

    Returns:
        DataFrame con estadísticas de ventas mensuales
    """
    print("\nANÁLISIS DE VENTAS MENSUALES")
    print("=" * 70)

    df_temp = prepare_temporal_data(df)

    # Agrupar por año y mes
    ventas_mensuales = df_temp.groupby(['año', 'mes']).agg({
        'persona_id': 'count',
        'num_productos': 'sum',
        'tiene_productos': 'sum'
    }).reset_index()

    ventas_mensuales.columns = ['año', 'mes', 'total_transacciones', 'total_productos', 'transacciones_con_productos']
    ventas_mensuales['promedio_productos_por_transaccion'] = (
        ventas_mensuales['total_productos'] / ventas_mensuales['total_transacciones']
    ).round(2)

    # Crear nombre de mes
    meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
             7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
    ventas_mensuales['mes_nombre'] = ventas_mensuales['mes'].map(meses)

    print(f"\nTotal de meses con datos: {len(ventas_mensuales)}")
    print(f"\nEstadísticas de ventas mensuales:")
    print(f"  • Promedio transacciones/mes: {ventas_mensuales['total_transacciones'].mean():.2f}")
    print(f"  • Mediana transacciones/mes: {ventas_mensuales['total_transacciones'].median():.2f}")
    print(f"  • Máximo transacciones/mes: {ventas_mensuales['total_transacciones'].max()}")
    print(f"  • Mínimo transacciones/mes: {ventas_mensuales['total_transacciones'].min()}")

    print(f"\n  • Promedio productos/mes: {ventas_mensuales['total_productos'].mean():.2f}")
    print(f"  • Máximo productos/mes: {ventas_mensuales['total_productos'].max()}")

    # Mostrar todos los meses
    print("\nVentas por mes:")
    print(ventas_mensuales[
        ['año', 'mes_nombre', 'total_transacciones', 'total_productos']
    ].to_string(index=False))

    return ventas_mensuales


def analyze_day_of_week_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza patrones de ventas por día de la semana

    Args:
        df: DataFrame transformado con fecha

    Returns:
        DataFrame con estadísticas por día de la semana
    """
    print("\nANÁLISIS DE PATRONES POR DÍA DE LA SEMANA")
    print("=" * 70)

    df_temp = prepare_temporal_data(df)

    # Agrupar por día de la semana
    ventas_dia_semana = df_temp.groupby(['dia_semana', 'dia_semana_nombre']).agg({
        'persona_id': 'count',
        'num_productos': 'sum',
        'tiene_productos': 'sum'
    }).reset_index()

    ventas_dia_semana.columns = ['dia_semana_num', 'dia_semana', 'total_transacciones', 'total_productos', 'transacciones_con_productos']
    ventas_dia_semana = ventas_dia_semana.sort_values('dia_semana_num')

    # Calcular porcentajes
    total_transacciones = ventas_dia_semana['total_transacciones'].sum()
    ventas_dia_semana['porcentaje_transacciones'] = (
        ventas_dia_semana['total_transacciones'] / total_transacciones * 100
    ).round(2)

    ventas_dia_semana['promedio_productos_por_transaccion'] = (
        ventas_dia_semana['total_productos'] / ventas_dia_semana['total_transacciones']
    ).round(2)

    print(f"\nVentas por día de la semana:")
    print(ventas_dia_semana[
        ['dia_semana', 'total_transacciones', 'porcentaje_transacciones', 'total_productos', 'promedio_productos_por_transaccion']
    ].to_string(index=False))

    # Identificar picos
    dia_mas_ventas = ventas_dia_semana.loc[ventas_dia_semana['total_transacciones'].idxmax()]
    dia_menos_ventas = ventas_dia_semana.loc[ventas_dia_semana['total_transacciones'].idxmin()]

    print(f"\n🔼 Día con MÁS ventas: {dia_mas_ventas['dia_semana']} ({dia_mas_ventas['total_transacciones']:.0f} transacciones)")
    print(f"🔽 Día con MENOS ventas: {dia_menos_ventas['dia_semana']} ({dia_menos_ventas['total_transacciones']:.0f} transacciones)")

    return ventas_dia_semana


def analyze_hourly_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza patrones de ventas por hora del día

    Args:
        df: DataFrame transformado con fecha

    Returns:
        DataFrame con estadísticas por hora
    """
    print("\nANÁLISIS DE PATRONES POR HORA DEL DÍA")
    print("=" * 70)

    df_temp = prepare_temporal_data(df)

    # Agrupar por hora
    ventas_hora = df_temp.groupby('hora').agg({
        'persona_id': 'count',
        'num_productos': 'sum',
        'tiene_productos': 'sum'
    }).reset_index()

    ventas_hora.columns = ['hora', 'total_transacciones', 'total_productos', 'transacciones_con_productos']

    # Calcular porcentajes
    total_transacciones = ventas_hora['total_transacciones'].sum()
    ventas_hora['porcentaje_transacciones'] = (
        ventas_hora['total_transacciones'] / total_transacciones * 100
    ).round(2)

    ventas_hora['promedio_productos_por_transaccion'] = (
        ventas_hora['total_productos'] / ventas_hora['total_transacciones']
    ).round(2)

    print(f"\nVentas por hora del día:")
    print(ventas_hora.to_string(index=False))

    # Identificar picos
    hora_mas_ventas = ventas_hora.loc[ventas_hora['total_transacciones'].idxmax()]
    hora_menos_ventas = ventas_hora.loc[ventas_hora['total_transacciones'].idxmin()]

    print(f"\n🔼 Hora con MÁS ventas: {int(hora_mas_ventas['hora']):02d}:00 ({hora_mas_ventas['total_transacciones']:.0f} transacciones)")
    print(f"🔽 Hora con MENOS ventas: {int(hora_menos_ventas['hora']):02d}:00 ({hora_menos_ventas['total_transacciones']:.0f} transacciones)")

    # Clasificar por franjas horarias
    ventas_hora['franja'] = ventas_hora['hora'].apply(lambda x:
        'Madrugada (0-6)' if 0 <= x < 6 else
        'Mañana (6-12)' if 6 <= x < 12 else
        'Tarde (12-18)' if 12 <= x < 18 else
        'Noche (18-24)'
    )

    ventas_franja = ventas_hora.groupby('franja').agg({
        'total_transacciones': 'sum',
        'total_productos': 'sum'
    }).reset_index()

    print(f"\nVentas por franja horaria:")
    print(ventas_franja.to_string(index=False))

    return ventas_hora


def analyze_trends_and_seasonality(df: pd.DataFrame) -> Dict:
    """
    Analiza tendencias y estacionalidad en las ventas

    Args:
        df: DataFrame transformado con fecha

    Returns:
        Diccionario con análisis de tendencias
    """
    print("\nANÁLISIS DE TENDENCIAS Y ESTACIONALIDAD")
    print("=" * 70)

    df_temp = prepare_temporal_data(df)

    # Ventas por mes para ver tendencia
    ventas_mes = df_temp.groupby('año_mes').agg({
        'persona_id': 'count',
        'num_productos': 'sum'
    }).reset_index()
    ventas_mes.columns = ['mes', 'transacciones', 'productos']

    # Calcular tendencia (crecimiento promedio)
    if len(ventas_mes) > 1:
        # Calcular tasa de crecimiento mes a mes
        ventas_mes['crecimiento_transacciones'] = ventas_mes['transacciones'].pct_change() * 100
        ventas_mes['crecimiento_productos'] = ventas_mes['productos'].pct_change() * 100

        crecimiento_promedio_trans = ventas_mes['crecimiento_transacciones'].mean()
        crecimiento_promedio_prod = ventas_mes['crecimiento_productos'].mean()

        print(f"\nTendencia de crecimiento:")
        print(f"  • Crecimiento promedio mensual (transacciones): {crecimiento_promedio_trans:+.2f}%")
        print(f"  • Crecimiento promedio mensual (productos): {crecimiento_promedio_prod:+.2f}%")

        # Determinar tendencia
        if crecimiento_promedio_trans > 5:
            tendencia = "Crecimiento fuerte"
        elif crecimiento_promedio_trans > 0:
            tendencia = "Crecimiento moderado"
        elif crecimiento_promedio_trans > -5:
            tendencia = "Estable"
        else:
            tendencia = "Decrecimiento"

        print(f"  • Tendencia general: {tendencia}")
    else:
        crecimiento_promedio_trans = 0
        crecimiento_promedio_prod = 0
        tendencia = "Datos insuficientes"
        print(f"\nDatos insuficientes para calcular tendencia (se necesitan al menos 2 meses)")

    # Análisis de estacionalidad por mes del año
    estacionalidad_mes = df_temp.groupby('mes').agg({
        'persona_id': 'count',
        'num_productos': 'sum'
    }).reset_index()
    estacionalidad_mes.columns = ['mes', 'transacciones', 'productos']

    meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
             7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
    estacionalidad_mes['mes_nombre'] = estacionalidad_mes['mes'].map(meses)

    # Calcular desviación respecto al promedio
    promedio_transacciones = estacionalidad_mes['transacciones'].mean()
    estacionalidad_mes['desviacion_promedio'] = (
        (estacionalidad_mes['transacciones'] - promedio_transacciones) / promedio_transacciones * 100
    ).round(2)

    print(f"\nEstacionalidad por mes del año:")
    print(estacionalidad_mes[['mes_nombre', 'transacciones', 'desviacion_promedio']].to_string(index=False))

    # Identificar meses con mayor/menor actividad
    mes_mas_activo = estacionalidad_mes.loc[estacionalidad_mes['transacciones'].idxmax()]
    mes_menos_activo = estacionalidad_mes.loc[estacionalidad_mes['transacciones'].idxmin()]

    print(f"\n  • Mes más activo: {mes_mas_activo['mes_nombre']} ({mes_mas_activo['transacciones']:.0f} transacciones)")
    print(f"  • Mes menos activo: {mes_menos_activo['mes_nombre']} ({mes_menos_activo['transacciones']:.0f} transacciones)")

    return {
        'tendencia': tendencia,
        'crecimiento_promedio_transacciones': crecimiento_promedio_trans,
        'crecimiento_promedio_productos': crecimiento_promedio_prod,
        'ventas_mensuales': ventas_mes,
        'estacionalidad': estacionalidad_mes,
        'mes_mas_activo': mes_mas_activo['mes_nombre'],
        'mes_menos_activo': mes_menos_activo['mes_nombre']
    }
