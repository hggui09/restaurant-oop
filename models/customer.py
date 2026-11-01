from models.person import Person


class Customer(Person):
    def get_role(self) -> str:
        return "Гость"
