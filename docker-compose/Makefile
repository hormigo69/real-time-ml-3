# Redpanda management
start-redpanda:
	docker compose -f redpanda.yml up -d

stop-redpanda:
	docker compose -f redpanda.yml down

add-one-partition-to-trades-topic:
	docker compose -f redpanda.yml exec redpanda rpk topic add-partitions trades --num 1


recreate-trades-topic-with-one-partition:
	docker compose -f redpanda.yml exec redpanda rpk topic delete trades
	docker compose -f redpanda.yml exec redpanda rpk topic create trades --partitions 1

# Technical indicators pipeline management
# for live data
build-technical-indicators-live:
	docker compose -f technical-indicators-live.yml build

start-technical-indicators-live: build-technical-indicators-live
	docker compose -f technical-indicators-live.yml up -d

stop-technical-indicators-live:
	docker compose -f technical-indicators-live.yml down

# for historical data
build-technical-indicators-historical:
	cd .. && \
	export RUN_ID=$$(uuidgen) && \
	ls -la services/candles/Dockerfile && \
	RUN_ID=$$RUN_ID docker compose -f docker-compose/technical-indicators-historical.yml build

backfill-technical-indicators: build-technical-indicators-historical
	$(eval RUN_ID := $(shell uuidgen))
	@echo "Starting backfill with RUN_ID: $(RUN_ID)"
	cd .. && RUN_ID=$(RUN_ID) docker compose -f docker-compose/technical-indicators-historical.yml up -d

# Technical indicators base pipeline management
build-technical-indicators-pipeline:
	docker compose -f technical-indicators-pipeline.yml build

start-technical-indicators-pipeline: build-technical-indicators-pipeline
	docker compose -f technical-indicators-pipeline.yml up -d

stop-technical-indicators-pipeline:
	docker compose -f technical-indicators-pipeline.yml down
