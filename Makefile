install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest tests

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

test-coverage-console:
	poetry run pytest --cov=page_analyzer

selfcheck:
	poetry check

check: selfcheck test lint