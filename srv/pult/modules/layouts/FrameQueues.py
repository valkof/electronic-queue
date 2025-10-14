import customtkinter as ctk

from ..elements.ButtonQueue import ButtonQueue
from ...pult_vars import AppSet
from ...pult import Mediator

class FrameQueues(ctk.CTkFrame):
    """
    Фрейм кнопок для управления очередями
    """
    def __init__(self, parent, mediator: Mediator, app_set: AppSet):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="green")

        self._mediator = mediator
        self._app_set = app_set

        self.buttons_create()

    def buttons_create(self):
        self.buttons: dict[str, ButtonQueue] = {}
        # self.bqueue_: dict[str, ctk.CTkButton] = {}
        # self.lqueue_: dict[str, ctk.CTkLabel] = {}
        column: int = 0
        row: int = 0
        for item in self._app_set.place['queues']:
            button = ButtonQueue(self, self._mediator, item)
            button.grid(row=row, column=column, padx=(3, 10), pady=(3, 3), ipadx=0, ipady=0, sticky="e")
            self.buttons[item['id']] = button
            if column < 2:
                column + 1
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
