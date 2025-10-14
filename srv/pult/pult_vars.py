import asyncio
from dataclasses import dataclass, field
import threading
import tkinter as tk
import aiohttp
import customtkinter as ctk
import json
from typing import Callable, List, TypedDict, Union
from pult_log import log_critical, log_debug
import sys
import requests

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

class TPult(TypedDict):
    eq_wplace: str  # ID рабочего места
    eq_url: str # Адрес сервера
    fil: str  # Номер филиала
    eq_auth: List[str]  # Login, Pass
    ui: TUi
    set: List[List[Union[int, str]]]

class TLedTablo(TypedDict):
    id: str
    title: str
    port: str

class TQueue(TypedDict):
    id: str
    title: str

class TSetQueue(TypedDict):
    user_id: str
    queues: List[TQueue]
    queues_delay: List[TQueue]
    adapter_setting: str
    led_tablo: TLedTablo
    month_id: str
    message: str

class TResponseSetQueue(TypedDict):
    stdout: TSetQueue
    stderr: str

@dataclass
class AppSet:
    """
    Класс базовых переменных

    :param pult: - параметры подключения к серверу
    :param place: - описание рабочего места
    :param queues: - описание очередей обслуживаемых рабочим местом
    """
    pult: TPult
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

class LockableButton(ctk.CTkButton):
    def __init__(self, master, text = "Кнопка", command=None):
        super().__init__(master, text = text, command=command)

        self.action = None
    # def handle_click(self):
    #     """Обработчик нажатия кнопки"""
    #     if self.cget("state") == ctk.NORMAL:
    #         self.lock()

    def lock(self):
        """Метод блокировки кнопки"""
        self.configure(state=ctk.DISABLED)
        # print(self)
        # print(self.cget("state"))
        self.action = self._command
        self._command = None

        # self.button.config(text="Заблокировано")

    def unlock(self):
        """Метод разблокировки кнопки"""
        self.configure(state=ctk.NORMAL)
        self._command = self.action
        # self.button.config(text=self.text)

class TRequest(TypedDict):
    stdout: Union[dict, None]  # Тело ответа
    stderr: str # Сообщение об ошибке


class ThreadLoop:
    def __init__(self, funcRequest: Callable[[str], TRequest], path: str, min_time: float, func: Callable):
        self.new_loop: asyncio.AbstractEventLoop = None
        self.min_time = min_time
        self.func: Callable = func
        self.new_loop = asyncio.new_event_loop()
        thread = threading.Thread(target=self.new_loop.run_forever)
        thread.start()
        loop = asyncio.run_coroutine_threadsafe(funcRequest(path), self.new_loop)
        loop.add_done_callback(self.callbackDataPult)
    
    def callbackDataPult(self, response: asyncio.Future):
        data = response.result()
        print(data)
        self.new_loop.call_soon_threadsafe(self.new_loop.stop)
        self.func(data, self.min_time)

class DataBase:
    def __init__(self, setting: TPult):
        self.setting = setting

    async def request(self, path: str) -> TRequest:
        data = {'stdout': None, 'stderr': ''}
        param = f"is10_09?sSd_=0&sfil_n={self.setting['fil']}&stst_=0&shead_=0&style_=2&"
        url = self.setting['eq_url'] + param + path
        # http://10.0.6.168:88/cgi-bin/is10_09?sSd_=0&sfil_n=19&svid_=1&stst_=0&sgr_l=360&shead_=0&sit_l=936&style_=2&oper_id=4&led_tablo_id=3
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # Проверка на ошибки HTTP
                    data = await response.json()
        except aiohttp.ClientError as e:
            # print(f"Ошибка при запросе к {url}: {e}")
            log_debug("Ошибка при запросе к " + url + " : " + str(e) + ". ")
            data['stderr'] = 'Ошибка c запросом по URL.'
        except asyncio.TimeoutError:
            # print(f"Таймаут при запросе к {url}")
            log_debug("Таймаут при запросе к " + url + ". ")
            data['stderr'] = 'Таймаут при запросе к URL.'             
        return data

    def getDataPult(self, min_time: float, func: Callable[[TResponseSetQueue], None], oper_id: str, wplace_id: str):
        path = f"svid_=1&sgr_l=360&sit_l=936&oper_id={oper_id}&led_tablo_id={wplace_id}"
        ThreadLoop(self.request, path, min_time, func)