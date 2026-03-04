from typing import Optional
import json
from commands import Command
from memento import KeyboardMemento
from command_factory import CommandFactory


class VirtualKeyboard:
    def __init__(self, command_factory=None) -> None:
        self.key_bindings: dict[str, Command] = {}
        self.history: list[dict[str, Command]] = []
        self.undo_stack: list[dict[str, Command]] = []
        self.command_factory = command_factory or CommandFactory()  # Сохраняем фабрику
        
        create_default_bindings(self) 
        
    def bind_key(self, key: str, command: Optional[Command]) -> None:
        self.key_bindings[key] = command
        
    def press_key(self, key: str) -> str | None:
        if key == "undo":
            return self.undo()
        elif key == "redo":
            return self.redo()
            
        command = self.key_bindings.get(key)
        if not command and len(key) == 1:
            # Используем фабрику вместо прямого создания
            new_command = self.command_factory.create_print_command(key)
            self.bind_key(key, new_command)
            command = self.key_bindings.get(key)
        if command:
            result = command.execute()
            self.history.append({"key": key, "command": command})
            self.undo_stack.clear()  
            return result
        return f"Unknown key: {key}"
        
    def undo(self) -> str:
        if not self.history:
            return "Nothing to undo"
            
        command = self.history.pop()
        result = command["command"].undo()
        self.undo_stack.append(command)
        return f"undo: {result}"
        
    def redo(self) -> str:
        if not self.undo_stack:
            return "Nothing to redo"
            
        command = self.undo_stack.pop()
        result = command["command"].redo()
        self.history.append(command)
        return f"redo: {result}"
        
    def save_state(self, filename: str = "laba6/data/keyboard_state.json") -> None:
        memento = KeyboardMemento.from_keyboard(self)
        try:
            with open(filename, "w") as f:
                json.dump(memento.state, f, indent=4)
        except Exception as e:
            print(f"Error saving state: {e}")
            raise e

    def load_state(self, filename: str = "laba6/data/keyboard_state.json") -> bool:
        try:
            with open(filename, "r") as f:
                state = json.load(f)
            
            # Используем фабрику вместо прямого доступа
            self.command_factory.set_text(state['text'])
            
            # Получаем классы команд через фабрику
            class_names = {}
            for key, factory in self.command_factory.get_default_bindings().items():
                cmd = factory()
                if cmd:
                    class_names[cmd.__class__.__name__] = cmd.__class__
                
            self.key_bindings.clear()
            for key, command_data in state.get('key_bindings', {}).items():
                if command_data is None:
                    self.key_bindings[key] = None
                else:
                    command_class = class_names.get(command_data['class'])
                    if command_class:
                        command = command_class(**command_data['state'])
                        self.key_bindings[key] = command

            self.history = [
                {"key": key, "command": self.key_bindings[key]} 
                for key in state.get('history', [])
                if key in self.key_bindings.keys() and self.key_bindings[key] is not None
            ]

            self.undo_stack = [
                {"key": key, "command": self.key_bindings[key]} 
                for key in state.get('undo_stack', [])
                if key in self.key_bindings.keys() and self.key_bindings[key] is not None
            ]
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError, AttributeError) as e:
            print(f"Error loading state: {e}")
            return False


def create_default_bindings(keyboard: VirtualKeyboard) -> None:
    """Функция для создания стандартных привязок клавиш"""
    default_bindings = keyboard.command_factory.get_default_bindings()
    for key, command_factory in default_bindings.items():
        keyboard.bind_key(key, command_factory())