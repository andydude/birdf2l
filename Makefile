all: html
	:

.PHONY: csv
csv:
	python -m birdf2l.oldalgseeds --csv > fixtures/algseeds.csv
	cat fixtures/algseeds.csv | python -m birdf2l.annotate --csv --oob > fixtures/alg.csv

.PHONY: html
html: csv
	python -m birdf2l.build_toc
	python -m birdf2l.build_patterns
	# python -m birdf2l.build_positions Ma > summer.html
	# python -m birdf2l.build_positions Jb > winter.html
