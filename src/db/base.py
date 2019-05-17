from abc import ABC, abstractmethod
from src.process import WeatherRecord
from typing import Tuple, List


class BaseDataLayer(ABC):
    @abstractmethod
    def put(self, record: WeatherRecord) -> bool:
        pass

    @abstractmethod
    def query(self, ts_from: int, ts_to: int,
              city: str) -> List[WeatherRecord]:
        pass
