"""Utilidades auxiliares para el backend"""

def format_number(value, decimals=2):
    """Formatea un número con separador de miles"""
    if value is None:
        return "N/A"
    try:
        return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)

def safe_division(numerator, denominator, default=0):
    """División segura que retorna default si el denominador es 0"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default

def parse_percentage(value_str):
    """Convierte un string de porcentaje a float"""
    try:
        if isinstance(value_str, str):
            return float(value_str.replace('%', '').strip())
        return float(value_str)
    except (ValueError, AttributeError):
        return 0.0
