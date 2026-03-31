#!/bin/bash

# python -m PyInstaller sb05.py  --hidden-import=python-vlc --add-data='/usr/lib64/vlc':'vlc/'
pyinstaller --noconfirm --onefile --windowed --paths "./" --hidden-import=python-vlc --add-data='/usr/lib64/vlc':'vlc/' sb05.py