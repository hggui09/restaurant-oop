from exceptions.order_status_error import OrderStatusError
from models.order import Order
from models.order_status import OrderStatus
from models.payment_method import PaymentMethod


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
