import json
import os
from typing import Generic, Optional, Sequence, TypeVar

from base import HasId
from config import USERS_FILE
from exceptions import DuplicateLoginError, StorageError
from interfaces import IDataRepository, ISerializer, IUserRepository
from user import User
from base import HasId

T = TypeVar("T", bound=HasId)

# Конкретная реализация сериализатора для типа User
class UserSerializer(ISerializer[User]):

    # Преобразует объект User в словарь для записи в JSON.
    # Пустые строки нормализуются в None.
    def to_dict(self, user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "login": user.login,
            "password": user.password,
            "email": user.email or None,
            "address": user.address or None,
        }

    # Восстанавливает объект User из словаря
    def from_dict(self, data: dict) -> User:
        return User(
            id=data["id"],
            name=data["name"],
            login=data["login"],
            password=data["password"],
            email=data.get("email"),
            address=data.get("address"),
        )


# Универсальный репозиторий: хранит данные любого типа T в JSON-файле.
# Конкретный способ сериализации передаётся через ISerializer[T].
class DataRepository(IDataRepository[T], Generic[T]):

    # Принимает сериализатор и путь к файлу; создаёт пустой файл если не существует
    def __init__(self, serializer: ISerializer[T], filepath: str) -> None:
        self._serializer: ISerializer[T] = serializer
        self._filepath: str = filepath
        if not os.path.exists(filepath):
            self._save([])
        self._check_duplicate_ids()

    # Предупреждает о дублирующихся id в файле при инициализации
    def _check_duplicate_ids(self) -> None:
        ids = [item.id for item in self._load()]
        duplicates = {id for id in ids if ids.count(id) > 1}
        if duplicates:
            print(f"[DataRepository] Обнаружены дублирующиеся id: {duplicates}")

    # Возвращает все записи, отсортированные по имени
    def get_all(self) -> Sequence[T]:
        return sorted(self._load())

    # Ищет запись по id; возвращает None если не найдена
    def get_by_id(self, id: int) -> Optional[T]:
        return next((item for item in self._load() if item.id == id), None)

    # Добавляет запись; автоматически назначает id если он некорректен или занят
    def add(self, item: T) -> None:
        items = list(self._load())
        existing_ids = {i.id for i in items}
        if item.id <= 0 or item.id in existing_ids:
            item.id = max(existing_ids, default=0) + 1
        items.append(item)
        self._save(items)

    # Обновляет запись по id; выбрасывает ValueError если не найдена
    def update(self, item: T) -> None:
        items = list(self._load())
        for i, existing in enumerate(items):
            if existing.id == item.id:
                items[i] = item
                self._save(items)
                return
        raise ValueError(f"Запись с id={item.id} не найдена")

    # Удаляет запись по id; выбрасывает ValueError если не найдена
    def delete(self, item: T) -> None:
        items = list(self._load())
        filtered = [i for i in items if i.id != item.id]
        if len(filtered) == len(items):
            raise ValueError(f"Запись с id={item.id} не найдена")
        self._save(filtered)

    # Читает записи из JSON-файла через сериализатор
    def _load(self) -> list[T]:
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                return [self._serializer.from_dict(d) for d in json.load(f)]
        except (json.JSONDecodeError, KeyError, OSError) as e:
            raise StorageError(self._filepath, str(e))

    # Записывает записи атомарно: сначала во временный файл, затем заменяет основной
    def _save(self, items: list[T]) -> None:
        tmp = self._filepath + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump([self._serializer.to_dict(i) for i in items], f, ensure_ascii=False, indent=2)
            os.replace(tmp, self._filepath)
        except OSError as e:
            raise StorageError(self._filepath, str(e))
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)


# Репозиторий пользователей: расширяет DataRepository поиском по логину
class UserRepository(DataRepository[User], IUserRepository):

    # Создаёт репозиторий с UserSerializer и путём к файлу из конфига
    def __init__(self, filepath: str = USERS_FILE) -> None:
        super().__init__(UserSerializer(), filepath)

    # Ищет пользователя по логину; возвращает None если не найден
    def get_by_login(self, login: str) -> Optional[User]:
        return next((u for u in self.get_all() if u.login == login), None)

    # Добавляет пользователя; выбрасывает DuplicateLoginError если логин занят
    def add(self, item: User) -> None:
        if self.get_by_login(item.login):
            raise DuplicateLoginError(item.login)
        super().add(item)
