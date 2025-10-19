import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
from .FrameTickets import FrameTickets
from .FrameTicket import FrameTicket
from .FrameControl import FrameControl
from .FrameQueues import FrameQueues
from .FrameMessage import FrameMessage

class FrameQueue(ctk.CTkFrame):
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent)

        self.columnconfigure(index=0, weight=1, minsize=db.pult["width"] * db.setPult['ui']['scaling'])
        self.rowconfigure(index=0, weight=1, minsize=db.pult["height"] * 3/4 * db.setPult['ui']['scaling'])
        self.rowconfigure(index=1, weight=1, minsize=db.pult["height"] * 1/4 * db.setPult['ui']['scaling'])
        # self._mediator = mediator
        # self._db = db
        
        self.router_pages = []

        mainPanel = ctk.CTkFrame(self)
        mainPanel.grid(row=0, column=0, sticky="nsew")
        mainPanel.columnconfigure(index=0, weight=1, minsize=db.pult["width"] *  1/4 * db.setPult['ui']['scaling'])
        mainPanel.columnconfigure(index=1, weight=1, minsize=db.pult["width"] * 3/4 * db.setPult['ui']['scaling'])
        mainPanel.rowconfigure(index=0, weight=1, minsize=db.pult['height'] * 1/4 * db.setPult['ui']['scaling'])
        mainPanel.rowconfigure(index=1, weight=1, minsize=db.pult['height'] * 2/4 * db.setPult['ui']['scaling'])
        
        self.f_ticket = FrameTicket(mainPanel, mediator, db)
        self.f_ticket.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.f_control = FrameControl(mainPanel, mediator, db)
        self.f_control.grid(row=0, column=1, sticky="ew")
        
        self.f_queues = FrameQueues(mainPanel, mediator, db)
        self.f_queues.grid(row=1, column=1, sticky="nsew")
        
        self.f_message = FrameMessage(self, mediator, db)
        self.f_message.grid(row=1, column=0, sticky="ew", padx=(5, 5))
        
        self.f_tickets = FrameTickets(self, mediator, db)
        self.f_tickets.grid(row=2, column=0, sticky="ew", padx=(5, 5))
        # self.f_tickets.columnconfigure(index=0, weight=1)
