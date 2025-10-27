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
        state = self._db.addInQueues(self.queue['id'])
        if state:
            self.button.configure(fg_color=self.second_color, hover_color=self.second_color)
            self.label.configure(bg_color=self.second_color)
        else:
            self.button.configure(fg_color=self.main_color, hover_color=self.main_color)
            self.label.configure(bg_color=self.main_color)

    def update_count_tickets(self):
        count = self._db.getCountQueueTickets(self.queue['id'])
        self.label.configure(text=f"{count}")
        # print(f"Отложено - {count}")
        self.label.after(5 * 1000, self.update_count_tickets)
