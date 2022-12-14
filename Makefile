lint:
	poetry run flake8 page_loader

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
	poetry run pytest --cov=page_loader --cov-report xml