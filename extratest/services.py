import random
import json

class Extrasense:
    """Класс реализующий экстрасенса"""

    __slots__ = ['numbers', 'rating']

    def __init__(self, numbers: list = [], rating: int = 0) -> None:
        self.numbers = numbers
        self.rating = rating

    def new_number(self) -> None:
        self.numbers.append(random.randrange(10,100))

    def __rateup(self) -> None:
        self.rating += 1

    def __ratedown(self) -> None:
        self.rating -= 1

    def check_last_number(self, number: int) -> None:
        if self.numbers[-1] == number:
            self.__rateup()
        else:
            self.__ratedown()


class ExtrasenseJsonEncoder(json.JSONEncoder):
    """Класс, реализующий кастомный энкодер для сериализации экстрасенса в JSON"""
    def default(self, o: Extrasense):
        if isinstance(o, Extrasense):
            return {'numbers': o.numbers, 'rating': o.rating}
        return super().default(o)


class ExtracenseList:
    """Класс, реализующий список экстрасенсов"""
    def __init__(self) -> None:
        self.list_of_extrasenses: list(Extrasense) = [] 
        self.index: int  = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.list_of_extrasenses):
            self.index = 0
            raise StopIteration
        index = self.index
        self.index += 1
        return self.list_of_extrasenses[index]

    def add_extrasense_to_begin(self, extrasense: Extrasense) -> None:
        self.list_of_extrasenses.insert(0, extrasense)
    
    def create_n_extrasenses_in_list(self, n:int) -> None:
        for i in range(n):
            ex = Extrasense()
            self.list_of_extrasenses.append(ex)
    
    def len_of_list(self) -> int:
        return len(self.list_of_extrasenses)


class ExtrasenseListJsonEncoder(json.JSONEncoder):
    """Класс, реализующий кастомный энкодер для сериализации списка экстрасенсов в JSON"""
    def default(self, o: ExtracenseList):
        if isinstance(o, ExtracenseList):
            jsoned_list = []
            for ex in o:
                jsoned_list.insert(0, { 'numbers': ex.numbers, 'rating': ex.rating })
            return jsoned_list
        return super().default(o)
