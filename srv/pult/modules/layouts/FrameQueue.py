import customtkinter as ctk

from pult_config import AppSet
from pult_types import TMediator
from pult_db import DataBase
from .FrameTicket import FrameTicket
from .FrameControl import FrameControl
from .FrameQueues import FrameQueues
from .FrameMessage import FrameMessage

class FrameQueue(ctk.CTkFrame):
    def __init__(self, parent, mediator: TMediator, app_set: AppSet, db: DataBase):
        super().__init__(parent)

        # self._mediator = mediator
        # self._app_set = app_set
        
        self.router_pages = []

        mainPanel = ctk.CTkFrame(self)
        mainPanel.grid(row=0, column=0, sticky="nsew")
        mainPanel.columnconfigure(index=0, weight=1)
        self.f_ticket = FrameTicket(mainPanel, mediator, app_set).grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.f_control = FrameControl(mainPanel, mediator, app_set).grid(row=0, column=1, sticky="ew")
        self.f_queues = FrameQueues(mainPanel, mediator, app_set).grid(row=1, column=1, sticky="nsew")
        
        self.f_message = FrameMessage(self, mediator, app_set)
        self.f_message.grid(row=1, column=0, sticky="ew", padx=(5, 5))
        self.f_message.columnconfigure(index=0, weight=1)
