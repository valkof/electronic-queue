import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
from ..elements.ButtonQueue import ButtonQueue

class FrameQueues(ctk.CTkFrame):
    """
    Фрейм кнопок для управления очередями
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="green")
        self.columnconfigure(index=[0,1,2], weight=1, minsize=int(db.pult["width"] *  1/4 * db.setPult['ui']['scaling']))
        self.rowconfigure(index=[0,1], weight=1, minsize=db.pult['height'] *  1/4 * db.setPult['ui']['scaling'])

        self._mediator = mediator
        self._db = db

        self.buttons: dict[str, ButtonQueue] = {}
        # self.bqueue_: dict[str, ctk.CTkButton] = {}
        # self.lqueue_: dict[str, ctk.CTkLabel] = {}
        
        self.buttons_create()

    def buttons_create(self):
        column: int = 0
        row: int = 0
        for item in self._db.setDevice['queues']:
            button = ButtonQueue(self, self._mediator, self._db, item)
            button.grid(row=row, column=column, padx=(0, 0), pady=(3, 3), ipadx=0, ipady=0, sticky="we")
            # button.configure(border_width=1, border_color="green")
            self.buttons[item['id']] = button
            if column < 2:
                column += 1
            else:
                column = 0
                row += 1

        # setLenQueue()

    # def setLenQueue():
    #     for key, value in dLenQueue.items():
    #         self.lqueue_[key].configure(text=str(value))
    #     self.l_len_aside.configure(text=self.count_aside)
        
    #     for key, value in dLenQueue.items():
    #         try:
    #             path = 'qlen?q=' + key
    #             dLenQueue[key] = self.get_request(path)["stdout"]
    #         finally:
    #             pass
    #     try:
    #         path = 'qlen?q=' + app_set.dH['eq_wplace']
    #         self.count_aside = 'Отлож. ' + str(self.get_request(path)["stdout"])
    #     finally:
    #         pass    
    #     self.after(app_set.dH["ui"]["timeout_check"]*1000, setLenQueue)

    def buttons_lock(self):
        for _, item in self.buttons.items():
            item.lock()

    def buttons_unlock(self):
        for _, item in self.buttons.items():
            item.unlock()