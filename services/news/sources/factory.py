from typing import Literal, Union, Optional
from pathlib import Path

from .historical_data_source import HistoricalNewsDataSource
from .news_data_source import NewsDataSource as LiveNewsDataSource
from loguru import logger

NewsDataSource = Union[LiveNewsDataSource, HistoricalNewsDataSource]


def get_source(
    data_source: Literal["live", "historical"],
    polling_interval_sec: Optional[int] = 10,
    url_rar_file: Optional[str] = None,
    path_to_csv_file: Optional[str] = None,
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
        url_rar_file = env_vars.get("HISTORICAL_DATA_SOURCE_URL_RAR_FILE")
        path_to_csv_file = env_vars.get("HISTORICAL_DATA_SOURCE_CSV_FILE")
        logger.info(f"HISTORICAL_DATA_SOURCE_URL_RAR_FILE: {url_rar_file}")
        logger.info(f"HISTORICAL_DATA_SOURCE_CSV_FILE: {path_to_csv_file}")

        # Primero intentamos usar url_rar_file si está disponible
        if url_rar_file:
            return HistoricalNewsDataSource(url_rar_file=url_rar_file)
        # Solo usamos path_to_csv_file si el archivo existe
        elif path_to_csv_file and Path(path_to_csv_file).exists():
            return HistoricalNewsDataSource(path_to_csv_file=path_to_csv_file)
        else:
            raise ValueError(
                "Either HISTORICAL_DATA_SOURCE_URL_RAR_FILE or HISTORICAL_DATA_SOURCE_CSV_FILE must be set"
            )

    # elif data_source == "historical":
    #     # We read the news from a CSV file, that we previously need to download from an external URL
    #     # https://github.com/soheilrahsaz/cryptoNewsDataset/raw/refs/heads/main/CryptoNewsDataset_csvOutput.rar
    #     # Unccompress and wrap it as Quix Streams CSVSource
    #     # All this logic is implemented in a Custom Quix Streams Source
    #     url_rar_file = env_vars.get("HISTORICAL_DATA_SOURCE_URL_RAR_FILE")
    #     path_to_csv_file = env_vars.get("HISTORICAL_DATA_SOURCE_CSV_FILE")
    #     logger.info(f"HISTORICAL_DATA_SOURCE_URL_RAR_FILE: {url_rar_file}")
    #     # if not url_rar_file:
    #     #     raise ValueError("HISTORICAL_DATA_SOURCE_URL_RAR_FILE is not set")
    #     # #return HistoricalNewsDataSource(url_rar_file=url_rar_file)
    #     # return HistoricalNewsDataSource(path_to_csv_file=path_to_csv_file)
    #     logger.info(f"HISTORICAL_DATA_SOURCE_CSV_FILE: {path_to_csv_file}")

    #     # Decide qué parámetro usar basado en lo que está disponible
    #     if path_to_csv_file:
    #         return HistoricalNewsDataSource(path_to_csv_file=path_to_csv_file)
    #     elif url_rar_file:
    #         return HistoricalNewsDataSource(url_rar_file=url_rar_file)
    #     else:
    #         raise ValueError("Either HISTORICAL_DATA_SOURCE_URL_RAR_FILE or HISTORICAL_DATA_SOURCE_CSV_FILE must be set")

    else:
        raise ValueError(f"Invalid data source: {data_source}")
