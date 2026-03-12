from dataclasses import dataclass
import random
from task import Task


@dataclass
class GeneratorConfig:
    """
    Конфигурация для GeneratorSource
    
    Атрибуты:
        count: Количество задач для генерации (по умолчанию 5)
        prefix: Префикс для идентификаторов задач (по умолчанию "task_")
        seed: Seed для генератора случайных чисел (None = без фиксации)
        random_priority: Если True, приоритет генерируется случайно (1-10)
    """
    count: int = 5
    prefix: str = "task_"
    seed: int | None = None
    random_priority: bool = True

    def __post_init__(self):
        """
        Валидация конфигурации после инициализации
        """
        if self.count < 0 or not isinstance(self.count, int):
            raise ValueError(
                "The number of tasks cannot be negative or not an integer")


class GeneratorSource:
    """
    Источник задач, генерирующий задачи программно
    """
    def __init__(self, config: GeneratorConfig | None = None):
        self.config = config if config is not None else GeneratorConfig()

    @classmethod
    def for_test(cls, count: int = 3) -> 'GeneratorSource':
        config = GeneratorConfig(count=count, seed=52, random_priority=False)
        return cls(config)

    def get_task(self) -> list[Task]:
        """
        Сгенерировать задачи 
        
        Returns:
            list[Task]: Список Task
        """
        if self.config.seed is not None:
            random.seed(self.config.seed)
        
        tasks = []

        for i in range(1, self.config.count + 1):
            if self.config.random_priority:
                priority = random.randint(1,10)
            else:
                priority = 5
            
            task = Task(
                id = f"{self.config.prefix}{i}",
                payload={
                    "generated": True,
                    "index": i,
                    "source": "GeneratorSource",
                    "priority": priority
                }
            )
            tasks.append(task)
        return tasks
