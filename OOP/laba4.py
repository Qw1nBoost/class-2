from typing import Any, List
from abc import ABC, abstractmethod


# Observer - поведенческий паттерн проектирования, который создает механизм подписки, позволяющий одним объектам следить и реагировать на события, происходящие в других объектах.
# Компоненты: Издатель (Subject) - объект, который генерирует события (User, Product)
#             Подписчик (Observer) - объекты, которые хотят получать уведомления (обработчики)
#             Событие - информация о том, что произошло


class EventHandler(ABC): # Интерфейс обработчика события
    @abstractmethod
    def handle(self, sender: Any, args: Any): #handle - метод-обработчик события
        pass                  #sender -  объект, который вызвал событие, args - данные


class Event: # Класс Event — событие. Хранит список подписчиков
    def __init__(self):
        self._handlers: List[EventHandler] = []  # список подписчиков

    def __iadd__(self, handler: EventHandler):
        self._handlers.append(handler)  # подписка
        return self

    def __isub__(self, handler: EventHandler):
        self._handlers.remove(handler)  # отписка
        return self

    def invoke(self, sender: Any, args: Any):
        for handler in self._handlers:  # оповещение всех, каждому подписчику вызываем handle
            handler.handle(sender, args)


class PropertyChangedEventArgs: # Аргументы события после изменения (информирует, какое свойство изменилось)
    def __init__(self, property_name: str):
        self.property_name = property_name


class PropertyChangedHandler(EventHandler): # Обработчик изменений: вывод в консоль
    # Реагирует на уже произошедшие изменения
    # Логирует, обновляет UI, отправляет уведомления
    def handle(self, sender: Any, args: PropertyChangedEventArgs):
        print(f"[CHANGED] {sender}: свойство '{args.property_name}' изменено") #реакция на  событие


class PropertyChangingEventArgs: # Аргументы события до изменения
    def __init__(self, property_name: str, old_value: Any, new_value: Any):
        self.property_name = property_name
        self.old_value = old_value
        self.new_value = new_value
        self.can_change = True  # можно ли менять значение (флаг для контроля разрешения)


class PropertyChangingValidator(EventHandler): # Валидатор с проверками
    # Проверяет корректность новых значений до того, как они будут установлены
    # Устанавливает can_change = False, если данные некорректны
    def handle(self, sender, args):
        # Проверка 1: Возраст не может быть меньше 0
        if args.property_name == "age" and isinstance(args.new_value, int) and args.new_value < 0:
            print(f"[VALIDATION] {sender}: возраст не может быть меньше 0")
            args.can_change = False
            
        # Проверка 2: Цена не может быть меньше 0
        elif args.property_name == "price" and isinstance(args.new_value, (int, float)) and args.new_value < 0:
            print(f"[VALIDATION] {sender}: цена не может быть меньше 0")
            args.can_change = False
            
        # Проверка 3: Имя пользователя не может быть пустым
        elif args.property_name == "name" and isinstance(args.new_value, str) and len(args.new_value.strip()) == 0:
            print(f"[VALIDATION] {sender}: имя не может быть пустым")
            args.can_change = False
            
        # Проверка 4: Количество товара не может быть отрицательным
        elif args.property_name == "quantity" and isinstance(args.new_value, int) and args.new_value < 0:
            print(f"[VALIDATION] {sender}: количество не может быть отрицательным")
            args.can_change = False


class User: # Класс User
    def __init__(self, name: str, age: int, score: int):
        self._name = name
        self._age = age
        self._score = score

        self.property_changing = Event()  # событие до изменения
        self.property_changed = Event()   # событие после изменения

    def __repr__(self):
        return f"User({self._name})"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # событие до изменения
        args = PropertyChangingEventArgs("name", self._name, value)
        self.property_changing.invoke(self, args)

        # если валидатор запретил то выходим
        if not args.can_change:
            return

        # меняем значение
        self._name = value

        # событие после изменения
        self.property_changed.invoke(self, PropertyChangedEventArgs("name"))

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        # событие до изменения
        args = PropertyChangingEventArgs("age", self._age, value)
        self.property_changing.invoke(self, args)

        # если валидатор запретил то выходим
        if not args.can_change:
            return

        # меняем значение
        self._age = value

        # событие после изменения
        self.property_changed.invoke(self, PropertyChangedEventArgs("age"))


class Product: # Класс Product
    def __init__(self, title: str, price: int, quantity: int):
        self._title = title
        self._price = price
        self._quantity = quantity

        self.property_changing = Event()
        self.property_changed = Event()

    def __repr__(self):
        return f"Product({self._title})"

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        args = PropertyChangingEventArgs("price", self._price, value)
        self.property_changing.invoke(self, args)

        if not args.can_change:
            return

        self._price = value
        self.property_changed.invoke(self, PropertyChangedEventArgs("price"))
        
    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        args = PropertyChangingEventArgs("quantity", self._quantity, value)
        self.property_changing.invoke(self, args)

        if not args.can_change:
            return

        self._quantity = value
        self.property_changed.invoke(self, PropertyChangedEventArgs("quantity"))


changed_handler = PropertyChangedHandler()  #создаем обработчики
validator = PropertyChangingValidator()

user = User("Andrey", 20, 100)
product = Product("Computer", 5000, 5)

# подписка на события
user.property_changing += validator
user.property_changed += changed_handler

product.property_changing += validator
product.property_changed += changed_handler

print(" Тестирование User ")
user.age = 41     # разрешено
user.age = -5     # запрещено
user.name = ""    # запрещено (пустое имя)
user.name = "Max" # разрешено

print("\n Тестирование Product ")
product.price = 2500    # разрешено
product.price = -1000   # запрещено
product.quantity = 5   # разрешено
product.quantity = -3  # запрещено (отрицательное количество)