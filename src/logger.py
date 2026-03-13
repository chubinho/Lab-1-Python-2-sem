import logging 
import sys


def set_logger(level: int = logging.INFO, log_file: str = "task.log") -> logging.Logger:
    """
    Настройка логирования для платформы
    
    Args:
        level: Уровень логирования
        log_file: Путь к файлу логов
    
    Returns:
        logging.Logger: Настроенный логгер платформы 
    """
    logger = logging.getLogger("task")
    logger.setLevel(level)

    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt='%d.%m.%Y %H:%M:%S'
    )

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    
    return logger