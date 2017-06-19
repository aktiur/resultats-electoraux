CONFIG := config.json

SCRUTINS := 2017-presidentielle-1 2017-presidentielle-2 2017-legislatives-1

FORMATS_LONG := bureau commune circonscription
FORMATS_LARGE := bureau commune circonscription

BUREAUX_LONG := $(addprefix dist/long/bureau/,$(addsuffix .csv,$(SCRUTINS)))
BUREAUX_LARGE := $(addprefix dist/large/bureau/,$(addsuffix .csv,$(SCRUTINS)))

COMMUNES_LONG := $(addprefix dist/long/commune/,$(addsuffix .csv,$(SCRUTINS)))
COMMUNES_LARGE := $(addprefix dist/large/commune/,$(addsuffix .csv,$(SCRUTINS)))

TARGETS := $(BUREAUX_LONG) $(BUREAUX_LARGE) $(COMMUNES_LONG) $(COMMUNES_LARGE)


DIRS := $(addprefix dist/long/,$(FORMATS_LONG)) $(addprefix dist/large/,$(FORMATS_LARGE))

all: $(TARGETS)

-include build/sources.d

build/sources.d: $(CONFIG) | build
	python scripts/create_download_dependencies.py $< > $@

$(COMMUNES_LARGE): dist/large/commune/% : dist/large/bureau/% |dist/large/commune
	python scripts/aggregate.py $< "departement,commune" "commune_libelle" > $@

$(COMMUNES_LONG): dist/long/commune/% : dist/long/bureau/% |dist/long/commune
	python scripts/aggregate.py $< "departement,commune,numero_panneau,nom" "commune_libelle,sexe,prenom,nuance" > $@

$(BUREAUX_LARGE): dist/large/bureau/% : dist/long/bureau/% |dist/large/bureau
	python scripts/long_to_large.py $< > $@

$(BUREAUX_LONG): dist/long/bureau/% : dist/raw/% |dist/long/bureau
	python scripts/scrutin2017_to_candidat_bureau.py $< > $@

build dist/raw $(DIRS):
	mkdir -p $@

clean:
	rm -rf build dist
