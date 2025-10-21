from urllib.parse import quote_plus
import customtkinter as ctk

from pult_types import TMediator, TResponseMessage
from pult_db import DataBase
# from ..elements.LockableButton import LockableButton

class FrameBackgroud(ctk.CTkFrame):
    """
    Фрейм для отмены талона с указанием причины
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        self._mediator = mediator
        self._db = db

        ctk.CTkLabel(self, text="● Отложить талон", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")
        
        f_ticket = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        f_ticket.grid(row=1, column=0, sticky="ew")
        # f_aside_ticket.configure(border_width=1, border_color="blue")
        f_ticket.columnconfigure(index=0, weight=1)
        
        self.text_ticket = ctk.CTkEntry(f_ticket, placeholder_text="Описание талона")
        self.text_ticket.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), sticky="ew")

        self.but_ticket = ctk.CTkButton(f_ticket, fg_color="transparent",
                                            text="Отложить талон", 
                                            border_width=2, text_color=("gray10", "#DCE4EE"),
                                            command=self.ticket_cancel)
        self.but_ticket.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), sticky="ew")

    def ticket_cancel(self):
        comment = quote_plus(self.text_ticket.get())
        self.text_ticket.delete(0, 300)
        self._mediator.state('background')
        self._db.getBackgroudTicket(self.callback_ticket_cancel, comment)

    def callback_ticket_cancel(self, data: TResponseMessage, time_out: float):
        print(data)
        if data['stderr'] != '':
            self._mediator.state('background_error', {'message': data['stderr']})
            return
        
        self._db.setTicket({'id': '', 'queue_id': '', 'title': '----'})
        self._mediator.state('background_success', {'message': data['stdout']['message']})
        self._mediator.state('background_success_after', {'time_out': time_out})
    

# ########## Расширенное меню, команда Отложить ##########
#     def eq_asidecurr(self):
#         self.mediator('beg_next')
#         r = {'stdout': None, 'stderr': None}
#         try:
#             path = 'taside?w=' + app_set.dH['eq_wplace'] + '&o=0' + '&d=' + quote_plus(self.text_aside_ticket.get())
#             r = self.get_request(path)
#         except Exception as e:
#             r['stderr'] = str(e) + ". "
        
#         if r['stderr'] is None:
#             self.mess = "Талон " + self.ticket + " отложен."
#             self.ticket = '----'
#             self.mediator('end_notshow')
#         else:
#             self.mess = r['stderr']
#             self.mediator('end_notshow', False)
# ########## Расширенное меню, команда Отложить ##########


    
