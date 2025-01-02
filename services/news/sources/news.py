from pydantic import BaseModel
from datetime import datetime, timezone


class News(BaseModel):
    """
    This is the data model for news.
    """

    title: str
    published_at: str  # "2024-12-18T12:29:27Z"
    source: str

    # Challenge: You can also keep the url and scrape it to get even more context
    # about this piece of news.

    @classmethod
    def from_csv_row(
        cls,
        source_id: int,
        title: str,
        news_datetime: str,
    ) -> "News":
        """
        This method is used to create a News object from a CSV row.

        The data we read from the CSV is in the following format:
        {
            "title": "string",
            "sourceId": "string",
            "newsDatetime": "string",: '7/12/2024 14:53'
        }
        """
        # parse a datetime string with this format '7/12/2024 14:53' into a datetime object
        # in UTC timezone
        news_datetime = datetime.strptime(news_datetime, "%m/%d/%Y %H:%M")
        news_datetime = news_datetime.replace(tzinfo=timezone.utc)

        # convert the datetime object to a string in the format '2024-12-18T12:29:27Z'
        published_at = news_datetime.isoformat()

        # convert the source_id to a string
        source = str(source_id)

        return cls(
            source=source,
            title=title,
            published_at=published_at,
        )

    def to_dict(self) -> dict:
        return {
            **self.model_dump(),
            "timestamp_ms": int(
                datetime.fromisoformat(
                    self.published_at.replace("Z", "+00:00")
                ).timestamp()
                * 1000
            ),
        }
