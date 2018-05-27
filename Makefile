all: html
	:

.PHONY: csv
csv:
	cat fixtures/algseeds.csv | python -m birdf2l.annotate --csv > fixtures/alg.csv

.PHONY: html
html: csv
	python -m birdf2l.build_patterns > index.html
	python -m birdf2l.build_positions Ma > summer.html
	python -m birdf2l.build_positions Jb > winter.html
