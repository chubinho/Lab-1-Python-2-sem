from typing import Protocol, runtime_checkable
from task import Task

@runtime_checkable
class TaskSource(Protocol):
    def get_task(self) -> list[Task]:
        pass
