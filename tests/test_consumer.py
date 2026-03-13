import pytest
from src.consumer import TaskConsumer
from src.sources.generator_source import GeneratorSource
from src.sources.api_mock_source import APIMockSource


class TestConsumer:

    def test_accept_tasks_generation(self):
        """Проверка получения задач при помощи генератора"""
        consumer = TaskConsumer()
        source = GeneratorSource()
        tasks = consumer.accept_tasks(source)
        assert len(tasks) == 5
        assert all(hasattr(task, 'id') for task in tasks)
        assert all(hasattr(task, 'payload') for task in tasks)

    def test_accept_tasks_with_generator_custom_count(self):
        """Проверка получения задач с кастомным количеством"""
        consumer = TaskConsumer()
        source = GeneratorSource()
        source.config.count = 7
        tasks = consumer.accept_tasks(source)

        assert len(tasks) == 7

    def test_accept_tasks_with_api(self):
        """Проверка получения задач из API"""
        consumer = TaskConsumer()
        source = APIMockSource()
        tasks = consumer.accept_tasks(source)

        assert len(tasks) == 3
        assert tasks[0].id == "api_1"
        assert tasks[1].id == "api_2"
        assert tasks[2].payload["action"] == "log_message"

    def test_accept_tasks_from_multiple_sources(self):
        """Проверка получения задач из нескольких источников"""
        consumer = TaskConsumer()
        sources = [
            GeneratorSource(),
            APIMockSource(),
        ]

        all_tasks = consumer.accept_tasks_from_multiple_sources(sources)

        assert len(all_tasks) == 8
        assert all(hasattr(task, 'id') for task in all_tasks)

    def test_accept_tasks_one_invalid_in_list(self):
        """Проверка ошибки при одном невалидном источнике в списке."""
        consumer = TaskConsumer()
        sources = [
            GeneratorSource(),
            {"invalid": "source"}
        ]

        with pytest.raises(TypeError):
            consumer.accept_tasks_from_multiple_sources(sources)
