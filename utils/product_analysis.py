"""
Módulo para análisis avanzado de productos
Incluye análisis de productos más vendidos y reglas de asociación (market basket analysis)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter
from itertools import combinations


def analyze_top_products(df: pd.DataFrame, top_n: int = 50) -> pd.DataFrame:
    """
    Analiza los productos más vendidos

    Args:
        df: DataFrame transformado con productos_list
        top_n: Número de productos top a analizar

    Returns:
        DataFrame con estadísticas de productos
    """
    print(f"\nANÁLISIS DE PRODUCTOS MÁS VENDIDOS (Top {top_n})")
    print("=" * 70)

    # Expandir lista de productos
    all_products = []
    for products in df["productos_list"]:
        if products:
            all_products.extend(products)

    # Contar frecuencias
    product_freq = pd.Series(all_products).value_counts()
    product_freq_df = pd.DataFrame({
        "producto_id": product_freq.index,
        "frecuencia": product_freq.values,
        "porcentaje": (product_freq.values / product_freq.sum() * 100).round(2),
    })

    # Calcular porcentaje acumulado
    product_freq_df['porcentaje_acumulado'] = product_freq_df['porcentaje'].cumsum()

    # Estadísticas generales
    total_productos_unicos = len(product_freq_df)
    total_items_vendidos = len(all_products)
    promedio_ventas = product_freq_df['frecuencia'].mean()

    print(f"\nEstadísticas generales:")
    print(f"  • Total de productos únicos: {total_productos_unicos:,}")
    print(f"  • Total de items vendidos: {total_items_vendidos:,}")
    print(f"  • Promedio de ventas por producto: {promedio_ventas:.2f}")
    print(f"  • Mediana de ventas por producto: {product_freq_df['frecuencia'].median():.2f}")

    # Análisis de concentración (Pareto)
    top_20_pct_productos = int(total_productos_unicos * 0.2)
    ventas_top_20_pct = product_freq_df.head(top_20_pct_productos)['frecuencia'].sum()
    porcentaje_ventas_top_20 = (ventas_top_20_pct / total_items_vendidos * 100)

    print(f"\nAnálisis de concentración (Principio de Pareto):")
    print(f"  • Top 20% de productos ({top_20_pct_productos} productos)")
    print(f"  • Representan {porcentaje_ventas_top_20:.2f}% de las ventas totales")

    # Mostrar top productos
    print(f"\nTop {min(top_n, len(product_freq_df))} productos más vendidos:")
    print(product_freq_df.head(top_n).to_string(index=False))

    return product_freq_df


def find_frequent_itemsets(transactions: List[List[str]], min_support: float = 0.01) -> Dict:
    """
    Encuentra conjuntos de items frecuentes usando un enfoque simplificado

    Args:
        transactions: Lista de listas, donde cada lista es una transacción con productos
        min_support: Soporte mínimo (porcentaje de transacciones)

    Returns:
        Diccionario con itemsets frecuentes por tamaño
    """
    n_transactions = len(transactions)
    min_count = int(min_support * n_transactions)

    # Items individuales (1-itemsets)
    items_count = Counter()
    for transaction in transactions:
        for item in set(transaction):  # set para evitar contar duplicados en la misma transacción
            items_count[item] += 1

    # Filtrar por soporte mínimo
    frequent_1_itemsets = {item: count for item, count in items_count.items() if count >= min_count}

    # Pares de items (2-itemsets)
    pairs_count = Counter()
    for transaction in transactions:
        if len(transaction) >= 2:
            for pair in combinations(sorted(set(transaction)), 2):
                # Solo considerar pares donde ambos items son frecuentes individualmente
                if pair[0] in frequent_1_itemsets and pair[1] in frequent_1_itemsets:
                    pairs_count[pair] += 1

    frequent_2_itemsets = {pair: count for pair, count in pairs_count.items() if count >= min_count}

    # Triples de items (3-itemsets)
    triples_count = Counter()
    for transaction in transactions:
        if len(transaction) >= 3:
            for triple in combinations(sorted(set(transaction)), 3):
                # Solo considerar triples donde todos los items son frecuentes
                if all(item in frequent_1_itemsets for item in triple):
                    # Y donde todos los pares son frecuentes
                    pairs = list(combinations(triple, 2))
                    if all(pair in frequent_2_itemsets for pair in pairs):
                        triples_count[triple] += 1

    frequent_3_itemsets = {triple: count for triple, count in triples_count.items() if count >= min_count}

    return {
        'n_transactions': n_transactions,
        'min_support': min_support,
        'min_count': min_count,
        '1-itemsets': frequent_1_itemsets,
        '2-itemsets': frequent_2_itemsets,
        '3-itemsets': frequent_3_itemsets
    }


def calculate_association_rules(frequent_itemsets: Dict, min_confidence: float = 0.3) -> pd.DataFrame:
    """
    Calcula reglas de asociación a partir de itemsets frecuentes

    Reglas de la forma: {A} -> {B}
    - Soporte: frecuencia de {A, B} juntos
    - Confianza: P(B|A) = soporte(A,B) / soporte(A)
    - Lift: confianza(A->B) / soporte(B)

    Args:
        frequent_itemsets: Diccionario con itemsets frecuentes
        min_confidence: Confianza mínima para las reglas

    Returns:
        DataFrame con reglas de asociación
    """
    rules = []

    itemsets_1 = frequent_itemsets['1-itemsets']
    itemsets_2 = frequent_itemsets['2-itemsets']
    n_transactions = frequent_itemsets['n_transactions']

    # Generar reglas de pares (A -> B)
    for (item_a, item_b), count_ab in itemsets_2.items():
        support_ab = count_ab / n_transactions
        count_a = itemsets_1[item_a]
        count_b = itemsets_1[item_b]

        # Regla: A -> B
        confidence_a_b = count_ab / count_a
        support_b = count_b / n_transactions
        lift_a_b = confidence_a_b / support_b if support_b > 0 else 0

        if confidence_a_b >= min_confidence:
            rules.append({
                'antecedente': item_a,
                'consecuente': item_b,
                'soporte': round(support_ab, 4),
                'confianza': round(confidence_a_b, 4),
                'lift': round(lift_a_b, 2),
                'num_transacciones': count_ab
            })

        # Regla: B -> A
        confidence_b_a = count_ab / count_b
        support_a = count_a / n_transactions
        lift_b_a = confidence_b_a / support_a if support_a > 0 else 0

        if confidence_b_a >= min_confidence:
            rules.append({
                'antecedente': item_b,
                'consecuente': item_a,
                'soporte': round(support_ab, 4),
                'confianza': round(confidence_b_a, 4),
                'lift': round(lift_b_a, 2),
                'num_transacciones': count_ab
            })

    # Generar reglas de triples si existen
    itemsets_3 = frequent_itemsets['3-itemsets']
    for (item_a, item_b, item_c), count_abc in itemsets_3.items():
        support_abc = count_abc / n_transactions

        # Reglas: {A, B} -> C
        pair_ab = tuple(sorted([item_a, item_b]))
        if pair_ab in itemsets_2:
            count_ab = itemsets_2[pair_ab]
            confidence = count_abc / count_ab
            count_c = itemsets_1[item_c]
            support_c = count_c / n_transactions
            lift = confidence / support_c if support_c > 0 else 0

            if confidence >= min_confidence:
                rules.append({
                    'antecedente': f"{item_a}, {item_b}",
                    'consecuente': item_c,
                    'soporte': round(support_abc, 4),
                    'confianza': round(confidence, 4),
                    'lift': round(lift, 2),
                    'num_transacciones': count_abc
                })

    rules_df = pd.DataFrame(rules)

    if len(rules_df) > 0:
        # Ordenar por lift descendente
        rules_df = rules_df.sort_values('lift', ascending=False).reset_index(drop=True)

    return rules_df


def analyze_association_rules(df: pd.DataFrame, min_support: float = 0.01, min_confidence: float = 0.3, top_n: int = 50) -> Tuple[pd.DataFrame, Dict]:
    """
    Análisis completo de reglas de asociación (Market Basket Analysis)

    Args:
        df: DataFrame transformado con productos_list
        min_support: Soporte mínimo (porcentaje de transacciones)
        min_confidence: Confianza mínima para las reglas
        top_n: Número de reglas top a mostrar

    Returns:
        Tupla con (DataFrame de reglas, Diccionario de estadísticas)
    """
    print(f"\nANÁLISIS DE REGLAS DE ASOCIACIÓN (MARKET BASKET ANALYSIS)")
    print("=" * 70)
    print(f"Parámetros:")
    print(f"  • Soporte mínimo: {min_support*100:.1f}%")
    print(f"  • Confianza mínima: {min_confidence*100:.1f}%")

    # Filtrar solo transacciones con productos
    df_with_products = df[df['tiene_productos']].copy()

    print(f"\nTotal de transacciones con productos: {len(df_with_products):,}")

    # Preparar transacciones
    transactions = df_with_products['productos_list'].tolist()

    # Calcular estadísticas de transacciones
    transaction_sizes = [len(t) for t in transactions]
    print(f"\nEstadísticas de tamaño de transacciones:")
    print(f"  • Promedio de productos por transacción: {np.mean(transaction_sizes):.2f}")
    print(f"  • Mediana: {np.median(transaction_sizes):.2f}")
    print(f"  • Máximo: {max(transaction_sizes)}")
    print(f"  • Mínimo: {min(transaction_sizes)}")

    # Encontrar itemsets frecuentes
    print(f"\nBuscando itemsets frecuentes...")
    frequent_itemsets = find_frequent_itemsets(transactions, min_support)

    print(f"\nItemsets frecuentes encontrados:")
    print(f"  • Items individuales: {len(frequent_itemsets['1-itemsets']):,}")
    print(f"  • Pares de items: {len(frequent_itemsets['2-itemsets']):,}")
    print(f"  • Triples de items: {len(frequent_itemsets['3-itemsets']):,}")

    # Calcular reglas de asociación
    print(f"\nCalculando reglas de asociación...")
    rules_df = calculate_association_rules(frequent_itemsets, min_confidence)

    if len(rules_df) == 0:
        print(f"\n⚠ No se encontraron reglas de asociación con los parámetros especificados.")
        print(f"   Intenta reducir el soporte mínimo o la confianza mínima.")
        return rules_df, {}

    print(f"\n✓ Se encontraron {len(rules_df):,} reglas de asociación")

    # Estadísticas de las reglas
    print(f"\nEstadísticas de las reglas:")
    print(f"  • Confianza promedio: {rules_df['confianza'].mean():.4f}")
    print(f"  • Lift promedio: {rules_df['lift'].mean():.2f}")
    print(f"  • Lift máximo: {rules_df['lift'].max():.2f}")

    # Mostrar top reglas
    print(f"\nTop {min(top_n, len(rules_df))} reglas por Lift (más interesantes):")
    print(rules_df.head(top_n).to_string(index=False))

    # Reglas con mayor confianza
    print(f"\nTop {min(20, len(rules_df))} reglas por Confianza:")
    top_confidence = rules_df.nlargest(20, 'confianza')
    print(top_confidence[['antecedente', 'consecuente', 'confianza', 'lift', 'num_transacciones']].to_string(index=False))

    # Productos más comunes en las reglas
    print(f"\nProductos más frecuentes en reglas de asociación:")
    all_items_in_rules = []
    for _, row in rules_df.iterrows():
        # Separar items compuestos
        antecedente_items = str(row['antecedente']).split(', ')
        consecuente_items = str(row['consecuente']).split(', ')
        all_items_in_rules.extend(antecedente_items)
        all_items_in_rules.extend(consecuente_items)

    items_freq = pd.Series(all_items_in_rules).value_counts().head(20)
    print(items_freq.to_string())

    stats = {
        'total_rules': len(rules_df),
        'avg_confidence': rules_df['confianza'].mean(),
        'avg_lift': rules_df['lift'].mean(),
        'max_lift': rules_df['lift'].max(),
        'frequent_itemsets': frequent_itemsets
    }

    return rules_df, stats


def analyze_product_cooccurrence(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """
    Analiza co-ocurrencia simple de productos (qué productos se compran juntos)

    Args:
        df: DataFrame transformado con productos_list
        top_n: Número de pares top a mostrar

    Returns:
        DataFrame con pares de productos y su frecuencia
    """
    print(f"\nANÁLISIS DE CO-OCURRENCIA DE PRODUCTOS")
    print("=" * 70)

    # Filtrar transacciones con al menos 2 productos
    df_with_products = df[df['num_productos'] >= 2].copy()

    print(f"\nTransacciones con 2+ productos: {len(df_with_products):,}")

    # Contar pares de productos
    pairs_count = Counter()
    for products in df_with_products['productos_list']:
        if len(products) >= 2:
            for pair in combinations(sorted(set(products)), 2):
                pairs_count[pair] += 1

    # Crear DataFrame
    pairs_df = pd.DataFrame([
        {
            'producto_1': pair[0],
            'producto_2': pair[1],
            'frecuencia': count,
            'porcentaje': round(count / len(df_with_products) * 100, 2)
        }
        for pair, count in pairs_count.most_common(top_n * 2)
    ])

    if len(pairs_df) == 0:
        print("\nNo se encontraron pares de productos.")
        return pairs_df

    print(f"\nTotal de pares únicos encontrados: {len(pairs_count):,}")
    print(f"\nTop {min(top_n, len(pairs_df))} pares de productos más frecuentes:")
    print(pairs_df.head(top_n).to_string(index=False))

    return pairs_df
