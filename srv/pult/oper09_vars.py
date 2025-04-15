from dataclasses import dataclass, field
import json
from logger import get_logger
import sys
import requests
import json


log = get_logger(__name__)

def read_settings_oper():
    # словарь для стартовой инициализации
    try:
        with open('oper09_set.json', 'r', encoding='utf-8') as data1:
            dHq = json.load(data1)
        return dHq
    except (Exception) as e:
        log.debug("Проблема с conf-файлом конфигурации: " + str(e))
        print(str(e))
        sys.exit()


@dataclass
class V:
    # Класс базовых переменных
    # dH - параметры подключения к серверу
    # dW - описание рабочего места
    # dE - описание очередей обслуживаемых рабочим местом
    dH: dict = field(default_factory=read_settings_oper)
    dW: dict = field(init=False)
    dE: dict = field(init=False)

    def __post_init__(self):
        try:
            url = self.dH['eq_url'] + 'get_wplace?w=' + self.dH['eq_wplace']
            auth = tuple(self.dH['eq_auth'])
            req = requests.get(url=url, auth=auth)
            dReq = json.loads(req.text)
            if dReq['stderr'] is None:
                self.dW = dReq['stdout']
            else:
                log.debug("Сервер ответил: " + dReq['stderr'])
                sys.exit()

            url = self.dH['eq_url'] + 'get_queues?w=' + self.dH['eq_wplace']
            auth = tuple(self.dH['eq_auth'])
            req = requests.get(url=url, auth=auth)
            dReq = json.loads(req.text)
            if dReq['stderr'] is None:
                self.dE = dReq['stdout']
            else:
                log.debug("Сервер ответил: " + dReq['stderr'])
                sys.exit()
        except Exception as e:
            log.debug("Проблема с подключением к серверу очереди: " + str(e))
            sys.exit()


if __name__ == '__main__':
    v = V()
    print("==============")
    print("dH=", v.dH)
    print("dW=", v.dW)
    print("dE=", v.dE)
