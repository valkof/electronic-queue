import asyncio
import aiohttp
import threading
from typing import Callable, TypedDict, Union
from pult_log import log_debug
from pult_types import TPult, TResponseSetQueue, TSetQueue

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

    def getDataPult(
            self, min_time: float, func: Callable[[TResponseSetQueue], None],
            oper_id: str, led_tablo_id: str
        ):
        """
        Получить настройки пульта
        """
        # svid_=1&sgr_l=360&sit_l=936&oper_id=4&led_tablo_id=3
        path = "svid_=1&sgr_l=360&sit_l=936"
        path += f"&oper_id={oper_id}&led_tablo_id={led_tablo_id}"
        ThreadLoop(self.request, path, min_time, func)

    def getNextTicket(
            self, min_time: float, func: Callable[[TResponseSetQueue], None],
            oper_id: str, oper_set: TSetQueue
        ):
        """
        Получить следующий талон
        
        Пример ответа:
        {
          "stdout": {
            "ticket": {
              "id": "5",
              "title": "Р002",
              "queue_id": "1"
            },
            "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
          },
          "stderr": ""
        }
        """
        # svid_=1&sgr_l=360&sit_l=22&oper_id=4&led_tablo_id=3&queues_ids=1&month_id=3&led_tablo_port=2323&led_tablo_title=1&adapter_setting=192.168.10.15#192.168.10.20,32109,1#192.168.10.20,32105#klient_talon,TTT,proidite,okno_nomer,NNN
        queues_ids = ','.join([x['id'] for x in oper_set['queues']])
        path = "svid_=1&sgr_l=360&sit_l=22"
        path += f"&oper_id={oper_id}&led_tablo_id={oper_set['led_tablo']['id']}"
        path += f"&queues_ids={queues_ids}&month_id={oper_set['month_id']}"
        path += f"&led_tablo_port={oper_set['led_tablo']['port']}"
        path += f"&led_tablo_title={oper_set['led_tablo']['title']}"
        path += f"&adapter_setting={oper_set['adapter_setting']}"
        ThreadLoop(self.request, path, min_time, func)

    def getCurrentTicket(
            self, min_time: float, func: Callable[[TResponseSetQueue], None],
            oper_id: str, oper_set: TSetQueue
        ):
        """
        Получить текущий талон
        {
          "stdout": {
            "ticket": {
              "id": "1",
              "title": "Р001",
              "queue_id": "1"
            },
            "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
          },
          "stderr": ""
        }
        """
        # svid_=1&sgr_l=360&sit_l=23&oper_id=4&led_tablo_id=3&month_id=3&led_tablo_port=2323&led_tablo_title=1&adapter_setting=192.168.10.15#192.168.10.20,32109,1#192.168.10.20,32105#klient_talon,TTT,proidite,okno_nomer,NNN
        path = "svid_=1&sgr_l=360&sit_l=23"
        path += f"&oper_id={oper_id}&led_tablo_id={oper_set['led_tablo']['id']}"
        path += f"&month_id={oper_set['month_id']}"
        path += f"&led_tablo_port={oper_set['led_tablo']['port']}"
        path += f"&led_tablo_title={oper_set['led_tablo']['title']}"
        path += f"&adapter_setting={oper_set['adapter_setting']}"
        ThreadLoop(self.request, path, min_time, func)

    def getAbortTicket(
            self, min_time: float, func: Callable[[TResponseSetQueue], None],
            ticket_id: str, oper_set: TSetQueue
        ):
        """
        Получить результат прерывания обслуживания
        {
          "stdout": {
            "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
          },
          "stderr": ""
        }
        """
        # svid_=1&sgr_l=360&sit_l=25&ticket_id=1&user_id=2&month_id=3&led_tablo_port=2323&adapter_setting=192.168.10.15#192.168.10.20,32109,1#192.168.10.20,32105#klient_talon,TTT,proidite,okno_nomer,NNN
        path = f"svid_=1&sgr_l=360&sit_l=25"
        path += f"&ticket_id={ticket_id}&user_id={oper_set['user_id']}"
        path += f"&month_id={oper_set['month_id']}"
        path += f"&led_tablo_port={oper_set['led_tablo']['port']}"
        path += f"&adapter_setting={oper_set['adapter_setting']}"
        ThreadLoop(self.request, path, min_time, func)

    def getFinishTicket(self, min_time: float, func: Callable[[TResponseSetQueue], None], oper_id: str, wplace_id: str):
        # svid_=1&sgr_l=360&sit_l=936&oper_id=4&led_tablo_id=3
        path = f"svid_=1&sgr_l=360&sit_l=936&oper_id={oper_id}&led_tablo_id={wplace_id}"
        ThreadLoop(self.request, path, min_time, func)