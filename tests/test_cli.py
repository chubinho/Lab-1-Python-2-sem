import pytest
from typer.testing import CliRunner
from pathlib import Path
import json

from src.cli import app

runner = CliRunner()


class TestCLICommands:

    def test_cli_help_shows_commands(self):
        """Проверка, что --help показывает все команды"""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "file" in result.stdout
        assert "generate" in result.stdout
        assert "api" in result.stdout
        assert "all" in result.stdout

    def test_generate_default_count(self):
        """Генерация задач с параметрами по умолчанию"""
        result = runner.invoke(app, ["generate"])
        assert result.exit_code == 0
        assert "GeneratorSource:" in result.stdout
        assert "5 задач" in result.stdout

    def test_generate_custom_count(self):
        """Генерация с кастомным количеством задач"""
        result = runner.invoke(app, ["generate", "--count", "30"])

        assert result.exit_code == 0
        assert "GeneratorSource: 30 задач" in result.stdout

    def test_api_command(self):
        """Проверка команды api — задачи из заглушки."""
        result = runner.invoke(app, ["api"])
        assert result.exit_code == 0
        assert "APIMockSource:" in result.stdout
        assert "3 задач" in result.stdout
        assert "api_1" in result.stdout

    def test_file_with_valid_json(self, tmp_path):
        """Загрузка задач из JSON-файла"""

        test_file = tmp_path / "tasks.json"
        data = [
            {"id": "1", "payload": {"test": True}},
            {"id": "2", "payload": {"test": False}},
        ]
        test_file.write_text(json.dumps(data))
        result = runner.invoke(app, ["file", str(test_file)])
        assert result.exit_code == 0
        assert "FileSource:" in result.stdout
        assert "2 задач" in result.stdout

    def test_generate_with_prefix(self):
        """Генерация с кастомным префиксом"""
        result = runner.invoke(app, ["generate", "--prefix", "test_"])
        assert result.exit_code == 0
        assert "test_1" in result.stdout

    def test_all_command_with_custom_file(self, tmp_path):
        """Команда all с кастомным файлом"""
        test_file = tmp_path / "tasks.json"
        test_file.write_text('[{"id": "1", "payload": {}}]')

    def test_cli_error_handling(self):
        """Проверка обработки ошибок в CLI"""
        result = runner.invoke(app, ["generate", "--count", "-1"])
        assert result.exit_code != 0

    def test_file_with_invalid_json(self, tmp_path):
        """Файл с невалидным JSON должен вызывать ошибку"""
        test_file = tmp_path / "invalid.json"
        test_file.write_text('{ not valid json }')

        result = runner.invoke(app, ["file", str(test_file)])

        assert result.exit_code != 0
        assert "Ошибка" in result.stdout

    def test_file_with_missing_payload(self, tmp_path):
        """Файл без поля payload должен вызывать ошибку"""
        test_file = tmp_path / "missing.json"
        data = [{"id": "1"}]
        test_file.write_text(json.dumps(data))
        result = runner.invoke(app, ["file", str(test_file)])

        assert result.exit_code != 0
        assert "Ошибка" in result.stdout
