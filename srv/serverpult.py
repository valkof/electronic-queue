from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import urllib

class JSONHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Парсим параметры запроса
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Получаем значение параметра sit_l
        sit_l = query_params.get('sit_l', [None])[0]
        
        # Формируем ответ в зависимости от значения sit_l
        if sit_l == '936':
            response_data = {
                "stdout": {
                    "user_id": "9",
                    "queues": [
                        {
                            "id": "1",
                            "title": "Регистратура"
                        },
                        {
                            "id": "2",
                            "title": "Справочная"
                        },
                        {
                            "id": "3",
                            "title": "Процедурная"
                        },
                        {
                            "id": "4",
                            "title": "Льгота"
                        }
                    ],
                    "queues_delay": [
                        {
                            "id": "1",
                            "title": "Регистратура"
                        },
                        {
                            "id": "3",
                            "title": "Процедурная"
                        }
                    ],
                    "adapter_setting": "156.156.156.156",
                    "led_tablo": {
                        "id": "3",
                        "title": "1",
                        "port": "2323"
                    },
                    "month_id": "4",
                    "message": ""
                },
                "stderr": ""
            }
        elif sit_l == '22':
            response_data = {
              "stdout": {
                "ticket": {
                  "id": "5",
                  "title": "Р002",
                  "queue_id": "1"
                },
                "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
              },
              "stderr": ""
            }
        elif sit_l == '23':
            response_data = {
              "stdout": {
                "ticket": {
                  "id": "5",
                  "title": "Р002",
                  "queue_id": "1"
                },
                "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
              },
              "stderr": ""
            }
        elif sit_l == '24':
            response_data = {
              "stdout": {
                "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
              },
              "stderr": ""
            }
        elif sit_l == '25':
            response_data = {
              "stdout": {
                "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
              },
              "stderr": ""
            }
        elif sit_l == '26':
            response_data = {
                "stdout": {
                  "tickets": [
                    {
                      "id": "9",
                      "title": "Р001",
                      "queues_id": "1",
                      "time": "10:33"
                    },
                    {
                      "id": "10",
                      "title": "С001",
                      "queues_id": "2",
                      "time": "10:33"
                    },
                    {
                      "id": "11",
                      "title": "Р002",
                      "queues_id": "1",
                      "time": "10:33"
                    },
                    {
                      "id": "12",
                      "title": "Р003",
                      "queues_id": "1",
                      "time": "10:33"
                    },
                    {
                      "id": "13",
                      "title": "С002",
                      "queues_id": "2",
                      "time": "10:33"
                    },
                    {
                      "id": "14",
                      "title": "С003",
                      "queues_id": "2",
                      "time": "10:33"
                    },
                    {
                      "id": "15",
                      "title": "С004",
                      "queues_id": "2",
                      "time": "10:33"
                    }
                  ],
                  "message": ""
                },
                "stderr": ""
              }
        elif sit_l == '27':
            response_data = {
              "stdout": {
                "ticket": {
                  "id": "5",
                  "title": "Р002",
                  "queue_id": "1"
                },
                "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
              },
              "stderr": ""
            }
        elif sit_l == '28':
            response_data = {
              "stdout": {
                "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
              },
              "stderr": ""
            }
        elif sit_l == '29':
            response_data = {
                'stdout': {
                    'tickets': [
                        {'id': '9', 'title': 'Р006', 'time': '20:47'},
                        {'id': '10', 'title': 'Р007', 'time': '14:12'},
                        {'id': '11', 'title': 'Р008', 'time': '14:13'},
                        {'id': '12', 'title': 'Р009', 'time': '14:14'},
                        {'id': '13', 'title': 'Р010', 'time': '14:15'}
                    ],
                    'message': ''
                },
                'stderr': ''
            }
        elif sit_l == '30':
            response_data = {
              "stdout": {
                "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
              },
              "stderr": ""
            }
        else:
            response_data = {}
        time.sleep(2)
        # Отправляем ответ
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

def run(server_class=HTTPServer, handler_class=JSONHandler, port=88):
    server_address = ('192.168.0.90', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
