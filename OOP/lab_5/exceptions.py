# Пользователь не найден в репозитории
class UserNotFoundError(Exception):
    def __init__(self, identifier: str) -> None:
        super().__init__(f"Пользователь '{identifier}' не найден")


# Неверный пароль при попытке входа
class InvalidCredentialsError(Exception):
    def __init__(self) -> None:
        super().__init__("Неверный пароль")


# Попытка добавить пользователя с уже занятым логином
class DuplicateLoginError(Exception):
    def __init__(self, login: str) -> None:
        super().__init__(f"Логин '{login}' уже занят")


# Ошибка чтения или записи файла хранилища
class StorageError(Exception):
    def __init__(self, path: str, reason: str) -> None:
        super().__init__(f"Ошибка хранилища '{path}': {reason}")
