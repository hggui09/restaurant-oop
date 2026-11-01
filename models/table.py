from exceptions.table_occupied_error import TableOccupiedError


class Table:
    def __init__(self, number: int, seats: int):
        if seats <= 0:
            raise ValueError("Количество мест должно быть больше нуля")
        self.number = number
        self.seats = seats
        self._is_occupied = False

    def occupy(self) -> None:
        if self._is_occupied:
            raise TableOccupiedError(self.number)
        self._is_occupied = True

    def release(self) -> None:
        self._is_occupied = False

    def is_free(self) -> bool:
        return not self._is_occupied
