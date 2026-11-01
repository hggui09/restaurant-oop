from exceptions.item_not_found_error import ItemNotFoundError
from models.waiter import Waiter
from repositories.repository import Repository


class WaiterRepository(Repository):
    def add(self, waiter: Waiter) -> None:
        if not isinstance(waiter, Waiter):
            raise TypeError("В репозиторий официантов можно добавить только официанта")
        if self._exists(waiter.name):
            raise ValueError(f"Официант с именем '{waiter.name}' уже есть")
        super().add(waiter)

    def get_by_name(self, name: str) -> Waiter:
        for waiter in self._items:
            if waiter.name.lower() == name.strip().lower():
                return waiter
        raise ItemNotFoundError("Официант", name)

    def total_tips(self) -> float:
        return sum(waiter.tips_total for waiter in self._items)

    def _exists(self, name: str) -> bool:
        return any(waiter.name.lower() == name.strip().lower() for waiter in self._items)
