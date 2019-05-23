import os
from itertools import product

import config
from electoral.aggregate import aggregate
from electoral.long_to_large import long_to_large


def task_creer_dossiers():
    yield {
        "basename": "creer_dossiers",
        "actions": ["mkdir -p dist/raw", "mkdir -p dist/data"],
    }


def task_telecharger_source():
    for scrutin in config.SCRUTINS:
        filename = scrutin.raw_filename()
        action = ["curl", "-o", filename, scrutin.url]

        if os.path.isfile(filename):
            action += ["-z", filename]

        yield {"name": scrutin.id, "targets": [filename], "actions": [action]}


def task_long_par_bureau():
    for scrutin in config.SCRUTINS:
        src_filename = scrutin.raw_filename()
        dest_filename = scrutin.dist_filename("long", "bureau")

        action = (scrutin.cleaner, [src_filename, dest_filename], {})

        yield {
            "name": scrutin.id,
            "targets": [dest_filename],
            "file_dep": [src_filename],
            "actions": [action],
        }


def task_large_par_bureau():
    for scrutin in config.SCRUTINS:
        src_filename = scrutin.dist_filename("long", "bureau")
        dest_filename = scrutin.dist_filename("large", "bureau")

        action = (long_to_large, [src_filename, dest_filename], {})

        yield {
            "name": scrutin.id,
            "targets": [dest_filename],
            "file_dep": [src_filename],
            "actions": [action],
        }


def task_fichiers_agreges():
    for format, unit, scrutin in product(config.FORMATS, config.UNITS, config.SCRUTINS):
        src_filename = scrutin.dist_filename(format, "bureau")
        dest_filename = scrutin.dist_filename(format, unit)

        agg_cols = config.AGG_COLS[unit]
        keep_cols = config.KEEP_COLS[unit]

        if format == "long":
            agg_cols += config.CANDIDAT_AGG
            keep_cols += keep_cols + config.CANDIDAT_KEEP

        action = (
            aggregate,
            [],
            {
                "src": src_filename,
                "dest": dest_filename,
                "agg_columns": agg_cols,
                "keep_columns": keep_cols,
            },
        )

        yield {
            "basename": "{}_par_{}".format(format, unit),
            "name": scrutin.id,
            "targets": [dest_filename],
            "file_dep": [src_filename],
            "actions": [action],
        }
