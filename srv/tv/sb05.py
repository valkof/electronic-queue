#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
from os import path
from datetime import datetime
from logger import get_logger
import psutil
from functools import partial
from http.server import http
import base64
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import unquote
import tkinter
from tkinter import messagebox
from sb05_ui import ScoreBoard
from sb05_vars import V
import threading
import asyncio
import json


def check_exist_wplace(wplace):
    # проверить id-окна
    for i in v.dW:
        if i == wplace:
            return wplace
    return None


class WORKER:
    def __init__(self, method, params):
        # инициализируем словарь r c ключами out-stdout, err-stderr
        self.r = {'stdout': None, 'stderr': None}
        self.method = method
        self.params = params

    def status(self):
        # set server-status
        self.query = self.params.query
        return str({'stdout': None, 'stderr': None})

    def ticket(self):
        # показать талон на инфотабло
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        self.wticket = None
        for key, value in self.dQuery.items():
            if key == 'p':
                # прочитать и проверить наличие окна "ticket?p=3" в запросе
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            elif key == 't':
                # читаем номер талона "ticket?t=3"
                self.wticket = value[0]
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if (self.wplace is not None and self.wticket is not None):
            # номер окна и талона актуален, отправляем данные на экран
            t_ui = threading.Thread(target=uiworker, args=[self.wplace, self.wticket])
            t_ui.start()
            # t_ui = threading.Thread()
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: Не указано/отсутствует окно или рабочее место'
            log.debug(str(self.r))
        return self.r


####################
class AuthHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        username = kwargs.pop("username")
        password = kwargs.pop("password")
        directory = kwargs.pop("directory")
        self._auth = base64.b64encode(f"{username}:{password}".encode()).decode()
        super().__init__(*args, **kwargs, directory=directory) #username=username, password=password,

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_AUTHHEAD(self):
        # https://developer.mozilla.org/ru/docs/Web/HTTP/Status/401
        self.send_response(401, "Unauthorized")
        self.send_header("WWW-Authenticate", 'Basic realm="Access to balancsrv"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_PUT(self):
        self.send_response(405)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        return

    def do_POST(self):
        self.send_response(405)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        return

    def check_AuthBasic(self):
        # тест авторизации
        if (self.headers.get("Authorization") is None and self._auth != "Og=="):
            # Даже не пытались авторизоваться
            # и параль доступа к сервису оставлен пустым
            return False
        elif (self.headers.get("Authorization") == "Basic " + self._auth or self._auth == "Og=="):
            # Авторизация - успешно
            return True
        else:
            # Авторизация - НЕ успешно
            return False

    def do_GET(self):
        if AuthHTTPRequestHandler.check_AuthBasic(self):
            self.fn = unquote(self.path.replace('/', ''))
            if len(self.fn) > 0:
                # в запросе установлен путь, продолжаем
                self.params = urlparse(self.fn)
                self.method = self.params.path
                # print(self.method, self.params)
                if self.method:
                    # выбираем метод по имени пути "self.method" в
                    # запросе и передаем ему параметры "self.params"
                    cls = globals()['WORKER']
                    rez = cls(self.method, self.params)
                    f = getattr(rez, self.method)

                    # Тут результат выполнения команды
                    self.result = f()
                    print("self.result=", self.result)

                    # Ответ отправляем клиенту
                    self.ret = self.result
                    if self.ret['stderr'] is None:
                        self.send_response(200)
                    else:
                        self.send_response(422)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(str(self.ret).encode())
                    return
                else:
                    self.send_response(405, "Method Not Allowed")
                    self.end_headers()
                    return
            else:
                # в запросе нет пути, выходим
                self.send_response(405, "Method Not Allowed")
                self.end_headers()
                return
        else:
                self.send_response(405)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                return


def on_closing():
    # Закрыть окно?
    if tkinter.messagebox.askokcancel("Выход", "Вы действительно хотите завершить задачу?"):
        root.destroy()


def httpd_start():
    handler_class = partial(
        AuthHTTPRequestHandler,
        username=v.dH['username'],
        password=v.dH['password'],
        directory=directory
    )
    http.server.test(
            HandlerClass=handler_class,
            port=v.dH['port'],
            bind=v.dH['bind'])


def uiworker(wplace, wticket):
    new_ticket = wticket
    # передача номера талона на "рабочее место"
    try:
        sb.wticket0_set(wplace, new_ticket)
    except Exception as e:
        log.debug(str(e))
        pass
    # if new_ticket != "----":
        # Отображение сообщения о закрытии окна
        # print("wplace===", wplace)


vers = "v0.4l"
pid = os.getpid()  # pid сервиса

path_def = os.getcwd()  # '.'
procname = path.splitext(os.path.basename(sys.argv[0]))[0]  # префикс сервиса

# инициализация логгера
global path_logfile, log
path_logfile = os.path.join(path_def, 'logs/'+procname+'{:%Y-%m-%d}.log'.format(datetime.now()))
log = get_logger(__name__, path_logfile)

# инициализируем словарь переменных
global v
v = V()

# Идентификатор основного сервиса
# "XDG_RUNTIME_DIR" - каталог в котором будем
# сохранять PID-процесса
if "XDG_RUNTIME_DIR" not in os.environ:
    filePid = os.path.join(path_def, procname+'.pid')
else:
    filePid = os.path.join(os.environ["XDG_RUNTIME_DIR"], procname+'.pid')

# Идентификатор основного сервиса
# filePid = os.path.join(path_def, procname+'.pid')

procname_running = False  # по-умолчанию личым, что процесс не запущен

# Проверяем наличие идентификатора другого процесса
if os.path.isfile(filePid):
    try:
        with open(filePid, "r") as file:
            fpid = file.read()
        # Читаем pid-процесса, если находим процесс с подобным идентификатором,
        # то завершаем работу, т.к. сервис уже запущен в другом сеансе.
        for proc in psutil.process_iter():
            if proc.pid == int(fpid):
                procname_running = True
                log.debug(procname+" is already running. Shutdown...")
                sys.exit()
    except:
        log.debug("Filepid("+filePid+") read error!")
        sys.exit()
    # Файл pid-существует, но процесс уже умер. Удаляем pid и продолжаем запуск
    if procname_running == False:
        log.debug("Filepid("+filePid+") exists, but the process is not started! Delete filepid")
        try:
             os.remove(filePid)
        except OSError:
            pass

# Если требуется, то создаем структуру каталогов
path_tmp1 = os.path.join(path_def, 'wwwroot')
try:
    os.makedirs(path_tmp1, exist_ok=True)
except:
    log.debug("Error creating directory structure: "+path_tmp1+". Shutdown...")
    sys.exit()
path_tmp2 = os.path.join(path_def, 'videos')
try:
    os.makedirs(path_tmp2, exist_ok=True)
except:
    log.debug("Error creating directory structure: "+path_tmp2+". Shutdown...")
    sys.exit()
path_tmp3 = os.path.join(path_def, 'wwwroot')
try:
    os.makedirs(path_tmp3, exist_ok=True)
except:
    log.debug("Error creating directory structure: "+path_tmp3+". Shutdown...")
    sys.exit()
fPid = open(filePid, 'w')
fPid.write(str(pid))
fPid.close()
directory = path_tmp1

# Стартуем нить httpd
threading.Thread(target=httpd_start, daemon=True).start()

# Стартуем UI
root = tkinter.Tk()
sb = ScoreBoard(root, v)

# Запуск GUI в отдельном потоке
def run_gui():
    asyncio.run(pusk())

async def pusk():
    await asyncio.sleep(2)  # Асинхронная пауза на 2 секунды
    sb.play_video()

threading.Thread(target=run_gui, daemon=True).start()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
