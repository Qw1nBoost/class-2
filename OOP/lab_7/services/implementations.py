from services.interfaces import IInterface1, IInterface2, IInterface3

# Debug реализация интерфейса 1
class Class1Debug(IInterface1):

    # Выполнение действия
    def execute(self) -> str:
        return "Debug1"

# Release реализация интерфейса 1
class Class1Release(IInterface1):

    # Выполнение действия
    def execute(self) -> str:
        return "Release1"

# Debug реализация интерфейса 2
class Class2Debug(IInterface2):

    # Конструктор с зависимостью от IInterface1
    def __init__(self, service1: IInterface1) -> None:
        self._service1 = service1

    # Выполнение обработки
    def process(self) -> str:
        return f"Debug2: {self._service1.execute()}"

# Release реализация интерфейса 2
class Class2Release(IInterface2):

    # Конструктор с зависимостью от IInterface1
    def __init__(self, service1: IInterface1) -> None:
        self._service1 = service1

    # Выполнение обработки
    def process(self) -> str:
        return f"Release2: {self._service1.execute()}"

# Debug реализация интерфейса 3
class Class3Debug(IInterface3):

    # Конструктор с зависимостями
    def __init__(self, service1: IInterface1, service2: IInterface2) -> None:
        self._service1 = service1
        self._service2 = service2

    # Запуск сервиса
    def run(self) -> str:
        return f"Debug3: {self._service1.execute()} -> {self._service2.process()}"

# Release реализация интерфейса 3
class Class3Release(IInterface3):

    # Конструктор с зависимостями
    def __init__(self, service1: IInterface1, service2: IInterface2) -> None:
        self._service1 = service1
        self._service2 = service2

    # Запуск сервиса
    def run(self) -> str:
        return f"Release3: {self._service1.execute()} | {self._service2.process()}"
