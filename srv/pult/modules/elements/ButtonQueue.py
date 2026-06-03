import functools
import customtkinter as ctk

from pult_types import TMediator, TQueue
from pult_db import DataBase
from .LockableButton import LockableButton

class ButtonQueue(ctk.CTkFrame):
    """
    Кнопка для управления очередью
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase, queue: TQueue):
        super().__init__(parent, corner_radius=0, fg_color='transparent')
        self.columnconfigure(index=0, weight=1)
        # self.configure(border_width=1, border_color="blue")

        self._mediator = mediator
        self._db = db

        self.ticket_count = '0'
        self.status_shake = False
        # self.state = True
        self.queue = queue

        self.button = LockableButton(
            self, text=queue['title'],
            command=functools.partial(self.button_toggle_state)
        )
        self.main_color = self.button.cget("fg_color")
        self.label_bg_color = self.button.cget("bg_color")
        self.second_color = '#AA4A44'
        self.button.configure(anchor="w", fg_color=self.second_color, hover_color=self.second_color)
        self.button.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky='we')

        self.label = ctk.CTkLabel(
            self,
            text='980',
            # text=str(dLenQueue[key]),
            font=ctk.CTkFont(weight="normal"),
            width=20, height=20,
            corner_radius=5,
            fg_color=self.label_bg_color,
            bg_color=self.second_color
        )
        self.label.grid(row=0, column=0, padx=(3, 7), pady=(3, 3), ipadx=0, ipady=0, sticky="e")

        self.update_count_tickets()

    def lock(self):
        self.button.lock()

    def unlock(self):
        self.button.unlock()

    def button_toggle_state(self):
        if self.status_shake:
            self.shake_stop()
            state = self._db.addInQueues(self.queue['id'], True)
        else:
            state = self._db.addInQueues(self.queue['id'])
            self._mediator.state('button_queue_toggle_state')
        if state:
            self.facade_inv()
        else:
            self.facade()

    def update_count_tickets(self):
        count = self._db.getCountQueueTickets(self.queue['id'])
        self.label.configure(text=f"{count}")
        # print(f"Отложено - {count}")
        isQueue = self._db.isInQueues(self.queue['id'])
        if self.ticket_count == '0' and self.ticket_count != count and not self.status_shake and isQueue:
            self._mediator.state('app_deiconify')
            self.status_shake = True
            self.shake()
        self.ticket_count = count
        if self.ticket_count == '0' and self.status_shake and isQueue:
            self.status_shake = False
        self.label.after(5 * 1000, self.update_count_tickets)

    def shake(self):
        # self.b_next.grid(pady=(1, 5))
        if self.status_shake:
            self.button.after(0 * 100, lambda: self.facade())
            self.button.after(5 * 100, lambda: self.facade_inv())
            self.button.after(10 * 100, lambda: self.shake())
        # print(f"Отложено")

    def shake_stop(self):
        self.status_shake = False

    def facade(self):
        self.button.configure(fg_color=self.main_color, hover_color=self.main_color)
        self.label.configure(bg_color=self.main_color)

    def facade_inv(self):
        self.button.configure(fg_color=self.second_color, hover_color=self.second_color)
        self.label.configure(bg_color=self.second_color)
