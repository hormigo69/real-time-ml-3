from typing import List

import requests
from loguru import logger
from pydantic import BaseModel


class News(BaseModel):
    """
    This is the data model for news.
    """

    title: str
    published_at: str
    source: str

    # Challenge: You can also keep the url and scrape it to get even more context
    # about this piece of news.

    def to_dict(self) -> dict:
        return self.model_dump()


class NewsDownloader:
    """
    This class is used to download news from Cryptopanic API.
    """

    URL = "https://cryptopanic.com/api/free/v1/posts/"

    def __init__(
        self,
        cryptopanic_api_key: str,
    ):
        self.cryptopanic_api_key = cryptopanic_api_key
        # self.last_published_at = None

    def get_news(self) -> List[News]:
        """
        Keeps on calling _get_batch_of_news until it gets an empty list.
        """
        news = []
        url = self.URL + "?auth_token=" + self.cryptopanic_api_key

        while True:
            # logger.debug(f"Fetching news from {url}")
            batch_of_news, next_url = self._get_batch_of_news(url)
            news += batch_of_news
            logger.debug(f"Fetched {len(batch_of_news)} news")

            if not batch_of_news:
                break
            if not next_url:
                logger.debug("No more news to fetch")
                break

            url = next_url

        # sort the news by published_at
        news.sort(key=lambda x: x.published_at, reverse=False)

        return news

    def _get_batch_of_news(self, url: str) -> tuple[List[News], str]:
        """
        Connects to Cryptopanic API and fetches news.

        Args:
            url: The URL to fetch news from.

        Returns:
            A tuple containing the list of news and the next URL to fetch from.
        """
        response = requests.get(url)

        try:
            response = response.json()
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            from time import sleep

            sleep(1)
            return ([], "")

        # Parse the API response into a piece of news  .
        news = [
            News(
                title=post["title"],
                published_at=post["published_at"],
                source=post["domain"],
            )
            for post in response["results"]
        ]

        # Extract the next URL from the API response.
        next_url = response["next"]

        return news, next_url


if __name__ == "__main__":
    from services.news.config import cryptopanic_config

    news_downloader = NewsDownloader(cryptopanic_api_key=cryptopanic_config.api_key)
    news = news_downloader.get_news()
    logger.debug(f"Fetched {len(news)} news items")

    breakpoint()
