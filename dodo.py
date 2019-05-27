import os
from itertools import product
from pathlib import Path

import config
from config import RAW_DIRECTORY, DATA_DIRECTORY, RELEASE_DIRECTORY
from electoral.aggregate import aggregate
from electoral.long_to_large import long_to_large


def directory_exists(d):
    def uptodate_check(task, values):
        if Path(d).exists():
            return True
        return False

    return uptodate_check


def task_creer_dossiers():
    yield {
        "name": "creer_dossiers",
        "actions": [f"mkdir -p {RAW_DIRECTORY}", f"mkdir -p {DATA_DIRECTORY}"],
        "uptodate": [directory_exists(RAW_DIRECTORY), directory_exists(DATA_DIRECTORY)],
    }


def task_telecharger_source():
    for scrutin in config.SCRUTINS:
        filename = RAW_DIRECTORY / scrutin.raw_filename()
        action = ["curl", "-o", filename, scrutin.url]

        if os.path.isfile(filename):
            action += ["-z", filename]

        yield {
            "name": scrutin.id,
            "targets": [filename],
            "actions": [action],
            "task_dep": ["creer_dossiers"],
        }


def task_long_par_bureau():
    for scrutin in config.SCRUTINS:
        src_filename = RAW_DIRECTORY / scrutin.raw_filename()
        dest_filename = DATA_DIRECTORY / scrutin.dist_filename("long", "bureau")

        action = (scrutin.cleaner, [src_filename, dest_filename], {})

        yield {
            "basename": "long_par_bureau",
            "name": scrutin.id,
            "targets": [dest_filename],
            "file_dep": [src_filename],
            "task_dep": ["creer_dossiers"],
            "actions": [action],
        }


def task_large_par_bureau():
    for scrutin in config.SCRUTINS:
        src_filename = DATA_DIRECTORY / scrutin.dist_filename("long", "bureau")
        dest_filename = DATA_DIRECTORY / scrutin.dist_filename("large", "bureau")

        action = (long_to_large, [src_filename, dest_filename], {})

        yield {
            "basename": "large_par_bureau",
            "name": scrutin.id,
            "targets": [dest_filename],
            "file_dep": [src_filename],
            "actions": [action],
        }


def task_fichiers_agreges():
    for format, unit, scrutin in product(
        config.FORMATS, config.UNITS[1:], config.SCRUTINS
    ):
        src_filename = DATA_DIRECTORY / scrutin.dist_filename(format, "bureau")
        dest_filename = DATA_DIRECTORY / scrutin.dist_filename(format, unit)

        agg_cols = list(config.AGG_COLS[unit])
        keep_cols = list(config.KEEP_COLS[unit])

        if format == "long":
            agg_cols += config.CANDIDAT_AGG
            keep_cols += config.CANDIDAT_KEEP

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


def task_ensure_dist_directory_exists():
    return {
        "actions": [f"git worktree add {RELEASE_DIRECTORY} resultats"],
        "uptodate": [directory_exists(RELEASE_DIRECTORY)],
    }


def task_compress_files_for_release():
    return {
        "basename": "compress_files_for_release",
        "actions": [
            f'for i in {DATA_DIRECTORY}/*.csv; do gzip --stdout "$i" > "$i.gz"; done'
        ],
        "task_dep": [
            "ensure_dist_directory_exists",
            *[
                f"{format}_par_{unit}"
                for format, unit in product(config.FORMATS, config.UNITS)
            ],
        ],
    }
