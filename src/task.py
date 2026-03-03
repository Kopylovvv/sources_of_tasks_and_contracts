from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    """
    Представление задачи

    attributes:
        id: id задачи
        payload: данные задачи
    """
    id: str
    payload: Any
