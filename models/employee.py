from models.person import Person


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
