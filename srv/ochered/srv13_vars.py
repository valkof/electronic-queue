from dataclasses import dataclass, field
import json
from logger import get_logger
import sys
import time


log = get_logger(__name__)


def read_settings_eq():
    # словарь описания "очередей"
    try:
        with open('srv13_set.json', 'r', encoding='utf-8') as data1:
            dEq = json.load(data1)['queue']
        return dEq
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


def read_settings_wp():
    # словарь описания "окон"
    try:
        with open('srv13_set.json', 'r', encoding='utf-8') as data1:
            dWp = json.load(data1)['wplace']
        return dWp
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


def read_settings_host():
    # базовые настройки фонового http-сервера
    try:
        with open('srv13_set.json', 'r', encoding='utf-8') as data1:
            dH = json.load(data1)['host']
        return dH
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


def read_settings_db():
    # настройки базы данных
    try:
        with open('srv13_set.json', 'r', encoding='utf-8') as data1:
            dB = json.load(data1)['db']
        return dB
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


def read_settings_au():
    # словарь описания "очередей"
    try:
        with open('srv13_set.json', 'r', encoding='utf-8') as data1:
            dAu = json.load(data1)['ausrv']
        return dAu
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


def read_settings_tv():
    # словарь описания "очередей"
    try:
        with open('srv13_set.json', 'r', encoding='utf-8') as data1:
            dTv = json.load(data1)['tvsrv']
        return dTv
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


def read_settings_led():
    # словарь описания "очередей"
    try:
        with open('srv13_set.json', 'r', encoding='utf-8') as data1:
            dLe = json.load(data1)['ledsrv']
        return dLe
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        sys.exit()


@dataclass
class V:
    # Класс базовых переменных
    # dE - словарь/описание очередей
    # dW - словарь/описание рабочих мест, "окон"
    # dD - словарь/описание подключения к сервису, БД
    # dH - словарь параметров запуска сервиса: хост/порт/аутентификация
    # dA - словарь/описание Аудиосерверов
    # dT - словарь/описание Инфотабло
    # dL - словарь/описание Табло
    # sD - строка - имя БД
    dE: dict = field(default_factory=read_settings_eq)
    dW: dict = field(default_factory=read_settings_wp)
    dH: dict = field(default_factory=read_settings_host)
    dD: dict = field(default_factory=read_settings_db)
    dA: dict = field(default_factory=read_settings_au)
    dT: dict = field(default_factory=read_settings_tv)
    dL: dict = field(default_factory=read_settings_led)
    sD: str = field(init=False)

    def __post_init__(self):
        self.sD = self.dD['base']
