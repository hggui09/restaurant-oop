from enum import Enum


class OrderStatus(Enum):
    CREATED = "Создан"
    COOKING = "Готовится"
    READY = "Готов"
    PAID = "Оплачен"
