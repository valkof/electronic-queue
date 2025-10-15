import customtkinter as ctk

from pult_config import AppSet
from pult_types import TMediator
from ..elements.LockableButton import LockableButton

class FrameControl(ctk.CTkFrame):
    """
    Фрейм кнопок для управления талоном
    """
    def __init__(self, parent, mediator: TMediator, app_set: AppSet):
        super().__init__(parent, corner_radius=0)
        # self.configure(border_width=1, border_color="blue")

        # self._mediator = mediator
        # self._app_set = app_set

        self.bmain_next = LockableButton(self, text="➜ Следующий", command=self.equqe_next)
        self.bmain_next.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")
        self.bmain_next.grid_remove()

        self.bmain_curr = LockableButton(self, text="⟳ Повторить") #TODO command=self.eq_curr_w)
        self.bmain_curr.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.bmain_notshow = LockableButton(self, text="✖ Не явился") #TODO command=self.eq_notshow_w)
        self.bmain_notshow.grid(row=0, column=2, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

        self.bmain_end = LockableButton(self, text="✔ Обслужен") #TODO command=self.eq_end_w)
        self.bmain_end.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), ipadx=0, sticky="ew")

    def equqe_next(self):
        """
          {
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
        """
        self.bmain_next.lock()
        # self.mediator('beg_next')
        # r = {'stdout': None, 'stderr': None}
        # try:
        #     qq = ','.join([x for x in queues])
        #     path = 'tnexts?w=' + app_set.dH['eq_wplace'] + '&qq=' + qq
        #     r = self.get_request(path)
        # except Exception as e:
        #     r['stderr'] = str(e) + ". "
        
        # self.mess = r['stderr']
        # if r['stdout'] is None:
        #     self.ticket = '----'
        #     self.mediator('end_next', False)
        # else:
        #     self.ticket = r['stdout']
        #     self.mediator('end_next')
        #     self.bmain_curr.after(app_set.dH["ui"]["timeout_next"]*1000, self.mediator, 'end_next_timeout')

"""
{
  "stdout": {
    "ticket": {
      "id": "1",
      "title": "Р001",
      "queue_id": "1"
    },
    "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
  },
  "stderr": ""
}
"""

"""
{
  "stdout": {
    "message": "Нет записи на табло окна оператора 192.168.10.15:2323"
  },
  "stderr": ""
}
"""