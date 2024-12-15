from abc import ABC, abstractmethod


class TradesAPI(ABC):
    @abstractmethod
    def get_trades(self):
        pass

    @abstractmethod
    def is_done(self) -> bool:
        pass
