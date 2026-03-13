from di.injector import Injector
from configurations import create_debug_config, create_release_config
from services.interfaces import IInterface1, IInterface2, IInterface3

# Демонстрация работы контейнера
def main() -> None:

    injector_debug = Injector()
    create_debug_config(injector_debug)

    print("DEBUG")

    with injector_debug.scope():
        s3a = injector_debug.get_instance(IInterface3)
        s3b = injector_debug.get_instance(IInterface3)
        print(s3a.run())
        print("Scoped одинаковые:", s3a is s3b)

    injector_release = Injector()
    create_release_config(injector_release)

    print("RELEASE")

    r1 = injector_release.get_instance(IInterface3)
    r2 = injector_release.get_instance(IInterface3)

    print(r1.run())
    print("PerRequest разные:", r1 is r2)

if __name__ == "__main__":
    main()
