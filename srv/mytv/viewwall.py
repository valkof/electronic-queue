import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QTimer

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.showFullScreen()
        
        path = self.read_settings_host()

        print(path)

        self.setWindowFlag(Qt.FramelessWindowHint)  # Скрываем заголовок окна

        self.setWindowTitle("Мой браузер")
        

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(path + "/cgi-bin/is10_08?sSd_=0&svid_=1&sgr_l=360&sit_l=1021&sfil_n=19"))
        self.setCentralWidget(self.browser)
        
        self.browser.loadFinished.connect(self.update_title)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_window)
        self.timer.start(60000)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - Мой браузер")

    def update_window(self):
        print('ewf')
        if not self.isFullScreen():
            self.showFullScreen()

    def read_settings_host(self, config_file='wall_set.json'):
        """
        Читает настройки хоста из JSON-файла.
        
        Args:
            config_file (str): Путь к JSON-файлу с настройками.
        
        Returns:
            str: Путь из настройки 'host.path', или None при ошибке.
        """
        # Проверяем существование файла
        if not os.path.exists(config_file):
            print(f"Ошибка: файл {config_file} не найден.")
            return None

        try:
            with open(config_file, 'r', encoding='utf-8') as data:
                config = json.load(data)
            
            # Проверяем наличие ключей
            if 'host' not in config:
                print("Ошибка: в конфигурации отсутствует раздел 'host'.")
                return None
            
            if 'path' not in config['host']:
                print("Ошибка: в разделе 'host' отсутствует ключ 'path'.")
                return None
            
            path = config['host']['path']
            
            # Дополнительная валидация (например, не пустой ли путь)
            if not path or not path.strip():
                print("Ошибка: значение 'path' пустое или состоит из пробелов.")
                return None
            
            return path.strip()
        
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None

if __name__ == "__main__":
    app = QApplication([])
    browser = Browser()
    browser.show()
    app.exec_()
