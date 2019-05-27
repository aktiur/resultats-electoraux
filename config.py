from pathlib import Path

from electoral.cleanup import clean_results2017, clean_results2014
from electoral.scrutin import Scrutin

SCRUTINS = [
    Scrutin(
        "2019-europeennes",
        "https://static.data.gouv.fr/resources/resultats-des-elections-europeennes-2019/20190527-104727/resultats-provisoires-par-bureau-de-vote.txt",
        clean_results2017,
    ),
    Scrutin(
        "2017-presidentielle-2",
        "https://www.data.gouv.fr/s/resources/election-presidentielle-des-23-avril-et-7-mai-2017-resultats-definitifs-du-2nd-tour-par-bureaux-de-vote/20170511-093541/PR17_BVot_T2_FE.txt",
        clean_results2017,
    ),
    Scrutin(
        "2017-presidentielle-1",
        "https://www.data.gouv.fr/s/resources/election-presidentielle-des-23-avril-et-7-mai-2017-resultats-definitifs-du-1er-tour-par-bureaux-de-vote/20170427-100955/PR17_BVot_T1_FE.txt",
        clean_results2017,
    ),
    Scrutin(
        "2017-legislatives-1",
        "https://www.data.gouv.fr/s/resources/elections-legislatives-des-11-et-18-juin-2017-resultats-par-bureaux-de-vote-du-1er-tour/20170613-100441/Leg_2017_Resultats_BVT_T1_c.txt",
        clean_results2017,
    ),
    Scrutin(
        "2017-legislatives-2",
        "https://www.data.gouv.fr/s/resources/elections-legislatives-des-11-et-18-juin-2017-resultats-du-2nd-tour-par-bureaux-de-vote/20170620-094954/Leg_2017_Resultats_BVT_T2_c.txt",
        clean_results2017,
    ),
    # "2014-municipales", "https://www.data.gouv.fr/s/resources/elections-municipales-2014-resultats-par-bureaux-de-vote/20150925-122128/MN14_Bvot_T1T2.txt",),
    Scrutin(
        "2014-europeennes",
        "https://www.data.gouv.fr/s/resources/elections-europeennes-2014-resultats-par-bureaux-de-vote/20150925-112120/ER14_BVOT.txt",
        clean_results2014,
    ),
]


FORMATS = ["long", "large"]
UNITS = ["bureau", "commune", "circonscription", "departement"]

AGG_COLS = {
    "commune": ["departement", "commune"],
    "circonscription": ["departement", "circonscription"],
    "departement": ["departement"],
}

KEEP_COLS = {"commune": ("commune_libelle",), "circonscription": (), "departement": ()}

CANDIDAT_AGG = ("numero_panneau", "nom", "nom_liste")
CANDIDAT_KEEP = ("sexe", "prenom", "genre", "nuance")


ROOT_DIRECTORY = Path(__file__).parent

RAW_DIRECTORY = ROOT_DIRECTORY / Path("build", "raw")
DATA_DIRECTORY = ROOT_DIRECTORY / Path("build", "data")
RELEASE_DIRECTORY = ROOT_DIRECTORY / Path("dist")
