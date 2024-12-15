from abc import ABC, abstractmethod

from .trade import Trade


class TradesAPI(ABC):
    @abstractmethod
    def get_trades(self):
        pass

    @abstractmethod
    def is_done(self) -> bool:
        pass

