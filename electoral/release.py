import re
from pathlib import Path

import quilt
from config import DATA_DIRECTORY


FILE_RE = re.compile(
    r"^(?P<scrutin>[A-Za-z0-9-]+)_par_(?P<unit>[a-z]+)_(?P<format>long|large).csv$"
)


def release():
    p = quilt.Package()

    files = Path(DATA_DIRECTORY).glob("*.csv")

    for f in files:
        m = FILE_RE.match(f.name)

        p = p.set(
            f"{m['scrutin']}/par_{m['unit']}/{m['format']}.csv", f, meta={"type": "csv"}
        )

    p.build("aktiur/elections_france")
    p.push("aktiur/elections_france")
