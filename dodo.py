import json
import os
from itertools import product

FORMATS = ['long', 'large']
UNITS = ['commune', 'circonscription', 'departement']

AGG_COLS = {
    'commune': ('departement', 'commune'),
    'circonscription': ('departement', 'circonscription'),
    'departement': ('departement',)
}

KEEP_COLS = {
    'commune': ('commune_libelle',),
    'circonscription': (),
    'departement': (),
}

CANDIDAT_AGG = ('numero_panneau', 'nom')
CANDIDAT_KEEP = ('sexe', 'prenom', 'genre', 'nuance')

with open('config.json') as f:
    config = json.load(f)


def get_raw_filename(scrutin):
    return os.path.join('dist', 'raw', scrutin + '.txt')


def get_dist_filename(format, unit, scrutin):
    return os.path.join('dist', 'data', '{scrutin}_par_{unit}_{format}.csv'.format(
        scrutin=scrutin, unit=unit, format=format
    ))


def task_creer_dossiers():
    yield {
        'basename': 'creer_dossiers',
        'actions': ['mkdir -p dist/raw', 'mkdir -p dist/data']
    }


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
    for format, unit, scrutin in product(FORMATS, UNITS, config['sources']):
        src_filename = get_dist_filename(format, 'bureau', scrutin)
        dest_filename = get_dist_filename(format, unit, scrutin)

        agg_cols = AGG_COLS[unit]
        keep_cols = KEEP_COLS[unit]

        if format == 'long':
            agg_cols += CANDIDAT_AGG
            keep_cols += keep_cols + CANDIDAT_KEEP

        action = 'python scripts/aggregate.py "{src}" "{agg}" "{keep}" > {dest}'.format(
            src=src_filename,
            dest=dest_filename,
            agg=','.join(agg_cols),
            keep=','.join(keep_cols)
        )

        yield {
            'basename': '{}_par_{}'.format(format, unit),
            'name': scrutin,
            'targets': [dest_filename],
            'file_dep': [src_filename],
            'actions': [action]
        }
