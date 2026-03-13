import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from auth_service import AuthService
from exceptions import DuplicateLoginError, InvalidCredentialsError, UserNotFoundError
from repository import UserRepository
from user import User
from validators import EmailValidator, LoginValidator, PasswordHasher

SEP: str = "─" * 60


def test_email_validator() -> bool:
    return (
            EmailValidator.is_valid("user@example.com") and
            EmailValidator.is_valid("name+tag@domain.co") and
        not EmailValidator.is_valid("not-an-email") and
        not EmailValidator.is_valid("@domain.com")
    )


def test_login_validator() -> bool:
    ok, _ = LoginValidator.validate("alice", [])
    short, _ = LoginValidator.validate("ab", [])
    taken, _ = LoginValidator.validate("alice", ["alice"])
    return ok and not short and not taken


def test_password_hidden() -> bool:
    user = User(id=1, name="Test", login="test", password="supersecret")
    return "supersecret" not in repr(user) and user.password == "supersecret"


def test_sorting() -> bool:
    users = [
        User(id=3, name="Яков", login="y", password="p"),
        User(id=1, name="Анна", login="a", password="p"),
        User(id=2, name="Михаил", login="m", password="p"),
    ]
    return [u.name for u in sorted(users)] == ["Анна", "Михаил", "Яков"]


def test_repository() -> bool:
    test_file = "_test_repo.json"
    try:
        repo = UserRepository(test_file)
        user = User(id=1, name="Test", login="testuser", password="pass")
        repo.add(user)

        if not repo.get_by_id(1) or not repo.get_by_login("testuser"):
            return False

        user.name = "Updated"
        repo.update(user)
        if repo.get_by_id(1).name != "Updated":
            return False

        repo.delete(user)
        return repo.get_by_id(1) is None
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


# Проверяет что DuplicateLoginError бросается при дублировании логина
def test_duplicate_login() -> bool:
    test_file = "_test_dup.json"
    try:
        repo = UserRepository(test_file)
        repo.add(User(id=1, name="Alice", login="alice", password="pass"))
        try:
            repo.add(User(id=2, name="Alice2", login="alice", password="pass2"))
            return False
        except DuplicateLoginError:
            return True
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


# Проверяет успешный вход, UserNotFoundError, InvalidCredentialsError и выход
def test_auth_service() -> bool:
    test_repo_file = "_test_auth_repo.json"
    test_session_file = "_test_auth_session.json"
    try:
        repo = UserRepository(test_repo_file)
        repo.add(User(id=1, name="Alice", login="alice", password=PasswordHasher.hash("pass123")))
        auth = AuthService(repo, test_session_file)

        if not auth.sign_in("alice", "pass123"):
            return False
        if not auth.is_authorized:
            return False

        try:
            auth.sign_in("unknown", "pass")
            return False
        except UserNotFoundError:
            pass

        try:
            auth.sign_in("alice", "wrong")
            return False
        except InvalidCredentialsError:
            pass

        auth.sign_out()
        return not auth.is_authorized
    finally:
        for f in (test_repo_file, test_session_file):
            if os.path.exists(f):
                os.remove(f)


if __name__ == "__main__":
    print(f"\n{SEP}\n  Автоматизированные тесты\n{SEP}")

    tests: dict[str, bool] = {
        "EmailValidator": test_email_validator(),
        "LoginValidator": test_login_validator(),
        "Password скрыт": test_password_hidden(),
        "Сортировка по имени": test_sorting(),
        "CRUD репозитория": test_repository(),
        "Дубликат логина": test_duplicate_login(),
        "AuthService": test_auth_service(),
    }

    for name, passed in tests.items():
        status = "ПРОЙДЕН" if passed else "НЕ ПРОЙДЕН"
        print(f"  {name}: {status}")

    all_passed = all(tests.values())
    print(f"\n  Итог: {'ВСЕ ТЕСТЫ ПРОЙДЕНЫ' if all_passed else 'ЕСТЬ ОШИБКИ'}")
    print(SEP + "\n")
