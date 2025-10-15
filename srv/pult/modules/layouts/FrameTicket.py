import customtkinter as ctk

from pult_config import AppSet
from pult_types import TMediator

class FrameTicket(ctk.CTkFrame):
    """
    Фрейм для отображения информации о текущем талоне
    """
    def __init__(self, parent, mediator: TMediator, app_set: AppSet):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")

        # self._mediator = mediator
        # self._app_set = app_set

        self.LTicket = ctk.CTkLabel(self, text="----", font=ctk.CTkFont(size=24, weight="bold"))
        self.LTicket.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.BOption = ctk.CTkButton(self, text="Дополнительно", font=ctk.CTkFont(weight="normal"), command=self.open_adv_opt)
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
