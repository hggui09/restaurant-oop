from exceptions.restaurant_error import RestaurantError


class NoFreeTableError(RestaurantError):
    def __init__(self, guests: int):
        self.guests = guests
        super().__init__(f"Нет свободного стола на {guests} гост.")
