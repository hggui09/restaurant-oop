class Repository:
    def __init__(self):
        self._items: list = []

    def add(self, item) -> None:
        self._items.append(item)

    def remove(self, item) -> None:
        self._items.remove(item)

    def get_all(self) -> list:
        return self._items

    def count(self) -> int:
        return len(self._items)
