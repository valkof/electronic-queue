import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
# from ..elements.LockableButton import LockableButton

class FrameChange(ctk.CTkFrame):
    """
    Фрейм для перемещения талона в другую очередь
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        # self._mediator = mediator
        self._db = db

        ctk.CTkLabel(self, text="● Перевести талон в другую очередь", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

        f_ticket = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        f_ticket.grid(row=1, column=0, sticky="nsew")
        # f_ticket.configure(border_width=1, border_color="green")
        f_ticket.columnconfigure(index=[0,1,2], weight=1)
# #         i_col = 0
# #         n_col = 3
# #         for key in app_set.dE.items():
# #             row = i_col // n_col
# #             col = i_col - row * n_col
# #             button = ctk.CTkButton(f_redir_ticket, text=app_set.dE[key[0]]["shortname"], fg_color="transparent",
# #                                   border_width=2, font=ctk.CTkFont(weight="normal"), text_color=("gray10", "#DCE4EE"),
# #                                   anchor="c", command=functools.partial(self.change_queue_w, key[0]))
# #             button.grid(row=row, column=col, padx=(3, 3), pady=(2, 2), sticky="ew")
# #             i_col += 1



    # def eq_asidecurr(self):
    #     pass
    

#     def change_queue_w(self, queue_id):
#         self.mediator('beg_next')
#         r = {'stdout': None, 'stderr': None}
#         try:
#             path = 'tchange?w=' + app_set.dH['eq_wplace'] + '&o=0' + '&q=' + str(queue_id)
#             r = self.get_request(path)
#         except Exception as e:
#             r['stderr'] = str(e) + ". "
        
#         if r['stderr'] is None:
#             self.mess = "Талон " + self.ticket + " перемещен в очередь " + app_set.dE[queue_id]["name"] + "."
#             self.ticket = '----'
#             self.mediator('end_notshow')
#         else:
#             self.mess = r['stderr']
#             self.mediator('end_notshow', False)