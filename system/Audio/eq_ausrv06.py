#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import json
import time
from os import path
from datetime import datetime
from logger import get_logger
import psutil
from functools import partial
from http.server import http
import base64
from urllib.parse import unquote
import threading
import queue
import pygame
import re


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
        return AuthHTTPRequestHandler.http405(self)

    def do_POST(self):
        return AuthHTTPRequestHandler.http405(self)

    def http405(self):
        log.debug(str(self.client_address) + " " + self.requestline)
        self.send_response(405)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        return

    def check_AuthBasic(self):
        # тест авторизации
        if self.headers.get("Authorization") is None:
            log.debug("Даже не пытались авторизоваться")
            return False
        elif self.headers.get("Authorization") == "Basic " + self._auth:
            # Авторизация - успешно
            return True
        else:
            log.debug("Авторизация - НЕ успешно")
            return False

    def do_GET(self):
        if AuthHTTPRequestHandler.check_AuthBasic(self):
            self.fn = self.path.replace('/', '')
            if len(self.fn) > 0:
                self.ret = unquote(self.fn)  # f()
                # print("======", self.ret, self.ret.encode(), type(self.ret))
                t_qin = threading.Thread(target=queueIn, args=(self.ret,))
                t_qin.start()
                # Ответ отправляем клиенту
                # self.wfile.write(self.ret.encode())
                self.send_response(200)
                self.end_headers()
                return
            else:
                log.debug("В запросе нет пути")
                return AuthHTTPRequestHandler.http405(self)
        else:
            return AuthHTTPRequestHandler.http405(self)


def read_settings():
    global BIND, PORT, USERNAME, PASSWORD, SETMODE
    try:
        with open(file_set) as data1:
            data1_ = json.load(data1)
    except (Exception) as e:
        log.debug("Проблема с файлом конфигурации: " + str(e))
        sys.exit()
    BIND = data1_["BIND"]
    PORT = int(data1_["PORT"])
    USERNAME = data1_["USERNAME"]
    PASSWORD = data1_["PASSWORD"]
    SETMODE = int(data1_["SETMODE"])
    del data1_
    log.debug("Service: " + BIND + ", " + str(PORT) + ", auth_basic" + str(SETMODE))


def queueIn(arg):
    with lock:
        q.put(arg)
        time.sleep(1)


def queuePl():
    while True:
        time.sleep(1)
        while q.qsize()>0:
            play_acontent3(q.get())
            time.sleep(1)


def queue_audio(fn):
    #pygame.mixer.init()
    s = pygame.mixer.Sound(fn)
    pygame.mixer.Sound.play(s)
    s.play()
    while pygame.mixer.get_busy():
        time.sleep(0.05)
        pass


def play_acontent3(acontent):
    path_content = 'content'
    if SETMODE == 1:
        acontent = split4ausrv(acontent)  # нормализуем
    aa = acontent.split(',')
    if len(aa) > 0:
        aa_norm = []
        for a in aa:
            if (a.isdigit()):
                if 1000 > int(a) > 0:
                    aa_norm.append(str(int(a)))
            else:
                aa_norm.append(a)
    for file in aa_norm:
        fn = os.path.join(path_content,file+".mp3")
        if os.path.exists(fn):
            queue_audio(fn)
        else:
            log.debug(fn + " not exists!")


def split4ausrv(s):
    ss = ''
    pre_num = False
    for c in s:
        if not c.isdigit():
            if not pre_num:
                ss += c
            else:
                ss += ',' + c
            pre_num = False
        else:
            if pre_num:
                ss += c
            else:
                ss += ',' + c
            pre_num = True
    return re.sub(",,", ",", ss)


def main():
    vers = "v0.4l"
    pid = os.getpid()

    # Идентификатор основного сервиса
    # "XDG_RUNTIME_DIR" - каталог в котором будем
    # сохранять PID-процесса
    if "XDG_RUNTIME_DIR" not in os.environ:
        filePid = os.path.join(path_default1, procname+'.pid')
    else:
        filePid = os.path.join(os.environ["XDG_RUNTIME_DIR"], procname+'.pid')

    procname_running = False  # по-умолчанию личым, что процесс не запущен

    # Проверяем наличие идентификатора другого процесса
    if os.path.isfile(filePid):
        try:
            with open(filePid, "r") as file:
                fpid = file.read()
            # Читаем pid-процесса, если находим процесс с подобным идентификатором,
            #  то завершаем работу, т.к. сервис уже запущен в другом сеансе.
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
    path_tmp1 = os.path.join(path_default1,'tmp')
    try:
        os.makedirs(path_tmp1, exist_ok=True)
    except:
        log.debug("Error creating directory structure: "+path_tmp1+". Shutdown...")
        sys.exit()

    global file_set
    file_set = os.path.join(path_default1, procname+'.json')
    read_settings()

    fPid = open(filePid, 'w')
    fPid.write(str(pid))
    fPid.close()
    directory = path_tmp1
    handler_class = partial(
        AuthHTTPRequestHandler,
        username=USERNAME,
        password=PASSWORD,
        directory=directory
    )
    t_qPl = threading.Thread(target=queuePl, args=())
    t_qPl.start()
    time.sleep(1)
    http.server.test(HandlerClass=handler_class, port=PORT, bind=BIND)


if __name__ == '__main__':
    q = queue.Queue()
    lock = threading.Lock()
    path_default1 = os.getcwd()  # '.'
    procname = path.splitext(os.path.basename(sys.argv[0]))[0]
    # global path_logfile, log
    path_logfile = os.path.join(path_default1, 'logs/'+procname+'{:%Y-%m-%d}.log'.format(datetime.now()))
    log = get_logger(__name__, path_logfile)
    pygame.mixer.init()
    main()
