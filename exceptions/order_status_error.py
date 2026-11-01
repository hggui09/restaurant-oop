from exceptions.restaurant_error import RestaurantError


class OrderStatusError(RestaurantError):
    def __init__(self, order_number: int, current_status, action: str):
        self.order_number = order_number
        self.current_status = current_status
        super().__init__(
            f"Заказ №{order_number}: нельзя {action}, "
            f"текущий статус - '{current_status.value}'"
        )
