import logging
from typing import Any
from src.task import Task

logger = logging.getLogger("task")
class APIMockSource:
    """
    Источник задач, имитирующий внешний API
    """
    def __init__(self, tasks_data: list[dict[str, Any]] | None = None) -> None:
        """
        Инициализация API-заглушки
        """
        if tasks_data is None:
            self.tasks_data = [{"id": "api_1", "payload": {
                "action": "send_email", "user": "test@example.com"}},
                {"id": "api_2", "payload": {
                    "action": "calc_stats", "date": "2025-03-08"}},
                {"id": "api_3", "payload": {
                 "action": "log_message", "text": "System started"}},
            ]
            logger.debug(
                "APIMockSource инициализирован с данными по умолчанию")
        else:
            self.tasks_data = tasks_data
            logger.debug(
                f"APIMockSource инициализирован с {len(tasks_data)} кастомными задачами")

    def get_task(self) -> list[Task]:
        """
        Получение задач из API-заглушки
        
        Returns:
            list[Task]: Список объектов Task
        
        Raises:
            KeyError: Если в данных отсутствуют обязательные поля
        """
        tasks = []
        logger.info(
            f"Получение задач из API: {len(self.tasks_data)} записей")
        for task_data in self.tasks_data:
            try:
                task = Task(id=str(task_data['id']),
                            payload=task_data['payload'])
                tasks.append(task)
                logger.debug(f"Создана задача: {task.id}")
            except KeyError as e:
                logger.error(
                    f"Отсутствует обязательное поле: {e}")
                raise KeyError(
                    f"Отсутствует обязательное поле в API-ответе: {e}"
                ) from e
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                raise ValueError(f"Ошибка: {e}")
        
        logger.info(f"Создано {len(tasks)} объектов Task из API")
        return tasks
