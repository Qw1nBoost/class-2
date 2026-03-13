from abc import ABC, abstractmethod

# Интерфейс 1
class IInterface1(ABC):

    # Метод действия
    @abstractmethod
    def execute(self) -> str:
        pass

# Интерфейс 2
class IInterface2(ABC):

    # Метод обработки
    @abstractmethod
    def process(self) -> str:
        pass

# Интерфейс 3
class IInterface3(ABC):

    # Метод запуска
    @abstractmethod
    def run(self) -> str:
        pass
