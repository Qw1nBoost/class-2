import json
import types
from enum import Enum
from typing import Dict, List, Optional, ClassVar
from types import TracebackType
import time

# classvar и optional
# * 5
# padded_line
# аннотация в _current_font

#методы, переменные класса, примеры и поведение, публичные защищенные и приватные переменные, инкапсуляция в питоне(name менгеринг)

class Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97


class ANSI:
    RESET = '\033[0m'

    @staticmethod
    def set_color(color: Color) -> str:
        return f'\033[{color.value}m'


class FontLoader:
    @staticmethod
    def load_font(filename: str) -> Dict[str, List[str]]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Font file {filename} not found!")
        except PermissionError:
            print(f"Ошибка: нет прав доступа к файлу '{filename}'")
        except IsADirectoryError:
            print(f"Ошибка: '{filename}' является директорией, а не файлом")
        except UnicodeDecodeError as e:
            print(f"Ошибка: проблема с кодировкой файла '{filename}'")
            print(f"Проблема в кодировке {e.encoding}")
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON в файле {filename}: в строке {e.lineno}, столбце {e.colno}")
        except OSError as e:
            print(f"Системная ошибка: {e} в файле {filename}")


class Printer:
    _current_font: ClassVar[Optional[Dict[str, List[str]]]] = None #атрибут принадлежит классу и доступен во всех экземплярах. изменение только через класс
    _font_height: ClassVar[int] = 0 # optional. переменная либо типа A, либо None

    def __init__(self, color: Color = Color.WHITE, symbol: str = '*', font_file: Optional[str] = None):
        self.color = color
        self.symbol = symbol

        if font_file:
            self.load_font(font_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Optional[type[BaseException]] = None, # тип возникшего исключения
                exc_val: Optional[BaseException] = None, # объект исключения
                exc_tb: Optional[TracebackType] = None): # объект traceback с информацией о стеке вызовов
        print(ANSI.RESET, end='')

    @classmethod
    def load_font(cls, font_file: str): # загрузка шрифта для класса
        cls._current_font = FontLoader.load_font(font_file)
        if cls._current_font:
            first_char = next(iter(cls._current_font.values())) #!!!!!!!!
            cls._font_height = len(first_char)

    @classmethod
    def print(cls, text: str, color: Color = Color.WHITE, symbol: str = '*'): # статический метод
        lines = [''] * cls._font_height

        for char in text.upper():
            if char == ' ':
                for i in range(cls._font_height):
                    lines[i] += ' ' * cls._font_height #$$$$
                continue

            if char in cls._current_font:
                char_pattern = cls._current_font[char]

                for i, line in enumerate(char_pattern):
                    rendered_line = line.replace('*', symbol)
                    padded_line = rendered_line.center(cls._font_height)
                    lines[i] += padded_line + ' '

        for line in lines:
            print(ANSI.set_color(color) + line + ANSI.RESET)

    def print_text(self, text: str): # вывод с настройками экземпляра
        self.__class__.print(text, self.color, self.symbol)
        print()


def demonstrate_printer() -> None:

    print("-- класс Printer --\n")

    # статическое использование 
    print("1. Статическое использование (шрифт 5x5):")
    Printer.load_font('font5x5.json')
    Printer.print("HELLO", Color.RED, '#')
    print()
    Printer.print("WORLD", Color.GREEN, '@')

    time.sleep(2)
    
    # контекстный менеджер
    print("2. Использование с контекстным менеджером (шрифт 5x5):")

    with Printer(Color.MAGENTA, '$', 'font5x5.json') as printer:
        printer.print_text("CONTEXT")
        printer.print_text("MANAGER")
        #print('------------------------------------------------------------------')
        #print(printer._current_font)

    time.sleep(2)
    
    print("3. Смена шрифта на 7x7:")
    Printer.load_font('font7x7.json')

    Printer.print("BIGGER", Color.BRIGHT_YELLOW, '$')
    print()
    Printer.print("FONT", Color.BRIGHT_CYAN, '#')

    time.sleep(2)
    
    # разные цвета и символы
    print("4. Разные цвета и символы (шрифт 7x7):")

    Printer.load_font('font7x7.json')
    Printer.print("BOMB", Color.BRIGHT_RED, '@')
    print()
    Printer.print("CIRCLE", Color.BRIGHT_GREEN, '*')
    print()
    Printer.print("CARS", Color.BRIGHT_BLUE, '@')

    time.sleep(2)

if __name__ == "__main__":
    demonstrate_printer()