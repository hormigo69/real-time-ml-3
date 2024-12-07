from datetime import datetime

from pydantic import BaseModel


class Trade(BaseModel):
    """
    A trade from the Kraken API.
        "symbol": "MATIC/USD",
        "side": "sell",
        "price": 0.5117,
        "qty": 40.0,
        "ord_type": "market",
        "trade_id": 4665906,
        "timestamp": "2023-09-25T07:49:37.708706Z"
    """

    pair: str
    price: float
    volume: float
    timestamp: datetime
    timestamp_ms: int

    '''@field_validator('timestamp_ms', mode='after')
    def set_timestamp_ms(cls, v, values):
        """
        Automatically set the timestamp_ms based on the timestamp field
        """
        timestamp = values.get('timestamp')
        if timestamp:
            return int(timestamp.timestamp() * 1000)
        return v'''

    # @property
    # def timestamp_ms(self) -> int:
    #     """
    #     Convert the timestamp to milliseconds
    #     """
    #     return int(self.timestamp.timestamp() * 1000)

    def to_dict(self) -> dict:
        # pydantic method to convert the model to a dict
        return self.model_dump_json()

    # if you prefer not to serialize all the fields, you can do this:
    # return {
    #     "pair": self.pair,
    #     "price": self.price,
    #     "volume": self.volume,
    #     "timestamp_ms": self.timestamp_ms,
    #     "timestamp": self.timestamp_ms,
    # }
