import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from filters import LevelFilter, ReLogFilter, SimpleLogFilter
from formatters import StandardFormatter
from handlers import (
    ConsoleHandler,
    FileHandler,
    SocketHandler,
    SyslogHandler,
    FtpHandler,
)
from log_level import LogLevel
from logger import Logger

SEP: str = "─" * 60
LOG_FILE: str = "app.log"


# Выводит заголовок раздела демонстрации
def section(title: str) -> None:
    print(f"\n{SEP}\n {title}\n{SEP}")


# Базовый логгер без фильтров: все сообщения в консоль и файл
def demo_basic() -> None:
    section("Сценарий 1 - базовый: ConsoleHandler + FileHandler")

    logger = Logger(
        formatters=[StandardFormatter()],
        handlers=[ConsoleHandler(), FileHandler(LOG_FILE)],
    )
    logger.log_info("Приложение запущено")
    logger.log_warn("Память заполнена на 80%")
    logger.log_error("Не удалось подключиться к БД")


# LevelFilter с минимальным уровнем: INFO будет отброшен
def demo_level_filter() -> None:
    section("Сценарий 2 - LevelFilter(WARN): пройдут WARN и ERROR")

    logger = Logger(
        filters=[LevelFilter(LogLevel.WARN)],
        formatters=[StandardFormatter()],
        handlers=[ConsoleHandler()],
    )
    logger.log_info("INFO  → отфильтровано")
    logger.log_warn("WARN  → пройдёт")
    logger.log_error("ERROR → пройдёт")


# SimpleLogFilter: пропускает только сообщения с подстрокой "database"
def demo_simple_filter() -> None:
    section("Сценарий 3 — SimpleLogFilter('database')")

    logger = Logger(
        filters=[SimpleLogFilter("database")],
        formatters=[StandardFormatter()],
        handlers=[ConsoleHandler()],
    )
    logger.log_error("Timeout: database connection refused") # пройдёт
    logger.log_error("Disk I/O error on /var/data") # отфильтруется
    logger.log_warn("database pool exhausted, retrying...") # пройдёт


# ReLogFilter: пропускает только сообщения с числовым кодом ошибки
def demo_regex_filter() -> None:
    section(r"Сценарий 4 - ReLogFilter(r'error\s*\d+')")

    logger = Logger(
        filters=[ReLogFilter(r"error\s*\d+")],
        formatters=[StandardFormatter()],
        handlers=[ConsoleHandler()],
    )
    logger.log_error("error 503: service unavailable")  # пройдёт
    logger.log_error("Connection refused") # отфильтруется
    logger.log_warn("error 42 warnings detected") # пройдёт


# Несколько фильтров с AND-логикой: пройдут только ERROR с подстрокой "auth"
def demo_multi_filter() -> None:
    section("Сценарий 5 - LevelFilter(ERROR) AND SimpleLogFilter('auth')")

    logger = Logger(
        filters=[LevelFilter(LogLevel.ERROR), SimpleLogFilter("auth")],
        formatters=[StandardFormatter()],
        handlers=[ConsoleHandler()],
    )
    logger.log_error("auth: token expired") # пройдёт оба фильтра
    logger.log_warn("auth: rate limit exceeded") # отфильтруется (WARN < ERROR)
    logger.log_error("disk: write failed") # отфильтруется (нет 'auth')


# Graceful degradation: SocketHandler не роняет приложение при недоступном сервере
def demo_resilience() -> None:
    section("Сценарий 6 - SocketHandler: graceful degradation")

    logger = Logger(
        formatters=[StandardFormatter()],
        handlers=[ConsoleHandler(), SocketHandler("127.0.0.1", 9999)],
    )
    logger.log_error("Сообщение при недоступном сокете")


# На Unix пишет в системный syslog, на Windows — корректный fallback в stderr.
def demo_syslog() -> None:
    section("Сценарий 7 - SyslogHandler")

    logger = Logger(
        formatters=[StandardFormatter()],
        handlers=[
            ConsoleHandler(),
            SyslogHandler(),
        ],
    )

    logger.log_info("INFO сообщение для SyslogHandler")
    logger.log_warn("WARN сообщение для SyslogHandler")
    logger.log_error("ERROR сообщение для SyslogHandler")


# Проверяет корректность LevelFilter с разными уровнями
def test_level_filter() -> bool:
    f = LevelFilter(LogLevel.WARN)
    return (
        not f.match(LogLevel.INFO, "test") and
            f.match(LogLevel.WARN, "test") and
            f.match(LogLevel.ERROR, "test")
    )


# Проверяет SimpleLogFilter: находит подстроку без учёта регистра
def test_simple_filter() -> bool:
    f = SimpleLogFilter("secret")
    return (
            f.match(LogLevel.INFO, "SECRET data") and
        not f.match(LogLevel.INFO, "public data")
    )


# Проверяет ReLogFilter: ищет число в тексте через regex
def test_regex_filter() -> bool:
    f = ReLogFilter(r"\d+")
    return (
            f.match(LogLevel.INFO, "error 404") and
        not f.match(LogLevel.INFO, "error text")
    )


# Проверяет StandardFormatter: в выводе присутствуют уровень, год и текст
def test_formatter() -> bool:
    formatted: str = StandardFormatter().format(LogLevel.ERROR, "test")
    return "[ERROR]" in formatted and "test" in formatted and "202" in formatted


# Проверяет, что несколько обработчиков получают одно и то же сообщение
def test_multiple_handlers() -> bool:
    from interfaces import ILogHandler

    received: list[str] = []

    class _Collector(ILogHandler):
        # Тестовый обработчик, собирающий сообщения в список
        def handle(self, log_level: LogLevel, text: str) -> None:
            received.append(text)

    logger = Logger(
        formatters=[StandardFormatter()],
        handlers=[_Collector(), _Collector()],
    )
    logger.log_info("ping")
    return len(received) == 2


def test_syslog_handler() -> bool:
    try:
        logger = Logger(
            formatters=[StandardFormatter()],
            handlers=[SyslogHandler()],
        )
        logger.log_info("Test syslog message")
        return True
    except Exception:
        return False


# Запускает все тесты и выводит итоговый отчёт
def run_tests() -> None:
    section("Автоматизированные тесты")

    tests: dict[str, bool] = {
        "LevelFilter (min_level)":    test_level_filter(),
        "SimpleLogFilter (регистр)":  test_simple_filter(),
        "ReLogFilter (regex)":        test_regex_filter(),
        "StandardFormatter (формат)": test_formatter(),
        "Multiple handlers":          test_multiple_handlers(),
        "SyslogHandler":              test_syslog_handler()
    }

    for name, passed in tests.items():
        status = "ПРОЙДЕН" if passed else "НЕ ПРОЙДЕН"
        print(f"{name}: {status}")

    all_passed: bool = all(tests.values())
    print(f"\nИтог: {'ВСЕ ТЕСТЫ ПРОЙДЕНЫ' if all_passed else 'ЕСТЬ ОШИБКИ'}")


if __name__ == "__main__":
    demo_basic()
    demo_level_filter()
    demo_simple_filter()
    demo_regex_filter()
    demo_multi_filter()
    demo_resilience()
    demo_syslog()
    run_tests()
    

    print(f"\n{SEP}")
    print(f"Лог записан в файл: app_<дата>.log")
    print(SEP + "\n")
