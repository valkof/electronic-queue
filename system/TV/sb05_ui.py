import customtkinter
import tkinter
# from tkinter import *
import time
from date_time import get_date_time


class ScoreBoard:
    def __init__(self, master, v):
        global cur_time
        cur_time = ''
        #root.option_add("*Font", "roman 100")
        master.option_add("*Background", "white")
        master.option_add("*Foreground", "black")
#        master.option_add( "*font", "Comic Sans MS" )
        master.configure(background='white')
        master.title('Очередь. Инфотабло.')
        master.attributes('-fullscreen', True)
        # master.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+1280+0")
        master.geometry(v.dU["win_geometry"])
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
        self.bgimg = tkinter.PhotoImage(file=v.dU["win_bg_img"])
        self.lbgimg = tkinter.Label(master, i=self.bgimg)
        self.lbgimg.pack()

        self.headertime = tkinter.Label(
                    master,
                    text=cur_time,
                    font=tuple(v.dU["clock"]["font"]),
                    fg=v.dU["clock"]["fg_bg"][0],
                    bg=v.dU["clock"]["fg_bg"][1])

        self.headertime.place(
                x=v.dU["clock"]["xy"][0],
                y=v.dU["clock"]["xy"][1],
                anchor='e')

        # self.lW = v.lW
        for key in v.dW:
            id = int(key)
            xp = v.dW[key]['wplace_xy'][0]
            yp = v.dW[key]['wplace_xy'][1]
            xt = v.dW[key]['wticket_xy'][0]
            yt = v.dW[key]['wticket_xy'][1]
            tct = v.dW[key]['wticket_fg_bg'][0]  # color text ticket
            tcp = v.dW[key]['wplace_fg_bg'][0]  # color text place
            btct = v.dW[key]['wticket_fg_bg'][1]  # color text ticket
            btcp = v.dW[key]['wplace_fg_bg'][1]  # color text place
            ft = tuple(v.dW[key]['wticket_font'])  # font text ticket
            fp = tuple(v.dW[key]['wplace_font'])  # font text place

            self.wticket0 = customtkinter.CTkLabel(
                        master, text="----",
                        text_color=(tct),
                        bg_color=btct,
                        font=ft)
            v.lW.insert(id, self.wticket0)
            self.wplace0 = customtkinter.CTkLabel(
                        master, text=v.dW[key]['wplace_name'],
                        text_color=(tcp),
                        bg_color=btcp,
                        font=fp)
            self.wticket0.place(x=xt, y=yt, anchor=tkinter.W)
            self.wplace0.place(x=xp, y=yp, anchor=tkinter.W)
        self.lW = v.lW

        def timetick():
            global cur_time
            newtime = time.strftime('%d.%m.%Y.%H.%M')
            if newtime != cur_time:
                cur_time = newtime
                text_time = get_date_time(newtime, v.dU["clock"]["mode"])
                self.headertime.configure(text=text_time)
            self.headertime.after(29000, timetick)
        timetick()

    def wticket0_set(self, id, new_ticket):
        # В перспективе, сделать плагины-примочки
        # для мигания талона, иконок
        # for number in range(3):
        self.lW[id].configure(text='    ')
        time.sleep(0.5)
        self.lW[id].configure(text=new_ticket)
        time.sleep(0.5)
        self.lW[id].configure(text='    ')
        time.sleep(0.5)
        self.lW[id].configure(text=new_ticket)
        time.sleep(0.5)
        self.lW[id].configure(text='    ')
        time.sleep(0.5)
        self.lW[id].configure(text=new_ticket)
        time.sleep(0.5)
        self.lW[id].configure(text='    ')
        time.sleep(0.5)
        self.lW[id].configure(text=new_ticket)
        time.sleep(0.5)
        self.lW[id].configure(text='    ')
        time.sleep(0.5)
        self.lW[id].configure(text=new_ticket)
        time.sleep(0.5)
        self.lW[id].configure(text='    ')
        time.sleep(0.5)
        self.lW[id].configure(text=new_ticket)
        return new_ticket
