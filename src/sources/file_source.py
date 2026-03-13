import logging
from typing import Protocol
from pathlib import Path
from src.task import Task
import json

logger = logging.getLogger("task")

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
        logger.info(f"Загрузка задач из файла: {self.path}")

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
                logger.error(f"Данный файл не найден: {self.path}")
                raise FileNotFoundError(
                    f"Файл с заданием не найден:{self.path}")

            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.debug(f"Успешно прочитан JSON: {len(data)} записей")

            tasks = []
            for task_data in data:
                task = Task(
                    id=task_data['id'],
                    payload=task_data['payload']
                )
                tasks.append(task)
            
        except json.JSONDecodeError as e:
            logger.error(f"Неверная запись JSON в файле {self.path}: {e}")
            raise ValueError(
                f"Неверная запись JSON в файле {self.path}: {e}")
        except KeyError as e:
            logger.error(f"Обязательное поле пропущено: {e}")
            raise KeyError(f"Обязательное поле пропущено: {e}")
        except Exception as e:
            logger.error(f"Ошибка: {self.path}")
            raise ValueError(f"Ошибка: {self.path}")

        logger.info(f"Создано {len(tasks)} объектов Task из файла")   
        return tasks
