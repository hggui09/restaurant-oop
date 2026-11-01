from models.menu_item import MenuItem


class Drink(MenuItem):
    def __init__(self, name: str, price: float, volume: int, is_alcoholic: bool = False):
        super().__init__(name, price)
        self.volume = volume
        self.is_alcoholic = is_alcoholic

    def describe(self) -> str:
        alc = ", 18+" if self.is_alcoholic else ""
        return f"{self.name} ({self.volume} мл{alc}) - {self.price:.0f} руб"
