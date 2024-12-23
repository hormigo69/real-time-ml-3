##Building a (better) Real Time ML System. Together
## TODOs


Tools
    - Code editor: Cursor, Visual Studio
        - https://www.cursor.com/
        - https://code.visualstudio.com/

- Feature pipeline steps
    - Ingest trades from external API
    - Transform trades into technical indicators
    - Save these tech indicators to a Feature Store.

-uv
    - We use uv to package our Python code.
    - https://docs.astral.sh/uv/getting-started/installation/
        - fron the folder: uv init _name_of_the_project

- Makefile
    - We use Makefile to define our build, run, test, etc.
    - https://www.gnu.org/software/make/manual/make.html
    - brew make

- loguru
    - We use loguru to log our messages.
    - https://github.com/Delgan/loguru
        - uv add loguru

- Docker
    - We use Docker to containerize our application.
    - https://www.docker.com/
        - para correr dockercompose con el fichero redpanda.yml: docker compose -f redpanda.yml up -d

- Kafka
    - We use Kafka to ingest trades from the Kraken API.
    - Kafka nos permite tener comunicación en tiempo real entre microservicios, en este caso entre Trades y Candles.
    - Permite tener una consistencia incluso en caso de que se caigan los microservicios. 
        - Kafka cluster: DB
        - Kafka topic: table
    - https://kafka.apache.org/
        - uv add kafka

-RedPanda
    - We use RedPanda as our Kafka provider.
    - https://redpanda.com/
    - uv add redpanda

- Pydantic
    - We use Pydantic to define our data models.
    - https://docs.pydantic.dev/
        - uv add pydantic

- quixstreams
    - We use Quix Streams to push our trades to Kafka.
    - https://quix.io/
    - 
    
- Pydantic settings
    - We use Pydantic settings to configure our Pydantic models.
    - https://docs.pydantic.dev/latest/usage/settings/
    - uv add pydantic-settings

