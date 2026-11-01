from models.employee import Employee


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
