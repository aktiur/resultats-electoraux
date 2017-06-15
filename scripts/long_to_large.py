import pandas as pd
import sys


def long_to_large(in_file, out_file):
    df = pd.read_csv(in_file, dtype={'departement': str, 'commune': str, 'bureau': str})

    with_nuance = 'nuance' in df

    grouping = ['departement', 'commune', 'bureau']
    col_var = 'nuance' if with_nuance else 'nom'

    stats = df.groupby(grouping).agg({
        'circonscription': 'first',
        'commune_libelle': 'first',
        'inscrits': 'first',
        'votants': 'first',
        'blancs': 'first',
        'exprimes': 'first',
    })

    voix = df.groupby(grouping + [col_var])['voix'].sum().unstack().fillna(0, downcast='infer')

    pd.concat([stats, voix], axis=1).to_csv(out_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/long_to_large.py fichier_source > fichier_dest")
        sys.exit(1)

    with open(sys.argv[1], 'r') as in_file:
        long_to_large(in_file, sys.stdout)
