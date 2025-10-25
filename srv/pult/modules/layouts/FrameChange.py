import functools
import customtkinter as ctk

from pult_types import TMediator, TQueue, TResponseMessage
from pult_db import DataBase
from ..elements.LockableButton import LockableButton

class FrameChange(ctk.CTkFrame):
    """
    Фрейм для перемещения талона в другую очередь
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        self._mediator = mediator
        self._db = db
        self.buttons = {}

        ctk.CTkLabel(self, text="● Перевести талон в другую очередь", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

        self.f_ticket = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f_ticket.grid(row=1, column=0, sticky="nsew")
        # f_ticket.configure(border_width=1, border_color="green")
        self.f_ticket.columnconfigure(index=[0,1,2,3], weight=1, minsize=db.pult["width"] *  1/4 * db.setPult['ui']['scaling'])
        self.buttons_create()

    def buttons_create(self):
        column: int = 0
        row: int = 0
        for item in self._db.setDevice["queues_delay"]:
            button = LockableButton(self.f_ticket, item["title"], command=functools.partial(self.change_queue, item))
            button.grid(row=row, column=column, padx=(3, 3), pady=(3, 3), ipadx=0, ipady=0, sticky="e")
            self.buttons[item['id']] = button
            if column < 2:
                column += 1
            else:
                column = 0
                row += 1
        

    def change_queue(self, queue: TQueue):
        self._mediator.state('change_queue')
        self._db.getChangeQueue(self.callback_change_queue, queue)

    def callback_change_queue(self, data: TResponseMessage, time_out: float):
        if data['stderr'] != '':
            self._mediator.state('change_queue_error', {'message': data['stderr']})
            return
        
        self._db.setTicket({'id':'', 'queue_id': '', 'title': '----', 'time': ''})
        self._mediator.state('change_queue_success', {'message': data['stdout']['message']})
        self._mediator.state('change_queue_success_after', {'time_out': time_out})
    

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