from dataclasses import dataclass, field
from typing import Optional
import pickle

@dataclass
class User:
    """Класс пользователя"""
    id: int
    name: str
    login: str
    password: str
    email: Optional[str] = None
    address: Optional[str] = None
    
    def __repr__(self):
        """Строковое представление без пароля"""
        return f"User(id={self.id}, name='{self.name}', login='{self.login}', email={self.email})"
    
    def __str__(self):
        return self.__repr__()
    
    def __lt__(self, other):
        """Для сортировки по имени"""
        return self.name < other.name

# Класс для сортируемой коллекции пользователей
class UserCollection(list):
    """Коллекция пользователей с возможностью сортировки по имени"""
    def sort_by_name(self):
        """Сортировка пользователей по имени"""
        self.sort(key=lambda user: user.name)
        return self

