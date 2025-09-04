import os
import platform
import vlc
import customtkinter as ctk
import tkinter as tk
# from tkinter import *
import time
from date_time import get_date_time

class CardCall:
    def __init__(self, parent, data, timeout):
        self.card = ctk.CTkFrame(parent, border_width=5, border_color="blue")
        
        card_left = ctk.CTkFrame(self.card)
        card_right = ctk.CTkFrame(self.card)

        self.card.columnconfigure(0, weight=1)
        self.card.columnconfigure(1, weight=1)
        self.card.rowconfigure(0, weight=1)
        
        card_left.grid(row=0, column=0, sticky="nsew")
        card_right.grid(row=0, column=1, sticky="nsew")

        self.tct = data['wticket_fg_bg'][0]  # color text ticket
        self.btct = data['wticket_fg_bg'][1]  # color text ticket
        ft = tuple(data['wticket_font'])  # font text ticket
        
        self.labelTicket = ctk.CTkLabel(card_left, text="----", text_color=(self.tct), bg_color=self.btct, font=ft, anchor=ctk.CENTER)
        card_left.columnconfigure(0, weight=1)
        card_left.rowconfigure(0, weight=1)
        self.labelTicket.grid(row=0, column=0, sticky="nsew")

        tcp = data['wplace_fg_bg'][0]  # color text place
        btcp = data['wplace_fg_bg'][1]  # color text place
        fp = tuple(data['wplace_font'])  # font text place

        labelWplace = ctk.CTkLabel(card_right, text=data['wplace_name'], text_color=(tcp), bg_color=btcp, font=fp, anchor=ctk.CENTER)
        card_right.columnconfigure(0, weight=1)
        card_right.rowconfigure(0, weight=1)
        labelWplace.grid(row=0, column=0, sticky="nsew")

        # Параметры мигания
        self.blink_interval = 500  # интервал в миллисекундах
        self.blink_time = timeout * 1000  # общее время мигания в миллисекундах (10 секунд)
        self.is_visible = True
    
    def put_to_row(self, row):
        self.card.grid(row=row, column=0, sticky="nsew", pady=5)

    def start_blinking(self):
        self.stop_timer = self.card.after(self.blink_time, self.stop_blinking)
        self.repeat_blinking()

    def repeat_blinking(self):
        self.toggle_visibility()
        self.blinking_task = self.card.after(self.blink_interval, self.repeat_blinking)

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.labelTicket.configure(text_color=self.tct)  # делаем видимым
        else:
            self.labelTicket.configure(text_color=self.btct)  # делаем невидимым

    def stop_blinking(self):
        self.card.after_cancel(self.blinking_task)
        self.card.after_cancel(self.stop_timer)
        self.labelTicket.configure(text_color=self.tct)  # возвращаем видимое состояние
        self.is_visible = True
        print('end')

class ScoreBoard:
    def __init__(self, master, v):
        global cur_time
        cur_time = ''
        #root.option_add("*Font", "roman 100")
        # master.option_add("*Background", "white")
        # master.option_add("*Foreground", "black")
#        master.option_add( "*font", "Comic Sans MS" )
        master.configure(background='green')
        master.title('Очередь. Инфотабло.')
        master.geometry(v.dU["win_geometry"])
        master.attributes('-fullscreen', True)
        # master.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+1280+0")
        # master.geometry("800x1600")
#        fontd40 = ("Liberation Mono", 40, "bold") # c точкой на нуле
#        fontd40_ = ("Liberation Mono", 40 )
#        fontd40 = ("Nimbus Mono PS", 50, "bold") #растянутый
#        fontd40_ = ("Nimbus Mono PS", 50)
#        fontd40_ = ("FreeMono", 80, "bold")
#        fontd40 = ("Nimbus Mono PS", 80, "bold")
#        fontd40_ = ("FreeMono", 80)
        fontd40 = ("Noto Sans Mono CJK TC", 60, "bold")
        fontd40_ = ("Noto Sans Mono CJK TC", 60)

#        font_ticket = ("Noto Sans Mono CJK TC", 80, "bold")
        # font_place = ("Nimbus Mono PS", 110, "bold")
        # font_ticket = ("Nimbus Mono PS", 120, "bold")
        # font_clock = ("DejaVu Sans", 60) #растянутый

        master.resizable(False, False)
        # self.imgheart = tkinter.PhotoImage(file = "images/h4.gif")
        # self.bgimg = tkinter.PhotoImage(file=v.dU["win_bg_img"])
        # self.lbgimg = tkinter.Label(master, i=self.bgimg)
        # self.lbgimg.pack()

        # Создаем фреймы (лево-право)
        self.frame_left = ctk.CTkFrame(master, fg_color=v.dU["videoplayer"]["fg_bg"][1])
        self.frame_right = ctk.CTkFrame(master, fg_color=v.dU["videoplayer"]["fg_bg"][1])

        # Размещаем фреймы с весами 1 и 4
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        self.frame_right.grid(row=0, column=1, sticky="nsew", pady=15, padx=15)

        # Настраиваем веса столбцов
        master.columnconfigure(0, weight=2)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(0, weight=1)  # Единственная строка

        # Левый фрейм делим на видеоплеер и время
        self.frame_left_player = ctk.CTkFrame(self.frame_left, fg_color=v.dU["videoplayer"]["fg_bg"][1])
        self.frame_left_time = ctk.CTkFrame(self.frame_left)

        # Настраиваем веса строк
        self.frame_left.columnconfigure(0, weight=1)
        self.frame_left.rowconfigure(0, weight=5)
        self.frame_left.rowconfigure(1, weight=1)

        self.frame_left_player.grid(row=0, column=0, sticky="nsew", pady=15, padx=15)
        self.frame_left_time.grid(row=1, column=0, sticky="nsew")

        self.frame_left_time.columnconfigure(0, weight=1)
        self.frame_left_time.rowconfigure(0, weight=1)
        
        # видеоплеер
        self.instance = vlc.Instance()
 
        self.player = self.instance.media_player_new()
        self.player.audio_set_volume(50)
        self.list_player = self.instance.media_list_player_new()

        folder_path = os.path.join(os.getcwd(), "videos")

        video_filesname = []
        video_filesname += os.listdir(folder_path)
        
        media_list = self.instance.media_list_new()
        for f in video_filesname:
          media = self.instance.media_new(os.path.join(os.getcwd(), "videos", str(f)))
          media_list.add_media(media)

        self.list_player.set_media_list(media_list)
        self.list_player.set_media_player(self.player)
        self.list_player.set_playback_mode(vlc.PlaybackMode.loop)

        # время
        self.headertime = ctk.CTkLabel(self.frame_left_time, text="", font=tuple(v.dU["clock"]["font"]), text_color=v.dU["clock"]["fg_bg"][0], bg_color=v.dU["clock"]["fg_bg"][1])
        self.headertime.grid(row=0, column=0, sticky="nsew")
        self.timetick(v.dU["clock"]["mode"])

        # правый фрейм делим на шапку и тело
        self.frame_right_header = ctk.CTkFrame(self.frame_right)
        self.frame_right_body = ctk.CTkFrame(self.frame_right, fg_color=v.dU["videoplayer"]["fg_bg"][1])
        
        # Настраиваем веса строк
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.rowconfigure(0, weight=1)
        self.frame_right.rowconfigure(1, weight=5)
        
        self.frame_right_header.grid(row=0, column=0, sticky="nsew")
        self.frame_right_body.grid(row=1, column=0, sticky="nsew")

        header = ctk.CTkFrame(self.frame_right_header)
        self.frame_right_header.rowconfigure(0, weight=1)
        self.frame_right_header.columnconfigure(0, weight=1)
        header.grid(row=0, column=0, sticky="nsew")

        header_left = ctk.CTkFrame(header)
        header_right = ctk.CTkFrame(header)

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.rowconfigure(0, weight=1)

        header_left.grid(row=0, column=0, sticky="nsew")
        header_right.grid(row=0, column=1, sticky="nsew")

        label_header_left = ctk.CTkLabel(header_left, text="ТАЛОН", text_color="white", bg_color="green", font=tuple(["Nimbus Mono PS", 60, "bold"]), anchor=ctk.CENTER)
        header_left.columnconfigure(0, weight=1)
        header_left.rowconfigure(0, weight=1)
        label_header_left.grid(row=0, column=0, sticky="nsew")

        label_header_right = ctk.CTkLabel(header_right, text="ОКНО", text_color="white", bg_color="green", font=tuple(["Nimbus Mono PS", 60, "bold"]), anchor=ctk.CENTER)
        header_right.columnconfigure(0, weight=1)
        header_right.rowconfigure(0, weight=1)
        label_header_right.grid(row=0, column=0, sticky="nsew")
        
        # Создаем элементы
        self.elementsWplace = []
        self.frame_right_body.columnconfigure(0, weight=1)  # Первый столбец (1 часть)
        i = 0
        for key in v.dW:
            self.frame_right_body.rowconfigure(i, weight=1)
            card = CardCall(self.frame_right_body, v.dW[key], v.dU["timeout_blink"])
            card.put_to_row(i)
            self.elementsWplace.append({'id': key, 'card': card})
            i += 1

    def timetick(self, mode):
        global cur_time
        newtime = time.strftime('%d.%m.%Y.%H.%M')
        if newtime != cur_time:
            cur_time = newtime
            text_time = get_date_time(newtime, mode)
            self.headertime.configure(text=text_time)
        self.headertime.after(1000, self.timetick, mode)

        
    def play_video(self, filename):
        print(f"Путь {os.path.join('videos', filename)} не найден")
        
        # # Воспроизведение
        print(f"код {self.frame_left_player.winfo_id()}")
        if platform.system() == 'Windows':
          self.player.set_hwnd(self.frame_left_player.winfo_id())
        else:
          self.player.set_xwindow(self.frame_left_player.winfo_id())
        self.list_player.play()
    
    def wticket0_set(self, id, new_ticket):
        index = next((i for i, el in enumerate(self.elementsWplace) if el['id'] == str(id)), None)

        element = self.elementsWplace.pop(index)  # Удаляем элемент по индексу 2
        element['card'].labelTicket.configure(text=new_ticket)
        self.elementsWplace.insert(0, element)  # Вставляем его в начало
        
        for i, el in enumerate(self.elementsWplace):
            el['card'].put_to_row(i)

        element['card'].start_blinking()