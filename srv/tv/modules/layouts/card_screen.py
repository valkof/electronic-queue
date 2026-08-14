import customtkinter as ctk
from typing import TypedDict

from sb05_vars import WaitScreenConfig as Twsc

class ScreenSize(TypedDict):
    w: float
    h: float

class FrameCardScreen(ctk.CTkFrame):
    """
    Фрейм отображения талона в экране ожидания 
    """
    def __init__(self, parent, config: Twsc, ticketTitle: str, size: ScreenSize):
        super().__init__(parent)
        # self.configure(border_width=1, border_color="blue")
        self.pads = {
            "x": 3,
            "y": 3
        }
        self.columnconfigure(0, minsize=size["w"] - 2* self.pads["x"])
        self.rowconfigure(0, minsize=size["h"] - 2* self.pads["y"])
        self.config: Twsc = config

        self.labelTicket = ctk.CTkLabel(self, text=ticketTitle, text_color=config.fg, bg_color=config.bg, font=tuple(config.font), anchor=ctk.CENTER)
        self.labelTicket.grid(row=0, column=0, sticky="nsew")

        # Параметры мигания
        self.blink_interval = 500  # интервал в миллисекундах
        self.blink_time = config.time_blink * 1000  # общее время мигания в миллисекундах
        self.is_visible = True
        self.blinking_task = ""
        self.stop_timer = ""

    def put_to_cell(self, row: int, col: int):
        self.grid(row=row, column=col, sticky="nsew", padx=self.pads["x"], pady=self.pads["y"])

    def start_blinking(self):
        self.stop_blinking()
        self.stop_timer = self.after(self.blink_time, self.stop_blinking)
        self.repeat_blinking()

    def repeat_blinking(self):
        self.toggle_visibility()
        self.blinking_task = self.after(self.blink_interval, self.repeat_blinking)

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.labelTicket.configure(text_color=self.config.fg)  # делаем видимым
        else:
            self.labelTicket.configure(text_color=self.config.bg)  # делаем невидимым

    def stop_blinking(self):
        if self.blinking_task:
            self.after_cancel(self.blinking_task)
        if self.stop_timer:
            self.after_cancel(self.stop_timer)
        self.labelTicket.configure(text_color=self.config.fg)  # возвращаем видимое состояние
        self.is_visible = True

    def set_text(self, text: str):
        """
        Задать текст в блоке
        """
        self.labelTicket.configure(text=text)
        