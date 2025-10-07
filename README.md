# electronic-queue

## TV-сервер

Путь: srv/tv

### Операционная система

Версия ОС Centos 8

- yum install bzip2-devel -y
- yum install ncurses-devel -y
- yum install libffi-devel -y
- yum install readline-devel -y
- yum install sqlite-devel -y
- yum install tk-devel -y

### Язык программирования

Python 3.8.10

### Библиотеки для Python

Файл: requirements1.txt

- altgraph==0.17.4
- certifi==2025.7.14
- charset-normalizer==3.4.2
- customtkinter==5.2.2
- darkdetect==0.8.0
- idna==3.10
- importlib_metadata==8.5.0
- packaging==25.0
- pillow==10.4.0
- psutil==7.0.0
- pygame==2.6.1
- pyinstaller==6.14.2
- pyinstaller-hooks-contrib==2025.8
- python-vlc==3.0.21203
- requests==2.32.4
- tk==0.1.0
- urllib3==2.2.3
- zipp==3.20.2

### Дополнительно

- VLC 3.0.21
- pyinstaller 6.14.2

### Сборка

Файл: build.sh
Команда: #!/bin/bash

```
python -m PyInstaller sb05.py --onefile --hidden-import=logger.py --hidden-import=sb05_ui.py --hidden-import=sb05_vars.py --hidden-import=date_time.py --hidden-import=customtkinter --hidden-import=tkinter --hidden-import=python-vlc --add-data='/usr/lib64/vlc':'vlc/'
```


