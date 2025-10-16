#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from __future__ import unicode_literals
import customtkinter as ctk
import time

from pult_types import TMediator, TResponseSetQueue
from pult_config import AppSet
from pult_db import DataBase
from modules.layouts.FrameAuth import FrameAuth
from modules.layouts.FrameQueue import FrameQueue

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

        self.frame_Auth = FrameAuth(self, mediator, app_set)
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
        self.frame_Queue = FrameQueue(self, mediator, app_set, db)
        
        self.frame_Auth.grid_remove()
        self.frame_Queue.grid(row=0, column=0, sticky="nsew")

class Mediator(TMediator):
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
