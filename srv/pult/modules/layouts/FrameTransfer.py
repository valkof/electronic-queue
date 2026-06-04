from urllib.parse import quote_plus
import customtkinter as ctk

from pult_types import TMediator, TResponseMessage
from pult_db import DataBase
from ..elements.LockableButton import LockableButton

class FrameTransfer(ctk.CTkFrame):
    """
    Фрейм для перемещения талонов в другую очередь
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        self._mediator = mediator
        self._db = db

        ctk.CTkLabel(self, text="● Переместить все ожидающие и отложенные талоны в другую очередь", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")
        
        f_work = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        f_work.grid(row=1, column=0, sticky="ew")
        # f_aside_ticket.configure(border_width=1, border_color="blue")

        f_work.grid_columnconfigure(0, weight=1)
        f_work.grid_columnconfigure(1, weight=1)
        f_work.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(f_work, text="Из очереди", text_color="white").grid(row=0, column=0, padx=(10, 10), pady=(2, 0), sticky="w")
        ctk.CTkLabel(f_work, text="В очередь", text_color="white").grid(row=0, column=1, padx=(10, 10), pady=(2, 0), sticky="w")
        

        self.queues = {item['title']: item['id'] for item in self._db.setDevice["queues"]}
        self.queues_delay = {item['title']: item['id'] for item in self._db.setDevice["queues_delay"]} 

        # В values передаем ключи (title) созданного словаря DEPT_MAP
        self.combo_1 = ctk.CTkOptionMenu(master=f_work, values=list(self.queues.keys()))
        self.combo_1.grid(row=1, column=0, padx=10, pady=(1, 10), sticky="ew")
        self.combo_1.set("Откуда?") 

        # Заполняем второй список ключами из SERV_MAP
        self.combo_2 = ctk.CTkOptionMenu(master=f_work, values=list(self.queues_delay.keys()))
        self.combo_2.grid(row=1, column=1, padx=10, pady=(1, 10), sticky="ew")
        self.combo_2.set("Куда?")

        self.btn_send = LockableButton(master=f_work, text="Перевести", command=self.send_data)
        self.btn_send.grid(row=1, column=2, columnspan=2, padx=10, pady=(1, 10), sticky="ew")

    def send_data(self):
        # Получаем выбранный текст
        selected_queue = self.combo_1.get()
        selected_queue_delay = self.combo_2.get()
        
        # Ищем ID по тексту
        queue_id = self.queues.get(selected_queue)
        queue_delay_id = self.queues_delay.get(selected_queue_delay)
        
        # Проверка на выбор заглушки
        if not queue_id or not queue_delay_id:
            self._mediator.state('tablo_error', {'message': 'Ошибка: Выберите значения из обоих списков!'})
            return
        
        if queue_id == queue_delay_id:
            self._mediator.state('tablo_error', {'message': 'Ошибка: Выберите разные очереди!'})
            return
            
        # Передаем чистые ID дальше
        print(f"Отправка на сервер -> ID Отделения: {queue_id} | ID Услуги: {queue_delay_id}")
        self.btn_send.lock()
        self._db.transferTickets(self.callback_send_data, queue_id, queue_delay_id)

    def callback_send_data(self, data: TResponseMessage, time_out: float):
        self.btn_send.unlock()
        if data['stderr'] != '':
            self._mediator.state('abort_error', {'message': data['stderr']})
            return
        
        self._mediator.state('tablo_error', {'message': data['stdout']['message']})