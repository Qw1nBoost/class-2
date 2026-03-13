from dataclasses import dataclass, field
from typing import Optional

from base import HasId
from validators import EmailValidator
from base import HasId


@dataclass(order=True)
class User(HasId):
    name: str
    ...

# Модель пользователя: order=True включает сортировку по полям с compare=True
@dataclass(order=True)
class User(HasId):
    id: int = field(compare=False)
    name: str = field(compare=True)
    login: str = field(compare=False)
    password: str = field(compare=False, repr=False)
    email: Optional[str] = field(default=None, compare=False)
    address: Optional[str] = field(default=None, compare=False)

    # Валидирует email при создании объекта
    def __post_init__(self) -> None:
        if self.email:
            EmailValidator.validate(self.email)

    # Выводит все поля кроме password
    def __str__(self) -> str:
        email_str = f", email='{self.email}'" if self.email else ""
        address_str = f", address='{self.address}'" if self.address else ""
        return f"User(id={self.id}, name='{self.name}', login='{self.login}'{email_str}{address_str})"
