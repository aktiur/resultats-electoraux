Résultats électoraux en France
==============================

Ce dépôt a vocation à compiler des fichiers de résultats électoraux dans
des formats normalisés et corrigés.

Il comporte à terme:

- l'ensemble des fichiers de production des résultats normalisés, sous la 
  forme d'une Makefile et des différents scripts de transformation
  (la branche master)
- les fichiers finaux, accessibles via [la branche resultats][resultats].

Le dépôt sera organisé pour permettre la production en local des fichiers pour
pouvoir en vérifier le contenu.

[resultats]: https://github.com/aktiur/resultats-electoraux/tree/resultats

Fichiers disponibles
--------------------

Les scrutins suivants sont disponibles :

* Présidentielle 2017, 1er et 2ème tour
* Législatives 2017, 1er tour

Les niveaux de détails administratifs suivants sont disponibles:
* Par bureau de votes
* Par commune
* Par circonscription législative
* Par département

Tous ces fichiers sont disponibles aux formats longs et cours (voir
ci-dessous)

Format des fichiers
-------------------

Tous les fichiers sont encodés en UTF-8, au format csv, avec champs
séparés par des virgules.

Pour chaque élection, et chaque niveau de détail (bureau de votes,
commune, circonscription législative, département), les fichiers sont
disponibles dans deux formats

### Format long

Les fichiers au format **long** comportent une ligne par couple
candidat/unité administrative.

Chaque ligne comporte les champs suivants :
* les informations d'identification de l'unité administrative (numéro
  de département, code commune INSEE,
* la répétition des informations propres à l'unité (nombre d'inscrits,
  de votants, de blancs, d'exprimés)
* la répétition des données propres au candidat (n° de panneau, genre,
  nom, prénom et nuance si pertinent).
* Le nombre de voix du candidat dans cette unité administrative

### Format large

Les fichiers au format **large** comportent une ligne par unité
administrative.

Chaque ligne

* Un format dit *large*, où chaque ligne correspond à une unité
  administrative, avec les informations afférentes, et où les
  informations des candidats sont présentés par colonne. Dans le cas,
  d'une élection nationale, c'est le nom du candidat qui est utilisé
  comme nom de colonne. Dans le cas d'une élection avec des candidats
  locaux, c'est le code de nuance. L'identité individuelle des candidats
  est donc perdue, et si plusieurs candidats sont identifiés sous la
  même nuance, leurs scores sont aggrégés dans ce format.


Pour générer soi-même les fichiers électoraux
---------------------------------------------

Créez un virtualenv python 3 et installez les dépendances :

```
pip install -r requirements.txt
```

Une fois ceci fait, la commande `doit` permet de créer tous les
fichiers électoraux.

```
doit
```

Il est aussi possible de ne réaliser que les étapes minimales pour
générer un des fichiers, par exemple

```
doit large_par_commune:2017-presidentielle-1
```

pour un fichier large (une colonne par candidat) pour le premier tour de
l'élection présidentielle de 2017.
