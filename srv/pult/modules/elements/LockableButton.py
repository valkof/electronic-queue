import customtkinter as ctk

from pult_types import TTicket

class LockableButton(ctk.CTkButton):
    _ticket: TTicket = {
        'id': '',
        'queue_id': '',
        'title': '----',
        'time': ''
    }
    
    def __init__(self, master, text = "Кнопка", command = None, font_style = "normal"):
        super().__init__(master, text = text, command=command)

        self.configure(font=ctk.CTkFont(weight=font_style))

    def lock(self):
        """Метод блокировки кнопки"""
        self.configure(state=ctk.DISABLED)

    def unlock(self):
        """Метод разблокировки кнопки"""
        self.configure(state=ctk.NORMAL)

    def setTicket(self, ticket: TTicket):
        """Метод установить талон"""
        self._ticket = ticket

    def getTicket(self) -> TTicket:
        """Метод получения талона"""
        return self._ticket