import customtkinter as ctk

class LockableButton(ctk.CTkButton):
    def __init__(self, master, text = "Кнопка", command = None, font_style = "normal"):
        super().__init__(master, text = text, command=command)

        self.configure(font=ctk.CTkFont(weight=font_style))

    def lock(self):
        """Метод блокировки кнопки"""
        self.configure(state=ctk.DISABLED)

    def unlock(self):
        """Метод разблокировки кнопки"""
        self.configure(state=ctk.NORMAL)