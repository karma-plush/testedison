from __future__ import annotations

import json

from abc import ABC, abstractmethod
from django.core.cache import cache

from importlib import import_module
from django.conf import settings as s

from extra.settings import STORAGE
from extratest.services import (Extrasense, ExtracenseList,
                                ExtrasenseListJsonEncoder, )


SessionStore = import_module(s.SESSION_ENGINE).SessionStore


class StorageFactory(ABC):
    """Интерфейс абстрактной фабрики сохранения состояния"""

    @abstractmethod
    def create_extrasense_saver(self) -> ExtrasenseSaver:
        pass
    

class DjangoSessionStorageFactory(StorageFactory):
    """Фабрика сэйвера состояния в DjangoSession"""

    def create_extrasense_saver(self) -> ExtrasenseSaver:
        return DjangoSessionExtrasenseSaver()


class CacheStorageFactory(StorageFactory):
    """Фабрика сэйвера состояния в cache"""

    def create_extrasense_saver(self) -> ExtrasenseSaver:
        return CacheExtrasenseSaver()


class ExtrasenseSaver(ABC):
    """Интерфейс сохранения состояния экстрасенсов"""
    def __init__(self) -> None:
        self.storage = None
        super().__init__()

    @abstractmethod
    def save(self, session_key, extrasense_list: ExtracenseList, my_numbers: list) -> None:
        pass

    @abstractmethod
    def load(self, session_key) -> dict:
        pass


class DjangoSessionExtrasenseSaver(ExtrasenseSaver):
    """Класс, реализующий сохранение состояния экстрасенсов в DjangoSession"""
 
    def __init__(self) -> None:
        self.storage = SessionStore()
    
    def save(self, session_key, extrasense_list: ExtracenseList, my_numbers: list) -> None:
        jsoned_list = json.dumps(extrasense_list, cls=ExtrasenseListJsonEncoder)
        self.storage['extrasense_list'] = jsoned_list
        self.storage['my_numbers'] = my_numbers
        self.storage.save()

    def load(self, session_key) -> dict:
        jsoned_list = json.loads(self.storage['extrasense_list'])
        extrasense_list = ExtracenseList()
        for ex_dict in jsoned_list:
            ex = Extrasense(numbers = ex_dict['numbers'], rating = ex_dict['rating'])
            extrasense_list.add_extrasense_to_begin(ex)
        return {
            'extrasense_list' : extrasense_list,
            'my_numbers': self.storage['my_numbers']
            }



class CacheExtrasenseSaver(ExtrasenseSaver):
    """Класс, реализующий сохранение состояния экстрасенсов в cache"""
 
    def __init__(self) -> None:
        self.storage = cache
    
    def save(self, session_key, extrasense_list: ExtracenseList, my_numbers: list) -> None:
        jsoned_list = json.dumps(extrasense_list, cls=ExtrasenseListJsonEncoder)
        self.storage.set(session_key, {
            'jsoned_list': jsoned_list,
            'my_numbers': my_numbers
            })

    def load(self, session_key) -> dict:
        jsoned_list = json.loads(self.storage.get(session_key)['jsoned_list'])
        extrasense_list = ExtracenseList()
        for ex_dict in jsoned_list:
            ex = Extrasense(numbers = ex_dict['numbers'], rating = ex_dict['rating'])
            extrasense_list.add_extrasense_to_begin(ex)
        return {
            'extrasense_list' : extrasense_list,
            'my_numbers': self.storage.get(session_key)['my_numbers']
            }
            
            
def create_extrasense_saver(factory: StorageFactory):
    return factory.create_extrasense_saver()

if STORAGE == 'DjangoSessions':
    store = create_extrasense_saver(DjangoSessionStorageFactory())
elif STORAGE == 'cache':
    store = create_extrasense_saver(CacheStorageFactory())
else:
    raise NotImplementedError('This storage not implemented. Check "STORAGE" in settings')