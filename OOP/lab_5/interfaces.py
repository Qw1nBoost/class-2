from abc import ABC, abstractmethod
from typing import Generic, Optional, Sequence, TypeVar

from base import HasId
from user import User

T = TypeVar("T", bound=HasId)


# Интерфейс сериализации: преобразует объект типа T в словарь и обратно
class ISerializer(ABC, Generic[T]):

    # Преобразует объект в словарь для записи в JSON
    @abstractmethod
    def to_dict(self, item: T) -> dict:
        pass

    # Восстанавливает объект из словаря
    @abstractmethod
    def from_dict(self, data: dict) -> T:
        pass


# Универсальный CRUD-интерфейс
class IDataRepository(ABC, Generic[T]):

    # Возвращает все записи из хранилища
    @abstractmethod
    def get_all(self) -> Sequence[T]:
        pass

    # Возвращает запись по идентификатору или None, если не найдена
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    # Добавляет новую запись и автоматически назначает id если он некорректен
    @abstractmethod
    def add(self, item: T) -> None:
        pass

    # Обновляет существующую запись по id
    @abstractmethod
    def update(self, item: T) -> None:
        pass

    # Удаляет запись; выбрасывает ValueError если не найдена
    @abstractmethod
    def delete(self, item: T) -> None:
        pass


# Репозиторий пользователей с дополнительным поиском по логину
class IUserRepository(IDataRepository[User]):

    # Возвращает пользователя по логину или None, если не найден
    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]:
        pass


# Сервис авторизации: вход по логину и паролю, выход, текущий пользователь
class IAuthService(ABC):

    # Проверяет логин и пароль; возвращает True при успехе
    @abstractmethod
    def sign_in(self, login: str, password: str) -> bool:
        pass

    # Завершает текущую сессию
    @abstractmethod
    def sign_out(self) -> None:
        pass

    # Возвращает True, если пользователь авторизован
    @property
    @abstractmethod
    def is_authorized(self) -> bool:
        pass

    # Возвращает текущего авторизованного пользователя или None
    @property
    @abstractmethod
    def current_user(self) -> Optional[User]:
        pass
