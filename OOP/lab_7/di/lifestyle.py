from enum import Enum

# Перечисление режимов жизненного цикла объектов
class LifeStyle(Enum):
    PER_REQUEST = "PerRequest"  # Новый объект при каждом запросе
    SCOPED = "Scoped"           # Один объект в пределах блока with
    SINGLETON = "Singleton"      # Один объект на всё приложение
