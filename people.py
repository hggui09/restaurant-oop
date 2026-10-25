from abc import ABC, abstractmethod
from enums import OrderStatus

class Person(ABC):
    def __init__(self, name: str, phone: str):
        if not name.strip():
            raise ValueError("Имя не может быть пустым")
        self.name = name
        self.phone = phone

    @abstractmethod
    def get_role(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.get_role()} {self.name}"

class Customer(Person):
    def get_role(self) -> str:
        return "Гость"

class Employee(Person):
    def __init__(self, name: str, phone: str, salary: float, position: str):
        super().__init__(name, phone)
        self.salary = salary
        self.position = position

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Зарплата должна быть больше нуля")
        self._salary = value

    def get_role(self) -> str:
        return "Сотрудник"


class Waiter(Employee):
    def __init__(self, name: str, phone: str, salary: float, position: str = "Официант"):
        super().__init__(name, phone, salary, position)
        self._tips_total = 0.0

    @property
    def tips_total(self) -> float:
        return self._tips_total

    def add_tips(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Чаевые не могут быть отрицательными")
        self._tips_total += amount

    def get_role(self) -> str:
        return "Официант"

class Chef(Employee):
    def __init__(self, name: str, phone: str, salary: float, position: str = "Повар"):
        super().__init__(name, phone, salary, position)

    def cook(self, order) -> None:
        order.set_status(OrderStatus.READY)

    def get_role(self) -> str:
        return "Повар"

