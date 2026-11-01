from models.employee import Employee
from models.order_status import OrderStatus


class Chef(Employee):
    def __init__(self, name: str, phone: str, salary: float, position: str = "Повар"):
        super().__init__(name, phone, salary, position)

    def cook(self, order) -> None:
        order.set_status(OrderStatus.READY)

    def get_role(self) -> str:
        return "Повар"
