import os
import pandas as pd
import time

from pathlib import Path
from loguru import logger

from quixstreams.sources.base import Source
from typing import Optional

from .news import News


def download_and_extract_rar_file(url_rar_file: str) -> str:
    """
    Checks if data/cryptopanic_news.csv exists, if not downloads and extracts it from RAR

    Args:
        url_rar_file: The URL of the RAR file to download

    Returns:
        str: The path to the extracted CSV file
    """
    # Define paths
    current_dir = Path(__file__).parent
    data_dir = current_dir / "data"
    temp_dir = current_dir / "temp"
    target_file = data_dir / "cryptopanic_news.csv"

    # If the file already exists, return it
    if target_file.exists():
        return str(target_file)

    # Create necessary directories
    data_dir.mkdir(exist_ok=True)
    temp_dir.mkdir(exist_ok=True)

    try:
        # Download and extract
        rar_path = temp_dir / "download.rar"
        os.system(f"wget -O {rar_path} {url_rar_file}")
        os.system(f"unar -f -o {temp_dir} {rar_path}")

        # Move the file to data
        extracted_file = temp_dir / "download" / "cryptopanic_news.csv"
        if not extracted_file.exists():
            raise FileNotFoundError(
                "No se encontró cryptopanic_news.csv en el archivo RAR"
            )

        extracted_file.rename(target_file)

        # Clean up temporary directory
        import shutil

        shutil.rmtree(temp_dir)

        return str(target_file)

    except Exception as e:
        logger.error(f"Error procesando el archivo: {e}")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise


### Commented in Backfill pipeline for news - Part 5 3:32

# HistoricalNewsDataSource = CSVSource

# def get_historical_data_source(url_rar_file: str) -> CSVSource:
#     # # to test the function
#     # # Use the direct url to the rar file
#     # url_rar_file = "https://github.com/soheilrahsaz/cryptoNewsDataset/raw/refs/heads/main/CryptoNewsDataset_csvOutput.rar"
#     # # Download the rar file
#     # path_to_csv_file = download_and_extract_rar_file(url_rar_file)
#     # # Create a CSVSource
#     # return CSVSource(path=path_to_csv_file, name="cryptopanic-news-data")

#     # when is working, remove the url_rar_file and the download_and_extract_rar_file function

#     # we dont need to read the url here because we do it from factory.py
#     # url_rar_file = os.getenv("HISTORICAL_DATA_SOURCE_URL")
#     # if not url_rar_file:
#     #     raise ValueError("HISTORICAL_DATA_SOURCE_URL no está configurada")
#     # Download the rar file
#     path_to_csv_file = download_and_extract_rar_file(url_rar_file)
#     # Create a CSVSource
#     return CSVSource(path=path_to_csv_file, name="historical_news")


class HistoricalNewsDataSource(Source):
    def __init__(
        self,
        url_rar_file: Optional[str] = None,
        path_to_csv_file: Optional[str] = None,
    ):
        super().__init__(name="news_historical_data_source")
        self.url_rar_file = url_rar_file
        self.path_to_csv_file = path_to_csv_file

        if self.url_rar_file:
            self.path_to_csv_file = download_and_extract_rar_file(self.url_rar_file)

        if not self.path_to_csv_file:
            if not self.url_rar_file:
                raise ValueError(
                    "Either url_rar_file or path_to_csv_file must be provided"
                )

    def run(self):
        with open(self.path_to_csv_file, "r"):  # as f:
            while self.running:
                # Load the csv file into a dataframe
                df = pd.read_csv(self.path_to_csv_file)

                # Drop nan values
                df = df.dropna()

                # convert the dataframe into a list of dictionaries
                rows = df[["title", "sourceId", "newsDatetime"]].to_dict(
                    orient="records"
                )

                for row in rows:
                    # Transform raw data into news object
                    news = News.from_csv_row(
                        title=row["title"],
                        source_id=row["sourceId"],
                        news_datetime=row["newsDatetime"],
                    )

                    # Serialize the News object into a JSON string
                    msg = self.serialize(key="", value=news.to_dict())

                    # Push message to internal Kafka topic that acts like a bridge
                    # between my source and the Quix Streams Application object that
                    # uses this source to ingest data
                    #   see in run.py
                    #   sdf = app.dataframe(source=news_source)
                    self.produce(
                        key=msg.key,
                        value=msg.value,
                    )

                    # Añadir un pequeño delay entre mensajes
                    time.sleep(0.01)  # 10ms de delay


if __name__ == "__main__":
    source = HistoricalNewsDataSource(
        path_to_csv_file="sources/data/cryptopanic_news.csv"
    )
    source.run()
