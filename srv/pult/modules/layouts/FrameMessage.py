import customtkinter as ctk

from pult_config import AppSet
from pult_types import TMediator

class FrameMessage(ctk.CTkFrame):
    """
    Фрейм для отображения информации о текущем талоне
    """
    def __init__(self, parent, mediator: TMediator, app_set: AppSet):
        super().__init__(parent, corner_radius=0, height=50, bg_color='#434B4D', fg_color="transparent")
        # self.configure(border_width=1, border_color="blue")

        # self._mediator = mediator
        # self._app_set = app_set

        self.lmess = ctk.CTkLabel(
            self, text="Привет", text_color="red",
            bg_color='#434B4D',
            font=ctk.CTkFont(family='Helvetica', weight='bold', size=14)
        )
        self.lmess.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")