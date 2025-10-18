from typing import Any, Dict, List, Optional, TypedDict, Union

class TMediator:
    def state(self, event: str, body: Optional[Dict[str, Any]] = None) -> None:
        pass
    
class TUi(TypedDict):
    timeout_next: int # Время отката при вызове
    timeout_check: int # Время ?
    winfo_x: int # ?
    winfo_y: int # ?
    mode: str # Modes: "System" (standard), "Dark", "Light"
    theme: str # Themes: "blue" (standard), "green", "dark-blue"
    scaling: float # Масштаб
    shift_left: int # Сдвиг слева
    shift_bottom: int # Сдвиг снизу

class TPult(TypedDict):
    eq_wplace: str  # ID рабочего места
    eq_url: str # Адрес сервера
    fil: str  # Номер филиала
    eq_auth: List[str]  # Login, Pass
    ui: TUi
    set: List[List[Union[int, str]]]

class TLedTablo(TypedDict):
    id: str
    title: str
    port: str

class TQueue(TypedDict):
    id: str
    title: str

class TSetQueue(TypedDict):
    user_id: str
    queues: List[TQueue]
    queues_delay: List[TQueue]
    adapter_setting: str
    led_tablo: TLedTablo
    month_id: str
    message: str

class TResponseSetQueue(TypedDict):
    stdout: TSetQueue
    stderr: str

class TTicket(TypedDict):
    id: str
    title: str
    queue_id: str

class TInfoTicket(TypedDict):
    ticket: TTicket
    message: str

class TResponseInfoTicket(TypedDict):
    stdout: TInfoTicket
    stderr: str

