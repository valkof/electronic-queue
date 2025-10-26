import customtkinter as ctk

from pult_types import TMediator
from pult_db import DataBase
from ..elements.LockableButton import LockableButton

class FrameAuth(ctk.CTkFrame):
    def __init__(self, parent, mediator: TMediator, db: DataBase):
        super().__init__(parent)

        self._mediator = mediator
        self._db = db
        
        # Создание переменных для хранения значений
        self.combo_var = ctk.StringVar()
        self.entry_var = ctk.StringVar()
        self.label_var = ctk.StringVar()
        
        # Создание виджетов
        # Выпадающий список
        self.combo = ctk.CTkComboBox(
            self, width=300,
            values=[item[2] for item in db.setPult['set']],
            variable=self.combo_var, state="readonly"
        )
        self.combo.set(db.setPult['set'][0][2])
        self.combo.grid(row=0, column=0, padx=20, pady=10)
        
        # Поле ввода чисел
        self.entry = ctk.CTkEntry(
            self, width=300,
            placeholder_text="Пароль",
            textvariable=self.entry_var
        )
        self.entry.grid(row=1, column=0, padx=20, pady=10)
        self.entry.focus_set()
        
        # Кнопка действия
        self.button = LockableButton(
            self,
            text="ВОЙТИ",
            command=self.button_click
        )
        self.button.grid(row=2, column=0, padx=20, pady=5)

        # Сообщение
        self.label = ctk.CTkLabel(
            self, width=300,
            text='', text_color='red'
        )
        self.label.grid(row=3, column=0, padx=20, pady=0)
        
        # Настройка растяжения столбцов
        self.grid_columnconfigure(0, weight=1)

        self.enter_unlock()

    def enter_lock(self):
        """Блокирование клавиши Enter"""
        self.entry.unbind("<Return>")
        self.entry.unbind("<KP_Enter>")

    def enter_unlock(self):
        """Активация клавиши Enter"""
        self.entry.bind("<Return>", self.on_enter_pressed)
        self.entry.bind("<KP_Enter>", self.on_enter_pressed)

    def on_enter_pressed(self, event):
        self.button_click()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def button_click(self):
        self.enter_lock()
        self.combo.configure(state=ctk.DISABLED)
        self.entry.configure(state=ctk.DISABLED)
        self.button.lock()
        self.verify_authorization()

    def verify_authorization(self):
        selected_option = self.combo_var.get()
        kod = self.entry_var.get()
        
        matches = []
    
        for item in self._db.setPult['set']:
            if item[1] == kod and item[2] == selected_option:
                matches.append(item)
        
        if len(matches) == 1:
            self.label_show()
            oper_id = matches[0][0]
            self._db.setOperId(oper_id)
            self._mediator.state('get_data_pult')
        else:
            self.label_show('Неверный пароль')
            self.button.unlock()
            self.enter_unlock()
            self.combo.configure(state=ctk.NORMAL)
            self.entry.configure(state=ctk.NORMAL)

    def label_show(self, message: str = ''):
        self.label.configure(text=message)

