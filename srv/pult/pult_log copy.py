from logging import FileHandler
import logging
import os
import errno
from datetime import datetime


def __mkdirlogs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


def get_logger(name=__file__, file='logs/{:%Y-%m-%d}.log'.format(datetime.now()), encoding='utf-8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s](%(funcName)s) %(message)s')

    # В файл
    __mkdirlogs(os.path.dirname(file))

    fh = FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # В stdout
#    sh = logging.StreamHandler(stream=sys.stdout)
#    sh.setFormatter(formatter)
#    log.addHandler(sh)
    return log
