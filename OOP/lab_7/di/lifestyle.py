from enum import Enum

# Перечисление режимов жизненного цикла объектов
class LifeStyle(Enum):
    PER_REQUEST = "PerRequest"
    SCOPED = "Scoped"
    SINGLETON = "Singleton"
