from abc import ABC, abstractmethod
from typing import List


class BaseReport(ABC):
    @abstractmethod
    def run(self, files: List[str]) -> None:
        ...
