import json
from typing import List

from loguru import logger
from websocket import create_connection

from .base import TradesAPI
from .trade import Trade


class KrakenWebsocketAPI(TradesAPI):
    URL = 'wss://ws.kraken.com/v2'

    def __init__(self, pairs: List[str]):
        self.pairs = pairs

        # Create a websocket client
        self._ws_client = create_connection(self.URL)

        # Subscribe to the websocket and wait for the initial snapshot
        self._subscribe()

    def get_trades(self) -> List[Trade]:
        """
        Fetches the trades from the Kraken websocket API and returns a list of Trade objects

        Returns:
            List[Trade]: A list of Trade objects
        """
        # receive the data from the websocket
        data = self._ws_client.recv()

        if 'heartbeat' in data:
            logger.info('Heartbeat received')
            return []

        # transform raw string into json
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')
            return []

        try:
            trades_data = data['data']
        except KeyError:
            logger.error(f"No 'data' field in the message: {data}")
            return []

        trades = [
            Trade.from_kraken_api_websocket_response(
                pair=trade['symbol'],
                price=trade['price'],
                volume=trade['qty'],
                timestamp=trade['timestamp'],
                # timestamp_ms=self.datestr2milliseconds(trade['timestamp']),
            )
            for trade in trades_data
        ]
        # breakpoint()
        return trades

    def is_done(self) -> bool:
        return False

    def _subscribe(self):
        """
        Subscribe to the websocket and wait for the initial snapshot
        """

        # Send the subscribe message to the websocket
        self._ws_client.send(
            json.dumps(
                {
                    'method': 'subscribe',
                    'params': {
                        'channel': 'trade',
                        'symbol': self.pairs,
                        'snapshot': True,
                    },
                }
            )
        )

        for _pair in self.pairs:
            _ = self._ws_client.recv()
            _ = self._ws_client.recv()

    def datestr2milliseconds(self, iso_time: str) -> int:
        """
        Convert a date string to milliseconds

        Args:
            iso_time (str): The date string in ISO format (e.g., 2024-01-01T00:00:00.000Z)
        Returns:
            int: Unix timestamp in milliseconds
        """
        from datetime import datetime

        dt = datetime.strptime(iso_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        return int(dt.timestamp() * 1000)
