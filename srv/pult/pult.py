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

class App(ctk.CTk):
    def __init__(self, mediator: Mediator, db: DataBase):
        super().__init__()

        self._mediator = mediator
        self._db = db

        self._db.pult['width'] = 600
        self._db.pult['height'] = 160

        self.title("Пульт оператора")
        self.resizable(False, False)
        self.put_position()
        self.grid_columnconfigure(0, weight=1, minsize=self._db.pult['width']*db.setPult['ui']['scaling'])
        self.grid_rowconfigure(0, weight=1, minsize=self._db.pult['height']*db.setPult['ui']['scaling'])
        # self.extmenu = False
        self.ticket = False
        # self.mess = None
        # self.curr_time = datetime.datetime.now()
        # self.columnconfigure(index=0, weight=1)
        # self.columnconfigure(index=1, weight=3)
        # self.count_aside = 'Отлож. 0'
        # self.clear_message = lambda: self.lmess = ''
        # self.timer_id = None

        self.frame_Auth = FrameAuth(self, mediator, db)
        self.frame_Auth.grid(row=0, column=0, sticky="nsew")

    def put_position(self, addHeight: int = 0):
        width = self._db.pult['width']
        height = self._db.pult['height']
        zoom = self._db.setPult['ui']['scaling']
        shift_x = self._db.setPult['ui']['shift_left']
        shift_y = self._db.setPult['ui']['shift_bottom']
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # print(addHeight)
        shift_pos_x = screen_width - int(width * zoom + shift_x)
        shift_pos_y = screen_height - int(height * zoom + shift_y + addHeight)
        self.geometry(f'{width}x{height + int(addHeight / zoom)}+{shift_pos_x}+{shift_pos_y}')
    
    def get_data_pult(self):
        db.getDataPult(self.callback_data_pult)        

    def callback_data_pult(self, data: TResponseSetQueue, time_out: float):
        if data['stderr'] != '':
            self.frame_Auth.after(time_out*1000, self._mediator.state, 'no_data_pult', {'message': data['stderr']})
            return
        
        self._db.setDeviceSetting(data['stdout'])
        self.frame_Auth.after(time_out*1000, self._mediator.state, 'open_frame_queue', {'message': 'Авторизация прошла успешно.'})

    def open_frame_queue(self):
        self.frame_Queue = FrameQueue(self, self._mediator, self._db)
        
        self.frame_Auth.grid_remove()
        self.frame_Queue.grid(row=0, column=0, sticky="nsew")
        self.frame_Queue.f_message.show_message('Здравствуйте')
        self._mediator.state('repeat')

class Mediator(TMediator):
    def __init__(self):
        self._app: App = None

    def set_app(self, app: App):
        self._app = app

    def state(self, event: str, body: any = None):
        if event == 'get_data_pult':
            self._app.get_data_pult()
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
        
        if event == 'buttons_lock':
            self._app.frame_Queue.f_ticket.button_lock()
            self._app.frame_Queue.f_queues.buttons_lock()
            return
        
        if event == 'buttons_unlock':
            self._app.frame_Queue.f_ticket.button_unlock()
            self._app.frame_Queue.f_queues.buttons_unlock()
            return
        
        if event == 'next':
            self.state('buttons_lock')
            return
        
        if event == 'next_error':
            self._app.frame_Queue.f_message.show_message(body['message'])
            self.state('buttons_unlock')
            return
        
        if event == 'next_success':
            self._app.frame_Queue.f_message.show_message(body['message'])
            self._app.frame_Queue.f_ticket.show_ticket()
            return
        
        if event == 'next_success_after':
            self._app.frame_Queue.f_ticket.button_unlock()
            return
        
        if event == 'current':
            self.state('buttons_lock')
            return
        
        if event == 'current_error':
            self._app.frame_Queue.f_message.show_message(body['message'])
            self._app.frame_Queue.f_ticket.button_unlock()
            return
        
        if event == 'current_success':
            self._app.frame_Queue.f_message.show_message(body['message'])
            self._app.frame_Queue.f_ticket.show_ticket()
            self._app.frame_Queue.f_ticket.set_action('adv_with_ticket')
            return
        
        if event == 'current_success_after':
            self._app.frame_Queue.f_ticket.button_unlock()
            return
        
        if event == 'abort':
            self.state('buttons_lock')
            return
        
        if event == 'abort_error':
            self._app.frame_Queue.f_message.show_message(body['message'])
            self._app.frame_Queue.f_ticket.button_unlock()
            return
        
        if event == 'abort_success':
            self._app.frame_Queue.f_message.show_message(body['message'])
            self._app.frame_Queue.f_ticket.show_ticket()
            return
        
        if event == 'abort_success_after':
            self.state('buttons_unlock')
            return
        
        if event == 'finish_success_after':
            self.state('buttons_unlock')
            return
        
        if event == 'repeat':
            self._app.frame_Queue.f_control.queue_curr()
            return
        
        if event == 'update_window':
            self._app.put_position(body['height'])
            return
        
        if event == 'adv_with_ticket':
            self._app.frame_Queue.adv_with_ticket()
            return
        
        if event == 'adv_without_ticket':
            self._app.frame_Queue.adv_without_ticket()
            return
        
        if event == 'background':
            self.state('adv_with_ticket')
            self._app.frame_Queue.f_control.buttons_lock()
            self.state('buttons_lock')
            return
        
        if event == 'background_error':
            self._app.frame_Queue.f_message.show_message(body['message'])
            self._app.frame_Queue.f_ticket.button_unlock()
            self._app.frame_Queue.f_control.b_curr.unlock()
            self._app.frame_Queue.f_control.b_finish.unlock()
            self._app.frame_Queue.f_control.b_abort.unlock()
            return
        
        if event == 'background_success':
            self._app.frame_Queue.f_message.show_message(body['message'])
            self._app.frame_Queue.f_ticket.show_ticket()
            self._app.frame_Queue.f_ticket.set_action('adv_without_ticket')
            return
        
        if event == 'background_success_after':
            self._app.frame_Queue.f_control.begin_state(body['time_out'])
            return
        
        if event == 'update_tickets_frame':
            self._app.frame_Queue.f_tickets.f_reserve.update_tickets()
            return
        
        if event == 'reserve_error':
            self._app.frame_Queue.f_message.show_message(body['message'])
            return

        if event == 'select_ticket':
            self.state('buttons_lock')
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
    app = App(mediator, db)
    mediator.set_app(app)
    app.wm_attributes("-topmost", True)
    app.mainloop()
