from exceptions.item_not_found_error import ItemNotFoundError
from exceptions.no_free_table_error import NoFreeTableError
from models.chef import Chef
from models.customer import Customer
from models.employee import Employee
from models.menu import Menu
from models.order import Order
from models.order_status import OrderStatus
from models.table import Table
from models.waiter import Waiter
from repositories.chef_repository import ChefRepository
from repositories.waiter_repository import WaiterRepository


class Restaurant:
    def __init__(self, name: str):
        self.name = name
        self.menu = Menu()
        self.waiters = WaiterRepository()
        self.chefs = ChefRepository()
        self._tables: list[Table] = []
        self._orders: list[Order] = []
        self._next_order_number = 1

    @property
    def tables(self) -> list[Table]:
        return self._tables

    @property
    def staff(self) -> list[Employee]:
        return self.waiters.get_all() + self.chefs.get_all()

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
        if isinstance(employee, Waiter):
            self.waiters.add(employee)
        elif isinstance(employee, Chef):
            self.chefs.add(employee)
        else:
            raise TypeError("Можно нанять только официанта или повара")

    def fire(self, employee: Employee) -> None:
        if isinstance(employee, Waiter):
            self.waiters.remove(employee)
        elif isinstance(employee, Chef):
            self.chefs.remove(employee)

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
