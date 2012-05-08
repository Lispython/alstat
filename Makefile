all: clean-pyc test

test:
	python setup.py nosetests --stop --tests tests.py


coverage:
	python setup.py nosetests  --with-coverage --cover-package=alstat --cover-html --cover-html-dir=coverage_out coverage


shell:
	../venv/bin/ipython

audit:
	python setup.py autdit

release:
	python setup.py sdist upload

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +