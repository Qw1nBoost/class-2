from abc import ABC, abstractmethod

from log_level import LogLevel


# Интерфейс фильтра: решает, должно ли сообщение пройти дальше
class ILogFilter(ABC):

    @abstractmethod
    def match(self, log_level: LogLevel, text: str) -> bool: ...


# Интерфейс форматтера: преобразует сообщение в готовую к выводу строку
class ILogFormatter(ABC):

    @abstractmethod
    def format(self, log_level: LogLevel, text: str) -> str: ...


# Интерфейс обработчика: доставляет готовое сообщение до назначения
class ILogHandler(ABC):

    @abstractmethod
    def handle(self, log_level: LogLevel, text: str) -> None: ...
