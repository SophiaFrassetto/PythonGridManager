import sys
from os import system, name

from .beautiful_print import CSI

__all__ = ['clear_windown', 'resize_windown']


def clear_windown():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

   
def resize_windown(lines, columns):
    sys.stdout.write(f"{CSI}8;{lines};{columns}t")