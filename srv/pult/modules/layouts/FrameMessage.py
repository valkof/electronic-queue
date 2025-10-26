import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase

class FrameMessage(ctk.CTkFrame):
    """
    Фрейм для отображения сообщений
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=10, height=50, bg_color='transparent', fg_color="#434B4D")
        # self.configure(border_width=1, border_color="blue")

        # self._mediator = mediator
        # self._db = db

        self.lmess = ctk.CTkLabel(
            self, text='', text_color="red",
            # bg_color='#434B4D',
            bg_color='transparent',
            font=ctk.CTkFont(family='Helvetica', weight='bold', size=14),
            corner_radius=10
        )
        self.lmess.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

    def show_message(self, text=''):
        self.lmess.configure(text=text)
        self.lmess.after(3 * 1000, self.clear_message)

    def clear_message(self):
        self.lmess.configure(text='')