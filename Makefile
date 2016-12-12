nosetest:
	nosetests -s --with-coverage --cover-erase --cover-package=spynedelegate --cover-xml --logging-level=INFO --with-doctest --verbosity=2

install:
	pip install -e .[test] 

test: install nosetest
