import customtkinter as ctk
from ...pult import Mediator

class FrameControl(ctk.CTkFrame):
    """
    Фрейм кнопок для управления талоном
    """
    def __init__(self, parent, mediator: Mediator):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")

        self._mediator = mediator


        self.bmain_next = ctk.CTkButton(self, text="➜ Следующий",
                                        font=ctk.CTkFont(weight="bold")) #,
                                        #TODO command=self.eq_nexts_w)
        self.bmain_next.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        self.bmain_next.grid_remove()

        self.bmain_curr = ctk.CTkButton(self, text="⟳ Повторить",
                                        font=ctk.CTkFont(weight="bold")) #,
                                        #TODO command=self.eq_curr_w)
        self.bmain_curr.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.bmain_notshow = ctk.CTkButton(self, text="✖ Не явился",
                                           font=ctk.CTkFont(weight="bold")) #,
                                           #TODO command=self.eq_notshow_w)
        self.bmain_notshow.grid(row=0, column=2, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.bmain_end = ctk.CTkButton(self, text="✔ Обслужен",
                                       font=ctk.CTkFont(weight="bold")) #,
                                       #TODO command=self.eq_end_w)
        self.bmain_end.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
