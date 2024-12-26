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

clean-redpanda-data:
	@echo "Stopping Redpanda..."
	docker compose -f redpanda.yml down
	@echo "Removing Redpanda volume..."
	docker volume rm $$(docker volume ls -q | grep redpanda)
	@echo "Starting Redpanda with clean state..."
	docker compose -f redpanda.yml up -d



########################################
## Technical indicators pipeline
########################################

# for live data
build-technical-indicators-live:
	docker compose -f technical-indicators-live.yml build

start-technical-indicators-live: build-technical-indicators-live
	# Primero detenemos y limpiamos
	docker compose -f technical-indicators-live.yml down -v

	# Luego iniciamos
	docker compose -f technical-indicators-live.yml up -d

stop-technical-indicators-live:
	docker compose -f technical-indicators-live.yml down

# for historical data
build-technical-indicators-historical:
	@echo "Building technical indicators pipeline for historical data"
	docker compose -f technical-indicators-historical.yml build


backfill-technical-indicators: build-technical-indicators-historical
	$(eval RUN_ID := $(shell uuidgen))
	@echo "Starting backfill with RUN_ID: $(RUN_ID)"
	# Primero limpiamos todo
	docker compose -f technical-indicators-historical.yml down -v
	# Luego iniciamos
	RUN_ID=$(RUN_ID) docker compose -f technical-indicators-historical.yml up -d

stop-technical-indicators-historical:
	docker compose -f technical-indicators-historical.yml down

# News signal pipeline management
build-news-signal-live:
	docker compose -f news-signal-live.yml build

start-news-signal-live: build-news-signal-live
	docker compose -f news-signal-live.yml up -d

stop-news-signal-live:
	docker compose -f news-signal-live.yml down



clean-backfill-kafka-topics:
	@echo "Removing all Kafka topics that contain the word historical"
	docker compose -f redpanda.yml exec redpanda rpk topic delete -r ".*historical.*"

# Comandos de diagnóstico para news-signal
logs-feature-store:
	docker compose -f news-signal-live.yml logs -f to-feature-store

check-news-signal-config:
	@echo "Verificando configuración de news-signal..."
	@cat ../services/to-feature-store/live.settings.news-signal.env
	@echo "\nVerificando que el servicio está corriendo:"
	@docker compose -f news-signal-live.yml ps to-feature-store

check-news-signal-topic:
	@echo "Verificando topic news_signal en Redpanda..."
	docker compose -f redpanda.yml exec redpanda rpk topic list | grep news_signal

logs-news:
	docker compose -f news-signal-live.yml logs -f news

logs-news-signal:
	docker compose -f news-signal-live.yml logs -f news-signal

watch-all-logs:
	@echo "Monitoreando logs de todos los servicios..."
	docker compose -f news-signal-live.yml logs -f
