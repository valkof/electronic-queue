import customtkinter as ctk
from ..elements import LockableButton
from ...pult_vars import AppSet
from ...pult import Mediator

class FrameAuth(ctk.CTkFrame):
    def __init__(self, parent, mediator: Mediator, app_set: AppSet):
        super().__init__(parent)

        self._mediator = mediator
        self._app_set = app_set
        
        # Создание переменных для хранения значений
        self.combo_var = ctk.StringVar()
        self.entry_var = ctk.StringVar()
        self.label_var = ctk.StringVar()
        
        # Создание виджетов
        # Выпадающий список
        self.combo = ctk.CTkComboBox(
            self, width=300,
            values=[item[2] for item in app_set.pult['set']],
            variable=self.combo_var, state="readonly"
        )
        self.combo.set(app_set.pult['set'][0][2])
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
        self.button.grid(row=2, column=0, padx=20, pady=10)

        # Сообщение
        self.label = ctk.CTkLabel(
            self, width=300,
            text='', text_color='red'
        )
        self.label.grid(row=3, column=0, padx=20, pady=10)
        
        # Настройка растяжения столбцов
        self.grid_columnconfigure(0, weight=1)

        self.entry.bind("<Return>", self.on_enter_pressed)
        self.entry.bind("<KP_Enter>", self.on_enter_pressed)

    def on_enter_pressed(self, event):
        self.button_click()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def button_click(self):
        self.button.lock()
        self.verify_authorization()

    def verify_authorization(self):
        selected_option = self.combo_var.get()
        kod = self.entry_var.get()
        
        matches = []
    
        for item in self._app_set.pult['set']:
            if item[1] == kod and item[2] == selected_option:
                matches.append(item)
        
        if len(matches) == 1:
            self.label_show()
            oper_id = matches[0][0]
            self._mediator.state('get_data_pult', {'oper_id': oper_id})
        else:
            self.label_show('Неверный пароль')
            self.button.unlock()

    def label_show(self, message: str = ''):
        self.label.configure(text=message)

