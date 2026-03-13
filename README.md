# Лабораторная работа №1: Источники задач и контракты

## Описание работы

Проект представляет собой платформу для приёма задач из различных источников через единый контракт. 
Реализована валидация источников через `@runtime_checkable` протоколы, логирование 
и CLI-интерфейс для удобной работы.

## Функционал 
- Протокол `TaskSource` с `@runtime_checkable` для проверки контрактов
- Runtime-проверка  в классе `TaskConsumer`
- Три источника задач: файлы (JSON), генератор, API-заглушка
- Тестирование с покрытием 80% (pytest)

## Структура 
```
Lab-1-Python-2-sem/
├── src/
│ ├── __init__.py
│ ├── main.py # Точка входа для python -m src
│ ├── cli.py # CLI-команды (typer)
│ ├── consumer.py # TaskConsumer + проверка контракта
│ ├── logger.py # Настройка логирования
│ ├── protocol.py # Protocol TaskSource (@runtime_checkable)
│ ├── task.py # Модель задачи (dataclass)
│── sources/
│ ├── __init__.py
│ ├── file_source.py # Источник из JSON-файла
│ ├── generator_source.py # Программный генератор
│ └── api_mock_source.py # API-заглушка
├── tests/
│ ├── __init__.py
│ ├── test_all_sources.py # Тесты источников
│ ├── test_cli.py # Тесты CLI
│ ├── test_consumer.py # Тесты Consumer
│ ├── test_protocol.py # Тесты протокола
│ └── test_task.py # Тесты модели Task
├── logs/
│ └── task.log # Файл логов (создаётся автоматически)
├── messages.json # Пример данных для FileSource
├── requirements.txt # Зависимости проекта
├── .gitignore  # Файл .gitignore
├── .pre-commit-config.yaml  # Конфиг .pre-commit
├── pyproject.toml # Конфиг проекта
└── README.md # Документация
```
## Установка зависимостей 
```
pip install -r requirements.txt
```

## CLI

### Вывод всей нужной информации по взаимодейстию с пользователем:
```
python -m src --help # 
```

## Тестирование
```
# Запустить все тесты
pytest tests/ -v

# С отчётом о покрытии
pytest tests/ -v --cov=src
```

