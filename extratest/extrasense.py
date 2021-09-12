import random

class Extrasense:

    def new_number(self) -> None:
        self.numbers.append(random.randrange(9,99))

    def rateup(self) -> None:
        self.rating += 1

    def ratedown(self) -> None:
        self.rating -= 1

    def last_number(self) -> int:
        return self.numbers[-1]

    def __init__(self, numbers = [], rating = 0) -> None:
        self.numbers = numbers
        self.rating = rating