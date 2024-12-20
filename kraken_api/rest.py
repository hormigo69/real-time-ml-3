import json
import time
from typing import List

import requests
from loguru import logger

from .base import TradesAPI
from .trade import Trade


class KrakenRestAPI(TradesAPI):
    def __init__(self, pairs: List[str], last_n_days: int):
        self.pairs = pairs
        self.last_n_days = last_n_days

        self.apis = [
            KrakenRestAPISinglePair(pair=pair, last_n_days=last_n_days)
            for pair in self.pairs
        ]

    def get_trades(self) -> List[Trade]:
        """
        Gets trades for each pair, srto the timestamp and return the trades
        """
        trades = []
        for api in self.apis:
            if not api.is_done():
                trades += api.get_trades()

        # sort the trades by timestamp
        trades.sort(key=lambda x: x.timestamp_ms)

        # breakpoint()

        return trades

    def is_done(self) -> bool:
        """
        We are done when all the apis are done
        """
        for api in self.apis:
            if not api.is_done():
                return False
        return True


class KrakenRestAPISinglePair(TradesAPI):
    URL = 'https://api.kraken.com/0/public/Trades'

    def __init__(
        self,
        pair: str,
        last_n_days: int,
    ):
        self.pair = pair
        self.last_n_days = last_n_days
        self._is_done = False

        # get current timestamp in nanoseconds
        self.since_timestamp_ns = int(
            time.time_ns() - last_n_days * 24 * 60 * 60 * 1000000000
        )

        logger.info(
            f'Getting trades for pair {self.pair} for the last {self.since_timestamp_ns * 1000000000} seconds'
        )

    def get_trades(self) -> List[Trade]:
        """
        Send a request to the Kraken API to get the trades for the pair and last n days.
        """

        headers = {'Accept': 'application/json'}
        params = {
            'pair': self.pair,
            'since': self.since_timestamp_ns,
        }

        response = requests.request('GET', self.URL, headers=headers, params=params)

        # TODO: revisar si esto lo puedo quitar. Añadimos un retraso de 2 segundos entre peticiones
        #time.sleep(0.5)

        # parse the response as json
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')
            return []

        # get the trades for the self.pair
        try:
            trades = data['result'][self.pair]
        except KeyError:
            logger.error(
                f'Error getting trades. Status code: {response.status_code}'
            )
            return []

        # convert the trades to Trade objects
        trades = [
            Trade.from_kraken_rest_api_response(
                pair=self.pair,
                price=trade[0],
                volume=trade[1],
                timestamp_sec=trade[2],
            )
            for trade in trades
        ]

        # update the since_timestamp_ns
        self.since_timestamp_ns = int(float(data['result']['last']))

        # Check if we are done
        # TODO: check if these stopping conditions are correct
        if self.since_timestamp_ns > int(time.time_ns() - 1000000000):
            self._is_done = True
        if self.since_timestamp_ns == 0:
            self._is_done = True

        return trades

    def is_done(self) -> bool:
        return self._is_done
