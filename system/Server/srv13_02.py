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
from urllib.parse import quote_plus
from srv13_vars import V
from srv13_lsql import SqLite
import requests
import socket


def prefix2queue(prefix):
    # найти id-очереди по префиксу
    for i in v.dE:
        if v.dE.get(i)['prefix'] == prefix:
            return i
    return None


def check_exist_queue(queue):
    # есть ли очередь? и вернуть префикс
    for i in v.dE:
        if i == queue:
            return v.dE.get(i)['prefix']
    return None


def check_exist_wplace(wplace):
    # есть ли рабочее место?
    for i in v.dW:
        if i == wplace:
            return wplace
    return None


class RunMedia:
    def __init__(self, wplace, ticket, dwplace):
        self.err = ''
        self.wplace = wplace
        self.ticket = ticket
        self.dwplace = dwplace

    def start_media(self):
        for key, value in self.dwplace.items():
            if key == 'tvsrv':
                self.err = self.err + RunMedia.run_tvsrv(self.wplace,
                                                         self.ticket,
                                                         self.dwplace['tvsrv'])
            elif key == 'ausrv':
                self.err = self.err + RunMedia.run_ausrv(self.wplace,
                                                         self.ticket,
                                                         self.dwplace['ausrv'])
            elif key == 'ledsrv':
                self.err = self.err + RunMedia.run_ledsrv(self.ticket,
                                                          self.dwplace['ledsrv'])
        return self.err

    def run_tvsrv(wplace, ticket, dsrv):
        # Вызов инфотабло
        err = ''
        for i in dsrv:
            # Обход по списку сервисов инфотабло
            try:
                # Читаем параметры Инфотабло
                url = v.dT[i]['tv_url'] + 'ticket'
                params = {'p': wplace,
                          't': ticket}
                auth = tuple(v.dT[i]['tv_auth'])
                timeout = v.dT[i]['tv_timeout']
                req = requests.get(url=url, params=params,
                                   auth=auth, timeout=timeout)
                if req.status_code != 200:
                    err = "Ошибка Инфотабло: несоответствие настройкам сервера: " + str(req.status_code) + ". "
                    log.debug(err)
            except Exception as e:
                # Проблема сетевого соединения с инфотабло?
                err = "Ошибка Инфотабло: возможно нет связи? "  # + str(e) + ". "
                log.debug(err + str(e) + ". ")
        return err

    def run_ausrv(wplace, ticket, dsrv):
        # Вызов Аудиосервера
        err = ''
        if ticket == '----':
            pass
        else:
            for i in dsrv:
                # Обход по списку сервисов голоса
                try:
                    # Читаем параметры Аудиосервера
                    url = v.dA[i]['au_url'] + quote_plus(v.dW[wplace]['au_prefix'] + "," + ticket + "," + v.dW[wplace]['au_place'])
                    auth = tuple(v.dA[i]['au_auth'])
                    timeout = v.dA[i]['au_timeout']
                    req = requests.get(url=url, auth=auth, timeout=timeout)
                    if req.status_code != 200:
                        err = "Ошибка Аудиосервера: несоответствие настройкам сервера: " + str(req.status_code) + ". "
                        log.debug(err)
                except Exception as e:
                    err = "Ошибка Аудиосервера: возможно нет связи? "  # + str(e) + ". "
                    log.debug(err + str(e) + ". ")
        return err

    def run_ledsrv(ticket, dsrv):
        # Вызов Табло
        err = ''
        for i in dsrv:
            # Обход по списку сервисов табло
            try:
                # Читаем параметры Табло
                led_ip = tuple(v.dL[i]['led_ip'])
                timeout = v.dL[i]['led_timeout']
                print()
                print(timeout)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(timeout)
                s.connect(led_ip)
                ticket = '!' + ticket + '^'
                s.send(ticket.encode('utf-8'))  # отправка
                s.recv(128)  # получение
                s.close()  # закрытие
            except Exception as e:
                err = "Ошибка Табло: возможно нет связи? "  # + str(e) + ". "
                log.debug(err + str(e) + ". ")
        return err


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

    def get_queues(self):
        # инфа о настройке рабочих окон
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if self.wplace is not None:
            # номер окна существует, возвращаем данные об окне
            self.r['stdout'] = {x:v.dE[x] for x in v.dW[self.wplace]['queue']}
        else:
            # в запросе отсутствует "рабочее окно"
            # возвращаем полный справочник очередей
            self.r['stdout'] = v.dE
            log.debug(json.dumps(self.r))
        return self.r

    def get_wplaces(self):
        # вернуть список "окон"
        self.query = self.params.query
        return json.dumps({'stdout': v.dW, 'stderr': None})

    def get_wplace(self):
        # инфа о настройке рабочих окон
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if self.wplace is not None:
            # номер окна существует, возвращаем данные об окне
            # s = SqLite(v.sD, {'w': self.wplace})
            self.r['stdout'] = v.dW[self.wplace]
                # print("self.r['stdout'] = ", json.dumps(self.r['stdout']))
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: отсутствует рабочее место. '
            log.debug(json.dumps(self.r))
        return self.r

    def tcreate(self):
        # создать талон следующий
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        self.queue = None
        self.prefix = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # определяем в запросе киоск, создавший талон
                self.wplace = value[0]  # check_exist_wplace(value[0])
                # continue
            elif key == 'q':
                # запрос по номеру очереди "tcreate?q=3", ищем префикс
                self.prefix = check_exist_queue(value[0])
                self.queue = value[0] if self.prefix is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.queue = None
                break
        if self.queue is not None:
            if self.wplace is None:
                # киоск не определен
                self.wplace = 0
            # номер очереди присутствует, создаем талон
            s = SqLite(v.sD, {'w': self.wplace, 'q': self.queue, 'p': self.prefix})
            ret = s.ticket_create()
            self.r['stdout'] = ret[0]
            self.r['stderr'] = ret[1]
        else:
            # нет номера очереди
            self.r['stderr'] = 'Ошибка: Очередь не найдена'
            log.debug(json.dumps(self.r))
        return self.r

    def tnext(self):
        # вызвать талон следующий
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.queue = None
        self.wplace = None
        for key, value in self.dQuery.items():
            if key == 'p':
                # запрос по префиксу "tnext?p=Ф", ищем очередь
                self.queue = prefix2queue(value[0])
                # continue
            elif key == 'q':
                # запрос по номеру очереди "tnext?q=3"
                self.queue = value[0] if check_exist_queue(value[0]) is not None else None
                # continue
            elif key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if (self.wplace is not None and self.queue is not None):
            # номер окна и очереди актуален, формируем запрос на следующего посетителя
            s = SqLite(v.sD, {'q': self.queue, 'w': self.wplace})
            ret = s.ticket_next()
            if ret[0] is not None:
                # Очередь не пустая, получили номер в ret[0][1]
                # Отправляем на проигрывание
                self.r['stderr'] = RunMedia(self.wplace,
                                            ret[0][0],
                                            v.dW[self.wplace]).start_media()
                if len(self.r['stderr']) == 0:
                    self.r['stderr'] = None
                self.r['stdout'] = ret[0][0]
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Очередь пуста! "
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: Проблема в описании очереди или рабочего места. '
            log.debug(json.dumps(self.r))
        return self.r

    def tnextbyname(self):
        # вызвать талон следующий по его имени
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.queue = None
        self.tname = None
        self.wplace = None
        for key, value in self.dQuery.items():
            if key == 'n':
                # запрос по префиксу "tnext?p=Ф", ищем очередь
                self.tname = unquote(value[0])
                # continue
            elif key == 'q':
                # запрос по номеру очереди "tnext?q=3"
                self.queue = value[0]
                # continue
            elif key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if (self.wplace is not None and self.queue is not None and self.tname is not None):
            # номер окна, очереди, талона актуален, формируем запрос на следующего посетителя
            s = SqLite(v.sD, {'q': self.queue, 'w': self.wplace, 'n': self.tname})
            ret = s.ticket_next_by_name()
            if ret[0] is not None:
                # Очередь не пустая, получили номер в ret[0][1]
                # Отправляем на проигрывание
                self.r['stderr'] = RunMedia(self.wplace,
                                            ret[0][0],
                                            v.dW[self.wplace]).start_media()
                if len(self.r['stderr']) == 0:
                    self.r['stderr'] = None
                self.r['stdout'] = (ret[0][0], ret[0][1], ret[0][2])
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Нет талона с номером " + value[0]
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: Проблема в описании очереди или рабочего места. '
            log.debug(json.dumps(self.r))
        return self.r

    def tcurr(self):
        # повторить вызов текущего посетителя
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if self.wplace is not None:
            # номер окна и очереди актуален, формируем запрос
            # повторное приглашение посетителя
            s = SqLite(v.sD, {'w': self.wplace})
            ret = s.ticket_current()
            if ret[0] is not None:
                # номер окна и очереди актуален, формируем запрос
                # повторное приглашение посетителя
                self.r['stderr'] = RunMedia(self.wplace,
                                            ret[0][0],
                                            v.dW[self.wplace]).start_media()
                if len(self.r['stderr']) == 0:
                    self.r['stderr'] = None
                self.r['stdout'] = ret[0][0]
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Нет талона для повтора! "
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: остутствует рабочее место. '
            log.debug(json.dumps(self.r))
        return self.r

    def tchecknew(self):
        # повторить вызов текущего посетителя
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.queue = None
        for key, value in self.dQuery.items():
            if key == 'q':
                # читаем номер окна
                self.queue = value[0]
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.queue = None
                break
        if self.queue is not None:
            # номер окна и очереди актуален, формируем запрос
            # повторное приглашение посетителя
            s = SqLite(v.sD, {'q': self.queue})
            ret = s.ticket_check_new()
            if ret[0] is not None and ret[0] > 0:
                # есть необслуженные талоны в очереди
                self.r['stderr'] = ret[1]
                self.r['stdout'] = ret[0]
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Нет свободных талонов в очереди! "
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: остутствует очередь. '
            log.debug(json.dumps(self.r))
        return self.r


    def tpause(self):
        # завершить обслуживание и поставить окно на паузу
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if self.wplace is not None:
            # номер окна и очереди актуален, формируем запрос
            # на закрытие всех талонов
            s = SqLite(v.sD, {'w': self.wplace})
            ret = s.ticket_pause()
            # Отправляем на проигрывание паузу
            if ret[1] is None:
                # номер окна и очереди актуален, формируем запрос
                # повторное приглашение посетителя
                self.r['stderr'] = RunMedia(self.wplace,
                                            "----",
                                            v.dW[self.wplace]).start_media()
                if len(self.r['stderr']) == 0:
                    self.r['stdout'] = ret[0]
                    self.r['stderr'] = None
            else:
                # возвращаем сообщение об ошибке
                self.r['stdout'] = None
                self.r['stderr'] = ret[1]
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: отсутствует рабочее место. '
            log.debug(json.dumps(self.r))
        return self.r


    def tend(self):
        # завершить обслуживание клиента "Успешно"
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if self.wplace is not None:
            # номер окна и очереди актуален, формируем запрос
            # на успешное закрытие всех талонов
            s = SqLite(v.sD, {'w': self.wplace})
            ret = s.ticket_end()
            self.r['stdout'] = ret[0]
            self.r['stderr'] = ret[1]
            RunMedia(self.wplace, '----', v.dW[self.wplace]).start_media()
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: отсутствует рабочее место. '
            log.debug(json.dumps(self.r))
        return self.r


    def tmove(self):
        # переместить талон (поднять в своей или переместить в чужую)
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        self.queue = None
        self.offset = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            elif key == 'q':
                # читаем номер очереди в которую переместим талон
                self.prefix = check_exist_queue(value[0])
                self.queue = value[0] if self.prefix is not None else None
                # continue
            elif key == 'o':
                # читаем насколько сдвинем в очереди текущий талон
                self.offset = int(value[0])-1
                # continue
            else:
                pass
        if self.wplace is not None and self.queue is not None and self.offset is not None:
            # номер окна и очереди и сдвига актуален, формируем запрос
            # на текущий номер талона
            s = SqLite(v.sD, {'w': self.wplace})
            ret = s.ticket_current()
            print("ret = s.ticket_current()=", ret)
            if ret[0] is not None:
                # номер окна и очереди актуален, формируем запрос
                # перемещение посетителя
                s = SqLite(v.sD, {'w': self.wplace, 'q': self.queue, 'o': self.offset, 't': ret[0][0]})
                ret = s.ticket_move()
                print("ret = s.ticket_move()=", ret)

                #if len(self.r['stderr']) == 0:
                #    self.r['stderr'] = None
                #self.r['stdout'] = ret[0][0]
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Не выбран талон для перемещения! "
            RunMedia(self.wplace, '----', v.dW[self.wplace]).start_media()
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: в запросе остутствует рабочее место, номер очереди или значение сдвига. '
            log.debug(json.dumps(self.r))
        return self.r

    def tnotshowing(self):
        # завершить обслуживание клиента, который не явился
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        for key, value in self.dQuery.items():
            if key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.wplace = None
                break
        if self.wplace is not None:
            # номер окна и очереди актуален, формируем запрос
            # на успешное закрытие всех талонов
            s = SqLite(v.sD, {'w': self.wplace})
            ret = s.ticket_notshowing()
            self.r['stdout'] = ret[0]
            self.r['stderr'] = ret[1]
            RunMedia(self.wplace, '----', v.dW[self.wplace]).start_media()
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: отсутствует рабочее место. '
            log.debug(json.dumps(self.r))
        return self.r

    def taside(self):
        # отложить талон в личную очередь
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.wplace = None
        self.queue = None
        self.offset = None
        self.description = ''
        for key, value in self.dQuery.items():
            if key == 'w':
                # читаем номер окна
                self.wplace = value[0] if check_exist_wplace(value[0]) is not None else None
                # continue
            elif key == 'o':
                # читаем насколько сдвинем в очереди текущий талон
                self.offset = int(value[0])
                # continue
            elif key == 'd':
                # читаем описание оператора к талону
                self.description = unquote(value[0])
                print(self.description)
                # continue
            else:
                pass
        if self.wplace is not None and self.offset is not None:
            # номер окна и очереди и сдвига актуален, формируем запрос
            # на текущий номер талона
            s = SqLite(v.sD, {'w': self.wplace})
            ret = s.ticket_current()
            print("ret = s.ticket_current()=", ret)
            if ret[0] is not None:
                # номер окна и очереди актуален, формируем запрос
                # перемещение посетителя
                s = SqLite(v.sD, {'w': self.wplace, 'q': self.wplace, 'o': self.offset, 't': ret[0][0], 'd': self.description})
                ret = s.ticket_move()
                print("ret = s.ticket_move()=", ret)
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Не выбран талон для перемещения! "
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: в запросе остутствует рабочее место, номер очереди или значение сдвига. '
            log.debug(json.dumps(self.r))
        return self.r

    def tlist_kiosk(self):
        # Список талонов в личной очереди
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.queue = None
        for key, value in self.dQuery.items():
            if key == 'q':
                # читаем номер очереди
                self.queue = value[0]
                # continue
            else:
                pass
        if self.queue is not None:
            # Номер очереди присутствует
            s = SqLite(v.sD, {'q': self.queue})
            ret = s.ticket_list_kiosk()
            print("ret = s.ticket_list_kiosk=", ret)
            if ret[0] is not None:
                self.r['stdout'] = ret[0]
                self.r['stderr'] = None
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Очередь пуста!"
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: в запросе остутствует номер очереди. '
            log.debug(json.dumps(self.r))
        return self.r

    def tlist_queue(self):
        # Список талонов в одной очереди
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.queue = None
        for key, value in self.dQuery.items():
            if key == 'q':
                # читаем номер очереди
                self.queue = value[0]
                # continue
            else:
                pass
        if self.queue is not None:
            # Номер очереди присутствует
            print(self.queue)
            s = SqLite(v.sD, {'q': self.queue})
            ret = s.ticket_list_queue()
            print("ret = s.ticket_list_queue=", ret)
            if ret[0] is not None:
                self.r['stdout'] = ret[0]
                self.r['stderr'] = None
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Очередь пуста!"
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: в запросе остутствует номер очереди. '
            log.debug(json.dumps(self.r))
        return self.r

    def tlist_queues(self):
        # Список талонов в списке очередей
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.queues = None
        for key, value in self.dQuery.items():
            if key == 'qq':
                # читаем список очередей
                self.queues = value[0]
                # continue
            else:
                pass
        if self.queues is not None:
            # Список очередей не пуст
            print(self.queues)
            s = SqLite(v.sD, params='', dparams={'qq': self.queues})
            ret = s.ticket_list_queues()
            print("ret = s.ticket_list_queues=", ret)
            if ret[0] is not None:
                self.r['stdout'] = ret[0]
                self.r['stderr'] = None
            else:
                # возвращаем сообщение о пустой очереди
                self.r['stdout'] = None
                self.r['stderr'] = "Очереди пусты!"
        else:
            # недостаточно или неверные параметры запроса
            self.r['stderr'] = 'Ошибка: в запросе остутствует список очередей. '
            log.debug(json.dumps(self.r))
        return self.r

    def qlen(self):
        # читать длину очереди
        self.query = self.params.query
        self.dQuery = parse_qs(self.query)
        self.queue = None
        for key, value in self.dQuery.items():
            if key == 'q':
                # запрос по номеру очереди "tcreate?q=3", ищем префикс
                self.prefix = check_exist_queue(value[0])
                self.queue = value[0] if self.prefix is not None else None
                # continue
            else:
                # запрос с плохими реквизитами, далее вернем ошибку
                self.queue = None
                break
        if self.queue is not None:
            # номер очереди присутствует, читаем его длину
            s = SqLite(v.sD, {'q': self.queue})
            ret = s.queue_len()
            self.r['stdout'] = ret[0]
            self.r['stderr'] = ret[1]
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
    vers = "v0.2l"
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
