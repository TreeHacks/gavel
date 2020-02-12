build:
	docker-compose build

start:
	docker-compose up -d
	@echo "gavel listening on port 5000"
	@echo "run 'make logs' to watch logs"

stop:
	docker-compose down

# watch the logs from gavel
logs:
	docker-compose logs -f -t gavel

# run all the migrations
migrate:
	docker-compose run gavel python initialize.py
	# db/containers still running