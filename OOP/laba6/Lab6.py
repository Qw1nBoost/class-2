from v_keyboard import VirtualKeyboard
from command_factory import CommandFactory  # Импортируем фабрику

COLORING = "\033[{}m{}\033[0m"

if __name__ == "__main__":
    command_factory = CommandFactory()
    keyboard = VirtualKeyboard(command_factory)
    
    if not keyboard.load_state():
        print(COLORING.format(33, "No saved state found, using defaults"))
    else:
        print(COLORING.format(33, "Keyboard state loaded"))
        # Используем фабрику для получения текста
        print(COLORING.format(33, command_factory.get_text()))
    
    with open("laba6/data/keyboard_log.txt", "w") as log_file:
        def print_and_log(message) -> None:
            print(COLORING.format(32, message))
            log_file.write(message + "\n")
        
        print_and_log(keyboard.press_key("a"))
        print_and_log(keyboard.press_key("b"))
        print_and_log(keyboard.press_key("c"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("redo"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl+-"))
        print_and_log(keyboard.press_key("ctrl+p"))
        print_and_log(keyboard.press_key("d"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("undo"))
        
        keyboard.save_state()
        print_and_log("Keyboard state saved")