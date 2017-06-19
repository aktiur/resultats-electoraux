import pandas as pd
import numpy as np
import sys


NON_SUMMABLE = {'circonscription', 'numero_panneau'}


def aggregate(input, agg_columns, keep_columns, output):
    df = pd.read_csv(input, dtype={'departement': str, 'commune': str, 'bureau': str})

    res = df.groupby(agg_columns).agg({
        **{c: 'first' for c in keep_columns if c in df.columns},
        **{c: 'sum' for c in df.select_dtypes([np.number]).columns if c not in NON_SUMMABLE}
    }).reset_index()

    # garder l'ordre original des colonnes
    order = [c for c in df.columns if c in res.columns]
    res.reindex(columns=order).to_csv(output, index=False)


if __name__ == '__main__':
    if not len(sys.argv) in [3,4]:
        print('Usage: python scripts/aggregate.py fichier aggfields [keepfields]', file=sys.stderr)

    keep = sys.argv[3].split(',') if len(sys.argv) == 4 else []

    with open(sys.argv[1], 'r') as f:
        aggregate(f, sys.argv[2].split(','), sys.argv[3].split(','), sys.stdout)
