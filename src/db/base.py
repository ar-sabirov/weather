from abc import ABC, abstractmethod
from src.process import WeatherRecord
from typing import Tuple, List


class BaseDataLayer(ABC):
    @abstractmethod
    def __init__(self, path: str):
        pass

    @abstractmethod
    def put(self, record: WeatherRecord) -> bool:
        pass

    @abstractmethod
    def query(self, interval: Tuple[int, int]) -> List[WeatherRecord]:
        pass