import json
import pytest
from src.sources.file_source import FileSource
from src.sources.generator_source import GeneratorConfig, GeneratorSource
from src.sources.api_mock_source import APIMockSource


class TestFileSource:
    def test_load_tasks_from_json(self, tmp_path):
        """Загружаем задачи из нормального JSON-файла"""
        test_file = tmp_path / "tasks.json"
        data = [
            {"id": "task_1", "payload": {"action": "test1"}},
            {"id": "task_2", "payload": {"action": "test2"}},
        ]
        test_file.write_text(json.dumps(data))

        source = FileSource(str(test_file))
        tasks = source.get_task()

        assert len(tasks) == 2
        assert tasks[0].id == "task_1"

    def test_invalid_json_content(self, tmp_path):
        """Тест на неправильный файл JSON"""
        test_file = tmp_path / "broken.json"
        test_file.write_text('{ this is not valid json }')

        source = FileSource(str(test_file))

        with pytest.raises(ValueError):
            source.get_task()

    def test_missing_payload_field(self, tmp_path):
        """Передача задачи без payload"""
        test_file = tmp_path / "missing.json"
        data = [{"id": "1"}]
        test_file.write_text(json.dumps(data))

        source = FileSource(str(test_file))

        with pytest.raises(KeyError):
            source.get_task()

    def test_file_not_exists(self):
        """Несуществующий файл"""
        source = FileSource("/nonexistent/path/file.json")

        with pytest.raises(ValueError):
            source.get_task()


class TestGeneratorSource:
    def test_len_default_count(self):
        """Проверка количества задач"""
        source = GeneratorSource()
        tasks = source.get_task()

        assert len(tasks) == 5

    def test_custom_count(self):
        """Проверка на задавание количества задач"""
        config = GeneratorConfig(count=21)
        source = GeneratorSource(config)
        tasks = source.get_task()

        assert len(tasks) == 21

    def test_prefix_in_task_id(self):
        """Префикс должен быть в начале id задачи"""
        config = GeneratorConfig(count=3, prefix="my_prefix_")
        source = GeneratorSource(config)
        tasks = source.get_task()

        assert tasks[0].id.startswith("my_prefix_")

    def test_negative_count_raises_error(self):
        """Проверка правильности количества"""
        with pytest.raises(ValueError):
            GeneratorConfig(count=-5)

    def test_zero_count_returns_empty(self):
        """Отсутствие задач"""
        config = GeneratorConfig(count=0)
        source = GeneratorSource(config)
        tasks = source.get_task()

        assert len(tasks) == 0

    def test_for_test_factory_method(self):
        """
        Проверка метода for_test().

        """
        source1 = GeneratorSource.for_test(count=3)
        source2 = GeneratorSource.for_test(count=3)

        tasks1 = source1.get_task()
        tasks2 = source2.get_task()

        assert len(tasks1) == 3
        assert [t.id for t in tasks1] == [t.id for t in tasks2]


class TestAPIMockSource:
    def test_default_tasks_count(self):
        """Проверка количеста задач по умолчанию"""
        source = APIMockSource()
        tasks = source.get_task()

        assert len(tasks) == 3

    def test_custom_tasks_data(self):
        """Проверка передач своих данных"""
        custom = [
            {"id": "custom_1", "payload": {"test": True}},
            {"id": "custom_2", "payload": {"test": '131315415'}},
        ]
        source = APIMockSource(tasks_data=custom)
        tasks = source.get_task()

        assert len(tasks) == 2
        assert tasks[0].id == "custom_1"
        assert tasks[1].payload == {"test": '131315415'}

    def test_missing_field_in_custom_data(self):
        """Отсутствие payload"""
        invalid = [{"id": "1"}]
        source = APIMockSource(tasks_data=invalid)

        with pytest.raises(KeyError):
            source.get_task()

    def test_empty_tasks_list(self):
        """Пустой список"""
        source = APIMockSource(tasks_data=[])
        tasks = source.get_task()

        assert len(tasks) == 0
