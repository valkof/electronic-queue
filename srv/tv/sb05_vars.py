from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional
import json

from dacite import from_dict

@dataclass
class ElementConfig:
    fg: str
    bg: str
    font: List[Any]

@dataclass
class WorkPlaceConfig:
    title: str
    place: ElementConfig
    ticket: ElementConfig

@dataclass
class HostConfig:
    bind: str
    port: str
    username: str
    password: str

@dataclass
class DateTimeConfig:
    fg: str
    bg: str
    px: int
    py: int
    font: List[Any]
    mode: int

@dataclass
class VideoPlayerConfig:
    fg: str
    bg: str
    px: int
    py: int
    font: List[Any]
    mode: int
    volume: int

@dataclass
class WorkCallConfig:
    fg: str
    bg: str
    px: int
    py: int
    wps: List[str]
    lh: str
    rh: str
    font: List[Any]
    hsize: int
    time_blink: int

@dataclass
class WaitScreenConfig:
    queues: List[int]
    fg: str
    bg: str
    px: int
    py: int
    row: int
    col: int
    font: List[Any]
    time_blink: int

@dataclass
class UIComponents:
    datetime: List[DateTimeConfig]
    videoplayer: List[VideoPlayerConfig]
    work_call: List[WorkCallConfig]
    wait_screen: List[WaitScreenConfig]

@dataclass
class UIConfig:
    win_geometry: str
    win_bg_img: str
    fg: str
    bg: str
    components: UIComponents

@dataclass
class ModeSubComponent:
    weight: int
    type: str
    view: int

@dataclass
class ModeColumn:
    components: List[ModeSubComponent]
    weight: int

@dataclass
class AppConfig:
    """Основная структура вашего JSON конфигурационного файла."""
    id: str
    host: HostConfig
    ui: UIConfig
    mode: int
    modes: List[List[ModeColumn]]

def read_settings_wplace():
    with open('sb05_wplace.json', 'r', encoding='utf-8') as data2:
        # словарь описания "окон"
        raw_dict = json.load(data2)
        return {
            key: from_dict(data_class=WorkPlaceConfig, data=value) 
            for key, value in raw_dict.items()
        }

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
        config = json.load(data1)
        mode_index: int = config["mode"]
        list_dM: List[ModeColumn] = config["modes"][mode_index]
        dM = []
        for item in list_dM:
            dM.append(from_dict(data_class=ModeColumn, data=item))
    return dM

@dataclass
class V:
    # Класс базовых переменных
    # dW - json словарь/описание рабочих мест "окон"
    # dH - json словарь параметров запуска сервиса: хост/порт/аутентификация
    # dU - json словарь параметров UI
    # lW - пустой список, заполнится в процессе рисования графических объектов
    dW: Dict[str, WorkPlaceConfig] = field(default_factory=read_settings_wplace)
    dH: HostConfig = field(default_factory=read_settings_host)
    dU: UIConfig = field(default_factory=read_settings_ui)
    dM: List[ModeColumn] = field(default_factory=read_settings_mode)
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

