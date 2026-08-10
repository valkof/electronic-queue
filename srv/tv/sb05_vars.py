from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional
import json

from dacite import from_dict

@dataclass
class HostConfig:
    bind: str
    port: str
    username: str
    password: str

@dataclass
class ClockConfig:
    fg: str
    bg: str
    font: List[Any]
    mode: int

@dataclass
class VideoPlayerConfig:
    fg: str
    bg: str
    font: List[Any]
    mode: int
    volume: int

@dataclass
class UIConfig:
    win_geometry: str
    win_bg_img: str
    timeout_blink: int
    kabinet_title: str
    clock: ClockConfig
    videoplayer: VideoPlayerConfig
    # wait_screen: Dict[str, Any] # Пустой словарь на данный момент

@dataclass
class ModeConfig:
    wait_screen: bool
    videoplayer: bool

@dataclass
class AppConfig:
    """Основная структура вашего JSON конфигурационного файла."""
    id: str
    host: HostConfig
    ui: UIConfig
    mode: ModeConfig

def read_settings_wplace():
    with open('sb05_wplace.json', 'r', encoding='utf-8') as data2:
        # словарь описания "окон"
        dW = json.load(data2)
    return dW

def read_settings_host():
    # базовые настройки фонового http-сервера
    with open('sb05_set.json', 'r', encoding='utf-8') as data1:
        dict_dH = json.load(data1)['host']
        dH = from_dict(data_class=HostConfig, data=dict_dH)
    return dH

def read_settings_ui():
    with open('sb05_set.json', 'r', encoding='utf-8') as data1:
        dict_dU = json.load(data1)['ui']
        dU = from_dict(data_class=UIConfig, data=dict_dU)
    return dU

def read_settings_mode():
    with open('sb05_set.json', 'r', encoding='utf-8') as data1:
        dict_dM = json.load(data1)['mode']
        dM = from_dict(data_class=ModeConfig, data=dict_dM)
    return dM

@dataclass
class V:
    # Класс базовых переменных
    # dW - json словарь/описание рабочих мест "окон"
    # dH - json словарь параметров запуска сервиса: хост/порт/аутентификация
    # dU - json словарь параметров UI
    # lW - пустой список, заполнится в процессе рисования графических объектов
    dW: dict = field(default_factory=read_settings_wplace)
    dH: HostConfig = field(default_factory=read_settings_host)
    dU: UIConfig = field(default_factory=read_settings_ui)
    dM: ModeConfig = field(default_factory=read_settings_mode)
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
    print(v.dU, v.dU.clock.x, v.dU.clock.y)
