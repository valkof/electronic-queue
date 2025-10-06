from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

# Константы для конфигурации
LOG_DIR = 'logs'
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 МБ
BACKUP_COUNT = 5

def __setup_logger():
    """
    Инициализация логгера с базовой конфигурацией
    """
    # Создаем директорию для логов, если её нет
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # Создаем логгер
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)  # Записываем все уровни сообщений
    
    # Создаем обработчик файла с ротацией
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, '{:%Y-%m-%d}.log'.format(datetime.now())),
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT
    )
    
    # Настраиваем формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)
    
    return logger

def log_error(message, exc_info=False):
    """
    Запись сообщения об ошибке
    :param message: сообщение для логирования
    :param exc_info: включать ли информацию об исключении
    """
    logger = __setup_logger()
    logger.error(message, exc_info=exc_info)

def log_warning(message):
    """
    Запись предупреждения
    :param message: сообщение для логирования
    """
    logger = __setup_logger()
    logger.warning(message)

def log_info(message):
    """
    Запись информационного сообщения
    :param message: сообщение для логирования
    """
    logger = __setup_logger()
    logger.info(message)

def log_debug(message):
    """
    Запись отладочного сообщения
    :param message: сообщение для логирования
    """
    logger = __setup_logger()
    logger.debug(message)

def log_critical(message):
    """
    Запись критического сообщения
    :param message: сообщение для логирования
    """
    logger = __setup_logger()
    logger.critical(message)
