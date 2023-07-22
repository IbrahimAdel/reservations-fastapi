start:
	docker-compose up -d


migrate-db:
	alembic upgrade head