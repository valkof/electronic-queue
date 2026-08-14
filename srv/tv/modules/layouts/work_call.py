import customtkinter as ctk
from typing import Dict, List, TypedDict

from sb05_vars import WorkCallConfig as Twcc
from sb05_vars import WorkPlaceConfig as Twpc
from .card_call import FrameCardCall as CardCall

class PlaceCardDict(TypedDict):
    id: int
    card: CardCall

class ScreenSize(TypedDict):
    w: float
    h: float

class FrameWorkCall(ctk.CTkFrame):
    """
    Фрейм отображения вызовов на рабочие места
    """
    def __init__(self, parent, config: Twcc, size: ScreenSize, wplace: Dict[str, Twpc], hsize: int):
        super().__init__(parent, fg_color=config.fg, bg_color=config.bg)
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, minsize=hsize)
        self.rowconfigure(1, weight=1)

        #  Создаем фрейм шапки
        frame_header = ctk.CTkFrame(self)
        frame_header.grid(row=0, column=0, sticky="nsew")
        frame_header.rowconfigure(0, weight=1)
        frame_header.columnconfigure(0, weight=1)
        frame_header.columnconfigure(1, weight=1)

        header_left = ctk.CTkFrame(frame_header)
        header_left.grid(row=0, column=0, sticky="nsew")
        header_left.columnconfigure(0, weight=1)
        header_left.rowconfigure(0, weight=1)

        label_header_left = ctk.CTkLabel(header_left, text=config.lh, text_color=config.fg, bg_color=config.bg, font=tuple(config.font), anchor=ctk.CENTER)
        label_header_left.grid(row=0, column=0, sticky="nsew")

        header_right = ctk.CTkFrame(frame_header)
        header_right.grid(row=0, column=1, sticky="nsew")
        header_right.columnconfigure(0, weight=1)
        header_right.rowconfigure(0, weight=1)

        label_header_right = ctk.CTkLabel(header_right, text=config.rh, text_color=config.fg, bg_color=config.bg, font=tuple(config.font), anchor=ctk.CENTER)
        label_header_right.grid(row=0, column=0, sticky="nsew")
        
        #  Создаем фрейм тела
        self.frame_body = ctk.CTkFrame(self, fg_color=config.bg, bg_color=config.bg)
        self.frame_body.grid(row=1, column=0, sticky="nsew")
        self.frame_body.columnconfigure(0, weight=1)

        # Создаем элементы
        self.elementsWplace: List[PlaceCardDict] = []
        for i, place in enumerate(config.wps):
            self.frame_body.rowconfigure(i, weight=1)
            card = CardCall(self.frame_body, wplace[place], config.time_blink)
            card.put_to_row(i)
            self.elementsWplace.append({'id': place, 'card': card})

    def ticketShow(self, idElement: int, ticketTitle: str):
        index = next((i for i, el in enumerate(self.elementsWplace) if el['id'] == str(idElement)), None)
        if index is None:
            return
        self.frame_body.grid_propagate(False)
        element = self.elementsWplace.pop(index)  # Удаляем элемент по индексу 2
        element['card'].set_text(ticketTitle)
        self.elementsWplace.insert(0, element)  # Вставляем его в начало
        
        for i, el in enumerate(self.elementsWplace):
            el['card'].put_to_row(i)
        self.frame_body.update_idletasks()
        self.frame_body.grid_propagate(True)
        element['card'].start_blinking()


