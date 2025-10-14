#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from __future__ import unicode_literals
import asyncio
import threading
from pult_vars import AppSet, DataBase, LockableButton, TQueue, TResponseSetQueue
import requests
import json
import tkinter as tk
from PIL import Image
import customtkinter as ctk
from urllib.parse import quote_plus
import functools
import time
import datetime

# queue = app_set.dW['queue'][0]

# dLenQueue = {}
# queues = []
# # список очередей по которым делаем запрос о количестве талонов
# queues_check = app_set.dW['queue'].copy()
# # добавим отложенную очередь
# queues_check.append(app_set.dH['eq_wplace'])
# print("queues_check=", queues_check)
# print(queues)
# for key, value in app_set.dE.items():
#     dLenQueue[key] = 0
# print()
# print(dLenQueue)

def _app_pos(self, width: int, height: int, zoom: float, shift_x, shift_y: int):
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    shift_pos_x = screen_width - int(width * zoom + shift_x)
    shift_pos_y = screen_height - int(height * zoom + shift_y)
    self.geometry(f'{width}x{height}+{shift_pos_x}+{shift_pos_y}')

class App(ctk.CTk):
    def __init__(self, mediator: Mediator):
        super().__init__()

        self._mediator = mediator

        self.title("Пульт оператора")
        self.resizable(False, False)
        _app_pos(self, 600, 200,
            app_set.pult['ui']['scaling'],
            app_set.pult['ui']['shift_left'],
            app_set.pult['ui']['shift_bottom']
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # self.extmenu = False
        self.ticket = False
        # self.mess = None
        # self.curr_time = datetime.datetime.now()
        # self.columnconfigure(index=0, weight=1)
        # self.columnconfigure(index=1, weight=3)
        # self.count_aside = 'Отлож. 0'
        # self.clear_message = lambda: self.lmess = ''
        # self.timer_id = None

        self.frame_Auth = FrameAuth(self, mediator)
        self.frame_Auth.grid(row=0, column=0, sticky="nsew")
    
    def get_data_pult(self, oper_id: str):
        db.getDataPult(time.time(), self.callback_data_pult, oper_id, app_set.pult['eq_wplace'])
        

    def callback_data_pult(self, data: TResponseSetQueue, min_time: float):
        # max_time = max(0, app_set.pult['ui']['timeout_next'] - (time.time() - min_time))
        max_time = max(0, 0 - (time.time() - min_time))
        if data['stderr'] != '':
            self.frame_Auth.after(max_time*1000, self._mediator.state, 'no_data_pult', {'message': data['stderr']})
            return
        
        app_set.place = data['stdout']
        self.frame_Auth.after(max_time*1000, self._mediator.state, 'open_frame_queue', {'message': 'Авторизация прошла успешно.'})

    def open_frame_queue(self):
        self.frame_Queue = FrameQueue(self, mediator)
        
        self.frame_Auth.grid_remove()
        self.frame_Queue.grid(row=0, column=0, sticky="nsew")

class FrameAuth(ctk.CTkFrame):
    def __init__(self, parent, mediator: Mediator):
        super().__init__(parent)

        self._mediator = mediator
        
        # Создание переменных для хранения значений
        self.combo_var = ctk.StringVar()
        self.entry_var = ctk.StringVar()
        self.label_var = ctk.StringVar()
        
        # Создание виджетов
        # Выпадающий список
        self.combo = ctk.CTkComboBox(
            self, width=300,
            values=[item[2] for item in app_set.pult['set']],
            variable=self.combo_var, state="readonly"
        )
        self.combo.set(app_set.pult['set'][0][2])
        self.combo.grid(row=0, column=0, padx=20, pady=10)
        
        # Поле ввода чисел
        self.entry = ctk.CTkEntry(
            self, width=300,
            placeholder_text="Пароль",
            textvariable=self.entry_var
        )
        self.entry.grid(row=1, column=0, padx=20, pady=10)
        self.entry.focus_set()
        
        # Кнопка действия
        self.button = LockableButton(
            self,
            text="ВОЙТИ",
            command=self.button_click
        )
        self.button.grid(row=2, column=0, padx=20, pady=10)

        # Сообщение
        self.label = ctk.CTkLabel(
            self, width=300,
            text='', text_color='red'
        )
        self.label.grid(row=3, column=0, padx=20, pady=10)
        
        # Настройка растяжения столбцов
        self.grid_columnconfigure(0, weight=1)

        self.entry.bind("<Return>", self.on_enter_pressed)
        self.entry.bind("<KP_Enter>", self.on_enter_pressed)

    def on_enter_pressed(self, event):
        self.button_click()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def button_click(self):
        self.button.lock()
        self.verify_authorization()

    def verify_authorization(self):
        selected_option = self.combo_var.get()
        kod = self.entry_var.get()
        
        matches = []
    
        for item in app_set.pult['set']:
            if item[1] == kod and item[2] == selected_option:
                matches.append(item)
        
        if len(matches) == 1:
            self.label_show()
            oper_id = matches[0][0]
            self._mediator.state('get_data_pult', {'oper_id': oper_id})
        else:
            self.label_show('Неверный пароль')
            self.button.unlock()

    def label_show(self, message: str = ''):
        self.label.configure(text=message)


class FrameQueue(ctk.CTkFrame):
    def __init__(self, parent, mediator: Mediator):
        super().__init__(parent)

        self._mediator = mediator
        
        self.router_pages = []

        mainPanel = ctk.CTkFrame(self)
        mainPanel.grid(row=0, column=0, sticky="nsew")
        mainPanel.columnconfigure(index=0, weight=1)
        self.f_ticket = FrameTicket(mainPanel, mediator).grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.f_control = FrameControl(mainPanel, mediator).grid(row=0, column=1, sticky="ew")
        self.f_queues = FrameQueues(mainPanel, mediator).grid(row=1, column=1, sticky="nsew")

# ########## Меню очереди, виджеты ##########
#         self.f_queue = ctk.CTkFrame(self, corner_radius=0)
#         # self.f_queue.configure(border_width=1, border_color="green")
#         self.f_queue.grid(row=1, column=1, sticky="ew")
#         column = 0
#         row = 0
#         self.bqueue_: dict[str, ctk.CTkButton] = {}
#         self.lqueue_: dict[str, ctk.CTkLabel] = {}
#         # for key, value in app_set.dE.items():
#         #     self.bqueue_[key] = ctk.CTkButton(self.f_queue,
#         #                                       text=app_set.dE[key]["shortname"],
#         #                                       font=ctk.CTkFont(weight="normal"),
#         #                                       anchor="w",
#         #                                       command=functools.partial(self.set_queues_w, key))
#         #     self.bqueue_[key].grid(row=row, column=column, padx=(3, 3),
#         #                                pady=(3, 3), ipadx=0, sticky='w')

#         #     self.lqueue_[key] = ctk.CTkLabel(self.f_queue, text=str(dLenQueue[key]),
#         #                                      font=ctk.CTkFont(weight="normal"),
#         #                                      width=20)
#         #     self.lqueue_[key].grid(row=row, column=column, padx=(3, 10), pady=(3, 3), ipadx=0, ipady=0, sticky="e")
#         #     column = 0 if column >= 2 else column + 1
#         #     if (column == 0): row += 1

#         # def setLenQueue():
#         #     for key, value in dLenQueue.items():
#         #         self.lqueue_[key].configure(text=str(value))
#         #     self.l_len_aside.configure(text=self.count_aside)
            
#         #     for key, value in dLenQueue.items():
#         #         try:
#         #             path = 'qlen?q=' + key
#         #             dLenQueue[key] = self.get_request(path)["stdout"]
#         #         finally:
#         #             pass
#         #     try:
#         #         path = 'qlen?q=' + app_set.dH['eq_wplace']
#         #         self.count_aside = 'Отлож. ' + str(self.get_request(path)["stdout"])
#         #     finally:
#         #         pass    
#         #     self.after(app_set.dH["ui"]["timeout_check"]*1000, setLenQueue)
#         # setLenQueue()
# ########## Меню очереди, виджеты ##########

# ########## Сообщения, виджеты##########
#         self.f_mess = ctk.CTkFrame(self, corner_radius=0, height=50, bg_color='#434B4D', fg_color="transparent" )
#         self.f_mess.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(5, 5))
#         # self.f_mess.configure(border_width=1, border_color="blue")
#         self.lmess = ctk.CTkLabel(self.f_mess, text="", text_color="red", bg_color='#434B4D')
#         self.lmess.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
# ########## Сообщения, виджеты##########

# ########## Рабочий фрейм ##########
#         self.f_work = ctk.CTkFrame(self, corner_radius=0)
#         self.f_work.grid(row=4, column=0, sticky="ew", columnspan=2)
#         # self.f_work.configure(border_width=1, border_color="blue")
#         self.f_work.columnconfigure(index=0, weight=1)

#         ctk.CTkLabel(self.f_work, text="● Отложенные талоны", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

#         self.f_aside_tickets = ctk.CTkScrollableFrame(self.f_work, corner_radius=10, bg_color='#434B4D', fg_color="transparent", height=110)
#         self.f_aside_tickets.grid(row=1, column=0, sticky="ew", padx=(3, 3), pady=(3, 3))
#         # self.f_aside_tickets.configure(border_width=1, border_color="red")
#         self.f_aside_tickets._scrollbar.configure(height=0)
#         self.f_aside_tickets.columnconfigure(index=[0,1,2], weight=1)

#         ctk.CTkLabel(self.f_work, text="● Талоны в выбранных очередях", text_color="white").grid(row=2, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

#         self.f_mark_tickets = ctk.CTkScrollableFrame(self.f_work, corner_radius=10, bg_color='#434B4D', fg_color="transparent", height=110)
#         self.f_mark_tickets.grid(row=3, column=0, sticky="ew", padx=(3, 3), pady=(3, 3))
#         # self.f_mark_tickets.configure(border_width=1, border_color="red")
#         self.f_mark_tickets._scrollbar.configure(height=0)
#         self.f_mark_tickets.columnconfigure(index=[0,1,2], weight=1)

#         self.router_pages.append(self.f_work)
#         # self.f_work.grid_remove()
# ##########  Рабочий фрейм ##########

# ##########  Фрейм дополнительных функций к текущему талону ##########
#         self.f_cur_ticket = ctk.CTkFrame(self, corner_radius=0)
#         self.f_cur_ticket.grid(row=5, column=0, sticky="ew", columnspan=2)
#         # self.f_cur_ticket.configure(border_width=1, border_color="red")
#         self.f_cur_ticket.columnconfigure(index=0, weight=1)
        
#         ctk.CTkLabel(self.f_cur_ticket, text="● Отложить талон", text_color="white").grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="w")
        
#         f_aside_ticket = ctk.CTkFrame(self.f_cur_ticket, corner_radius=0, fg_color="transparent")
#         f_aside_ticket.grid(row=1, column=0, sticky="ew")
#         # f_aside_ticket.configure(border_width=1, border_color="blue")
#         f_aside_ticket.columnconfigure(index=0, weight=1)
        
#         self.text_aside_ticket = ctk.CTkEntry(f_aside_ticket, placeholder_text="Описание талона")
#         self.text_aside_ticket.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), sticky="ew")

#         self.but_aside_ticket = ctk.CTkButton(f_aside_ticket, fg_color="transparent",
#                                             text="Отложить талон", 
#                                             border_width=2, text_color=("gray10", "#DCE4EE"),
#                                             command=self.eq_asidecurr)
#         self.but_aside_ticket.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), sticky="ew")
        
#         ctk.CTkLabel(self.f_cur_ticket, text="● Перевести талон в другую очередь", text_color="white").grid(row=2, column=0, padx=(5, 5), pady=(2, 2), sticky="w")

#         f_redir_ticket = ctk.CTkFrame(self.f_cur_ticket, corner_radius=0, fg_color="transparent")
#         f_redir_ticket.grid(row=3, column=0, sticky="nsew")
#         # f_redir_ticket.configure(border_width=1, border_color="green")
#         f_redir_ticket.columnconfigure(index=[0,1,2], weight=1)
#         i_col = 0
#         n_col = 3
#         for key in app_set.dE.items():
#             row = i_col // n_col
#             col = i_col - row * n_col
#             button = ctk.CTkButton(f_redir_ticket, text=app_set.dE[key[0]]["shortname"], fg_color="transparent",
#                                   border_width=2, font=ctk.CTkFont(weight="normal"), text_color=("gray10", "#DCE4EE"),
#                                   anchor="c", command=functools.partial(self.change_queue_w, key[0]))
#             button.grid(row=row, column=col, padx=(3, 3), pady=(2, 2), sticky="ew")
#             i_col += 1

#         self.router_pages.append(self.f_cur_ticket)
#         self.f_cur_ticket.grid_remove()
# ##########  Фрейм дополнительных функций к текущему талону ##########

# ########## Запуска пульта проверка на наличие открытого талона ###########
#         # global first_run_app
#         # if first_run_app:
#         self.eq_curr_w()
#             # first_run_app = False
#         self.set_queues_w(queue)
# ########## Запуска пульта проверка на наличие открытого талона ##########

########## Медиатор ##########
    def mediator(self, event: str, status: bool = True):
        if event == 'beg_next':
            self.router()
            self.bmain_next.configure(state=tk.DISABLED)
            self.bmain_curr.configure(state=tk.DISABLED)
            self.bmain_notshow.configure(state=tk.DISABLED)
            self.bmain_end.configure(state=tk.DISABLED)
            self.b_adv_opt.configure(state=tk.DISABLED)
            for key in self.bqueue_:
                self.bqueue_[key].configure(state=tk.DISABLED)
            return
        
        if event == 'end_next':
            if not status:
              self.bmain_next.configure(state=tk.NORMAL)
              self.b_adv_opt.configure(state=tk.NORMAL)
              for key in self.bqueue_:
                self.bqueue_[key].configure(state=tk.NORMAL)
            self.lmain_tick.configure(text=self.ticket)

            self.show_message(self.mess)
            return
        
        if event == 'end_next_timeout':
            self.bmain_next.grid_remove()
            self.bmain_end.grid()
            self.bmain_end.configure(state=tk.NORMAL)
            self.bmain_curr.configure(state=tk.NORMAL)
            return
        
        if event == 'end_curr':
            if not status:
              self.bmain_end.grid_remove()
              self.bmain_next.grid()
              self.bmain_next.configure(state=tk.NORMAL)
              self.b_adv_opt.configure(state=tk.NORMAL)
              for key in self.bqueue_:
                  self.bqueue_[key].configure(state=tk.NORMAL)
            self.lmain_tick.configure(text=self.ticket)
            self.show_message(self.mess)
            return
        
        if event == 'end_curr_timeout':
            self.bmain_end.configure(state=tk.NORMAL)
            self.bmain_curr.configure(state=tk.NORMAL)
            self.bmain_notshow.configure(state=tk.NORMAL)
            self.b_adv_opt.configure(state=tk.NORMAL)
            return
        
        if event == 'end_notshow':
            if status:
                self.bmain_next.configure(state=tk.NORMAL)
                self.bmain_end.grid_remove()
                self.bmain_next.grid()
                self.b_adv_opt.configure(state=tk.NORMAL)
                for key in self.bqueue_:
                    self.bqueue_[key].configure(state=tk.NORMAL)
            else:
                self.bmain_curr.configure(state=tk.NORMAL)
                self.bmain_notshow.configure(state=tk.NORMAL)
                self.bmain_end.configure(state=tk.NORMAL)
            self.lmain_tick.configure(text=self.ticket)
            self.show_message(self.mess)
            return
########## Медиатор ##########

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



########## Основное меню, команда Следующий ##########
    def eq_nexts_w(self):
        self.mediator('beg_next')
        r = {'stdout': None, 'stderr': None}
        try:
            qq = ','.join([x for x in queues])
            path = 'tnexts?w=' + app_set.dH['eq_wplace'] + '&qq=' + qq
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        
        self.mess = r['stderr']
        if r['stdout'] is None:
            self.ticket = '----'
            self.mediator('end_next', False)
        else:
            self.ticket = r['stdout']
            self.mediator('end_next')
            self.bmain_curr.after(app_set.dH["ui"]["timeout_next"]*1000, self.mediator, 'end_next_timeout')
########## Основное меню, команда Следующий ##########

########## Основное меню, команда Повторить ##########
    def eq_curr_w(self):
        self.mediator('beg_next')
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tcurr?w=' + app_set.dH['eq_wplace']
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        self.mess = r['stderr']
        if r['stdout'] is None:
            self.ticket = '----'
            self.mediator('end_curr', False)
        else:
            self.ticket = r['stdout']
            self.mediator('end_curr')
            self.bmain_curr.after(app_set.dH["ui"]["timeout_next"]*1000, self.mediator, 'end_curr_timeout')
########## Основное меню, команда Повторить ##########

########## Основное меню, команда Не явился ##########
    def eq_notshow_w(self):
        self.mediator('beg_next')
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tnotshowing?w=' + app_set.dH['eq_wplace']
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        
        self.ticket = '----'
        self.mess = r['stderr']
        if r['stdout'] is None and r['stderr'] is None:
            self.mediator('end_notshow')
        else:
            self.mediator('end_notshow', False)
########## Основное меню, команда Не явился ##########

########## Основное меню, команда Завершить ##########
    def eq_end_w(self):
        self.mediator('beg_next')
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tend?w=' + app_set.dH['eq_wplace']
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        
        self.ticket = '----'
        self.mess = r['stderr']
        if r['stdout'] is None and r['stderr'] is None:
            self.mediator('end_notshow')
        else:
            self.mediator('end_notshow', False)
########## Основное меню, команда Завершить ##########

########## Меню очереди, выбор очереди ##########
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

        self.router()

    def change_queue_w(self, queue_id):
        self.mediator('beg_next')
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tchange?w=' + app_set.dH['eq_wplace'] + '&o=0' + '&q=' + str(queue_id)
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        
        if r['stderr'] is None:
            self.mess = "Талон " + self.ticket + " перемещен в очередь " + app_set.dE[queue_id]["name"] + "."
            self.ticket = '----'
            self.mediator('end_notshow')
        else:
            self.mess = r['stderr']
            self.mediator('end_notshow', False)
########## Меню очереди, выбор очереди ##########

########## Расширенное меню ##########
    def destroy_frame_children(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

########## Расширенное меню, команда Отложить ##########
    def eq_asidecurr(self):
        self.mediator('beg_next')
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'taside?w=' + app_set.dH['eq_wplace'] + '&o=0' + '&d=' + quote_plus(self.text_aside_ticket.get())
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        
        if r['stderr'] is None:
            self.mess = "Талон " + self.ticket + " отложен."
            self.ticket = '----'
            self.mediator('end_notshow')
        else:
            self.mess = r['stderr']
            self.mediator('end_notshow', False)
########## Расширенное меню, команда Отложить ##########

########## Расширенное меню, команда Панель список отложенных ##########
    def eq_queuelist_w(self, update):
        if not update:
            self.destroy_frame_children(self.f_aside_tickets)
            return

        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tlist_queues?qq=' + app_set.dH['eq_wplace']
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "

        if r['stdout'] is None or len(r['stdout']) == 0:
            self.mess = r['stderr']
            self.destroy_frame_children(self.f_aside_tickets)
            return
        
        n_col = 3
        for i in range(len(r['stdout'])):
            row = i // n_col
            col = i - row * n_col
            text = r['stdout'][i][2] + "   Время: " + r['stdout'][i][4]
            ctk.CTkButton(self.f_aside_tickets, fg_color="transparent", text=text, width=170,
                          border_width=2, text_color=("gray10", "#DCE4EE"),
                          command=functools.partial(self.eq_queuelist, r['stdout'][i][0], r['stdout'][i][2])
                          ).grid(row=row, column=col, padx=(3, 3), pady=(3, 3), sticky="w")

    def eq_queueslist_w(self, update): 
        if not update:
            self.destroy_frame_children(self.f_mark_tickets)
            return

        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tlist_queues?qq=' + self.list2str(queues)
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "

        if r['stdout'] is None or len(r['stdout']) == 0:
            self.mess = r['stderr']
            self.destroy_frame_children(self.f_mark_tickets)
            return
        
        n_col = 3
        for i in range(len(r['stdout'])):
            row = i // n_col
            col = i - row * n_col
            text = r['stdout'][i][2] + "   Время: " + r['stdout'][i][4]
            ctk.CTkButton(self.f_mark_tickets, fg_color="transparent", text=text, width=170,
                          border_width=2, text_color=("gray10", "#DCE4EE"),
                          command=functools.partial(self.eq_queuelist, r['stdout'][i][0], r['stdout'][i][2])
                          ).grid(row=row, column=col, padx=(3, 3), pady=(3, 3), sticky="w", )

    def eq_queuelist(self, queue_id, tick_name=''):
        self.mediator('beg_next')
        r = {'stdout': None, 'stderr': None}
        try:
            path = 'tnextbyname?w=' + app_set.dH['eq_wplace'] + '&q=' + str(queue_id) + '&n=' + quote_plus(tick_name)
            r = self.get_request(path)
        except Exception as e:
            r['stderr'] = str(e) + ". "
        
        self.mess = r['stderr']
        if r['stdout'] is None:
            self.ticket = '----'
            self.mediator('end_next', False)
        else:
            self.ticket = r['stdout'][0]
            self.mediator('end_next')
            self.bmain_curr.after(app_set.dH["ui"]["timeout_next"]*1000, self.mediator, 'end_next_timeout')  
########## Расширенное меню, команда Список отложенных ##########


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

    # def change_scaling_event(self, new_scaling: str):
    #     new_scaling_float = int(new_scaling.replace("%", "")) / 100
    #     ctk.set_widget_scaling(new_scaling_float)
    #     ctk.set_window_scaling(new_scaling_float)

    # def sidebar_button_event(self):
    #     print("sidebar_button click")

class FrameTicket(ctk.CTkFrame):
    """
    Фрейм для отображения информации о текущем талоне
    """
    def __init__(self, parent, mediator: Mediator):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")

        self._mediator = mediator


        self.LTicket = ctk.CTkLabel(self, text="----", font=ctk.CTkFont(size=24, weight="bold"))
        self.LTicket.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.BOption = ctk.CTkButton(self, text="Дополнительно", font=ctk.CTkFont(weight="normal"), command=self.open_adv_opt)
        self.BOption.grid(row=1, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        
        self.LMessage = ctk.CTkLabel(self, text="Отлож. 0", font=ctk.CTkFont(weight="normal"))
        self.LMessage.grid(row=2, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

    def open_adv_opt(self):
        if mediator._app.ticket:  # есть номер талона
            # self.router(self.f_cur_ticket)
            pass
        else:  # нет выбранного талона
            # self.router(self.f_work)
            pass

class FrameControl(ctk.CTkFrame):
    """
    Фрейм кнопок для управления талоном
    """
    def __init__(self, parent, mediator: Mediator):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")

        self._mediator = mediator


        self.bmain_next = ctk.CTkButton(self, text="➜ Следующий",
                                        font=ctk.CTkFont(weight="bold")) #,
                                        #TODO command=self.eq_nexts_w)
        self.bmain_next.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        self.bmain_next.grid_remove()

        self.bmain_curr = ctk.CTkButton(self, text="⟳ Повторить",
                                        font=ctk.CTkFont(weight="bold")) #,
                                        #TODO command=self.eq_curr_w)
        self.bmain_curr.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.bmain_notshow = ctk.CTkButton(self, text="✖ Не явился",
                                           font=ctk.CTkFont(weight="bold")) #,
                                           #TODO command=self.eq_notshow_w)
        self.bmain_notshow.grid(row=0, column=2, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.bmain_end = ctk.CTkButton(self, text="✔ Обслужен",
                                       font=ctk.CTkFont(weight="bold")) #,
                                       #TODO command=self.eq_end_w)
        self.bmain_end.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

class FrameQueues(ctk.CTkFrame):
    """
    Фрейм кнопок для управления очередями
    """
    def __init__(self, parent, mediator: Mediator):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="green")

        self._mediator = mediator

        self.buttons_create()

    def buttons_create(self):
        self.buttons: dict[str, ButtonQueue] = {}
        # self.bqueue_: dict[str, ctk.CTkButton] = {}
        # self.lqueue_: dict[str, ctk.CTkLabel] = {}
        column: int = 0
        row: int = 0
        for item in app_set.place['queues']:
            button = ButtonQueue(self, self._mediator, item)
            button.grid(row=row, column=column, padx=(3, 10), pady=(3, 3), ipadx=0, ipady=0, sticky="e")
            self.buttons[item['id']] = button
            if column < 2:
                column + 1
            else:
                column = 0
                row += 1

        # setLenQueue()

    # def setLenQueue():
    #     for key, value in dLenQueue.items():
    #         self.lqueue_[key].configure(text=str(value))
    #     self.l_len_aside.configure(text=self.count_aside)
        
    #     for key, value in dLenQueue.items():
    #         try:
    #             path = 'qlen?q=' + key
    #             dLenQueue[key] = self.get_request(path)["stdout"]
    #         finally:
    #             pass
    #     try:
    #         path = 'qlen?q=' + app_set.dH['eq_wplace']
    #         self.count_aside = 'Отлож. ' + str(self.get_request(path)["stdout"])
    #     finally:
    #         pass    
    #     self.after(app_set.dH["ui"]["timeout_check"]*1000, setLenQueue)


class ButtonQueue(ctk.CTkFrame):
    """
    Кнопка для управления очередью
    """
    def __init__(self, parent, mediator: Mediator, queue: TQueue):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="green")

        self._mediator = mediator

        self.button = ctk.CTkButton(
            self,
            text=queue['title'],
            font=ctk.CTkFont(weight="normal"),
            anchor="w",
            # command=functools.partial(self.set_queues_w, key)
        )
        self.button.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky='w')

        self.label = ctk.CTkLabel(
            self,
            text='0',
            # text=str(dLenQueue[key]),
            font=ctk.CTkFont(weight="normal"),
            width=20
        )
        self.label.grid(row=0, column=0, padx=(3, 10), pady=(3, 3), ipadx=0, ipady=0, sticky="e")


class Mediator:
    def __init__(self):
        self._app = None

    def set_app(self, app: App):
        self._app = app

    def state(self, event: str, body: any = None):
        if event == 'get_data_pult':
            self._app.get_data_pult(body['oper_id'])
            return
        
        if event == 'no_data_pult':
            with self._app.frame_Auth as frame:
                frame.label_show(body['message'])
                frame.button.unlock()
            return
        
        if event == 'open_frame_queue':
            with self._app.frame_Auth as frame:
                frame.label_show(body['message'])
                frame.button.lock()
            self._app.open_frame_queue()
            return

# Main run
if __name__ == "__main__":
    app_set = AppSet()
    db = DataBase(app_set.pult)
    ctk.set_appearance_mode(app_set.pult["ui"]["mode"])
    ctk.set_default_color_theme(app_set.pult["ui"]["theme"])
    ctk.set_widget_scaling(app_set.pult["ui"]["scaling"])
    ctk.set_window_scaling(app_set.pult["ui"]["scaling"])

    mediator = Mediator()
    app = App(mediator)
    mediator.set_app(app)
    app.wm_attributes("-topmost", True)
    app.mainloop()
