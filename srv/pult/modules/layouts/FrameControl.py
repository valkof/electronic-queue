import customtkinter as ctk

from pult_types import TMediator, TResponseInfoTicket
from pult_db import DataBase
from ..elements.LockableButton import LockableButton

class FrameControl(ctk.CTkFrame):
    """
    Фрейм кнопок для управления талоном
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")

        self._mediator = mediator
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
        self.b_finish.lock()
        self.b_finish.grid_remove()

    def equqe_next(self):
        self.b_next.lock()
        self._mediator.state('next')
        self._db.getNextTicket(self.callback_equqe_next)
    
    def callback_equqe_next(self, data: TResponseInfoTicket, time_out: float):
        print(data)
        if data['stderr'] != '':
            self._mediator.state('next_error', {'message': data['stderr']})
            self.b_next.unlock()
            return
        
        self._db.setTicket(data['stdout']['ticket'])
        self.b_finish.grid()
        self.b_next.grid_remove()
        self._mediator.state('next_success', {'message': data['stdout']['message']})
        self.b_finish.after(time_out * 1000, self.b_finish.unlock)
        self.b_next.after(time_out * 1000, self._mediator.state, 'next_success_after')

    def equqe_curr(self):
        self.b_curr.lock()

    def equqe_abort(self):
        self.b_abort.lock()

    def equqe_finish(self):
        self.b_finish.lock()

    def buttons_lock(self):
        self.b_next.lock()
        self.b_curr.lock()
        self.b_abort.lock()
        self.b_finish.lock()
