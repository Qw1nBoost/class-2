from di.injector import Injector
from di.lifestyle import LifeStyle
from services.interfaces import IInterface1, IInterface2, IInterface3
from services.implementations import (
    Class1Debug,
    Class1Release,
    Class2Debug,
    Class2Release,
    Class3Debug,
    Class3Release,
)

# Debug конфигурация регистраций
def create_debug_config(injector: Injector) -> None:
    injector.register(IInterface1, Class1Debug, LifeStyle.SINGLETON)
    injector.register(IInterface2, Class2Debug, LifeStyle.PER_REQUEST)
    injector.register(IInterface3, Class3Debug, LifeStyle.SCOPED)

# Release конфигурация регистраций
def create_release_config(injector: Injector) -> None:
    injector.register(IInterface1, Class1Release, LifeStyle.SINGLETON)
    injector.register(IInterface2, Class2Release, LifeStyle.SINGLETON)

    # Фабрика создания IInterface3
    def factory():
        s1 = injector.get_instance(IInterface1)
        s2 = injector.get_instance(IInterface2)
        return Class3Release(s1, s2)

    injector.register(IInterface3, fabric_method=factory, life_style=LifeStyle.PER_REQUEST)
