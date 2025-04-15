#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import json
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
# from urllib.parse import quote_plus
from ksk08_vars import V
import requests
import random
import subprocess


# def check_exist_wplace(wplace):
#    # есть ли рабочее место?
#    for i in v.dW:
#        if i == wplace:
#            return wplace
#    return None


class PrintTicket:
    def __init__(self, d_queue, l_ticket):
        self.r = {'stdout': l_ticket, 'stderr': None}
        self.err = ''
        self.d_queue = d_queue
        self.l_ticket = l_ticket

    def start_print(self):
        err = ''
        try:
            with open(self.d_queue['template'], 'r', encoding='koi8-r') as tmp:
                temp = tmp.read()
        except (Exception) as e:
            err = "Ошибка киоска: Неверная конфигурация шаблона. "  # + str(e) + ". "
            log.debug(err + str(e) + ". ")
            return err
        try:
            temp = temp.format(ticket=self.l_ticket[0], time=self.l_ticket[1])
        except (Exception) as e:
            err = "Ошибка киоска: Ошибка конвертации шаблона. "  # + str(e) + ". "
            log.debug(err + str(e) + ". ")
            return err
        try:
            fn_random = os.path.join('/tmp',
                                     str(random.randint(0, 999999)) + '.ps')
            print(type(temp))
            with open(fn_random, "w", encoding='koi8-r') as f:
                f.write(temp)
        except (Exception) as e:
            err = "Ошибка киоска: Ошибка сохранения временного файла. "  # + str(e) + ". "
            log.debug(err + str(e) + ". ")
            return err
        try:
            cmd = self.d_queue['printcommand'] + ' ' + fn_random
            lcmd = list(cmd.split(" "))
            subprocess.run(lcmd,
                           capture_output = True,
                           text = True,
                           shell=False,
                           check=True)
        except (Exception) as e:
            err = "Ошибка киоска: Ошибка печати временного файла. "  # + str(e) + ". "
            log.debug(err + str(e) + ". ")
            return err
        #print(temp)
        return None


class WORKER:
    def __init__(self, method, params):
        # инициализируем словарь r c ключами out-stdout, err-stderr
        self.r = {'stdout': None, 'stderr': None}
        self.method = method
        self.params = params
        # log.debug(str(self.method), str(self.params))

    def status(self):
        # вернуть статус, будем думать, что в нем вывести
        self.query = self.params.query
        return json.dumps({'stdout': None, 'stderr': None})

    def tcreate(self):
        # создать талон следующий
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        self.queue = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # определяем в запросе киоск, создавший талон
                self.wplace = value[0]  # check_exist_wplace(value[0])
                # continue
            elif key == 'q':
                # запрос по номеру очереди "tcreate?q=3"
                self.queue = value[0]
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.queue = None
                break
        if self.queue is not None:
            if self.wplace is None:
                # киоск не определен
                self.wplace = 0
            # номер очереди присутствует, создаем запрос на талон
            try:
                # Читаем параметры очереди
                url = v.dE[self.queue]['url'] + 'tcreate'
                params = {'q': self.queue, 'w': self.wplace}
                auth = tuple(v.dE[self.queue]['auth'])
                timeout = v.dE[self.queue]['timeout']
                req = requests.get(url=url, params=params,
                                   auth=auth, timeout=timeout)
                if req.status_code != 200:
                    self.r['stderr'] = "Ошибка киоска: несоответствие настройкам сервера ЭО: " + str(req.status_code) + ". "
                    log.debug(self.r['stderr'])
                else:
                    d_req = json.loads(req.text)
                    self.r['stdout'] = d_req['stdout']
                    print(v.dE[self.queue], d_req['stdout'])
                    self.r['stderr'] = PrintTicket(v.dE[self.queue], d_req['stdout']).start_print()
            except Exception as e:
                # Проблема сетевого соединения с сервером ЭО
                # или нет описания очереди
                self.r['stderr'] = "Ошибка киоска: нет связи с сервером ЭО или отсутствует описание очереди "  # + str(e) + ". "
                log.debug(self.r['stderr'] + str(e) + ". ")
        else:
            # нет номера очереди
            self.r['stderr'] = 'Ошибка: Очередь не найдена'
            log.debug(json.dumps(self.r))
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
                    self.ret = json.dumps(self.result)  # "OK"
                    self.send_response(200)
                    # добавлен для веб-киоска
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(self.ret.encode())
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


def main():
    vers = "v0.7l"
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
        filePid = os.path.join("/var/run/", procname+'.pid')
    else:
        filePid = os.path.join(os.environ["XDG_RUNTIME_DIR"], procname+'.pid')


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
    path_tmp1 = os.path.join(path_def,'wwwroot')
    try:
        os.makedirs(path_tmp1, exist_ok=True)
    except:
        log.debug("Error creating directory structure: "+path_tmp1+". Shutdown...")
        sys.exit()

    fPid = open(filePid, 'w')
    fPid.write(str(pid))
    fPid.close()
    directory = path_tmp1
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


main()
