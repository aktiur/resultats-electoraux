CONFIG := config.json

SCRUTINS := 2017-presidentielle-1 2017-presidentielle-2 2017-legislatives-1

FORMATS_LONG := bureau commune circonscription
FORMATS_LARGE := bureau commune circonscription

TARGETS_LONG := $(addprefix dist/long/bureau/,$(addsuffix .csv,$(SCRUTINS)))
TARGETS_LARGE := $(addprefix dist/large/bureau/,$(addsuffix .csv,$(SCRUTINS)))
TARGETS := $(TARGETS_LONG) $(TARGETS_LARGE)


DIRS := $(addprefix dist/long/,$(FORMATS_LONG)) $(addprefix dist/large/,$(FORMATS_LARGE))

all: $(TARGETS)

-include build/sources.d

build/sources.d: $(CONFIG) | build
	python scripts/create_download_dependencies.py $< > $@

$(TARGETS_LARGE): dist/large/bureau/% : dist/long/bureau/% |dist/large/bureau
	python scripts/long_to_large.py $< > $@

$(TARGETS_LONG): dist/long/bureau/% : dist/raw/% |dist/long/bureau
	python scripts/scrutin2017_to_candidat_bureau.py $< > $@

build dist/raw $(DIRS):
	mkdir -p $@

clean:
	rm -rf build dist
