from src.sources.generator_source import GeneratorSource
from src.protocol import TaskSource


class TestProtocol:
    def test_generator_source_implements_protocol(self):
        """Проверка, что GeneratorSource реализует протокол"""
        source = GeneratorSource()
        assert isinstance(source, TaskSource)

    def test_source_has_get_task_method(self):
        """Проверка, что источник имеет метод get_task"""
        source = GeneratorSource()
        assert hasattr(source, 'get_task')

    def test_get_task_returns_list(self):
        """Проверка, что get_task возвращает список"""
        source = GeneratorSource()
        tasks = source.get_task()
        assert isinstance(tasks, list)

    def test_runtime_checkable_attribute_exists(self):
        """
        Проверка, что у протокола есть атрибут _is_runtime_protocol.
        """
        assert hasattr(TaskSource, '_is_runtime_protocol')
        assert TaskSource._is_runtime_protocol is True
