from exceptions.order_status_error import OrderStatusError
from models.customer import Customer
from models.menu_item import MenuItem
from models.order_status import OrderStatus
from models.table import Table
from models.waiter import Waiter


class Order:
    _NEXT_STATUS = {
        OrderStatus.CREATED: OrderStatus.COOKING,
        OrderStatus.COOKING: OrderStatus.READY,
        OrderStatus.READY: OrderStatus.PAID,
    }

    def __init__(self, number: int, waiter: Waiter, table: Table, customer: Customer):
        self.number = number
        self.waiter = waiter
        self.table = table
        self.customer = customer
        self._items: dict[MenuItem, int] = {}
        self._status = OrderStatus.CREATED

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def items(self) -> dict[MenuItem, int]:
        return self._items

    def add_item(self, item: MenuItem, quantity: int = 1) -> None:
        if self._status != OrderStatus.CREATED:
            raise OrderStatusError(self.number, self._status, "добавлять позиции")
        if quantity < 1:
            raise ValueError("Количество должно быть не меньше 1")
        self._items[item] = self._items.get(item, 0) + quantity

    def total(self) -> float:
        return sum(item.price * qty for item, qty in self._items.items())

    def set_status(self, new_status: OrderStatus) -> None:
        if self._NEXT_STATUS.get(self._status) != new_status:
            raise OrderStatusError(
                self.number, self._status, f"перевести в '{new_status.value}'"
            )
        self._status = new_status

    def print_bill(self) -> str:
        lines = [f"Счет по заказу №{self.number}, стол №{self.table.number}"]
        for item, qty in self._items.items():
            lines.append(f"  {item.name} x{qty} = {item.price * qty:.0f} руб")
        lines.append(f"  ИТОГО: {self.total():.0f} руб")
        return "\n".join(lines)
