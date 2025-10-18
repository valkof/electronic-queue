import customtkinter as ctk

from pult_types import TMediator, TQueue
from .LockableButton import LockableButton

class ButtonQueue(ctk.CTkFrame):
    """
    Кнопка для управления очередью
    """
    def __init__(self, parent, mediator: TMediator, queue: TQueue):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="green")

        self._mediator = mediator

        self.button = LockableButton(
            self, text=queue['title'],
            # command=functools.partial(self.set_queues_w, key)
        )
        self.button.configure(anchor="w")
        self.button.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky='w')

        self.label = ctk.CTkLabel(
            self,
            text='0',
            # text=str(dLenQueue[key]),
            font=ctk.CTkFont(weight="normal"),
            width=20
        )
        self.label.grid(row=0, column=0, padx=(3, 10), pady=(3, 3), ipadx=0, ipady=0, sticky="e")

    def lock(self):
        self.button.lock()

    def unlock(self):
        self.button.unlock()
