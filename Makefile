lint:
	poetry run flake8 gendiff

install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

tests:
	poetry run pytest

test-cov:
	poetry run pytest --cov=gendiff --cov-report xml