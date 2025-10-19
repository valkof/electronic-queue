import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
from ..elements.LockableButton import LockableButton

class FrameTicket(ctk.CTkFrame):
    """
    Фрейм для отображения информации о текущем талоне
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1, minsize=db.pult["width"] *  1/4 * db.setPult['ui']['scaling'])
        self.rowconfigure(index=[0,1,2], weight=1, minsize=db.pult["height"] *  1/4 * db.setPult['ui']['scaling'])

        # self._mediator = mediator
        self._db = db

        self.LTicket = ctk.CTkLabel(self, text="----", font=ctk.CTkFont(size=24, weight="bold"))
        self.LTicket.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.BOption = LockableButton(self, text="Дополнительно", command=self.open_adv_opt)
        self.BOption.grid(row=1, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        
        self.LMessage = ctk.CTkLabel(self, text="Отлож. 0", font=ctk.CTkFont(weight="normal"))
        self.LMessage.grid(row=2, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

    def open_adv_opt(self):
        if self._mediator._app.ticket:  # есть номер талона
            # self.router(self.f_cur_ticket)
            pass
        else:  # нет выбранного талона
            # self.router(self.f_work)
            pass
        
    def button_lock(self):
        self.BOption.lock()
        
    def button_unlock(self):
        self.BOption.unlock()

    def show_ticket(self):
        ticket = self._db.getTicket()
        self.LTicket.configure(text=ticket["title"])

    
