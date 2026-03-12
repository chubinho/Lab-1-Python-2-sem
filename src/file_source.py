from typing import Protocol
from pathlib import Path
from task import Task
import json


class FileSource:
    """
    Источник задач, загружающий данные из файла
    """

    def __init__(self, file_path: str | Path) -> None:
        """
        Инициализация источника
        Args:
            file_path
        """
        self.path = Path(file_path)

    def get_task(self) -> list[Task]:
        """
        Загрузить задачи из файла
        
        Returns:
            list[Task]: Список объектов Task
        
        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если файл содержит невалидный JSON
            KeyError: Если в задаче отсутствуют обязательные поля
        """
        try:
            if not self.path.exists():
                raise FileNotFoundError(
                    f"The task file was not found:{self.path}")

            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            tasks = []
            for task_data in data:
                task = Task(
                    id=task_data['id'],
                    payload=task_data['payload']
                )
                tasks.append(task)
            return tasks
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON format in the file {self.path}: {e}")
        except KeyError as e:
            raise KeyError((f"The required field is missing in the task {e}"))
        except Exception as e:
            raise ValueError(f"Error creating task from data: {self.path}")
