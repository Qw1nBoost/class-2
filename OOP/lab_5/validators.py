import hashlib
import re


# Проверяет корректность email по стандартному шаблону
class EmailValidator:

    __PATTERN: re.Pattern[str] = re.compile(
        r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    )

    # Возвращает True, если строка является валидным email
    @classmethod
    def is_valid(cls, email: str) -> bool:
        return bool(cls.__PATTERN.match(email))

    # Выбрасывает ValueError, если email некорректен
    @classmethod
    def validate(cls, email: str) -> None:
        if email and not cls.is_valid(email):
            raise ValueError(f"Некорректный email: '{email}'")


# Хеширует пароли через SHA-256; сравнивает пароль с хешем
class PasswordHasher:

    # Возвращает SHA-256 хеш строки
    @staticmethod
    def hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # Возвращает True если пароль совпадает с хешем
    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return PasswordHasher.hash(password) == hashed


# Проверяет корректность логина: длина и уникальность среди существующих
class LoginValidator:

    MIN_LENGTH: int = 3

    # Возвращает True и пустую строку если логин корректен, иначе False и причину
    @classmethod
    def validate(cls, login: str, existing_logins: list[str]) -> tuple[bool, str]:
        if not login:
            return False, "Логин не может быть пустым"
        if len(login) < cls.MIN_LENGTH:
            return False, f"Логин должен быть не менее {cls.MIN_LENGTH} символов"
        if login in existing_logins:
            return False, "Логин уже занят"
        return True, ""
