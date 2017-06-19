import json
import os
from itertools import product


FORMATS = ['long', 'large']

AGG_COLS = {
    'long': ['departement', 'commune', 'numero_panneau', 'nom'],
    'large': ['departement', 'commune']
}

KEEP_COLS = {
    'long': ['commune_libelle', 'sexe', 'prenom', 'genre', 'nuance'],
    'large': ['commune_libelle']
}


with open('config.json') as f:
    config = json.load(f)


def get_raw_filename(scrutin):
    return os.path.join('dist', 'raw', scrutin + '.txt')


def get_dist_filename(format, unit, scrutin):
    return os.path.join('dist', format, unit, scrutin + '.csv')


def task_telecharger_source():
    for scrutin, url in config['sources'].items():
        filename = get_raw_filename(scrutin)
        action = ['curl', '-o', filename, url]

        if os.path.isfile(filename):
            action += ['-z', filename]

        yield {
            'name': scrutin,
            'targets': [filename],
            'actions': [action]
        }


def task_long_par_bureau():
    for scrutin in config['sources']:
        src_filename = get_raw_filename(scrutin)
        dest_filename = get_dist_filename('long', 'bureau', scrutin)

        # varier l'action en fonction de l'année du scrutin !
        action = 'python scripts/scrutin2017_to_candidat_bureau.py {src} > {dest}'.format(
                src=src_filename, dest=dest_filename
            )

        yield {
            'name': scrutin,
            'targets': [dest_filename],
            'file_dep': [src_filename],
            'actions': [action]
        }


def task_large_par_bureau():
    for scrutin in config['sources']:
        src_filename = get_dist_filename('long', 'bureau', scrutin)
        dest_filename = get_dist_filename('large', 'bureau', scrutin)

        action = 'python scripts/long_to_large.py {src} > {dest}'.format(
            src=src_filename, dest=dest_filename
        )

        yield {
            'name': scrutin,
            'targets': [dest_filename],
            'file_dep': [src_filename],
            'actions': [action]
        }


def task_par_commune():
    for format, scrutin in product(FORMATS, config['sources']):
        src_filename = get_dist_filename(format, 'bureau', scrutin)
        dest_filename = get_dist_filename(format, 'commune', scrutin)

        action = 'python scripts/aggregate.py {src} {agg} {keep} > {dest}'.format(
            src=src_filename,
            dest=dest_filename,
            agg=','.join(AGG_COLS[format]),
            keep=','.join(KEEP_COLS[format])
        )

        yield {
            'basename': '{}_par_commune'.format(format),
            'name': scrutin,
            'targets': [dest_filename],
            'file_dep': [src_filename],
            'actions': [action]
        }
