export PYTHONPATH := ./src:./src/django_project/:$(PYTHONPATH)
export DJANGO_SETTINGS_MODULE := django_project.settings

test:
	pytest -s -v

migrate:
	python -m manage migrate

migrations:
	python -m manage makemigrations

run:
	python -m manage runserver

shell:
	python -m manage shell_plus

runfast:
	uvicorn src.fastapi_project.main:app --reload
