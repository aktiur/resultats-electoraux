Résultats électoraux en France
==============================

Ce dépôt a vocation à compiler des fichiers de résultats électoraux dans
des formats normalisés et corrigés.

Il comportera à terme:

- l'ensemble des fichiers de production des résultats normalisés, sous la 
  forme d'une Makefile et des différents scripts de transformation
- les fichiers finaux, accessibles via une seconde branche.

Le dépôt sera organisé pour permettre la production en local des fichiers pour
pouvoir en vérifier le contenu.

Pour générer les fichiers électoraux
------------------------------------

Créez un virtualenv python 3 et installez les dépendances :

```
pip install -r requirements.txt
```

Une fois ceci fait, la commande `make` permet de créer tous les
fichiers électoraux.

```
make
```

Il est aussi possible de ne réaliser que les étapes minimales pour
générer un des fichiers, par exemple

```
make dist/large/bureau/2017-presidentielles-1.csv
```

pour un fichier large (une colonne par candidat) pour le premier tour de
l'élection présidentielle de 2017.
