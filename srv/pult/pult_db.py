import asyncio
import time
import aiohttp
import threading
from typing import Callable, List, TypedDict, Union
from pult_log import log_debug
from pult_types import TPult, TResponseInfoTicket, TResponseMessage, TResponseSetQueue, TSetQueue, TTicket

class TRequest(TypedDict):
    stdout: Union[dict, None]  # Тело ответа
    stderr: str # Сообщение об ошибке

class TPultSize(TypedDict):
    width: int
    height: int

class ThreadLoop:
    def __init__(self, funcRequest: Callable[[str], TRequest], path: str, min_time: float, max_time: float, func: Callable):
        self.new_loop: asyncio.AbstractEventLoop = None
        self.min_time = min_time
        self.max_time = max_time
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
        time_out = max(self.max_time, self.max_time - (time.time() - self.min_time))
        self.func(data, time_out)

class DataBase:
    oper_id: str = ''
    setDevice: TSetQueue = {}
    ticket: TTicket = {
        'id': '',
        'queue_id': '',
        'title': '----'
    }
    queues: List[str] = []
    pult: TPultSize = {
      'width': 0,
      'height': 0
    }
    
    def __init__(self, setPult: TPult):
        self.setPult = setPult

    def setOperId(self, oper_id: str):
        self.oper_id = oper_id

    def setTicket(self, ticket: TTicket):
        self.ticket = ticket

    def getTicket(self) -> TTicket:
        return self.ticket

    def setDeviceSetting(self, setDevice: TSetQueue):
        self.setDevice = setDevice
        self.setInitialSetting()

    def setInitialSetting(self):
        for item in self.setDevice['queues']:
            self.queues.append(item['id'])

    def addInQueues(self, queue) -> bool:
        if queue in self.queues:
            self.queues.remove(queue)
            return False
        else:
            self.queues.append(queue)
            return True

    async def request(self, path: str) -> TRequest:
        data = {'stdout': None, 'stderr': ''}
        param = f"is10_09?sSd_=0&sfil_n={self.setPult['fil']}&stst_=0&shead_=0&style_=2&"
        url = self.setPult['eq_url'] + param + path
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

    def getDataPult(self, func: Callable[[TResponseSetQueue], None]):
        """
        Получить настройки пульта
        """
        # svid_=1&sgr_l=360&sit_l=936&oper_id=4&led_tablo_id=3
        path = "svid_=1&sgr_l=360&sit_l=936"
        path += f"&oper_id={self.oper_id}&led_tablo_id={self.setPult['eq_wplace']}"
        ThreadLoop(self.request, path, time.time(), 0, func)

    def getNextTicket(self, func: Callable[[TResponseInfoTicket, float], None]):
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
        queues_ids = ','.join([x for x in self.queues])
        path = "svid_=1&sgr_l=360&sit_l=22"
        path += f"&oper_id={self.oper_id}&led_tablo_id={self.setDevice['led_tablo']['id']}"
        path += f"&queues_ids={queues_ids}&month_id={self.setDevice['month_id']}"
        path += f"&led_tablo_port={self.setDevice['led_tablo']['port']}"
        path += f"&led_tablo_title={self.setDevice['led_tablo']['title']}"
        path += f"&adapter_setting={self.setDevice['adapter_setting']}"
        ThreadLoop(self.request, path, time.time(), self.setPult['ui']['timeout_next'], func)

    def getCurrentTicket(self, func: Callable[[TResponseInfoTicket, float], None]):
        """
        Получить текущий талон

        Пример ответа:
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
        path += f"&oper_id={self.oper_id}&led_tablo_id={self.setDevice['led_tablo']['id']}"
        path += f"&month_id={self.setDevice['month_id']}"
        path += f"&led_tablo_port={self.setDevice['led_tablo']['port']}"
        path += f"&led_tablo_title={self.setDevice['led_tablo']['title']}"
        path += f"&adapter_setting={self.setDevice['adapter_setting']}"
        ThreadLoop(self.request, path, time.time(), self.setPult['ui']['timeout_next'], func)

    def getAbortTicket(self, func: Callable[[TResponseMessage, float], None]):
        """
        Получить результат прерывания обслуживания

        Пример ответа:
        {
          "stdout": {
            "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
          },
          "stderr": ""
        }
        """
        # svid_=1&sgr_l=360&sit_l=25&ticket_id=1&user_id=2&month_id=3&led_tablo_port=2323&adapter_setting=192.168.10.15#192.168.10.20,32109,1#192.168.10.20,32105#klient_talon,TTT,proidite,okno_nomer,NNN
        path = f"svid_=1&sgr_l=360&sit_l=25"
        path += f"&ticket_id={self.ticket['id']}&user_id={self.setDevice['user_id']}"
        path += f"&month_id={self.setDevice['month_id']}"
        path += f"&led_tablo_port={self.setDevice['led_tablo']['port']}"
        path += f"&adapter_setting={self.setDevice['adapter_setting']}"
        ThreadLoop(self.request, path, time.time(), 0, func)

    def getFinishTicket(self, func: Callable[[TResponseMessage, float], None]):
        # svid_=1&sgr_l=360&sit_l=936&oper_id=4&led_tablo_id=3
        path = f"svid_=1&sgr_l=360&sit_l=936&oper_id={self.oper_id}&led_tablo_id={self.setDevice['led_tablo']['id']}"
        ThreadLoop(self.request, path, time.time(), self.setPult['ui']['timeout_next'], func)

    def getBackgroudTicket(self, func: Callable[[TResponseInfoTicket, float], None], comment: str):
        """
        Отложить текущий талон
        """
        # 
        path = f"svid_=1&sgr_l=360&sit_l=25"
        path += f"&ticket_id={self.ticket['id']}&user_id={self.setDevice['user_id']}"
        path += f"&message={comment}"
        path += f"&month_id={self.setDevice['month_id']}"
        path += f"&led_tablo_port={self.setDevice['led_tablo']['port']}"
        path += f"&adapter_setting={self.setDevice['adapter_setting']}"
        ThreadLoop(self.request, path, time.time(), 0, func)