import os
from itertools import product

SOURCES = {
    "2017-presidentielle-2": "https://www.data.gouv.fr/s/resources/election-presidentielle-des-23-avril-et-7-mai-2017-resultats-definitifs-du-2nd-tour-par-bureaux-de-vote/20170511-093541/PR17_BVot_T2_FE.txt",
    "2017-presidentielle-1": "https://www.data.gouv.fr/s/resources/election-presidentielle-des-23-avril-et-7-mai-2017-resultats-definitifs-du-1er-tour-par-bureaux-de-vote/20170427-100955/PR17_BVot_T1_FE.txt",
    "2017-legislatives-1": "https://www.data.gouv.fr/s/resources/elections-legislatives-des-11-et-18-juin-2017-resultats-par-bureaux-de-vote-du-1er-tour/20170613-100441/Leg_2017_Resultats_BVT_T1_c.txt",
    "2017-legislatives-2": "https://www.data.gouv.fr/s/resources/elections-legislatives-des-11-et-18-juin-2017-resultats-du-2nd-tour-par-bureaux-de-vote/20170620-094954/Leg_2017_Resultats_BVT_T2_c.txt",
    # "2014-municipales": "https://www.data.gouv.fr/s/resources/elections-municipales-2014-resultats-par-bureaux-de-vote/20150925-122128/MN14_Bvot_T1T2.txt"
}

SCRUTINS = list(SOURCES)

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
    for scrutin, url in SOURCES.items():
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
    for scrutin in SCRUTINS:
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
    for scrutin in SCRUTINS:
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
    for format, unit, scrutin in product(FORMATS, UNITS, SCRUTINS):
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
