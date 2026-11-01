from exceptions.item_not_found_error import ItemNotFoundError
from models.chef import Chef
from repositories.repository import Repository


class ChefRepository(Repository):
    def add(self, chef: Chef) -> None:
        if not isinstance(chef, Chef):
            raise TypeError("В репозиторий поваров можно добавить только повара")
        if self._exists(chef.name):
            raise ValueError(f"Повар с именем '{chef.name}' уже есть")
        super().add(chef)

    def get_by_name(self, name: str) -> Chef:
        for chef in self._items:
            if chef.name.lower() == name.strip().lower():
                return chef
        raise ItemNotFoundError("Повар", name)

    def _exists(self, name: str) -> bool:
        return any(chef.name.lower() == name.strip().lower() for chef in self._items)
