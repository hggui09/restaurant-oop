from exceptions.restaurant_error import RestaurantError


class ItemNotFoundError(RestaurantError):
    def __init__(self, what: str, key):
        self.what = what
        self.key = key
        super().__init__(f"Не найдено: {what.lower()} '{key}'")
