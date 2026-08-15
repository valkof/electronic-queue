import customtkinter as ctk
import tkinter as tk
from dataclasses import dataclass, field
from typing import List
from PIL import Image
from sb05_vars import V
from modules.layouts.videoplayer import FrameVideoplayer as FVP
from modules.layouts.datetime import FrameDateTime as FDT
from modules.layouts.work_call import FrameWorkCall as FWC
from modules.layouts.wait_screen import FrameWaitScreen as FWS

@dataclass
class TIComponents:
    videoplayer: List[FVP]
    datetime: List[FDT]
    work_call: List[FWC]
    wait_screen: List[FWS]

COMPONENT_REGISTRY = {
    "videoplayer": FVP,
    "datetime": FDT,
    "work_call": FWC,
    "wait_screen": FWS
}

class ScoreBoard:
    instans_components: TIComponents = {
        "videoplayer": [],
        "datetime": [],
        "work_call": [],
        "wait_screen": []
    }

    def __init__(self, master: tk.Tk, v: V):
        #root.option_add("*Font", "roman 100")
        # master.option_add("*Background", "white")
        # master.option_add("*Foreground", "black")
#        master.option_add( "*font", "Comic Sans MS" )
        master.configure(background=v.dU.bg)
        master.title('Очередь. Инфотабло.')
        master.geometry(v.dU.win_geometry)
        master.attributes('-fullscreen', True)
        master.is_fullscreen = True
        master.bind("<Double-Button-1>", lambda event: self.toggle_fullscreen(master, event))
        fontd40 = ("Noto Sans Mono CJK TC", 60, "bold")
        fontd40_ = ("Noto Sans Mono CJK TC", 60)

        master.resizable(False, False)
        win_H = master.winfo_screenheight()
        win_W = master.winfo_screenwidth()
        master.rowconfigure(0, minsize=win_H)  # Единственная строка
        master.columnconfigure(0, minsize=win_W)
        master_frame = ctk.CTkFrame(master, bg_color=v.dU.bg, fg_color=v.dU.fg)
        master_frame.grid(row=0, column=0, sticky="nsew", padx=v.dU.px, pady=v.dU.py)
        master_frame.rowconfigure(0, minsize=win_H - 2* v.dU.py)
        # Настраиваем столбцы
        for i, column in enumerate(v.dM):
            master_frame.columnconfigure(i, minsize=(win_W - 2* v.dU.px) * column.weight / 100)
            frame = ctk.CTkFrame(master_frame, bg_color=v.dU.bg, fg_color=v.dU.fg)
            frame.grid(row=0, column=i, sticky="nsew")
            frame.columnconfigure(0, minsize=(win_W - 2* v.dU.px) * column.weight / 100)
            # Настраиваем компоненты
            for j, row in enumerate(column.components):
                frame.rowconfigure(j, minsize=(win_H - 2* v.dU.py) * row.weight / 100)
                cls = COMPONENT_REGISTRY[row.type]
                params = {
                    "parent": frame,
                    "config": getattr(v.dU.components, row.type)[row.view],
                }
                params["size"] = {
                    "w": (win_W - 2* v.dU.px) * column.weight / 100 - 2 * getattr(params["config"], "px"),
                    "h": (win_H - 2* v.dU.py) * row.weight / 100 - 2 * getattr(params["config"], "py")
                }
                if row.type == "work_call":
                    params["wplace"] = v.dW
                    params["hsize"] = (win_H - 2* v.dU.py) * getattr(params["config"], "hsize")/100
                instance: ctk.CTkFrame = cls(**params)
                self.instans_components[row.type].append(instance)
                instance.grid(**{
                    "row": j,
                    "column": 0,
                    "padx": getattr(params["config"], "px"),
                    "pady": getattr(params["config"], "py"),
                    "sticky": "nsew"
                })


        # self.imgheart = tkinter.PhotoImage(file = "images/h4.gif")
        # self.bgimg = tkinter.PhotoImage(file=v.dU.win_bg_img)
        # self.lbgimg = tkinter.Label(master, i=self.bgimg)
        # self.lbgimg.pack()
        
        # фотозаставка
        # folder_image_path = os.path.join(os.getcwd(), "images")
        # file_image_path = os.path.join(folder_image_path, 'screen.jpg')
        # if os.path.isfile(file_image_path):
        #     self.screen = ctk.CTkImage(
        #         light_image=Image.open(file_image_path)
        #         # size=(1200, 800)  # Размер изображения
        #     )
        #     self.label_screen = ctk.CTkLabel(self.frame_left_player, image=self.screen, text='')
        # else:
        #     self.label_screen = ctk.CTkLabel(self.frame_left_player, text='')
        
    # def put_photo(self):
    #     width = self.frame_left_player.winfo_width() * 3/4
    #     height = self.frame_left_player.winfo_height() * 3/4
    #     self.screen.configure(size=(width, height))
    #     self.label_screen.grid(row=0, column=0, pady=0, padx=0, sticky="nsew")
        
    def toggle_fullscreen(self, master, event=None):
        # Инвертируем состояние
        master.is_fullscreen = not master.is_fullscreen
        
        # Устанавливаем атрибут полноэкранного режима
        master.attributes("-fullscreen", master.is_fullscreen)
        
        # Если выходим из полноэкранного режима, полезно принудительно 
        # вернуть фокус, чтобы окно не "спряталось"
        if not master.is_fullscreen:
            master.deiconify()

    def ticketShow(self, idElement: int, ticketTitle: str):
        for frame in self.instans_components["work_call"]:
            frame.ticketShow(idElement, ticketTitle)

    def ticketWaitShow(self, idElement: int, ticketTitle: str, action: int):
        for frame in self.instans_components["wait_screen"]:
            frame.ticketShow(idElement, ticketTitle, action)

    def play_video(self):
        for frame in self.instans_components["videoplayer"]:
            frame.play_video() 