import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
from .FrameTablo import FrameTablo
from .FrameReserve import FrameReserve
# from ..elements.LockableButton import LockableButton

class FrameTickets(ctk.CTkFrame):
    """
    Фрейм для отображения ожидающих талонов
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        # self._mediator = mediator
        self._db = db

        self.f_reserve = FrameReserve(self, mediator, db)
        self.f_reserve.grid(row=0, column=0, sticky="nsew")

        self.f_tablo = FrameTablo(self, mediator, db)
        self.f_tablo.grid(row=1, column=0, sticky="nsew")


#     def eq_queuelist(self, queue_id, tick_name=''):
#         self.mediator('beg_next')
#         r = {'stdout': None, 'stderr': None}
#         try:
#             path = 'tnextbyname?w=' + app_set.dH['eq_wplace'] + '&q=' + str(queue_id) + '&n=' + quote_plus(tick_name)
#             r = self.get_request(path)
#         except Exception as e:
#             r['stderr'] = str(e) + ". "
        
#         self.mess = r['stderr']
#         if r['stdout'] is None:
#             self.ticket = '----'
#             self.mediator('end_next', False)
#         else:
#             self.ticket = r['stdout'][0]
#             self.mediator('end_next')
#             self.bmain_curr.after(app_set.dH["ui"]["timeout_next"]*1000, self.mediator, 'end_next_timeout') 

    
