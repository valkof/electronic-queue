import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
from .FrameChange import FrameChange
from .FrameBackgroud import FrameBackgroud
# from ..elements.LockableButton import LockableButton

class FrameCancel(ctk.CTkFrame):
    """
    Фрейм для отмены талонов
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        # self._mediator = mediator
        self._db = db

        self.f_backgroud = FrameBackgroud(self, mediator, db)
        self.f_backgroud.grid(row=0, column=0, sticky="nsew")

        self.f_сhange = FrameChange(self, mediator, db)
        self.f_сhange.grid(row=1, column=0, sticky="nsew")

    
