import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
# from ..elements.LockableButton import LockableButton

class FrameReserve(ctk.CTkFrame):
    """
    Фрейм для отображения отложенных талонов
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        # self._mediator = mediator
        self._db = db

        
        ctk.CTkLabel(self, text="● Отложенные талоны", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

        self.f_tickets = ctk.CTkScrollableFrame(self, corner_radius=10, bg_color='#434B4D', fg_color="transparent", height=110)
        self.f_tickets.grid(row=1, column=0, sticky="ew", padx=(3, 3), pady=(3, 3))
        # self.f_tickets.configure(border_width=1, border_color="red")
        self.f_tickets._scrollbar.configure(height=0)
        self.f_tickets.columnconfigure(index=[0,1,2], weight=1)


    
