import pandas as pd


def long_to_large(src, dest):
    df = pd.read_csv(src, dtype={"departement": str, "commune": str, "bureau": str})

    with_nuance = "nuance" in df

    grouping = ["departement", "commune", "bureau"]
    col_var = "nuance" if with_nuance else "nom"
    keep_cols = [
        "circonscription",
        "commune_libelle",
        "inscrits",
        "votants",
        "blancs",
        "exprimes",
    ]

    stats = df.groupby(grouping).agg({c: "first" for c in keep_cols if c in df.columns})

    voix = (
        df.groupby(grouping + [col_var])["voix"]
        .sum()
        .unstack()
        .fillna(0, downcast="infer")
    )

    pd.concat([stats, voix], axis=1).to_csv(dest)
