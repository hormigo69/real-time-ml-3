from loguru import logger
from quixstreams import Application
from llms.base import BaseNewsSignalExtractor
from datetime import datetime


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    llm: BaseNewsSignalExtractor,
):
    logger.info("Hello from new-signal!")

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset="earliest",
    )

    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer="json",
    )

    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer="json",
    )

    sdf = app.dataframe(input_topic)

    ##### Adding this part to calculate the timestamp_ms in the same way that the news data source does
    # but it's not working as expected

    # Process the incoming news into a news signal
    def process_message(value):
        logger.debug(f"Processing message: {value}")
        timestamp_ms = int(
            datetime.fromisoformat(
                value["published_at"].replace("Z", "+00:00")
            ).timestamp()
            * 1000
        )
        return {
            "news": value["title"],
            "timestamp_ms": timestamp_ms,
            **llm.get_signal(value["title"]),
            "model_name": llm.model_name,
        }

    # Process the incoming news into a news signal
    sdf = sdf.apply(process_message)

    #########################################################

    # This is the original code that is not working
    # At the end of session 6, Pau detect this error but decide to fix it later.
    # The code above calculates the timestamp_ms in the same way that the news data source does,
    # but I let it commented until to see wath Pau do with it.
    # sdf = sdf.apply(
    #     lambda value: {
    #         "news": value["title"],
    #         **llm.get_signal(value["title"]),
    #         "model_name": llm.model_name,
    #         "timestamp_ms": value["timestamp_ms"],
    #     }
    # )

    sdf = sdf.update(lambda value: logger.debug(f"Final message: {value}"))

    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == "__main__":
    from config import config
    from llms.factory import get_llm

    logger.info(f"Using model provider: {config.model_provider}")
    llm = get_llm(config.model_provider)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        llm=llm,
    )
