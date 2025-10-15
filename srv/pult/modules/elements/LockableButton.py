import customtkinter as ctk

class LockableButton(ctk.CTkButton):
    def __init__(self, master, text = "Кнопка", command = None, font_style = "normal"):
        super().__init__(master, text = text, command=command)

        self.action = None
        self.configure(font=ctk.CTkFont(weight=font_style))
    # def handle_click(self):
    #     """Обработчик нажатия кнопки"""
    #     if self.cget("state") == ctk.NORMAL:
    #         self.lock()

    def lock(self):
        """Метод блокировки кнопки"""
        self.configure(state=ctk.DISABLED)
        # print(self)
        # print(self.cget("state"))
        self.action = self._command
        self._command = None

        # self.button.config(text="Заблокировано")

    def unlock(self):
        """Метод разблокировки кнопки"""
        self.configure(state=ctk.NORMAL)
        self._command = self.action
        # self.button.config(text=self.text)