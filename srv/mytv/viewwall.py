from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QStatusBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.showFullScreen()
        
        self.setWindowFlag(Qt.FramelessWindowHint)  # Скрываем заголовок окна

        self.setWindowTitle("Мой браузер")
        
        # Создаем веб-просмотр
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://tutmed.by/infotablo/"))
        self.setCentralWidget(self.browser)
        
        # Добавляем панель состояния
        # self.status = QStatusBar()
        # self.setStatusBar(self.status)
        
        # Создаем панель инструментов
        # toolbar = QToolBar()
        # self.addToolBar(toolbar)
        
        # Кнопка "Назад"
        # back_btn = QAction("Назад", self)
        # back_btn.triggered.connect(self.browser.back)
        # toolbar.addAction(back_btn)
        
        # Кнопка "Вперед"
        # next_btn = QAction("Вперед", self)
        # next_btn.triggered.connect(self.browser.forward)
        # toolbar.addAction(next_btn)
        
        # Кнопка "Обновить"
        # reload_btn = QAction("Обновить", self)
        # reload_btn.triggered.connect(self.browser.reload)
        # toolbar.addAction(reload_btn)
        
        # Поле ввода URL
        # self.urlbar = QLineEdit()
        # self.urlbar.returnPressed.connect(self.navigate_to_url)
        # toolbar.addWidget(self.urlbar)
        
        # Кнопка "Стоп"
        # stop_btn = QAction("Стоп", self)
        # stop_btn.triggered.connect(self.browser.stop)
        # toolbar.addAction(stop_btn)
        
        # Связываем события
        # self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - Мой браузер")

    # def navigate_to_url(self):
    #     q = QUrl(self.urlbar.text())
    #     if q.scheme() == "":
    #         q.setScheme("http")
    #     self.browser.setUrl(q)

    # def update_urlbar(self, q):
    #     self.urlbar.setText(q.toString())
    #     self.urlbar.setCursorPosition(0)

if __name__ == "__main__":
    app = QApplication([])
    browser = Browser()
    browser.show()
    app.exec_()
