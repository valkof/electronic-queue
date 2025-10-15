import json
from pult_log import log_critical
import sys

from pult_types import TPult, TSetQueue

class AppSet:
    """
    Класс базовых переменных

    :param pult: - параметры подключения к серверу
    :param place: - описание рабочего места
    """
    pult: TPult
    place: TSetQueue
    # queues: dict = field(init=False)
    # :param queues: - ?описание очередей обслуживаемых рабочим местом

    def __init__(self):
        try:
            with open('pult_set.json', 'r', encoding='utf-8') as data_set:
                self.pult = json.load(data_set)
        except Exception as e:
            log_critical("Проблема с файлом конфигурации.")
            sys.exit()

