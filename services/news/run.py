from loguru import logger
from sources import NewsDataSource
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    news_source: NewsDataSource,
):
    """
    Gets news from the Cryptopanic API, removes duplicates and pushes them to a Kafka topic.
    We will use QuixStreams to push the news to the Kafka topic.
    Args:
        kafka_broker_address: The address of the Kafka broker.
        kafka_topic: The topic to push the news to.
        news_source: The news source to use.
    Returns:
        None
    """
    logger.info("Hello from news!")

    app = Application(broker_address=kafka_broker_address)

    # Topic where the news will be pushed
    output_topic = app.topic(name=kafka_topic, value_serializer="json")

    # Create the streaming dataframe
    sdf = app.dataframe(source=news_source)

    # Let's printing to check if this thing works
    # sdf.print(metadata=True)

    # Push the news to the output topic
    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == "__main__":
    from config import config

    # Create the news source either for
    # -  Live data -> via Cryptopanic API
    # -  Historical data -> via reading a CSV file we got from an external URL
    from sources import get_source

    news_source = get_source(
        config.data_source,
        polling_interval_sec=config.polling_interval_sec,
        url_rar_file=config.historical_data_source_url_rar_file,
        path_to_csv_file=config.historical_data_source_csv_file,
    )

    # Run the streaming application
    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        news_source=news_source,
    )
