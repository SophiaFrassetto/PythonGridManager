import sys
from enum import Enum
from logging import info, error, debug, warning, warn

ANSI = u'\u001b['
CSI = u'\x1b['

#https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation
__all__ = ['bprint', 'ANSI', 'CSI', 'DEFAULT_COLORS', 'DEFAULT_BG_COLORS', 'DEFAULT_DECORATIONS']


class DEFAULT_COLORS(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    WHITE = 255


class DEFAULT_BG_COLORS(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    WHITE = 255


class DEFAULT_DECORATIONS(Enum):
    BOLD = 1
    UNDERLINE = 4
    REVERSED = 7


def bprint(
    command: str,
    lines: int = 0,
    columns: int = 0,
    color: int = None,
    bg_color: int = None,
    decoration: list = None,
    log: object = print,
    clear_line: bool = False,
    reset_cursor: bool = False):
    # mapping to levels for color default
    log_level_map = {print: 255, info: 255, error: 196, debug: 200, warning: 220}

    if log == warn:
        log = warning
    if log not in log_level_map:
        log = print

    if not color:
        color = log_level_map[log]

    # save last cursor position
    sys.stdout.write(f"{CSI}s")

    # clear line
    if clear_line:
        print(f"{CSI}K")
    if lines and columns:
        # set line and column
        sys.stdout.write(f"{CSI}{lines};{columns}f")
    elif lines and not columns:
        # set line
        sys.stdout.write(f"{CSI}{lines}f")
    elif columns and not lines:
        # set column
        sys.stdout.write(f"{CSI}u")
        sys.stdout.write(f"{CSI}1A")
        sys.stdout.write(f"{CSI}{columns - 1}C")
        sys.stdout.flush()

    # set decoration
    if decoration:
        if isinstance(decoration, list):
            for dec in decoration:
                sys.stdout.write(f"{ANSI}{dec}m")
        else:
            sys.stdout.write(f"{ANSI}{decoration}m")

    # set background
    if bg_color:
        sys.stdout.write(f"{ANSI}48;5;{bg_color}m")

    # set color
    sys.stdout.write(f"{ANSI}38;5;{color}m")

    sys.stdout.flush()
    log(command)

    # reset color
    sys.stdout.write(f"{CSI}m")
    sys.stdout.flush()

    if reset_cursor:
        sys.stdout.write(f"{CSI}u")
        sys.stdout.flush()