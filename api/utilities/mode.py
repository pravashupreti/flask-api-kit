"""Tools for setting system modes across processes without using the DB"""
import os

from config import Config

MODE_PATH = Config.ROOT + "/var/modes/{}"

MODE_MAINTENANCE = "maintenance"


def has_mode(mode: str) -> bool:
    return os.path.exists(MODE_PATH.format(mode))


def set_mode(mode: str):
    if has_mode(mode):
        return
    path = MODE_PATH.format(mode)
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    with open(path, 'a'):
        os.utime(path, None)


def remove_mode(mode: str):
    if not has_mode(mode):
        return
    os.remove(MODE_PATH.format(mode))



