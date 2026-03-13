import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from auth_service import AuthService
from config import SESSION_FILE, USERS_FILE
from exceptions import DuplicateLoginError, InvalidCredentialsError, UserNotFoundError
from repository import UserRepository
from user import User
from validators import PasswordHasher

SEP: str = "─" * 60


def section(title: str) -> None:
    print(f"\n{SEP}\n  {title}\n{SEP}")


def cleanup() -> None:
    for path in (USERS_FILE, SESSION_FILE):
        if os.path.exists(path):
            os.remove(path)


# 1. Добавляет тестовых пользователей; показывает обработку дубликата логина
def demo_add_users(repo: UserRepository) -> None:
    section("1. Добавление пользователей")

    users = [
        User(id=1, name="Мария Сидорова", login="maria", password=PasswordHasher.hash("qwerty"),
             email="maria@mail.com"),
        User(id=2, name="Иван Петров", login="ivan", password=PasswordHasher.hash("12345"),
             email="ivan@mail.com", address="Москва, ул. Ленина, 1"),
        User(id=3, name="Алексей Иванов", login="alex", password=PasswordHasher.hash("password123")),
    ]

    for user in users:
        repo.add(user)
        print(f"Добавлен: {user.name}")

    print(f"\nВсего пользователей: {len(repo.get_all())}")
    print(f"Отсортированы по имени: {[u.name for u in repo.get_all()]}")

    print("\nПопытка добавить пользователя с занятым логином:")
    try:
        repo.add(User(id=99, name="Другой Иван", login="ivan", password="pass"))
    except DuplicateLoginError as e:
        print(f"[DuplicateLoginError] {e}")


# 2. Изменяет email и адрес существующего пользователя
def demo_update_user(repo: UserRepository) -> None:
    section("2. Редактирование пользователя")

    ivan = repo.get_by_login("ivan")
    print(f"До: {ivan}")
    ivan.email = "ivan.new@company.ru"
    ivan.address = "Санкт-Петербург, Невский пр., 10"
    repo.update(ivan)
    print(f"После: {repo.get_by_login('ivan')}")


# 3. Показывает успешный вход и оба вида ошибок авторизации
def demo_sign_in(auth: AuthService) -> None:
    section("3. Авторизация пользователя")

    print("Несуществующий пользователь:")
    try:
        auth.sign_in("unknown", "pass")
    except UserNotFoundError as e:
        print(f"[UserNotFoundError] {e}")

    print("\nНеверный пароль:")
    try:
        auth.sign_in("ivan", "wrong")
    except InvalidCredentialsError as e:
        print(f"[InvalidCredentialsError] {e}")

    print("\nУспешный вход:")
    auth.sign_in("ivan", "12345")
    print(f"Авторизован: {auth.is_authorized}")
    print(f"Текущий пользователь: {auth.current_user}")


# 4. Выходит из текущего аккаунта и входит под другим пользователем
def demo_switch_user(auth: AuthService) -> None:
    section("4. Смена пользователя")

    print(f"Текущий: {auth.current_user.login}")
    auth.sign_out()
    print(f"Авторизован после выхода: {auth.is_authorized}")

    auth.sign_in("maria", "qwerty")
    print(f"Новый текущий: {auth.current_user.login}")


# 5. Демонстрирует три сценария автовхода
def demo_auto_login(repo: UserRepository) -> None:
    section("5. Автоматическая авторизация при повторном запуске")

    print("[Запуск 1] Пользователь авторизован, программа завершается...")
    print(f"Сессия сохранена в файле: {SESSION_FILE}")

    print("\n[Запуск 2] Создаём новый AuthService (симуляция перезапуска)...")
    auth2 = AuthService(repo)
    print(f"Авторизован автоматически: {auth2.is_authorized}")
    if auth2.current_user:
        print(f"Восстановлен пользователь: {auth2.current_user.name}")

    auth2.sign_out()

    print("\n[Запуск 3] После выхода - создаём новый AuthService...")
    auth3 = AuthService(repo)
    print(f"Авторизован автоматически: {auth3.is_authorized}")
    if not auth3.current_user:
        print("Сессия не найдена - вход не выполнен")


if __name__ == "__main__":
    cleanup()

    repo = UserRepository()
    auth = AuthService(repo)

    demo_add_users(repo)
    demo_update_user(repo)
    demo_sign_in(auth)
    demo_switch_user(auth)
    demo_auto_login(repo)

    print(f"\n{SEP}")
    print(f"Данные сохранены в: {USERS_FILE}")
    print(f"Конфигурация: config.json")
    print(SEP + "\n")
