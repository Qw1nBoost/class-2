from typing import Any, Callable, Dict, Optional, Type
from .lifestyle import LifeStyle

# Класс регистрации зависимости
class Registration:

    # Сохраняет метаданные регистрации
    def __init__(
        self,
        life_style: LifeStyle,
        class_type: Optional[Type] = None,
        params: Optional[Dict[str, Any]] = None,
        fabric_method: Optional[Callable[[], Any]] = None,
    ) -> None:
        if class_type is None and fabric_method is None:
            raise ValueError("Нужно указать class_type или fabric_method")
        self.life_style = life_style
        self.class_type = class_type
        self.params = params or {}
        self.fabric_method = fabric_method
