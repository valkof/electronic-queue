#!/bin/bash

python -m PyInstaller sb05.py --onefile --hidden-import=logger.py --hidden-import=sb05_ui.py --hidden-import=sb05_vars.py --hidden-import=date_time.py --hidden-import=customtkinter --hidden-import=tkinter --hidden-import=python-vlc --add-data='/usr/lib64/vlc':'vlc/'

