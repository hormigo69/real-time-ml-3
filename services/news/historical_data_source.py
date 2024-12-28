from quixstreams.sources import CSVSource
import os
from pathlib import Path
from loguru import logger


def download_and_extract_rar_file(url_rar_file: str) -> str:
    """
    Downloads a RAR file from a URL, extracts it, and returns the path to the first CSV file found.
        Downloads a RAR file from a URL, extracts it, and returns the path to cryptopanic_news.csv

    Args:
        url_rar_file (str): URL of the RAR file to download

    Returns:
        str: Path to the extracted CSV file
    """
    # Create temporary directory if it doesn't exist
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    # Download the RAR file
    rar_path = temp_dir / "download.rar"
    os.system(f"wget -O {rar_path} {url_rar_file}")

    # Extract using unar command (macOS version)
    os.system(f"unar -o {temp_dir} {rar_path}")

    # Buscar específicamente cryptopanic_news.csv
    target_file = temp_dir / "download" / "cryptopanic_news.csv"
    if target_file.exists():
        return str(target_file)

    # If not found, show available files and raise error
    logger.error("Archivos CSV disponibles:")
    for file in temp_dir.glob("**/*.csv"):
        logger.error(f"- {file}")

    raise FileNotFoundError("No se encontró el archivo cryptopanic_news.csv")


def get_historical_data_source(
    url_rar_file: str,
) -> CSVSource:
    # Download the rar file
    path_to_csv_file = download_and_extract_rar_file(url_rar_file)

    # Create a CSVSource
    return CSVSource(path=path_to_csv_file, name="cryptopanic-news-data")


if __name__ == "__main__":
    url_rar_file = "https://github.com/soheilrahsaz/cryptoNewsDataset/raw/refs/heads/main/CryptoNewsDataset_csvOutput.rar"
    path_to_csv_file = get_historical_data_source(url_rar_file)
    logger.info(f"CSV file path: {path_to_csv_file}")
