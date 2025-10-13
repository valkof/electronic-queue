from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

class JSONHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Формируем JSON-ответ
        response_data = {
            "stdout": {
                "user_id": "9",
                "queues": [
                    {
                        "id": "1",
                        "title": "Регистратура"
                    }
                ],
                "queues_delay": [
                    {
                        "id": "1",
                        "title": "Регистратура"
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
        time.sleep(5)
        # Отправляем ответ
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

def run(server_class=HTTPServer, handler_class=JSONHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
