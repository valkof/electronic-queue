import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
from .FrameTransfer import FrameTransfer
# from ..elements.LockableButton import LockableButton

class FrameAllCancel(ctk.CTkFrame):
    """
    Фрейм для отмены талонов
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        # self._mediator = mediator
        self._db = db

        self.f_сhange = FrameTransfer(self, mediator, db)
        self.f_сhange.grid(row=1, column=0, sticky="nsew")