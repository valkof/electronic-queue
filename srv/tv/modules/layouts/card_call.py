import customtkinter as ctk

from sb05_vars import WorkPlaceConfig as Twpc

class FrameCardCall(ctk.CTkFrame):
    """
    Фрейм отображения карточки рабочего места
    """
    def __init__(self, parent, config: Twpc, time_blink: int):
        super().__init__(parent)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.pcolor = config.ticket.fg
        self.scolor = config.ticket.bg

        card_left = ctk.CTkFrame(self)
        card_left.grid(row=0, column=0, sticky="nsew")
        card_left.columnconfigure(0, weight=1)
        card_left.rowconfigure(0, weight=1)
        
        self.labelTicket = ctk.CTkLabel(card_left, text="----", text_color=self.pcolor, bg_color=self.scolor, font=tuple(config.ticket.font), anchor=ctk.CENTER)
        self.labelTicket.grid(row=0, column=0, sticky="nsew")

        card_right = ctk.CTkFrame(self)
        card_right.grid(row=0, column=1, sticky="nsew")
        card_right.columnconfigure(0, weight=1)
        card_right.rowconfigure(0, weight=1)
        
        labelWplace = ctk.CTkLabel(card_right, text=config.title, text_color=config.place.fg, bg_color=config.place.bg, font=tuple(config.place.font), anchor=ctk.CENTER)
        labelWplace.grid(row=0, column=0, sticky="nsew")

        # Параметры мигания
        self.blink_interval = 500  # интервал в миллисекундах
        self.blink_time = time_blink * 1000  # общее время мигания в миллисекундах
        self.is_visible = True
        self.blinking_task = ""
        self.stop_timer = ""

    def put_to_row(self, row: int):
        self.grid(row=row, column=0, sticky="nsew", pady=5)

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
            self.labelTicket.configure(text_color=self.pcolor)  # делаем видимым
        else:
            self.labelTicket.configure(text_color=self.scolor)  # делаем невидимым

    def stop_blinking(self):
        if self.blinking_task:
            self.after_cancel(self.blinking_task)
        if self.stop_timer:
            self.after_cancel(self.stop_timer)
        self.labelTicket.configure(text_color=self.pcolor)  # возвращаем видимое состояние
        self.is_visible = True

    def set_text(self, text: str):
        """
        Задать текст в блоке слева
        """
        self.labelTicket.configure(text=text)
        