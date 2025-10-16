import customtkinter as ctk

from pult_config import AppSet
from pult_types import TMediator
from pult_db import DataBase
from ..elements.LockableButton import LockableButton

class FrameControl(ctk.CTkFrame):
    """
    Фрейм кнопок для управления талоном
    """
    def __init__(self, parent, mediator: TMediator, app_set: AppSet, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")

        # self._mediator = mediator
        self._app_set = app_set
        self._db = db

        self.b_next = LockableButton(self, text="➜ Следующий", command=self.equqe_next)
        self.b_next.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        # self.b_next.grid_remove()

        self.b_curr = LockableButton(self, text="⟳ Повторить", command=self.equqe_curr)
        self.b_curr.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.b_abort = LockableButton(self, text="✖ Не явился", command=self.equqe_abort)
        self.b_abort.grid(row=0, column=2, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.b_finish = LockableButton(self, text="✔ Обслужен", command=self.equqe_finish)
        self.b_finish.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        self.b_finish.grid_remove()

    def equqe_next(self):
        self.b_next.lock()
        # self.mediator('beg_next')
        # self._db.getNextTicket(
        #     self._app_set.pult["ui"]["timeout_next"],
        #     self.ewf, self._app_set.pult["eq_wplace"], self._app_set.place
        # )
        # r = {'stdout': None, 'stderr': None}
        # try:
        #     qq = ','.join([x for x in queues])
        #     path = 'tnexts?w=' + app_set.dH['eq_wplace'] + '&qq=' + qq
        #     r = self.get_request(path)
        # except Exception as e:
        #     r['stderr'] = str(e) + ". "
        
        # self.mess = r['stderr']
        # if r['stdout'] is None:
        #     self.ticket = '----'
        #     self.mediator('end_next', False)
        # else:
        #     self.ticket = r['stdout']
        #     self.mediator('end_next')
        #     self.bmain_curr.after(app_set.dH["ui"]["timeout_next"]*1000, self.mediator, 'end_next_timeout')

    def equqe_curr(self):
        self.b_curr.lock()

    def equqe_abort(self):
        self.b_abort.lock()

    def equqe_finish(self):
        self.b_finish.lock()
