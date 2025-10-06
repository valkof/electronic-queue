from dataclasses import dataclass, field
import json
from typing import List, TypedDict, Union
from pult_log import log_critical
import sys
import requests
import json

class TUi(TypedDict):
    timeout_next: int # Время отката при вызове
    timeout_check: int # Время ?
    winfo_x: int # ?
    winfo_y: int # ?
    mode: str # Modes: "System" (standard), "Dark", "Light"
    theme: str # Themes: "blue" (standard), "green", "dark-blue"
    scaling: float # Масштаб
    shift_left: int # Сдвиг слева
    shift_bottom: int # Сдвиг снизу

class TAppSet(TypedDict):
    eq_wplace: str  # ID рабочего места
    eq_url: str # Адрес сервера
    fil: str  # Номер филиала
    eq_auth: List[str]  # Login, Pass
    ui: TUi
    set: List[List[Union[int, str]]]

@dataclass
class app_set:
    """
    Класс базовых переменных

    :param pult: - параметры подключения к серверу
    :param place: - описание рабочего места
    :param queues: - описание очередей обслуживаемых рабочим местом
    """
    pult: TAppSet
    place: dict = field(init=False)
    queues: dict = field(init=False)

    def __init__(self):
        try:
            with open('pult_set.json', 'r', encoding='utf-8') as data_set:
                self.pult = json.load(data_set)
        except Exception as e:
            log_critical("Проблема с файлом конфигурации.")
            sys.exit()

    # def get_setting_pult(self):
    #     try:
    #         url = self.dH['eq_url'] + 'get_wplace?w=' + self.dH['eq_wplace']
    #         auth = tuple(self.dH['eq_auth'])
    #         req = requests.get(url=url, auth=auth)
    #         dReq = json.loads(req.text)
    #         if dReq['stderr'] is None:
    #             self.dW = dReq['stdout']
    #         else:
    #             log.debug("Сервер ответил: " + dReq['stderr'])
    #             sys.exit()

    #         url = self.dH['eq_url'] + 'get_queues?w=' + self.dH['eq_wplace']
    #         auth = tuple(self.dH['eq_auth'])
    #         req = requests.get(url=url, auth=auth)
    #         dReq = json.loads(req.text)
    #         if dReq['stderr'] is None:
    #             self.dE = dReq['stdout']
    #         else:
    #             log.debug("Сервер ответил: " + dReq['stderr'])
    #             sys.exit()
    #     except Exception as e:
    #         log.debug("Проблема с подключением к серверу очереди: " + str(e))
    #         sys.exit()


if __name__ == '__main__':
    app_set()
