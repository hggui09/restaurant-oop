from abc import ABC, abstractmethod


class MenuItem(ABC):
    def __init__(self, name: str, price: float):
        if not name.strip():
            raise ValueError("Название позиции не может быть пустым")
        self.name = name
        self.price = price

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = value

    @abstractmethod
    def describe(self) -> str:
        pass
