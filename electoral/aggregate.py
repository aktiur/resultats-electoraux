import numpy as np
import pandas as pd

NON_SUMMABLE = {"circonscription", "numero_panneau"}


def aggregate(src, agg_columns, keep_columns, dest):
    df = pd.read_csv(src, dtype={"departement": str, "commune": str, "bureau": str})

    if not set(agg_columns) <= set(df.columns):
        return

    keep_columns = [c for c in keep_columns if c in df.columns]

    res = (
        df.groupby(agg_columns)
        .agg(
            {
                **{c: "first" for c in keep_columns if c in df.columns},
                **{
                    c: "sum"
                    for c in df.select_dtypes([np.number]).columns
                    if c not in NON_SUMMABLE
                },
            }
        )
        .reset_index()
    )

    # garder l'ordre original des colonnes
    order = [c for c in df.columns if c in res.columns]
    res.reindex(columns=order).to_csv(dest, index=False)
