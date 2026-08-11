import time
import customtkinter as ctk

from sb05_vars import DateTimeConfig as Tdtc

class FrameDateTime(ctk.CTkFrame):
    """
    Фрейм отображения даты и времени
    """
    cur_time: str = ""

    def __init__(self, parent, config: Tdtc):
        super().__init__(parent, fg_color=config.bg)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # self._mediator = mediator

        self.headertime = ctk.CTkLabel(self, text="", font=tuple(config.font), text_color=config.fg, bg_color=config.bg)
        self.headertime.grid(row=0, column=0, sticky="nsew")
        self.timetick(config.mode)

    def timetick(self, mode):
        newtime = time.strftime('%d.%m.%Y.%H.%M')
        if newtime != self.cur_time:
            self.cur_time = newtime
            text_time = self.get_date_time(newtime, mode)
            self.headertime.configure(text=text_time)
            print(text_time)
        self.after(1000, self.timetick, mode)

    def get_date_time(self, date, mode=0):
        # if mode<>1: strftime '11.04.24.01.24' as '11 апреля 2024г. 01:24'
        # if mode=1: strftime '11.04.24.01.24' as
        #    '11 апреля 2024г.
        #         01:24'

        month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                      'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        date_list = date.split('.')
        chr_ = ''
        if mode == 1:
            chr_ = chr(10)
        text_time = (
            date_list[0] + ' ' + month_list[int(date_list[1]) - 1] +
            ' ' + date_list[2] + 'г. ' + chr_ + date_list[3] + ':' + date_list[4])
        return text_time
    

