from dataclasses import dataclass, field
import json


def read_settings_wplace():
    with open('sb05_wplace.json', 'r', encoding='utf-8') as data2:
        # словарь описания "окон"
        dW = json.load(data2)
    return dW


def read_settings_host():
    # базовые настройки фонового http-сервера
    with open('sb05_set.json', 'r', encoding='utf-8') as data1:
        dH = json.load(data1)['host']
    return dH


def read_settings_ui():
    # базовые настройки фонового http-сервера
    with open('sb05_set.json', 'r', encoding='utf-8') as data1:
        dU = json.load(data1)['ui']
    return dU


@dataclass
class V:
    # Класс базовых переменных
    # dW - json словарь/описание рабочих мест "окон"
    # dH - json словарь параметров запуска сервиса: хост/порт/аутентификация
    # dU - json словарь параметров UI
    # lW - пустой список, заполнится в процессе рисования графических объектов
    dW: dict = field(default_factory=read_settings_wplace)
    dH: dict = field(default_factory=read_settings_host)
    dU: dict = field(default_factory=read_settings_ui)
    lW: list = field(init=False)

    def __post_init__(self):
        # создания пустого списка lW с длинной равной максимальному значению
        # id в sb03_wplace.json
        def read_settings_lwplace(dW):
            max = 0
            for dL1 in self.dW:
                if int(dL1) > max:
                    max = int(dL1)
            return [None] * max
        self.lW = read_settings_lwplace(self.dW)


if __name__ == '__main__':
    v = V()
    print(v.dW)
    print(v.dU, v.dU["clock"]["xy"])
