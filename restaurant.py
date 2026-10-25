from enums import OrderStatus, PaymentMethod
from exceptions import (
    TableOccupiedError, NoFreeTableError, ItemNotFoundError, OrderStatusError,
)
from menu import Menu, MenuItem
from people import Customer, Employee, Waiter, Chef


class Table:
    def __init__(self, number: int, seats: int):
        if seats <= 0:
            raise ValueError("Количество мест должно быть больше нуля")
        self.number = number
        self.seats = seats
        self._is_occupied = False

    def occupy(self) -> None:
        if self._is_occupied:
            raise TableOccupiedError(self.number)
        self._is_occupied = True

    def release(self) -> None:
        self._is_occupied = False

    def is_free(self) -> bool:
        return not self._is_occupied


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

class Payment:
    def __init__(self, order: Order, method: PaymentMethod, tip_percent: float = 0):
        if not 0 <= tip_percent <= 100:
            raise ValueError("Процент чаевых должен быть от 0 до 100")
        self.order = order
        self.method = method
        self.tip_percent = tip_percent

    def tips_amount(self) -> float:
        return self.order.total() * self.tip_percent / 100

    def total_with_tips(self) -> float:
        return self.order.total() + self.tips_amount()

    def pay(self) -> None:
        if self.order.status != OrderStatus.READY:
            raise OrderStatusError(self.order.number, self.order.status, "оплатить")
        self.order.set_status(OrderStatus.PAID)
        self.order.waiter.add_tips(self.tips_amount())
        self.order.table.release()


class Restaurant:
    def __init__(self, name: str):
        self.name = name
        self.menu = Menu()
        self._tables: list[Table] = []
        self._staff: list[Employee] = []
        self._orders: list[Order] = []
        self._next_order_number = 1

    @property
    def tables(self) -> list[Table]:
        return self._tables

    @property
    def staff(self) -> list[Employee]:
        return self._staff

    @property
    def orders(self) -> list[Order]:
        return self._orders

    def add_table(self, seats: int, number: int | None = None) -> Table:
        if number is None:
            number = len(self._tables) + 1
        table = Table(number, seats)
        self._tables.append(table)
        return table

    def get_table(self, number: int) -> Table:
        for table in self._tables:
            if table.number == number:
                return table
        raise ItemNotFoundError("Стол", number)

    def find_table(self, guests: int) -> Table:
        if guests < 1:
            raise ValueError("Количество гостей должно быть не меньше 1")
        for table in self._tables:
            if table.is_free() and table.seats >= guests:
                return table
        raise NoFreeTableError(guests)

    def seat_customer(self, guests: int) -> Table:
        table = self.find_table(guests)
        table.occupy()
        return table

    def hire(self, employee: Employee) -> None:
        self._staff.append(employee)

    def fire(self, employee: Employee) -> None:
        self._staff.remove(employee)

    def get_waiter(self, name: str) -> Waiter:
        for waiter in self.waiters():
            if waiter.name.lower() == name.strip().lower():
                return waiter
        raise ItemNotFoundError("Официант", name)

    def get_chef(self, name: str) -> Chef:
        for chef in self.chefs():
            if chef.name.lower() == name.strip().lower():
                return chef
        raise ItemNotFoundError("Повар", name)

    def waiters(self) -> list[Waiter]:
        return [e for e in self._staff if isinstance(e, Waiter)]

    def chefs(self) -> list[Chef]:
        return [e for e in self._staff if isinstance(e, Chef)]

    def take_order(self, table: Table, waiter: Waiter, customer: Customer) -> Order:
        order = Order(self._next_order_number, waiter, table, customer)
        self._next_order_number += 1
        self._orders.append(order)
        return order

    def add_existing_order(self, order: Order) -> None:
        self._orders.append(order)
        self._next_order_number = max(self._next_order_number, order.number + 1)

    def get_order(self, number: int) -> Order:
        for order in self._orders:
            if order.number == number:
                return order
        raise ItemNotFoundError("Заказ", number)

    def revenue(self) -> float:
        return sum(o.total() for o in self._orders if o.status == OrderStatus.PAID)
