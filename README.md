Résultats électoraux en France
==============================

Ce dépôt vise à proposer des fichiers des résultats des élections
conduites en France dans des formats normalisés et directement
exploitables informatiquement.

Les fichiers sources mis à disposition par le fichier de l'intérieur
sont retraités pour en uniformiser le format et en corriger les erreurs.

Tous les fichiers produits sont au format csv avec la virgule comme
séparateur et le codage des caractères UTF-8, puis compressés au format
gzip (sinon ils font plus de 100 Mo et Github ne me laisse pas les mettre en ligne).

[Une autre branche][master] de ce dépôt contient l'ensemble des fichiers
de production. Cela permet de vérifier la pertinence des traitements et
de reproduire les fichiers finaux soi-même.

Les fichiers
------------

Chaque fichier suit la nomenclature suivante :
`[annee]-[scrutin]-([tour]_)par_[unite]_[format].csv.gz`.

* `[annee]` est l'année du scrutin sur 4 chiffres.
* `[scrutin]` est le nom du scrutin en lettres minuscules, sans les accents
* `[tour]` est le tour du scrutin, en 1 chiffre, si pertinent
* `[unite]` est l'unité de base (`bureau`, `commune`, `departement` ou `circonscription`)
* `[format]` est le format du fichier (`long` pour un fichier avec une ligne par couple
  candidat/unité, `large` pour un fichier avec une ligne par unité et chaque nuance en 
  colonne. Les nuances utilisées sont celles présentes dans les résultats du ministère
  de l'intérieur.

[master]: https://github.com/aktiur/resultats-electoraux/tree/master
