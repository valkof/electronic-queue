import functools
import customtkinter as ctk

from pult_types import TMediator, TResponseInfoTicket, TResponseInfoTickets, TTicket
from pult_db import DataBase
from ..elements.LockableButton import LockableButton
# from ..elements.LockableButton import LockableButton

class FrameTablo(ctk.CTkFrame):
    """
    Фрейм для отображения талонов в очередях
    """
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(index=0, weight=1)

        self._mediator = mediator
        self._db = db

        ctk.CTkLabel(self, text="● Талоны в выбранных очередях", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

        self.f_tickets = ctk.CTkScrollableFrame(self, corner_radius=10, bg_color='#434B4D', fg_color="transparent", height=110)
        self.f_tickets.grid(row=1, column=0, sticky="ew", padx=(3, 3), pady=(3, 3))
        # self.f_mark_tickets.configure(border_width=1, border_color="red")
        self.f_tickets._scrollbar.configure(height=0)
        self.f_tickets.columnconfigure(index=[0,1,2], weight=1,  minsize=int(db.pult["width"] *  1/3 * db.setPult['ui']['scaling']))

    def update_tickets(self):
        for widget in self.f_tickets.winfo_children():
            widget.destroy()

        # self._mediator.state('abort')
        self._db.getTabloTickets(self.callback_update_tickets)

    def callback_update_tickets(self, data: TResponseInfoTickets, time_out: float):
        # print(data)
        if data['stderr'] != '':
            self._mediator.state('tablo_error', {'message': data['stderr']})
            return
        
        column: int = 0
        row: int = 0
        for item in data['stdout']['tickets']:
            text = f"{item['title']}   Время: {item['time']}"
            button = LockableButton(
                self.f_tickets, text=text,
                command=functools.partial(self.button_click, item)
            )
            button.setTicket(item)
            button.configure(
                fg_color="transparent", width=170, border_width=2,
                text_color=("gray10", "#DCE4EE")
            )
            button.grid(row=row, column=column, padx=(3, 3), pady=(3, 3), sticky="w")
            if column < 2:
                column += 1
            else:
                column = 0
                row += 1

    def button_click(self, ticket: TTicket):
        self._mediator.state('select_ticket')
        self._db.getSelectTicket(self.callback_button_click, ticket, '1')
    
    def callback_button_click(self, data: TResponseInfoTicket, time_out: float):
        if data['stderr'] != '':
            self._mediator.state('select_ticket_error', {'message': data['stderr']})
            return
        
        self._db.setTicket(data['stdout']['ticket'])
        self._mediator.state('select_ticket_success', {'message': data['stdout']['message']})
        self._mediator.state('select_ticket_success_after', {'time_out': time_out})