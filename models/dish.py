from models.menu_item import MenuItem


class Dish(MenuItem):
    def __init__(self, name: str, price: float, weight: int):
        super().__init__(name, price)
        self.weight = weight

    def describe(self) -> str:
        return f"{self.name} ({self.weight} г) - {self.price:.0f} руб"
