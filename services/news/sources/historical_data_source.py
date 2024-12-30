from quixstreams.sources import CSVSource
import os

from pathlib import Path
from loguru import logger


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


HistoricalNewsDataSource = CSVSource


def get_historical_data_source(url_rar_file: str) -> CSVSource:
    # # to test the function
    # # Use the direct url to the rar file
    # url_rar_file = "https://github.com/soheilrahsaz/cryptoNewsDataset/raw/refs/heads/main/CryptoNewsDataset_csvOutput.rar"
    # # Download the rar file
    # path_to_csv_file = download_and_extract_rar_file(url_rar_file)
    # # Create a CSVSource
    # return CSVSource(path=path_to_csv_file, name="cryptopanic-news-data")

    # when is working, remove the url_rar_file and the download_and_extract_rar_file function

    # we dont need to read the url here because we do it from factory.py
    # url_rar_file = os.getenv("HISTORICAL_DATA_SOURCE_URL")
    # if not url_rar_file:
    #     raise ValueError("HISTORICAL_DATA_SOURCE_URL no está configurada")
    # Download the rar file
    path_to_csv_file = download_and_extract_rar_file(url_rar_file)
    # Create a CSVSource
    return CSVSource(path=path_to_csv_file, name="historical_news")


# if __name__ == "__main__":
#     #url_rar_file = "https://github.com/soheilrahsaz/cryptoNewsDataset/raw/refs/heads/main/CryptoNewsDataset_csvOutput.rar"
#     path_to_csv_file = get_historical_data_source()
#     logger.info(f"CSV file path: {path_to_csv_file}")
