from abc import ABC, abstractmethod


class Rule(ABC):
    name: str
    category: str
    severity: str
    penalty: int

    @abstractmethod
    def evaluate(self, architecture):
        pass