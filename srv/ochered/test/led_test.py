#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import socket

def run_led(wplace, ticket):
    # Запуск led-табло
    led_addr = tuple(["10.0.5.185", 2323])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect(("10.0.5.139", 2323))
    s.settimeout(2)
    s.connect(led_addr)
    
    ticket = '!' + '' + ticket + '^'
    s.send(ticket.encode('utf-8'))  # отправка
    data = s.recv(1024)  # получение
 
    print(len(data))
    print(data)
    
    s.close()  # закрытие



run_led('1',"Ф222")
