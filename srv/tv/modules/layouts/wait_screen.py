import customtkinter as ctk
from typing import Dict, List, Optional, TypedDict

from sb05_vars import WaitScreenConfig as Twsc
# from sb05_vars import WorkPlaceConfig as Twpc
from .card_screen import FrameCardScreen as CardScreen

class ScreenCardDict(TypedDict):
    title: str
    card: CardScreen

class ScreenSize(TypedDict):
    w: float
    h: float

class FrameWaitScreen(ctk.CTkFrame):
    """
    Фрейм отображения ожидающих талонов в очереди
    """
    def __init__(self, parent, config: Twsc, size: ScreenSize):
        super().__init__(parent, fg_color=config.bg, bg_color=config.bg)
        # self.configure(border_width=1, border_color="blue")
        self.cell_w = size['w'] / config.col
        self.cell_h = size['h'] / config.row
        for i in range(config.row):
            self.rowconfigure(i, minsize=self.cell_h )
        for i in range(config.col):
            self.columnconfigure(i, minsize=self.cell_w)

        self.config: Twsc = config
        self.s_size: ScreenSize = size
        self.elementsTicket: List[ScreenCardDict] = []

        # Создаем элементы
        # self.elementsWplace: List[PlaceCardDict] = []
        # for i, place in enumerate(config.wps):
        #     self.frame_body.rowconfigure(i, weight=1)

    def ticketShow(self, wqueue: str, ticketTitle: str, waction: str):
        if int(wqueue) not in self.config.queues:
            return
        found_index: Optional[int]
        found_card: Optional[CardScreen]
        found_index, found_card = next(
            (
                (index, item["card"])
                for index, item in enumerate(self.elementsTicket)
                if item["title"] == ticketTitle
            ),
            (None, None),
        )
        # found_card: Optional[CardScreen] = next(
        #     (item['card'] for item in self.elementsTicket if item["title"] == ticketTitle), 
        #     None
        # )
        if found_card is None:
            if int(waction) == 0:
              card = CardScreen(self, self.config, ticketTitle, {'w': self.cell_w, 'h': self.cell_h})
              self.elementsTicket.append({'title': ticketTitle, 'card': card})
              self.grid_propagate(False)
              for i, item in enumerate(self.elementsTicket):
                  x = i % self.config.col
                  y = i // self.config.col
                  item['card'].put_to_cell(y, x)
              self.update_idletasks()
              self.grid_propagate(True)
              card.start_blinking()
              return
            return

        if (int(waction) == 1) and (found_index is not None):
            found_card.destroy()
            found_card is None
            self.elementsTicket.pop(found_index)
            print(found_index)
            self.grid_propagate(False)
            for i, item in enumerate(self.elementsTicket):
                x = i % self.config.col
                y = i // self.config.col
                item['card'].put_to_cell(y, x)
            self.update_idletasks()
            self.grid_propagate(True)
            print("wqd")
            return

        found_card.start_blinking()    



