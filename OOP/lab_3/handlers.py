
import ftplib
import io
import platform
import socket
import sys
from datetime import datetime
from interfaces import ILogHandler
from log_level import LogLevel
if platform.system() != "Windows":
    import syslog

from constants import (
    CONSOLE_COLOR_ERROR,
    CONSOLE_COLOR_INFO,
    CONSOLE_COLOR_RESET,
    CONSOLE_COLOR_WARN,
    DATE_FORMAT,
    ENCODING,
    FTP_APPEND_COMMAND,
    FTP_DEFAULT_PORT,
    FTP_TIMEOUT,
    SOCKET_TIMEOUT,
)


# Выводит сообщение в консоль с цветовой подсветкой по уровню
class ConsoleHandler(ILogHandler):

    __COLORS: dict[LogLevel, str] = {
        LogLevel.INFO: CONSOLE_COLOR_INFO,
        LogLevel.WARN: CONSOLE_COLOR_WARN,
        LogLevel.ERROR: CONSOLE_COLOR_ERROR,
    }

    # Печатает текст в консоль с цветом, соответствующим уровню лога
    def handle(self, log_level: LogLevel, text: str) -> None:
        color: str = self.__COLORS.get(log_level, "")
        print(f"{color}{text}{CONSOLE_COLOR_RESET}")


# Дозаписывает сообщение в файл с датой в имени
class FileHandler(ILogHandler):

    # Подставляет текущую дату в имя файла и проверяет доступность для записи
    def __init__(self, filepath: str) -> None:
        self.__base: str = filepath
        self.__filepath: str | None = None
        self.__open(filepath)

    # Формирует путь с датой и открывает файл
    def __open(self, filepath: str) -> None:
        date: str = datetime.now().strftime(DATE_FORMAT)
        name, _, ext = filepath.rpartition(".")
        dated: str = f"{name}_{date}.{ext}" if name else f"{filepath}_{date}"
        try:
            with open(dated, "a", encoding=ENCODING):
                pass
            self.__filepath = dated
        except PermissionError as e:
            print(f"[FileHandler] Нет доступа к файлу '{dated}': {e}")
        except OSError as e:
            print(f"[FileHandler] Ошибка файловой системы '{dated}': {e}")

    # Переоткрывает файл если наступил новый день, затем дозаписывает сообщение
    def handle(self, log_level: LogLevel, text: str) -> None:
        date: str = datetime.now().strftime(DATE_FORMAT)
        if self.__filepath and date not in self.__filepath:
            self.__open(self.__base)
        if self.__filepath is None:
            return
        try:
            with open(self.__filepath, "a", encoding=ENCODING) as fh:
                fh.write(text + "\n")
        except OSError as e:
            print(f"[FileHandler] Ошибка записи: {e}")

    def __repr__(self) -> str:
        return f"FileHandler(base={self.__base!r})"


# Отправляет сообщение на TCP-сервер; при недоступности выводит предупреждение
class SocketHandler(ILogHandler):

    # Сохраняет адрес TCP-сервера для последующих подключений
    def __init__(self, host: str, port: int) -> None:
        self.__host: str = host
        self.__port: int = port

    # Открывает соединение, отправляет сообщение и закрывает сокет
    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with socket.create_connection((self.__host, self.__port), timeout=SOCKET_TIMEOUT) as sock:
                sock.sendall((text + "\n").encode(ENCODING))
        except OSError as e:
            print(f"[SocketHandler] Не удалось отправить лог: {e}")

    def __repr__(self) -> str:
        return f"SocketHandler(host={self.__host!r}, port={self.__port})"


# Записывает сообщение в системный журнал (syslog на Unix, stderr на Windows)
class SyslogHandler(ILogHandler):

    # Пишет в syslog на Unix или в stderr на Windows
    def handle(self, log_level: LogLevel, text: str) -> None:
        if platform.system() == "Windows":
            return

        priority_map: dict[LogLevel, int] = {
            LogLevel.INFO: syslog.LOG_INFO,
            LogLevel.WARN: syslog.LOG_WARNING,
            LogLevel.ERROR: syslog.LOG_ERR,
        }
        try:
            syslog.syslog(priority_map.get(log_level, syslog.LOG_INFO), text)
        except OSError as e:
            print(f"[SyslogHandler] Не удалось записать в syslog: {e}")


# Дозаписывает сообщение в файл на FTP-сервере командой APPE
class FtpHandler(ILogHandler):

    # Сохраняет параметры подключения к FTP-серверу
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        remote_path: str,
        port: int = FTP_DEFAULT_PORT,
    ) -> None:
        self.__host: str = host
        self.__username: str = username
        self.__password: str = password
        self.__remote_path: str = remote_path
        self.__port: int = port

    # Подключается к FTP и дозаписывает сообщение в удалённый файл
    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with ftplib.FTP() as ftp:
                ftp.connect(self.__host, self.__port, timeout=FTP_TIMEOUT)
                ftp.login(self.__username, self.__password)
                payload = io.BytesIO((text + "\n").encode(ENCODING))
                ftp.storbinary(f"{FTP_APPEND_COMMAND} {self.__remote_path}", payload)
        except ftplib.all_errors as e:
            print(f"[FtpHandler] Не удалось отправить лог на FTP: {e}")

    def __repr__(self) -> str:
        return f"FtpHandler(host={self.__host!r}, remote_path={self.__remote_path!r})"
