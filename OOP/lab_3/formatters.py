from datetime import datetime

from constants import DATETIME_FORMAT, LOG_MESSAGE_TEMPLATE
from interfaces import ILogFormatter
from log_level import LogLevel


# Форматирует сообщение по шаблону: [LEVEL] [yyyy.MM.dd hh:mm:ss] text
class StandardFormatter(ILogFormatter):

    # Принимает опциональный формат времени; по умолчанию берёт из constants
    def __init__(self, time_format: str = DATETIME_FORMAT) -> None:
        self.__time_format: str = time_format

    # Подставляет уровень, текущее время и текст в шаблон сообщения
    def format(self, log_level: LogLevel, text: str) -> str:
        timestamp: str = datetime.now().strftime(self.__time_format)
        return LOG_MESSAGE_TEMPLATE.format(
            level=log_level.name,
            timestamp=timestamp,
            text=text,
        )
