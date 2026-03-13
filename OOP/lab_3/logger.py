from interfaces import ILogFilter, ILogFormatter, ILogHandler
from log_level import LogLevel


class Logger:

    # Сохраняет списки фильтров, форматтеров и обработчиков
    def __init__(
        self,
        filters: list[ILogFilter] | None = None,
        formatters: list[ILogFormatter] | None = None,
        handlers: list[ILogHandler] | None = None,
    ) -> None:
        self.__filters: list[ILogFilter] = list(filters or [])
        self.__formatters: list[ILogFormatter] = list(formatters or [])
        self.__handlers: list[ILogHandler] = list(handlers or [])

    # Прогоняет сообщение через фильтры, форматтеры и передаёт обработчикам
    def log(self, log_level: LogLevel, text: str) -> None:
        if not self.__passes_filters(log_level, text):
            return
        formatted: str = self.__apply_formatters(log_level, text)
        self.__dispatch(log_level, formatted)

    # Записывает сообщение с уровнем INFO
    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)

    # Записывает сообщение с уровнем WARN
    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)

    # Записывает сообщение с уровнем ERROR
    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)

    # Возвращает True, если сообщение прошло все фильтры
    def __passes_filters(self, log_level: LogLevel, text: str) -> bool:
        return all(f.match(log_level, text) for f in self.__filters)

    # Последовательно применяет каждый форматтер к результату предыдущего
    def __apply_formatters(self, log_level: LogLevel, text: str) -> str:
        result: str = text
        for formatter in self.__formatters:
            result = formatter.format(log_level, result)
        return result

    # Передаёт готовое сообщение каждому обработчику
    def __dispatch(self, log_level: LogLevel, text: str) -> None:
        for handler in self.__handlers:
            handler.handle(log_level, text)
