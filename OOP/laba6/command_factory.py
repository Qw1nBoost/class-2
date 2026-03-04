from commands import *

class CommandFactory: #Фабрика для создания команд"
    
    @staticmethod
    def create_print_command(char: str):
        return PrintCharCommand(char)
    
    @staticmethod
    def get_default_bindings(): #Возвращает словарь с фабриками для стандартных команд
        return {
            "a": lambda: PrintCharCommand("a"),
            "b": lambda: PrintCharCommand("b"),
            "c": lambda: PrintCharCommand("c"),
            "d": lambda: PrintCharCommand("d"),
            "ctrl++": lambda: VolumeUpCommand(),
            "ctrl+-": lambda: VolumeDownCommand(),
            "ctrl+p": lambda: MediaPlayerCommand(),
            "undo": lambda: None,
            "redo": lambda: None,
        }
    
    @staticmethod
    def get_text():
        """Получить текущий текст"""
        return PrintCharCommand.text
    
    @staticmethod
    def set_text(text):
        """Установить текст"""
        PrintCharCommand.text = text