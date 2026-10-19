from enum import Enum

class OrderStatus(Enum):
    CREATED = "Создан"
    COOKING = "Готовится"
    READY = "Готов"
    PAID = "Оплачен"

class PaymentMethod(Enum):
    CARD = "Карта"
    CASH = "Наличные"

class Table:
    def __init__(self, number: int, seats: int):
        self.number = number
        self.seats = seats
        self._is_occupied = False

    def occupy(self):
        if self._is_occupied:
            raise RuntimeError(f"Стол №{self.number} уже занят")
        self._is_occupied = True

    def release(self):
        self._is_occupied = False

    def is_free(self):
        return not self._is_occupied


