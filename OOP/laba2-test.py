from typing import Dict, List, Optional, ClassVar

class BankAccount:
    # Переменная класса
    bank_name: ClassVar[str] = "Национальный Банк"
    interest_rate: ClassVar[float] = 0.03  # 3% годовых
    total_accounts: ClassVar[int] = 0

    def __init__(self, owner: str, balance: int = 0):
        # Переменные экземпляра
        self.owner = owner
        self.balance = balance
        self.account_number = BankAccount.total_accounts + 1
        BankAccount.total_accounts += 1
        print(f"Счет #{self.account_number} для {self.owner} создан.")

    # Метод экземпляра
    def deposit(self, amount: int):
        if self._validate_amount(amount):  # Вызов статического метода
            self.balance += amount
            print(f"Депозит {amount}. Баланс: {self.balance}")
        else:
            print("Неверная сумма")

    # Метод экземпляра
    def withdraw(self, amount: int):
        if self._validate_amount(amount) and self.balance >= amount:
            self.balance -= amount
            print(f"Снято {amount}. Баланс: {self.balance}")
        else:
            print("Недостаточно средств или неверная сумма")

    # Статический метод (вспомогательный)
    @staticmethod
    def _validate_amount(amount: int):
        return amount > 0

    # Метод класса (работает со всеми счетами)
    @classmethod
    def change_interest_rate(cls, new_rate: float):
        if 0 <= new_rate <= 1:
            cls.interest_rate = new_rate
            print(f"Процентная ставка изменена на {new_rate:.2%}")
        else:
            print("Некорректная ставка")

    # Метод класса (альтернативный конструктор для валютных счетов)
    @classmethod
    def from_usd(cls, owner: str, usd_amount: int, usd_rate: int = 90):
        # Конвертируем доллары в рубли и создаем счет
        rub_amount = usd_amount * usd_rate
        return cls(owner, rub_amount)

# --- Пример использования ---
# Создаем счета
acc1 = BankAccount("Иван", 1000)
acc2 = BankAccount.from_usd("Мэри", 100)  # Создаем через альтернативный конструктор

print(f'acc1 name:{acc1.owner}, acc1 balance:{acc1.balance}')
print(f'acc1 name:{acc2.owner}, acc1 balance:{acc2.balance}')
print('=' * 20)

# Работаем с методами экземпляра
print('Работа с acc1 (Иван)')
acc1.deposit(500)      # Депозит 500. Баланс: 1500
acc1.withdraw(200)     # Снято 200. Баланс: 1300
acc1.withdraw(5000)    # Недостаточно средств или неверная сумма

print('=' * 20)
# Работаем с методом класса
BankAccount.change_interest_rate(0.05)  # Ставка для всех счетов теперь 5%

print('=' * 20)
# Проверяем переменные класса и экземпляра
print(f"Банк: {BankAccount.bank_name}")  # Национальный Банк
print(f"Всего счетов: {acc1.total_accounts}")  # 2
print(f"Баланс Мэри: {acc2.balance} руб.")  # 9000 руб.