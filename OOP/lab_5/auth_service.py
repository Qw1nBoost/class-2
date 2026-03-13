import json
import os
from contextlib import suppress
from typing import Optional

from config import SESSION_FILE
from exceptions import InvalidCredentialsError, UserNotFoundError
from interfaces import IAuthService, IUserRepository
from user import User
from validators import PasswordHasher


# Хранит сессию в JSON-файле; при старте автоматически восстанавливает пользователя
class AuthService(IAuthService):

    # Загружает сохранённую сессию из файла при инициализации
    def __init__(self, repository: IUserRepository, session_file: str = SESSION_FILE) -> None:
        self.__repository: IUserRepository = repository
        self.__session_file: str = session_file
        self.__current_user: Optional[User] = None
        self.__load_session()

    # Проверяет логин и пароль; выбрасывает исключение при ошибке
    def sign_in(self, login: str, password: str) -> bool:
        user = self.__repository.get_by_login(login)
        if not user:
            raise UserNotFoundError(login)
        if not PasswordHasher.verify(password, user.password):
            raise InvalidCredentialsError()
        self.__current_user = user
        self.__save_session()
        print(f"Добро пожаловать, {user.name}!")
        return True

    # Завершает сессию текущего пользователя и удаляет файл сессии
    def sign_out(self) -> None:
        if self.__current_user:
            print(f"До свидания, {self.__current_user.name}!")
        self.__current_user = None
        self.__clear_session()

    # Возвращает True, если текущий пользователь установлен
    @property
    def is_authorized(self) -> bool:
        return self.__current_user is not None

    # Возвращает текущего авторизованного пользователя
    @property
    def current_user(self) -> Optional[User]:
        return self.__current_user

    # Сохраняет id текущего пользователя в файл сессии
    def __save_session(self) -> None:
        try:
            with open(self.__session_file, "w", encoding="utf-8") as f:
                json.dump({"user_id": self.__current_user.id}, f)
        except OSError as e:
            print(f"[AuthService] Ошибка сохранения сессии: {e}")

    # Читает файл сессии и восстанавливает пользователя из репозитория
    def __load_session(self) -> None:
        if not os.path.exists(self.__session_file):
            return
        try:
            with open(self.__session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            user = self.__repository.get_by_id(data["user_id"])
            if user:
                self.__current_user = user
                print(f"Автоматический вход: {user.name}")
        except (json.JSONDecodeError, KeyError, OSError) as e:
            print(f"[AuthService] Ошибка загрузки сессии: {e}")

    # Удаляет файл сессии при выходе
    def __clear_session(self) -> None:
        with suppress(FileNotFoundError):
            os.remove(self.__session_file)
