#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import threading
from oper09_vars import V
import requests
import json
import tkinter as tk
#import pystray
from PIL import Image
import customtkinter as ctk
from urllib.parse import quote_plus
import functools
# import threading
import time
import datetime
#import os

global v
v = V()
ctk.set_appearance_mode(v.dH["ui"]["mode"])  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme(v.dH["ui"]["theme"])  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_widget_scaling(v.dH["ui"]["scaling"])
ctk.set_window_scaling(v.dH["ui"]["scaling"])
# v.dW['queue'].append(v.dH['eq_wplace'])
print(v.dW)
# v.dE[v.dH['eq_wplace']] = {"name": "Отложенные"}
print(v.dE)
queue = v.dW['queue'][0]
# first_run_app = True
dLenQueue = {}
queues = []
# список очередей по которым делаем запрос о количестве талонов
queues_check = v.dW['queue'].copy()
# добавим отложенную очередь
queues_check.append(v.dH['eq_wplace'])
print("queues_check=", queues_check)
print(queues)
for key, value in v.dE.items():
    dLenQueue[key] = 0
print()
print(dLenQueue)

class EqWin(ctk.CTk):
    def __init__(self):
        super().__init__()

        # self.extmenu = False
        self.ticket = "----"
        self.mess = None
        self.curr_time = datetime.datetime.now()
        self.router_pages = []
        # configure window
        self.title("Пульт оператора")
        self.geometry("600")
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=3)
        self.resizable(False, False)
        self.count_aside = 'Отлож. 0'
        # self.clear_message = lambda: self.lmess = ''
        self.timer_id = None
        

        ########## Виджеты талона ##########
        self.f_ticket = ctk.CTkFrame(self, corner_radius=0)
        # self.f_ticket.configure(border_width=1, border_color="blue")
        self.f_ticket.grid(row=0, column=0, sticky="nsew", rowspan=2)

        self.lmain_tick = ctk.CTkLabel(self.f_ticket, text="???", font=ctk.CTkFont(size=24, weight="bold"))
        self.lmain_tick.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.b_adv_opt = ctk.CTkButton(self.f_ticket, text="Дополнительно", font=ctk.CTkFont(weight="normal"),
                                       command=self.open_adv_opt)
        self.b_adv_opt.grid(row=1, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.l_len_aside = ctk.CTkLabel(self.f_ticket, text="Отлож. 0", font=ctk.CTkFont(weight="normal"))
        self.l_len_aside.grid(row=2, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        ########## Виджеты талона ##########

        ########## Основное меню, виджеты ##########
        self.f_main = ctk.CTkFrame(self, corner_radius=0)
        # self.f_main.configure(border_width=1, border_color="blue")
        self.f_main.grid(row=0, column=1, sticky="ew")

        self.bmain_next = ctk.CTkButton(self.f_main, text="➜ Следующий",
                                        font=ctk.CTkFont(weight="bold"),
                                        command=self.eq_nexts_w)
        self.bmain_next.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        self.bmain_next.grid_remove()

        self.bmain_curr = ctk.CTkButton(self.f_main, text="⟳ Повторить",
                                        font=ctk.CTkFont(weight="bold"),
                                        command=self.eq_curr_w)
        self.bmain_curr.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.bmain_notshow = ctk.CTkButton(self.f_main, text="✖ Не явился",
                                           font=ctk.CTkFont(weight="bold"),
                                           command=self.eq_notshow_w)
        self.bmain_notshow.grid(row=0, column=2, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.bmain_end = ctk.CTkButton(self.f_main, text="✔ Обслужен",
                                       font=ctk.CTkFont(weight="bold"),
                                       command=self.eq_end_w)
        self.bmain_end.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
########## Основное меню, виджеты ##########


########## Меню очереди, виджеты ##########
        self.f_queue = ctk.CTkFrame(self, corner_radius=0)
        # self.f_queue.configure(border_width=1, border_color="green")
        self.f_queue.grid(row=1, column=1, sticky="ew")
        column = 0
        row = 0
        self.bqueue_ = {}
        self.lqueue_ = {}
        for key, value in v.dE.items():
            self.bqueue_[key] = ctk.CTkButton(self.f_queue,
                                              text=v.dE[key]["shortname"],
                                              font=ctk.CTkFont(weight="normal"),
                                              anchor="w",
                                              command=functools.partial(self.set_queues_w, key))
            self.bqueue_[key].grid(row=row, column=column, padx=(3, 3),
                                       pady=(3, 3), ipadx=0, sticky='w')

            self.lqueue_[key] = ctk.CTkLabel(self.f_queue, text=str(dLenQueue[key]),
                                             font=ctk.CTkFont(weight="normal"),
                                             width=20)
            self.lqueue_[key].grid(row=row, column=column, padx=(3, 10), pady=(3, 3), ipadx=0, ipady=0, sticky="e")
            column = 0 if column >= 2 else column + 1
            if (column == 0): row += 1

        def setLenQueue():
            for key, value in dLenQueue.items():
                self.lqueue_[key].configure(text=str(value))
            self.l_len_aside.configure(text=self.count_aside)
            
            for key, value in dLenQueue.items():
                try:
                    path = 'qlen?q=' + key
                    dLenQueue[key] = self.get_request(path)["stdout"]
                finally:
                    pass
            try:
                path = 'qlen?q=' + v.dH['eq_wplace']
                self.count_aside = 'Отлож. ' + str(self.get_request(path)["stdout"])
            finally:
                pass    
            self.after(v.dH["ui"]["timeout_check"]*1000, setLenQueue)
        setLenQueue()
########## Меню очереди, виджеты ##########

########## Сообщения, виджеты##########
        self.f_mess = ctk.CTkFrame(self, corner_radius=0, height=50, bg_color='#434B4D', fg_color="transparent" )
        self.f_mess.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(5, 5))
        # self.f_mess.configure(border_width=1, border_color="blue")
        self.lmess = ctk.CTkLabel(self.f_mess, text="", text_color="red", bg_color='#434B4D')
        self.lmess.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
########## Сообщения, виджеты##########

########## Рабочий фрейм ##########
        self.f_work = ctk.CTkFrame(self, corner_radius=0)
        self.f_work.grid(row=4, column=0, sticky="ew", columnspan=2)
        # self.f_work.configure(border_width=1, border_color="blue")
        self.f_work.columnconfigure(index=0, weight=1)

        ctk.CTkLabel(self.f_work, text="● Отложенные талоны", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

        self.f_aside_tickets = ctk.CTkScrollableFrame(self.f_work, corner_radius=10, bg_color='#434B4D', fg_color="transparent", height=110)
        self.f_aside_tickets.grid(row=1, column=0, sticky="ew", padx=(3, 3), pady=(3, 3))
        # self.f_aside_tickets.configure(border_width=1, border_color="red")
        self.f_aside_tickets._scrollbar.configure(height=0)
        self.f_aside_tickets.columnconfigure(index=[0,1,2], weight=1)

        ctk.CTkLabel(self.f_work, text="● Талоны в выбранных очередях", text_color="white").grid(row=2, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

        self.f_mark_tickets = ctk.CTkScrollableFrame(self.f_work, corner_radius=10, bg_color='#434B4D', fg_color="transparent", height=110)
        self.f_mark_tickets.grid(row=3, column=0, sticky="ew", padx=(3, 3), pady=(3, 3))
        # self.f_mark_tickets.configure(border_width=1, border_color="red")
        self.f_mark_tickets._scrollbar.configure(height=0)
        self.f_mark_tickets.columnconfigure(index=[0,1,2], weight=1)

        self.router_pages.append(self.f_work)
        # self.f_work.grid_remove()
##########  Рабочий фрейм ##########

##########  Фрейм дополнительных функций к текущему талону ##########
        self.f_cur_ticket = ctk.CTkFrame(self, corner_radius=0)
        self.f_cur_ticket.grid(row=5, column=0, sticky="ew", columnspan=2)
        # self.f_cur_ticket.configure(border_width=1, border_color="red")
        self.f_cur_ticket.columnconfigure(index=0, weight=1)
        
        ctk.CTkLabel(self.f_cur_ticket, text="● Отложить талон", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")
        
        f_aside_ticket = ctk.CTkFrame(self.f_cur_ticket, corner_radius=0, fg_color="transparent")
        f_aside_ticket.grid(row=1, column=0, sticky="ew")
        # f_aside_ticket.configure(border_width=1, border_color="blue")
        f_aside_ticket.columnconfigure(index=0, weight=1)
        
        self.text_aside_ticket = ctk.CTkEntry(f_aside_ticket, placeholder_text="Описание талона")
        self.text_aside_ticket.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), sticky="ew")

        self.but_aside_ticket = ctk.CTkButton(f_aside_ticket, fg_color="transparent",
                                            text="Отложить талон", 
                                            border_width=2, text_color=("gray10", "#DCE4EE"),
                                            command=self.eq_asidecurr)
        self.but_aside_ticket.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), sticky="ew")
        
        ctk.CTkLabel(self.f_cur_ticket, text="● Перевести талон в другую очередь", text_color="white").grid(row=2, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

        f_redir_ticket = ctk.CTkFrame(self.f_cur_ticket, corner_radius=0, fg_color="transparent")
        f_redir_ticket.grid(row=3, column=0, sticky="nsew")
        # f_redir_ticket.configure(border_width=1, border_color="green")
        f_redir_ticket.columnconfigure(index=[0,1,2], weight=1)
        col = 0
        row = 0
        for key, value in v.dE.items():
            button = ctk.CTkButton(f_redir_ticket, text=v.dE[key]["shortname"], fg_color="transparent",
                                  border_width=2, font=ctk.CTkFont(weight="normal"), text_color=("gray10", "#DCE4EE"),
                                  anchor="c", command=functools.partial(self.change_queue_w, key))
            button.grid(row=row, column=col, padx=(3, 3), pady=(2, 2), sticky="ew")
            col += 1
            if col >3:
                col =0
                row += 1

        self.router_pages.append(self.f_cur_ticket)
        self.f_cur_ticket.grid_remove()
##########  Фрейм дополнительных функций к текущему талону ##########

########## Запуска пульта проверка на наличие открытого талона ###########
        # global first_run_app
        # if first_run_app:
        self.eq_curr_w()
            # first_run_app = False
        self.set_queues_w(queue)
########## Запуска пульта проверка на наличие открытого талона ##########

########## Роутер ##########
    def router(self, page = None):
        open_page = True
        if page in self.grid_slaves():
            open_page = False
        for element in self.router_pages:
            element.grid_remove()
            self.update_page(page, False)
        if page and open_page:
            self.update_page(page)
            page.grid()

    def update_page(self, page, update=True):
        if page == self.f_work:
            self.eq_queuelist_w(update)
            self.eq_queueslist_w(update)
            
    def clear_message(self):
        self.lmess.configure(text='')

    def show_message(self, message = None):
        if message: self.lmess.configure(text=message)
            
        if self.timer_id: self.timer_id.cancel()
        self.timer_id = threading.Timer(5.0, self.clear_message)
        self.timer_id.start()
########## Роутер ##########

##########   Основное меню, команды обновления фреймов ##########
    def eq_mess_w(self):
        if self.mess:
            # self.bmess_mess.configure(text=self.mess)
            self.f_mess.grid(row=2, column=0, sticky="nsew")
        # else:
        #     self.f_mess.grid_remove()

    def open_adv_opt(self):
        # self.destroy_frame_children(self.f_work)
        # if self.extmenu:
        #     self.f_mess.grid_remove()
        #     self.extmenu = False
        if self.ticket and self.ticket != '???':  # есть номер талона
            # self.extmenu = True
            # self.eq_asidecurr_w()
            self.router(self.f_cur_ticket)
        else:  # нет выбранного талона
            # self.extmenu = True
            self.router(self.f_work)
            # self.eq_queueslist_w()

    def eq_frame_forget(self):
        self.f_work.grid_forget()
        # self.f_mess.grid_forget()


##########   Основное меню, команды обновления фреймов ##########

########## Основное меню, команда Следующий ##########
    def eq_next_w(self):
        self.f_work.grid_remove()
        self.bmain_next.configure(state=tk.DISABLED)
        self.bmain_curr.configure(state=tk.DISABLED)
        self.bmain_notshow.configure(state=tk.DISABLED)
        self.bmain_end.configure(state=tk.DISABLED)
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tnext?w=' + v.dH['eq_wplace'] + '&q=' + queue
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            if r['stdout'] is None:
                self.ticket = '----'
                self.bmain_next.configure(state=tk.NORMAL)
            else:
                self.ticket = r['stdout']
                self.bmain_curr.after(v.dH["ui"]["timeout_next"]*1000, self.btn_timeout_next)
        self.lmain_tick.configure(text=self.ticket)
        # self.title("Следующий в очередь " + v.dW['queue'][0] + '. ' + v.dE[ v.dW['queue'][0] ]['name'])
        self.mess = r['stderr']
        self.eq_mess_w()
        # self.stop_thread()

    def btn_timeout_next(self):
        self.bmain_curr.configure(state=tk.NORMAL)
        self.bmain_end.configure(state=tk.NORMAL)

    def eq_nexts_w(self):
        # self.f_work.grid_remove()
        self.bmain_next.configure(state=tk.DISABLED)
        self.bmain_curr.configure(state=tk.DISABLED)
        self.bmain_notshow.configure(state=tk.DISABLED)
        self.bmain_end.configure(state=tk.DISABLED)
        r = {'stdout': None, 'stderr': None}
        try:
            qq = ','.join([x for x in queues])
            path = 'tnexts?w=' + v.dH['eq_wplace'] + '&qq=' + qq
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            if r['stdout'] is None:
                self.ticket = '???'
                self.bmain_next.configure(state=tk.NORMAL)
            else:
                self.ticket = r['stdout']
                self.bmain_curr.after(v.dH["ui"]["timeout_next"]*1000, self.btn_timeout_next)
                self.bmain_next.grid_remove()
                self.bmain_end.grid()
        self.lmain_tick.configure(text=self.ticket)
        # self.title("Следующий в очередь " + v.dW['queue'][0] + '. ' + v.dE[ v.dW['queue'][0] ]['name'])
        self.mess = r['stderr']
        self.router()
        self.show_message(self.mess)
        # self.stop_thread()
########## Основное меню, команда Следующий ##########

########## Основное меню, команда Повторить ##########
    def eq_curr_w(self):
        self.f_work.grid_remove()
        self.bmain_next.configure(state=tk.DISABLED)
        self.bmain_curr.configure(state=tk.DISABLED)
        self.bmain_notshow.configure(state=tk.DISABLED)
        self.bmain_end.configure(state=tk.DISABLED)
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tcurr?w=' + v.dH['eq_wplace']
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            if r['stdout'] is None:
                self.ticket = '???'
                self.bmain_next.configure(state=tk.NORMAL)
                self.bmain_end.grid_remove()
                self.bmain_next.grid()
            else:
                self.ticket = r['stdout']
                self.bmain_curr.after(v.dH["ui"]["timeout_next"]*1000, self.btn_timeout_curr)
        self.lmain_tick.configure(text=self.ticket)
        # self.title("Повтор вызова в очередь " + v.dW['queue'][0] + '. ' + v.dE[ v.dW['queue'][0] ]['name'])
        self.mess = r['stderr']
        self.eq_mess_w()

    def btn_timeout_curr(self):
        self.bmain_curr.configure(state=tk.NORMAL)
        self.bmain_notshow.configure(state=tk.NORMAL)
        self.bmain_end.configure(state=tk.NORMAL)
########## Основное меню, команда Повторить ##########

########## Основное меню, команда Не явился ##########
    def eq_notshow_w(self):
        self.f_work.grid_remove()
        self.bmain_next.configure(state=tk.DISABLED)
        self.bmain_curr.configure(state=tk.DISABLED)
        self.bmain_notshow.configure(state=tk.DISABLED)
        self.bmain_end.configure(state=tk.DISABLED)
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tnotshowing?w=' + v.dH['eq_wplace']
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            if r['stdout'] is None and r['stderr'] is None:
                self.ticket = '???'
                self.bmain_next.configure(state=tk.NORMAL)
                self.bmain_end.grid_remove()
                self.bmain_next.grid()
                #self.bmain_end.configure(state=tk.DISABLED)
            else:
                self.ticket = '----'
                self.bmain_curr.configure(state=tk.NORMAL)
                self.bmain_notshow.configure(state=tk.NORMAL)
                self.bmain_end.configure(state=tk.NORMAL)
        self.lmain_tick.configure(text=self.ticket)
        # self.title("Не явился в очередь " + v.dW['queue'][0] + '. ' + v.dE[ v.dW['queue'][0]]['name'])
        self.mess = r['stderr']
        self.eq_mess_w()
        self.curr_time = datetime.datetime.now()
########## Основное меню, команда Не явился ##########

########## Основное меню, команда Завершить ##########
    def eq_end_w(self):
        self.f_work.grid_remove()
        self.bmain_next.configure(state=tk.DISABLED)
        self.bmain_curr.configure(state=tk.DISABLED)
        self.bmain_notshow.configure(state=tk.DISABLED)
        self.bmain_end.configure(state=tk.DISABLED)
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tend?w=' + v.dH['eq_wplace']
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            if r['stdout'] is None and r['stderr'] is None:
                self.ticket = '???'
                self.bmain_next.configure(state=tk.NORMAL)
                self.bmain_end.grid_remove()
                self.bmain_next.grid()
            else:
                self.ticket = '----'
                self.bmain_curr.configure(state=tk.NORMAL)
                self.bmain_notshow.configure(state=tk.NORMAL)
                self.bmain_end.configure(state=tk.NORMAL)
        self.lmain_tick.configure(text=self.ticket)
        # self.title("Завершен вызов в очередь " + v.dW['queue'][0] + '. ' + v.dE[ v.dW['queue'][0] ]['name'])
        self.mess = r['stderr']
        self.eq_mess_w()
        self.curr_time = datetime.datetime.now()
########## Основное меню, команда Завершить ##########

########## Меню очереди, выбор очереди ##########
    # def set_queue_w(self, queue_id):
    #     # Установка одной очереди
    #     # self.destroy_frame_children(self.f_work)
    #     # self.f_mess.grid_remove()
    #     #self.destroy_frame_children(self.f_mess)
    #     global queue
    #     queue = queue_id
    #     fg_color = self.bmain_next.cget("fg_color")
    #     hover_color = self.bmain_next.cget("hover_color")
    #     for i in self.bqueue_:
    #         self.bqueue_[i].configure(fg_color=fg_color)
    #         self.bqueue_[i].configure(hover_color=hover_color)
    #     self.bqueue_[queue].configure(fg_color="#AA4A44")
    #     self.bqueue_[queue].configure(hover_color="#880808")

    #     if self.extmenu and self.ticket == '----':
    #         self.f_work.grid_remove()
    #         self.eq_queueslist_w()

    def set_queues_w(self, queue_id):
        # установка списка очередей
        # self.destroy_frame_children(self.f_work)
        # self.f_mess.grid_remove()
        #self.destroy_frame_children(self.f_mess)
        global queue, queues
        queue = queue_id
        fg_color = self.bmain_next.cget("fg_color")
        hover_color = self.bmain_next.cget("hover_color")

        if queue in queues:
            # Убрать очередь из списка
            queues.remove(queue)
            self.bqueue_[queue].configure(fg_color=fg_color)
            self.bqueue_[queue].configure(hover_color=hover_color)
        else:
            # Добавить очередь из списка
            queues.append(queue)
            self.bqueue_[queue].configure(fg_color="#AA4A44")
            self.bqueue_[queue].configure(hover_color="#880808")

        #if self.extmenu and self.ticket == '----':
        #    self.f_work.grid_remove()
        #    self.eq_queuelist_w()
        self.router()

    def change_queue_w(self, queue_id):
        self.bmain_next.configure(state=tk.DISABLED)
        self.bmain_curr.configure(state=tk.DISABLED)
        self.bmain_notshow.configure(state=tk.DISABLED)
        self.bmain_end.configure(state=tk.DISABLED)
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tchange?w=' + v.dH['eq_wplace'] + '&o=0' + '&q=' + str(queue_id)
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            if r['stderr'] is None:
                # self.mess = "Талон " + self.ticket + " перемещен."
                self.show_message("Талон " + self.ticket + " перемещен.")
                self.ticket = '???'
                self.lmain_tick.configure(text=self.ticket)
                self.bmain_next.configure(state=tk.NORMAL)
                self.bmain_end.grid_remove()
                self.bmain_next.grid()
            else:
                self.mess = r['stderr']
                self.bmain_next.grid_remove()
                self.bmain_end.grid_remove()
        # self.title("Отложить талон для рабочего места " + v.dH['eq_wplace'] + '. ')
        # self.destroy_frame_children(self.f_work)
        # self.eq_mess_w()
        self.router()
        self.text_aside_ticket.delete(0, "end")
        self.curr_time = datetime.datetime.now()
########## Меню очереди, выбор очереди ##########

########## Расширенное меню ##########
    def destroy_frame_children(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

########## Расширенное меню, команда Отложить ##########
    # def eq_asidecurr_w(self):
        # self.f_mess.grid_remove()
        # self.f_work.grid(row=4, column=0, sticky="nsew")
        # self.f_work.grid()
        # if self.ticket and self.ticket != '???':
        #     self.router(self.f_cur_ticket)
            # self.ew_aside = ctk.CTkEntry(self.f_work, placeholder_text="Описание талона", width=400)
            # self.ew_aside.grid(row=5, column=0, columnspan=3, padx=(3, 3), pady=(3, 3), sticky="nsew")

            # self.bw_aside = ctk.CTkButton(self.f_work, fg_color="transparent",
            #                                    text="Отложить талон", width=120,
            #                                    border_width=2, text_color=("gray10", "#DCE4EE"),
            #                                    command=self.eq_asidecurr)
            # self.bw_aside.grid(row=5, column=3, padx=(3, 3), pady=(3, 3),
            #                    sticky="nsew")
        # else:
        #     self.destroy_frame_children(self.f_work)
        #     self.mess = "Нет талона для операции отложить"
        #     self.eq_mess_w()

    def eq_asidecurr(self):
        self.bmain_next.configure(state=tk.DISABLED)
        self.bmain_curr.configure(state=tk.DISABLED)
        self.bmain_notshow.configure(state=tk.DISABLED)
        self.bmain_end.configure(state=tk.DISABLED)
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'taside?w=' + v.dH['eq_wplace'] + '&o=0' + '&d=' + quote_plus(self.text_aside_ticket.get())
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            # self.destroy_frame_children(self.f_work)
            if r['stderr'] is None:
                # self.mess = "Талон " + self.ticket + " отложен."
                self.show_message("Талон " + self.ticket + " отложен.")
                self.ticket = '???'
                self.lmain_tick.configure(text=self.ticket)
                self.bmain_next.configure(state=tk.NORMAL)
                self.bmain_end.grid_remove()
                self.bmain_next.grid()
            else:
                self.mess = r['stderr']
        # self.title("Отложить талон для рабочего места " + v.dH['eq_wplace'] + '. ')
        # self.destroy_frame_children(self.f_work)
        # self.eq_mess_w()
        self.router()
        self.text_aside_ticket.delete(0, "end")
        self.curr_time = datetime.datetime.now()
########## Расширенное меню, команда Отложить ##########

########## Расширенное меню, команда Список отложенных ##########
    def eq_queuelist_w(self, update):
        print(v.dH['eq_wplace'])
        if not update:
            self.destroy_frame_children(self.f_aside_tickets)
            return
    #     self.destroy_frame_children(self.f_work)
    #     # self.f_mess.grid_remove()
    #     self.f_work.grid(row=4, column=0, sticky="nsew")
    #     # self.f_work.grid(row=4, column=0)  #, sticky="nsew")
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tlist_queues?qq=' + v.dH['eq_wplace']
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            if r['stdout'] is None or len(r['stdout']) == 0:
                self.destroy_frame_children(self.f_aside_tickets)
                self.mess = "Очередь пуста!"
            else:
                # self.f_queuelist = ctk.CTkScrollableFrame(self.f_work,
                #                                           label_text="Просмотр талонов в очереди"  + v.dE[queue]["name"],
                #                                           width=520)
                # self.f_queuelist.grid(row=5, column=0) # , padx=(0, 0), pady=(3, 3)), sticky="nsew")
                # self.scrollable_frame_switches = []
                row = 0
                col = 0
                for i in range(len(r['stdout'])):
                    text = r['stdout'][i][2] + "   Время: " + r['stdout'][i][4]
                    ctk.CTkButton(self.f_aside_tickets, fg_color="transparent",
                                  text=text, width=170,
                                  border_width=2, text_color=("gray10", "#DCE4EE"),
                                  command=functools.partial(self.eq_queuelist,
                                                            r['stdout'][i][0],
                                                            r['stdout'][i][2]
                                                            )
                                  ).grid(row=row, column=col, padx=(3, 3), pady=(3, 3), sticky="w")
                    col += 1
                    if col > 2:
                        col =0
                        row += 1

                    # text = r['stdout'][i][5]
                    # self.bw_descr = ctk.CTkButton(self.f_aside_tickets,
                    #               text=' ',
                    #               border_width=0, corner_radius=0,
                    #               fg_color="transparent",
                    #               hover_color="white",
                    #               text_color_disabled="red",
                    #               width=350, anchor='w',
                    #               state=tk.DISABLED)
                    # self.bw_descr.configure(text=text)
                    # self.bw_descr.grid(row=row+i, column=1)  #, padx=(3, 3), pady=(3, 3), ipadx=0)
                    # self.bw_descr._text_label.configure(wraplength=400)
                self.mess = r['stderr']
    #     # self.title("Список отложенных талонов на рабочем месте " + v.dH['eq_wplace'] + '. ')
    #     self.eq_mess_w()

    def eq_queueslist_w(self, update): 
        if not update:
            self.destroy_frame_children(self.f_mark_tickets)
            return

        # self.destroy_frame_children(self.f_work)
        # self.f_mess.grid_remove()
        # self.f_work.grid(row=4, column=0, sticky="nsew")
        # self.f_work.grid(row=4, column=0)  #, sticky="nsew")
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tlist_queues?qq=' + self.list2str(queues)
            print(path)
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            if r['stdout'] is None or len(r['stdout']) == 0:
                self.destroy_frame_children(self.f_mark_tickets)
                self.mess = "Очередь пуста!"
            else:
                # self.f_queuelist = ctk.CTkScrollableFrame(self.f_mark_tickets,
                #                                           label_text="Просмотр талонов в очереди  ",
                #                                           width=520)
                # self.f_queuelist.grid(row=5, column=0) # , padx=(0, 0), pady=(3, 3)), sticky="nsew")
                # self.scrollable_frame_switches = []
                row = 0
                col = 0
                for i in range(len(r['stdout'])):
                    text = r['stdout'][i][2] + "   Время: " + r['stdout'][i][4]
                    ctk.CTkButton(self.f_mark_tickets, fg_color="transparent",
                                  text=text, width=170,
                                  border_width=2, text_color=("gray10", "#DCE4EE"),
                                  command=functools.partial(self.eq_queuelist,
                                                            r['stdout'][i][0],
                                                            r['stdout'][i][2]
                                                            )
                                  ).grid(row=row, column=col, padx=(3, 3), pady=(3, 3), sticky="w", )
                    col += 1
                    if col > 2:
                        col =0
                        row += 1

                    # text = r['stdout'][i][5]
                    # self.bw_descr = ctk.CTkButton(self.f_mark_tickets,
                    #               text=' ',
                    #               border_width=0, corner_radius=0,
                    #               fg_color="transparent",
                    #               hover_color="white",
                    #               text_color_disabled="red",
                    #               width=350, anchor='w',
                    #               state=tk.DISABLED)
                    # self.bw_descr.configure(text=text)
                    # self.bw_descr.grid(row=row+i, column=1)  #, padx=(3, 3), pady=(3, 3), ipadx=0)
                    # self.bw_descr._text_label.configure(wraplength=400)
                self.mess = r['stderr']
        # self.title("Список отложенных талонов на рабочем месте " + v.dH['eq_wplace'] + '. ')
        # self.eq_mess_w()

    def eq_queuelist(self, queue_id, tick_name=''):
        # self.destroy_frame_children(self.f_work)
        self.bmain_next.configure(state=tk.DISABLED)
        self.bmain_curr.configure(state=tk.DISABLED)
        self.bmain_notshow.configure(state=tk.DISABLED)
        self.bmain_end.configure(state=tk.DISABLED)
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tnextbyname?w=' + v.dH['eq_wplace'] + '&q=' + str(queue_id) + '&n=' + quote_plus(tick_name)
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        finally:
            self.mess = ''
            if r['stdout'] is not None:
                self.ticket = r['stdout'][0]
                # self.mess += "Талон " + self.ticket + " " + r['stdout'][2] + chr(10)  # "     "
                self.show_message("Талон " + self.ticket + " " + r['stdout'][2] + chr(10))
                self.bmain_curr.configure(state=tk.NORMAL)
                self.bmain_end.configure(state=tk.NORMAL)
                self.bmain_next.grid_remove()
                self.bmain_end.grid()
            else:
                self.ticket = '???'
                self.bmain_next.configure(state=tk.NORMAL)
                self.bmain_end.grid_remove()
                self.bmain_next.grid()
            if r['stderr'] is not None:
                self.mess += r['stderr']
        self.lmain_tick.configure(text=self.ticket)
        self.router()
    #     # self.f_mess.grid_remove()
    #     # self.title("Вызов талона из очереди " + queue + '. ')
    #     self.destroy_frame_children(self.f_work)
    #     self.eq_mess_w()
########## Расширенное меню, команда Список отложенных ##########

##########   http-запрос   ##########
    def get_request(self, path=''):
        r = {'stdout': None, 'stderr': None}
        try:
            url = v.dH['eq_url'] + path
            print(url)
            auth = tuple(v.dH['eq_auth'])
            print(auth)
            req = requests.get(url=url, auth=auth)
            print('refer = ')
            dReq = json.loads(req.text)
            print(dReq)
            r['stdout'] = dReq['stdout']
            r['stderr'] = dReq['stderr']
        except Exception as e:
            r['stderr'] = 'Ошибка связи с сервером очереди. ' + str(e) + ". "
        return r
##########   http-запрос   ##########

##########   преобразовать список в строку   ##########
    def list2str(self, list_=[]):
        # преобразуем список в строку
        try:
            buf = ''
            delimiter = ''
            for i in list_:
                ii = i if isinstance(i, str) else str(i)
                buf += delimiter + ii
                delimiter = ','
        except:
            buf = ''
        return buf
##########   преобразовать список в строку   ##########

    def button_pass(self):
        pass

    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        ctk.set_window_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

if __name__ == "__main__":
    app = EqWin()
    app.wm_attributes("-topmost", True)
    app.mainloop()
