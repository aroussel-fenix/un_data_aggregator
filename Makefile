install-dev:  # install dev dependencies
	pipenv install --dev

install:  # install dependencies
	pipenv install

flake8:  # lint python
	flake8 --max-line-length=100 .

isort:  # sort python imports
	isort .

black:  # format python code
	black .
