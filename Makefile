setup_db:
	docker build -t local_postgres .
	docker run -p 5432:5432 local_postgres

run:
	poetry run python -m app

tests:
