from abc import ABC, abstractmethod


class TransactionPattern(ABC):

    @abstractmethod
    def matches(self, text: str) -> bool:
        pass

    @abstractmethod
    def normalize(self, text: str, source_bank: str):
        pass