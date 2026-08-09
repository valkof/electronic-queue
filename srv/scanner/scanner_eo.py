import datetime
import os
import json
import sys
import time
import requests
import serial
import logger

CONFIG_FILE = "config.json"

path_def = os.getcwd()  # '.'
procname = os.path.splitext(os.path.basename(sys.argv[0]))[0]  # префикс сервиса

# инициализация логгера
global path_logfile, log
path_logfile = os.path.join(path_def, 'logs/'+procname+'{:%Y-%m-%d}.log'.format(datetime.datetime.now()))
log = logger.get_logger(__name__, path_logfile)

def load_config():
    """Загрузка настроек из файла JSON"""
    if not os.path.exists(CONFIG_FILE):
        # Создаем дефолтный конфиг, если файла нет
        default_config = {
            "COM_PORT": "COM3",
            "BAUD_RATE": 9600,
            "API_URL": "http://example.com"
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        return default_config
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def send_http_request(url, barcode):
    """Отправка HTTP-запроса с добавленным кодом"""
    full_url = f"{url}&ticket_code={barcode}"
    log.info(f"[HTTP] Отправка запроса на: {full_url}")
    
    try:
        # timeout=10 защищает от вечного зависания, если сервер упал
        response = requests.get(full_url) 
        log.info(f"[HTTP] Ответ сервера (Код {response.status_code}): {response.text[:100]}")
    except requests.exceptions.RequestException as e:
        log.debug(f"[HTTP Ошибка]: Не удалось отправить запрос. Причина: {e}")

def main():
    config = load_config()
    com_port = config.get("COM_PORT", "COM3")
    baud_rate = config.get("BAUD_RATE", 9600)
    api_url = config.get("API_URL", "")

    log.info(f"[Система] Запуск. Ожидание сканера на порту {com_port}...")

    while True:
        try:
            # Открываем порт
            with serial.Serial(com_port, baud_rate, timeout=1) as ser:
                log.info(f"[Система] Сканер подключен и готов к работе.")
                
                while True:
                    # Проверяем, пришли ли данные в буфер порта
                    if ser.in_waiting > 0:
                        # Считываем строку (сканер отправляет код + символ переноса строки)
                        raw_data = ser.readline()
                        barcode = raw_data.decode('utf-8').strip()
                        
                        if barcode:
                            log.info(f"[Сканер] Код успешно считан: {barcode}")
                            log.info("[Система] Ожидание кода приостановлено. Обработка...")
                            
                            # Отправляем запрос (пока функция выполняется, новые коды не считываются)
                            send_http_request(api_url, barcode)
                            
                            # Очищаем буфер порта на случай, если пользователь успел пикнуть еще раз
                            ser.reset_input_buffer()
                            
                            log.info("[Система] Возврат в режим фонового ожидания кодов...")
                            
                    time.sleep(0.05) # Минимальная пауза для разгрузки процессора
                    
        except serial.SerialException:
            log.debug(f"[Ошибка] Порт {com_port} недоступен. Повторное подключение через 5 секунд...")
            time.sleep(5)
        except KeyboardInterrupt:
            log.gebug("\n[Система] Приложение остановлено пользователем.")
            break
        except Exception as e:
            log.critical(f"[Критическая ошибка]: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
