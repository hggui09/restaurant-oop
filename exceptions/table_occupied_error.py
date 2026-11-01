from exceptions.restaurant_error import RestaurantError


class TableOccupiedError(RestaurantError):
    def __init__(self, table_number: int):
        self.table_number = table_number
        super().__init__(f"Стол №{table_number} уже занят")
