from typing import Literal, Union, Optional

from .news_data_source import NewsDataSource as LiveNewsDataSource
from .historical_data_source import (
    get_historical_data_source,
    HistoricalNewsDataSource,
)
from loguru import logger

NewsDataSource = Union[LiveNewsDataSource, HistoricalNewsDataSource]


def get_source(
    data_source: Literal["live", "historical"],
    polling_interval_sec: Optional[int] = 10,
) -> NewsDataSource:
    # Leer variables de entorno directamente del archivo
    env_vars = {}
    with open("settings.env") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                env_vars[key] = value

    logger.info(f"DATA_SOURCE: {env_vars.get('DATA_SOURCE')}")
    logger.info(f"KAFKA_BROKER_ADDRESS: {env_vars.get('KAFKA_BROKER_ADDRESS')}")
    logger.info(f"KAFKA_TOPIC: {env_vars.get('KAFKA_TOPIC')}")

    if data_source == "live":
        # Set up the source to download the news from cryptopanic API
        from .news_downloader import NewsDownloader
        from config import cryptopanic_config

        # Create News Downloader object
        news_downloader = NewsDownloader(cryptopanic_api_key=cryptopanic_config.api_key)

        # Quix Streams data source that wraps the news downloader
        news_source = LiveNewsDataSource(
            news_downloader=news_downloader,
            polling_interval_sec=polling_interval_sec,
        )

        return news_source

        # return LiveNewsDownloader()

    elif data_source == "historical":
        url_rar_file = env_vars.get("HISTORICAL_DATA_SOURCE_URL")
        logger.info(f"HISTORICAL_DATA_SOURCE_URL: {url_rar_file}")
        if not url_rar_file:
            raise ValueError("HISTORICAL_DATA_SOURCE_URL no está configurada")
        return get_historical_data_source(url_rar_file)
    else:
        raise ValueError(f"Invalid data source: {data_source}")
