test:
	pytest -s -v

migrate:
	python -m manage migrate

migrations:
	python -m manage makemigrations

run:
	python -m manage runserver 0.0.0.0:8000

shell:
	python -m manage shell_plus

runfast:
	uvicorn src.fastapi_project.main:app --reload --port 3000

dmysql:
	docker exec -it codeflix-mysql-1 mysql -u root -proot -D mysql

runmysql:
	mysql -h '127.0.0.1' -P 3306 -u root -proot
