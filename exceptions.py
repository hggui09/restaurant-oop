class RestaurantError(Exception):
    pass

class TableOccupiedError(RestaurantError):
    def __init__(self, table_number: int):
        self.table_number = table_number
        super().__init__(f"Стол №{table_number} уже занят")


class NoFreeTableError(RestaurantError):
    def __init__(self, guests: int):
        self.guests = guests
        super().__init__(f"Нет свободного стола на {guests} гост.")


class ItemNotFoundError(RestaurantError):
    def __init__(self, what: str, key):
        self.what = what
        self.key = key
        super().__init__(f"Не найдено: {what.lower()} '{key}'")

class OrderStatusError(RestaurantError):
    def __init__(self, order_number: int, current_status, action: str):
        self.order_number = order_number
        self.current_status = current_status
        super().__init__(
            f"Заказ №{order_number}: нельзя {action}, "
            f"текущий статус - '{current_status.value}'"
        )

class StorageError(RestaurantError):
    pass
