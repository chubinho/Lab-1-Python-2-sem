from pathlib import Path
import typer
import logging

from src.sources.file_source import FileSource
from src.sources.generator_source import GeneratorConfig, GeneratorSource
from src.sources.api_mock_source import APIMockSource
from src.consumer import TaskConsumer
from src.logger import set_logger


logger = logging.getLogger(__name__)
set_logger(logging.INFO)


app = typer.Typer(help="Платформа обработки задач")


@app.command()
def file(path: Path = typer.Argument(..., help="Путь к JSON-файлу")):
    """
    Получение задачи из файла
    """
    logger.info(f"Запуск команды 'file': path={path}")
    consumer = TaskConsumer()
    try:
        logger.debug("Создание FileSource для {path}")
        source = FileSource(path)
        tasks = consumer.accept_tasks(source)
        logger.info(f"FileSource: получено {len(tasks)} задач")
        typer.echo(f"FileSource: {len(tasks)} задач")
        for task in tasks:
            typer.echo(f" - {task.id}: {task.payload}")

    except FileNotFoundError as e:
        logger.error(f"Файл с путем - {path} не найден - {e}")
        typer.echo(f"Ошибка: Файл {e} не найден")
        raise typer.Exit(1)
    except TypeError as e:
        logger.error(f"Нарушение контракта - {e}")
        typer.echo(f"Нарушение контракта - {e}")
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        typer.echo(f"Ошибка: {e}")
        raise typer.Exit(1)


@app.command()
def generate(
        count: int = typer.Option(5, "--count", "-n", help="Кол-во задач"),
        prefix: str = typer.Option("task_", "--prefix", "-p", help="Префикс")):
    """
    Генерация задачи
    """
    consumer = TaskConsumer()
    try:
        config = GeneratorConfig(count=count, prefix=prefix)
        source = GeneratorSource(config)
        tasks = consumer.accept_tasks(source)
        typer.echo(f"GeneratorSource: {len(tasks)} задач")
        for task in tasks:
            typer.echo(f"   • {task.id}: {task.payload}")
    except Exception as e:
        typer.echo(f"Ошибка: {e}")
        raise typer.Exit(1)


@app.command()
def api():
    """Получить задачи из API-заглушки."""
    consumer = TaskConsumer()
    try:
        source = APIMockSource()
        tasks = consumer.accept_tasks(source)
        typer.echo(f"APIMockSource: {len(tasks)} задач")
        for task in tasks:
            typer.echo(f"   • {task.id}: {task.payload}")
    except Exception as e:
        typer.echo(f"Ошибка: {e}")
        raise typer.Exit(1)


@app.command()
def all(
    file: Path = typer.Option("tasks.json", "--file",
                              "-f", help="Путь к JSON-файлу"),
    count: int = typer.Option(
        3, "--count", "-n", help="Количество задач для генератора"),
):
    """Получить задачи из всех источников."""
    consumer = TaskConsumer()
    try:
        sources = [
            FileSource(file),
            GeneratorSource(GeneratorConfig(count=count)),
            APIMockSource(),
        ]
        all_tasks = consumer.accept_tasks_from_multiple_sources(sources)
        typer.echo(f" Всего: {len(all_tasks)} задач из 3 источников")
    except Exception as e:
        typer.echo(f"Ошибка: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
