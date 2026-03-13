import inspect
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional, Type

from .lifestyle import LifeStyle
from .registration import Registration
from .strategies import PerRequestStrategy, ScopedStrategy, SingletonStrategy

# Контейнер зависимостей
class Injector:

    # Инициализация контейнера
    def __init__(self) -> None:
        self._registrations: Dict[Type, Registration] = {}
        self._singleton_strategies: Dict[Type, SingletonStrategy] = {}
        self._scoped_strategy = ScopedStrategy()

    # Регистрация зависимости интерфейс -> реализация или фабрика
    def register(
        self,
        interface_type: Type,
        class_type: Optional[Type] = None,
        life_style: LifeStyle = LifeStyle.PER_REQUEST,
        params: Optional[Dict[str, Any]] = None,
        fabric_method: Optional[Callable[[], Any]] = None,
    ) -> None:
        self._registrations[interface_type] = Registration(
            life_style, class_type, params, fabric_method
        )
        if life_style == LifeStyle.SINGLETON:
            self._singleton_strategies[interface_type] = SingletonStrategy()

    # Открытие scope для Scoped зависимостей
    @contextmanager
    def scope(self):
        with self._scoped_strategy.scope():
            yield

    # Получение экземпляра по интерфейсу
    def get_instance(self, interface_type: Type) -> Any:
        if interface_type not in self._registrations:
            raise ValueError(f"{interface_type.__name__} не зарегистрирован")
        reg = self._registrations[interface_type]
        factory = self._build_factory(reg)
        strategy = self._resolve_strategy(interface_type, reg.life_style)
        return strategy.get_instance(factory)

    # Выбор стратегии по типу жизненного цикла
    def _resolve_strategy(self, interface_type: Type, life_style: LifeStyle):
        if life_style == LifeStyle.SINGLETON:
            return self._singleton_strategies[interface_type]
        if life_style == LifeStyle.SCOPED:
            return self._scoped_strategy
        return PerRequestStrategy()

    # Создание фабрики создания объекта
    def _build_factory(self, reg: Registration):
        if reg.fabric_method is not None:
            return reg.fabric_method

        def factory():
            return self._create_instance(reg)

        return factory

    # Создание экземпляра класса с автоподстановкой зависимостей
    def _create_instance(self, reg: Registration):
        cls = reg.class_type
        explicit_params = reg.params.copy()
        constructor_args: Dict[str, Any] = {}

        hints = inspect.get_annotations(cls.__init__)
        hints.pop("return", None)

        for name, type_ in hints.items():
            if type_ in self._registrations:
                constructor_args[name] = self.get_instance(type_)
            elif name in explicit_params:
                constructor_args[name] = explicit_params[name]

        for key, value in explicit_params.items():
            if key not in constructor_args:
                constructor_args[key] = value

        return cls(**constructor_args)
