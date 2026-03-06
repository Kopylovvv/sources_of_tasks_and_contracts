import json
import random

from src.task import Task


class FileTaskSource:
    """
    Источник задач из файла.
    чтение задач из JSON-файла.
    """

    def __init__(self, file_path: str):
        """
        Инициализация источника.

        Args:
            file_path: Путь к файлу с задачами
        """
        self.file_path = file_path

    def get_tasks(self) -> list[Task]:
        """
        Чтение задач из файла.

        Returns:
            list[Task]: Список задач из файла
        """
        # Чтение из реального файла
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)

                # Проверка, что данные - это список
                if not isinstance(tasks_data, list):
                    print(f"Ошибка: файл {self.file_path} должен содержать список задач")
                    return []

                # Преобразование данных в задачи
                tasks = []
                for task in tasks_data:
                    if "id" not in task:
                        print(f"Пропущен элемент: {task} - отсутствует поле 'id'")
                        continue

                    task_id = task["id"]
                    payload = {k: v for k, v in task.items() if k != "id"}
                    tasks.append(Task(id=task_id, payload=payload))

                return tasks

        except FileNotFoundError:
            print(f"Файл не найден по данному пути {self.file_path}")
        except PermissionError:
            print(f"Нет доступа к файлу {self.file_path}")
        except UnicodeDecodeError:
            print(f"Неверная кодировка файла {self.file_path}")
        except json.JSONDecodeError:
            print(f"Некорректный JSON файл {self.file_path}")

        return []


class RandomTaskSource:
    """
    Источник задач, генерирующий их программно.
    """

    def __init__(self, count: int = 5):
        """
        Инициализация генератора задач.

        Args:
            count: Количество генерируемых задач
        """
        self.count = count

    def get_tasks(self) -> list[Task]:
        """
        Генерация случайных задач.

        Returns:
            list[Task]: Список сгенерированных задач
        """
        tasks = []
        task_types = ["order", "notification", "stats", "check", "process"]

        for i in range(self.count):
            task_id = f"gen_{i}_{random.randint(1000, 9999)}"
            task_type = random.choice(task_types)

            # Генерация разных payload в зависимости от типа
            match task_type:
                case "order":
                    payload = {"type": "order", "order_id": random.randint(1, 1000)}
                case "notification":
                    payload = {
                        "type": "notification",
                        "user": f"user_{random.randint(1, 100)}",
                        "message": "Test notification"
                    }
                case "stats":
                    payload = {"type": "stats", "period": random.choice(["hour", "day", "week"])}
                case _:
                    payload = {"type": task_type, "value": random.random()}

            tasks.append(Task(id=task_id, payload=payload))

        return tasks


class APITaskSource:
    """
    Источник задач из API-заглушки.
    Имитирует получение задач из внешнего API.
    """

    def __init__(self, endpoint: str = "http://fake-api.example.com/tasks"):
        """
        Инициализация API-источника.

        Args:
            endpoint: URL эндпоинта API
        """
        self.endpoint = endpoint

    def get_tasks(self) -> list[Task]:
        """
        Получение задач через API.

        Returns:
            List[Task]: Список задач из API
        """
        # Эмуляция API-запроса
        api_response = {
            "status": "success",
            "data": [
                {"id": "api_001", "type": "email", "recipient": "user@example.com"},
                {"id": "api_002", "type": "report", "format": "pdf"},
                {"id": "api_003", "type": "sync", "target": "external_system"},
            ]
        }

        tasks = []
        for item in api_response["data"]:
            task_id = item["id"]
            payload = {k: v for k, v in item.items() if k != "id"}
            tasks.append(Task(id=task_id, payload=payload))

        return tasks
