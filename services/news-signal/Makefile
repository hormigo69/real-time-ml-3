run-dev-live:
	cp live.settings.env settings.env
	uv run python -m run

run-dev-historical:
	cp historical.settings.env settings.env
	uv run python -m run

# This was added because I was getting an error when running the command "make run-ollama"
#.PHONY: build run run-dev run-claude run-ollama test

build:
	docker build -f Dockerfile -t news-signal .

run-with-anthropic: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		-e MODEL_PROVIDER=anthropic \
		--env-file anthropic_credentials.env \
		news-signal

run-with-ollama: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		-e MODEL_PROVIDER=ollama \
		--env-file ollama.env \
		news-signal

#LLM specific things
# Sanity checking each of the LLMs
run-claude:
	uv run python -m llms.claude

run-ollama:
	uv run python -m llms.ollama




# Generation of an instruction dataset with tupples (instruction, input, output)
#  to do supervised Fine-tuning of the model.
golden-dataset-with-claude:
	uv run python golden_dataset.py \
		--model_provider=anthropic \
		--n 1000 \
		--output_file ./data/golden_dataset_claude.jsonl

golden-dataset-with-ollama:
	uv run python golden_dataset.py \
		--model_provider=ollama \
		--n 1000 \
		--output_file ./data/golden_dataset_ollama.jsonl


# To install the dependencies for the GPU instance
venv-gpu-instance:
	curl -LsSf https://astral.sh/uv/install.sh | sh && \
	source $HOME/.local/bin/env && \
	uv sync --group gpu-instance

# To login to Comet ML during fine-tuning
login-comet:
	uv run comet login

# To fine-tune the model
fine-tune:
	uv run python fine_tuning.py \
		--base_llm_name unsloth/Llama-3.2-1B-bnb-4bit \
		--dataset_path ./data/instruction_dataset_ollama_10k.jsonl \
		--comet_ml_project_name news-signal-extractor \
		--max_steps 100
