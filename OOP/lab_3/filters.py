import re
from interfaces import ILogFilter
from log_level import LogLevel


# Пропускает сообщения, содержащие заданную подстроку (без учёта регистра)
class SimpleLogFilter(ILogFilter):

    # Переводит паттерн в нижний регистр для регистронезависимого сравнения
    def __init__(self, pattern: str) -> None:
        self.__pattern: str = pattern.lower()

    # Возвращает True, если паттерн найден в тексте сообщения
    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.__pattern in text.lower()

    def __repr__(self) -> str:
        return f"SimpleLogFilter(pattern={self.__pattern!r})"


# Пропускает сообщения, соответствующие регулярному выражению (r'\d+' найдет любое сообщение с цифрами)
class ReLogFilter(ILogFilter):

    # Компилирует регулярное выражение; выбрасывает ValueError при некорректном паттерне
    def __init__(self, pattern: str) -> None:
        try:
            self.__regex: re.Pattern[str] = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Некорректное регулярное выражение '{pattern}': {e}") from e

    # Возвращает True, если регулярное выражение нашло совпадение в тексте
    def match(self, log_level: LogLevel, text: str) -> bool:
        return bool(self.__regex.search(text))

    def __repr__(self) -> str:
        return f"ReLogFilter(pattern={self.__regex.pattern!r})"


# Пропускает сообщения с уровнем НЕ ниже указанного минимума
class LevelFilter(ILogFilter):

    # Сохраняет минимальный допустимый уровень логирования
    def __init__(self, min_level: LogLevel) -> None:
        self.__min_level: LogLevel = min_level

    # Сравнивает числовые значения уровней для определения допустимости
    def match(self, log_level: LogLevel, text: str) -> bool:
        return log_level.value >= self.__min_level.value

    def __repr__(self) -> str:
        return f"LevelFilter(min_level={self.__min_level})"
