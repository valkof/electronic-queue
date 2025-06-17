from dataclasses import dataclass, field
import json
from logger import get_logger
import sys
import time

log = get_logger(__name__)


def read_settings_eq():
    # словарь описания "очередей"
    try:
        with open('ksk08_set.json', 'r', encoding='utf-8') as data1:
            dEq = json.load(data1)['queue']
        return dEq
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


def read_settings_host():
    # базовые настройки фонового http-сервера
    try:
        with open('ksk08_set.json', 'r', encoding='utf-8') as data1:
            dH = json.load(data1)['host']
        return dH
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


@dataclass
class V:
    # Класс базовых переменных
    # dE - словарь/описание очередей
    # dH - словарь параметров запуска сервиса: хост/порт/аутентификация
    dE: dict = field(default_factory=read_settings_eq)
    dH: dict = field(default_factory=read_settings_host)


if __name__ == '__main__':
    v = V()
    print("dE=", v.dE)
    print()
    print("dH=", v.dH)
    print()
