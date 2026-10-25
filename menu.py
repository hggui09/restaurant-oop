from abc import ABC, abstractmethod
from exceptions import ItemNotFoundError

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


class Dish(MenuItem):
    def __init__(self, name: str, price: float, weight: int):
        super().__init__(name, price)
        self.weight = weight

    def describe(self) -> str:
        return f"{self.name} ({self.weight} г) - {self.price:.0f} руб"


class Drink(MenuItem):
    def __init__(self, name: str, price: float, volume: int, is_alcoholic: bool = False):
        super().__init__(name, price)
        self.volume = volume
        self.is_alcoholic = is_alcoholic

    def describe(self) -> str:
        alc = ", 18+" if self.is_alcoholic else ""
        return f"{self.name} ({self.volume} мл{alc}) - {self.price:.0f} руб"


class Menu:
    def __init__(self):
        self._items: list[MenuItem] = []

    @property
    def items(self) -> list[MenuItem]:
        return self._items

    def add(self, item: MenuItem) -> None:
        self._items.append(item)

    def remove(self, item: MenuItem) -> None:
        self._items.remove(item)

    def find(self, name: str) -> MenuItem:
        for item in self._items:
            if item.name.lower() == name.strip().lower():
                return item
        raise ItemNotFoundError("Позиция меню", name)

    def show(self) -> str:
        if not self._items:
            return "Меню пустое"
        return "\n".join(f"  {item.describe()}" for item in self._items)
