from dataclasses import dataclass


# Гарантирует наличие поля id у любого класса-наследника
@dataclass
class HasId:
    id: int
