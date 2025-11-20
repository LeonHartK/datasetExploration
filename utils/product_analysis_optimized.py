"""
Análisis de productos optimizado usando mlxtend
Mucho más rápido para datasets grandes
"""

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import fpgrowth, association_rules as mlxtend_rules
from mlxtend.preprocessing import TransactionEncoder


def analyze_association_rules_optimized(
    df: pd.DataFrame,
    min_support: float = 0.01,
    min_confidence: float = 0.3,
    use_fpgrowth: bool = True,
    max_len: int = 3
) -> pd.DataFrame:
    """
    Análisis de reglas de asociación OPTIMIZADO usando mlxtend

    Args:
        df: DataFrame transformado con productos_list
        min_support: Soporte mínimo (0.01 = 1%)
        min_confidence: Confianza mínima
        use_fpgrowth: Si True usa FP-Growth (rápido), si False usa Apriori
        max_len: Longitud máxima de itemsets (3 = triples máximo)

    Returns:
        DataFrame con reglas de asociación
    """
    print(f"\n{'='*70}")
    print(f"ANÁLISIS DE REGLAS DE ASOCIACIÓN (OPTIMIZADO con {'FP-Growth' if use_fpgrowth else 'Apriori'})")
    print(f"{'='*70}")
    print(f"Parámetros:")
    print(f"  • Soporte mínimo: {min_support*100:.2f}%")
    print(f"  • Confianza mínima: {min_confidence*100:.1f}%")
    print(f"  • Max longitud itemsets: {max_len}")

    # 1. Filtrar transacciones con productos
    df_with_products = df[df['tiene_productos']].copy()
    n_transactions = len(df_with_products)
    print(f"\nTransacciones con productos: {n_transactions:,}")

    # 2. Preparar transacciones como lista
    transactions = df_with_products['productos_list'].tolist()

    # Estadísticas
    sizes = [len(t) for t in transactions]
    print(f"\nEstadísticas de transacciones:")
    print(f"  • Productos/transacción (promedio): {np.mean(sizes):.2f}")
    print(f"  • Productos/transacción (mediana): {np.median(sizes):.0f}")

    # 3. Convertir a formato one-hot (matriz binaria)
    print(f"\nConvirtiendo a formato one-hot...")
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

    print(f"  • Productos únicos encontrados: {len(te.columns_):,}")
    print(f"  • Matriz de transacciones: {df_encoded.shape}")

    # 4. Encontrar itemsets frecuentes (FP-Growth o Apriori)
    print(f"\nBuscando itemsets frecuentes con {'FP-Growth' if use_fpgrowth else 'Apriori'}...")

    if use_fpgrowth:
        # FP-Growth es mucho más rápido
        frequent_itemsets = fpgrowth(
            df_encoded,
            min_support=min_support,
            use_colnames=True,
            max_len=max_len
        )
    else:
        # Apriori (más lento pero también optimizado)
        from mlxtend.frequent_patterns import apriori
        frequent_itemsets = apriori(
            df_encoded,
            min_support=min_support,
            use_colnames=True,
            max_len=max_len
        )

    print(f"  ✓ Itemsets frecuentes encontrados: {len(frequent_itemsets):,}")

    if len(frequent_itemsets) == 0:
        print("\n⚠️  No se encontraron itemsets frecuentes con estos parámetros")
        return pd.DataFrame()

    # Estadísticas por longitud
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(len)
    length_counts = frequent_itemsets['length'].value_counts().sort_index()
    print(f"\nDistribución por longitud:")
    for length, count in length_counts.items():
        print(f"  • {length}-itemsets: {count:,}")

    # 5. Generar reglas de asociación
    print(f"\nGenerando reglas de asociación...")
    rules = mlxtend_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence
    )

    if len(rules) == 0:
        print("\n⚠️  No se encontraron reglas con estos parámetros")
        return pd.DataFrame()

    print(f"  ✓ Reglas encontradas: {len(rules):,}")

    # 6. Formatear resultados (nombres en español para compatibilidad)
    rules_formatted = pd.DataFrame({
        'antecedente': rules['antecedents'].apply(lambda x: ', '.join(sorted(list(x)))),
        'consecuente': rules['consequents'].apply(lambda x: ', '.join(sorted(list(x)))),
        'soporte': rules['support'].round(4),
        'confianza': rules['confidence'].round(4),
        'lift': rules['lift'].round(2),
        'conviction': rules['conviction'].round(2) if 'conviction' in rules.columns else None,
        'num_transacciones': (rules['support'] * n_transactions).astype(int)
    })

    # Ordenar por lift descendente
    rules_formatted = rules_formatted.sort_values('lift', ascending=False).reset_index(drop=True)

    # Estadísticas
    print(f"\nEstadísticas de las reglas:")
    print(f"  • Confianza promedio: {rules_formatted['confianza'].mean():.3f}")
    print(f"  • Confianza mediana: {rules_formatted['confianza'].median():.3f}")
    print(f"  • Lift promedio: {rules_formatted['lift'].mean():.2f}")
    print(f"  • Lift máximo: {rules_formatted['lift'].max():.2f}")

    # Top 10 reglas
    print(f"\n📊 Top 10 reglas por Lift:")
    print(rules_formatted[['antecedente', 'consecuente', 'confianza', 'lift']].head(10).to_string(index=False))

    return rules_formatted


def analyze_association_rules_sampled(
    df: pd.DataFrame,
    sample_frac: float = 0.1,
    **kwargs
) -> pd.DataFrame:
    """
    Análisis de reglas usando una MUESTRA del dataset
    Útil para datasets muy grandes

    Args:
        df: DataFrame completo
        sample_frac: Fracción a muestrear (0.1 = 10%)
        **kwargs: Argumentos para analyze_association_rules_optimized
    """
    print(f"\n⚡ MODO MUESTREO: Usando {sample_frac*100:.0f}% del dataset")
    print(f"   Total: {len(df):,} → Muestra: {int(len(df)*sample_frac):,}")

    df_sample = df.sample(frac=sample_frac, random_state=42)
    return analyze_association_rules_optimized(df_sample, **kwargs)
