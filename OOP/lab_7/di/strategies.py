from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional

# Абстрактная стратегия получения экземпляра
class InstanceStrategy(ABC):

    # Получить экземпляр согласно стратегии
    @abstractmethod
    def get_instance(self, factory: Callable[[], Any]) -> Any:
        pass

# Стратегия: новый объект при каждом запросе
class PerRequestStrategy(InstanceStrategy):

    # Всегда создаёт новый экземпляр
    def get_instance(self, factory: Callable[[], Any]) -> Any:
        return factory()

# Стратегия: один объект на всё время жизни контейнера
class SingletonStrategy(InstanceStrategy):

    # Инициализация кэша singleton
    def __init__(self) -> None:
        self._instance: Optional[Any] = None

    # Возвращает один и тот же экземпляр
    def get_instance(self, factory: Callable[[], Any]) -> Any:
        if self._instance is None:
            self._instance = factory()
        return self._instance

# Стратегия: один объект внутри активного scope
class ScopedStrategy(InstanceStrategy):

    # Инициализация словаря scoped-объектов
    def __init__(self) -> None:
        self._scoped_instances: Optional[Dict[int, Any]] = None

    # Открытие области видимости
    @contextmanager
    def scope(self):
        previous = self._scoped_instances
        self._scoped_instances = {}
        try:
            yield
        finally:
            self._scoped_instances = previous

    # Возвращает один объект в пределах scope
    def get_instance(self, factory: Callable[[], Any]) -> Any:
        if self._scoped_instances is None:
            raise RuntimeError("Нет активного scope. Используйте with injector.scope():")
        key = id(factory)
        if key not in self._scoped_instances:
            self._scoped_instances[key] = factory()
        return self._scoped_instances[key]
