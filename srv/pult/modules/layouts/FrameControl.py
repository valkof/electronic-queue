import customtkinter as ctk

from pult_types import TMediator, TResponseInfoTicket, TResponseMessage
from pult_db import DataBase
from ..elements.LockableButton import LockableButton

class FrameControl(ctk.CTkFrame):
    """
    Фрейм кнопок для управления талоном
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=[0,1,2], weight=1, minsize=db.pult["width"] *  1/4 * db.setPult['ui']['scaling'])
        self.rowconfigure(index=0, weight=1, minsize=db.pult['height'] *  1/4 * db.setPult['ui']['scaling'])

        self._mediator = mediator
        self._db = db

        self.b_next = LockableButton(self, text="➜ Следующий", command=self.queue_next)
        self.b_next.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        self.b_next.grid_remove()

        self.b_curr = LockableButton(self, text="⟳ Повторить", command=self.queue_curr)
        self.b_curr.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.b_abort = LockableButton(self, text="✖ Не явился", command=self.queue_abort)
        self.b_abort.grid(row=0, column=2, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.b_finish = LockableButton(self, text="✔ Обслужен", command=self.queue_finish)
        self.b_finish.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        # self.b_finish.grid_remove()

    def queue_next(self):
        self.buttons_lock()
        self._mediator.state('next')
        self._db.getNextTicket(self.callback_queue_next)
    
    def callback_queue_next(self, data: TResponseInfoTicket, time_out: float):
        # print(data)
        if data['stderr'] != '':
            self._mediator.state('next_error', {'message': data['stderr']})
            self.b_next.unlock()
            return
        
        self._db.setTicket(data['stdout']['ticket'])
        self._mediator.state('next_success', {'message': data['stdout']['message']})
        self.next_state(time_out)

    def queue_curr(self):
        self.buttons_lock()
        self._mediator.state('current')
        self._db.getCurrentTicket(self.callback_queue_curr)

    def callback_queue_curr(self, data: TResponseInfoTicket, time_out: float):
        # print(data)
        if data['stderr'] != '':
            if data['stderr'] == 'Нет доступных талонов':
                self.callback_queue_abort(data={'stdout':{'message':'Нет доступных талонов'},'stderr':''}, time_out=time_out)
                return

            self._mediator.state('current_error', {'message': data['stderr']})
            self.b_finish.unlock()
            self.b_abort.unlock()
            self.b_curr.unlock()
            return
        
        self._db.setTicket(data['stdout']['ticket'])
        self._mediator.state('current_success', {'message': data['stdout']['message']})
        self.b_finish.after(time_out * 1000, self.b_finish.unlock)
        self.b_curr.after(time_out * 1000, self.b_curr.unlock)
        self.b_abort.after(time_out * 1000, self.b_abort.unlock)
        self.b_next.after(time_out * 1000, self._mediator.state, 'current_success_after')

    def queue_abort(self):
        # print('ok')
        self.buttons_lock()
        self._mediator.state('abort')
        self._db.getAbortTicket(self.callback_queue_abort)

    def callback_queue_abort(self, data: TResponseMessage, time_out: float):
        # print(data)
        if data['stderr'] != '':
            self._mediator.state('abort_error', {'message': data['stderr']})
            self.b_curr.unlock()
            self.b_finish.unlock()
            self.b_abort.unlock()
            return
        
        self._db.setTicket({'id':'', 'queue_id': '', 'title': '----', 'time': ''})
        self._mediator.state('abort_success', {'message': data['stdout']['message']})
        self.begin_state(time_out)

    def queue_finish(self):
        self.buttons_lock()
        self._mediator.state('finish')
        self._db.getFinishTicket(self.callback_queue_finish)

    def callback_queue_finish(self, data: TResponseMessage, time_out: float):
        # print(data)
        if data['stderr'] != '':
            self._mediator.state('abort_error', {'message': data['stderr']})
            self.b_curr.unlock()
            self.b_finish.unlock()
            self.b_abort.unlock()
            return
        
        self._db.setTicket({'id':'', 'queue_id': '', 'title': '----', 'time': ''})
        self._mediator.state('abort_success', {'message': data['stdout']['message']})
        self.begin_state(time_out)

    def begin_state(self, time_out: float):
        self.b_next.grid()
        self.b_finish.grid_remove()
        self.b_next.after(time_out * 1000, self.b_next.unlock)
        self.b_next.after(time_out * 1000, self._mediator.state, 'finish_success_after')
    
    def next_state(self, time_out: float):
        self.b_finish.grid()
        self.b_next.grid_remove()
        self.b_curr.after(time_out * 1000, self.b_curr.unlock)
        self.b_finish.after(time_out * 1000, self.b_finish.unlock)
        self.b_next.after(time_out * 1000, self._mediator.state, 'next_success_after')
        
    def buttons_lock(self):
        self.b_next.lock()
        self.b_curr.lock()
        self.b_abort.lock()
        self.b_finish.lock()
