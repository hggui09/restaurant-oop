from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name: str, phone: str):
        if not name.strip():
            raise ValueError("Имя не может быть пустым")
        self.name = name
        self.phone = phone

    @abstractmethod
    def get_role(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.get_role()} {self.name}"
