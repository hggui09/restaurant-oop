from exceptions.item_not_found_error import ItemNotFoundError
from models.menu_item import MenuItem


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
