"""
Sawmill is a custom logger class which processes default logs and outputs nicer ones!
Use config.py file to alter log format, colour & file output settings.
Use utils.py file to add new log formats & colour options.

"Felled logs are generally transported to a sawmill to be cut up/processed"
Author: Lee Booth
"""
from contextlib import contextmanager
from enum import Enum
from logging.handlers import RotatingFileHandler
import copy
import logging
import sys

from .config import Conf
from .utils import Colour


class Sawmill(logging.Logger):
    """A custom logger which can be configured to output logs to the user's preference. Includeds a colour formatter."""
    def __init__(self, name, console_lvl=None, file_lvl=None, sysout_lvl=None):
        super().__init__(name, logging.DEBUG)
        self.propagate = False
        self.developer_mode = Conf.DEVELOPER_MODE
        self.console_level = console_lvl if console_lvl else Conf.DEFAULT_CONSOLE_LEVEL
        self.file_level = file_lvl if file_lvl else Conf.DEFAULT_FILE_LEVEL
        self.sysout_level = sysout_lvl if sysout_lvl else Conf.DEFAULT_SYSOUT_LEVEL

        if self.developer_mode:
            console = logging.StreamHandler()
            console.setFormatter(ColoredFormatter())
            console.setLevel(self.console_level)
            self.addHandler(console)

            log_file = RotatingFileHandler(
                filename=Conf.FILE['OUTPUT_DIR'],
                maxBytes=Conf.FILE['MAX_BYTES'],
                backupCount=Conf.FILE['BACKUPS'],
                delay=True,
            )
            log_file.setFormatter(logging.Formatter(fmt=Conf.FILE['MSG_FMT'].value, datefmt=Conf.FILE['DATE_FMT']))
            log_file.setLevel(self.file_level)
            self.addHandler(log_file)

        else:
            syslog = logging.StreamHandler(sys.stdout)
            syslog.setFormatter(logging.Formatter(fmt=Conf.SYSOUT['MSG_FMT'].value, datefmt=Conf.SYSOUT['DATE_FMT']))
            syslog.setLevel(self.sysout_level)
            self.addHandler(syslog)

    @property
    def console_level_name(self):
        return logging.getLevelName(self.console_level)

    @property
    def file_level_name(self):
        return logging.getLevelName(self.file_level)

    @property
    def sysout_level_name(self):
        return logging.getLevelName(self.sysout_level)

    @classmethod
    def new_logger(cls, logger_name: str, custom_console_lvl=None, custom_file_lvl=None, custom_sysout_lvl=None):
        """Create a new Sawmill logger with handlers. Custom levels can be passed in, otherwise they default."""
        return cls(logger_name, custom_console_lvl, custom_file_lvl, custom_sysout_lvl)


class ColoredFormatter(logging.Formatter):
    """Custom formatter which overrides log messages and uses escape charaters to insert colour codes"""
    def __init__(self):
        super().__init__(datefmt='%d/%m/%Y %I:%M:%S%p')
        self.use_colour = True

    class Codes(Enum):
        """Escape character values"""
        RESET = '\033[0m'
        COLOUR = '\033[%dm'
        COLOUR_256 = '\033[38;5;%dm'
        COLOUR_B256 = '\033[48;5;%dm'
        BOLD = '\033[1m'
        DIM = '\033[2m'
        ITALIC = '\033[3m'
        UNDERLINE = '\033[4m'
        INVERT = '\033[7m'

    @contextmanager
    def non_destructive_style_change(self, record):
        format_orig = self._style._fmt
        try:
            FMT, COL1, COL2, COL3 = getattr(Conf, record.levelname).values()
            self._style._fmt = FMT.value
            yield copy.copy(record), FMT.name, COL1.value, COL2.value, COL3.value

        finally:
            self._style._fmt = format_orig

    def format(self, record):
        """create a copy of the log records & modify them using the config settings"""
        with self.non_destructive_style_change(record) as recordcopy:
            log, msg_fmt, primary_col, secondary_col, tertiary_col = recordcopy
            if self.use_colour:
                log.name = self.apply_styling(record.name, colour=secondary_col)
                log.levelname = self.apply_styling(record.levelname, colour=tertiary_col, bold=True)
                log.pathname = self.apply_styling(record.pathname, colour=Colour.DARK_BLUE.value, underline=True, italic=True)
                log.lineno = self.apply_styling(str(record.lineno), colour=secondary_col, bold=True)

                # change the way the function name is displayed
                if record.funcName == '<module>':
                    log.funcName = ''
                else:
                    if msg_fmt in ['SIMPLE', 'LINE']:
                        log.funcName = self.apply_styling(record.funcName, colour=tertiary_col)
                    else:
                        log.funcName = self.apply_styling(f'def {record.funcName}():', colour=tertiary_col)

                # boxed styling - split message lines, add tabs and '|' before each 
                if msg_fmt in ['BOXED_L', 'BOXED_M', 'BOXED_S']:
                    lines = record.msg.split('\n')
                    for i, val in enumerate(lines):
                        lines[i] = '\t| ' + self.apply_styling(val, colour=primary_col)
                    log.msg = '\n'.join(lines)
                else:
                    log.msg = self.apply_styling(record.msg, colour=primary_col)

            return logging.Formatter.format(self, log)

    def apply_styling(self, log_str, colour=None, back_colour=None, bold=False, dim=False, italic=False, underline=False, invert=False):
        """inserts values into a string allowing us to apply visial styles to it in the bash terminal"""
        log_str = self.Codes.COLOUR_256.value % colour + log_str if colour else log_str
        log_str = self.Codes.COLOUR_B256.value % back_colour + log_str if back_colour else log_str

        for style, value in {'BOLD': bold, 'DIM': dim, 'ITALIC': italic, 'UNDERLINE': underline, 'INVERT': invert}.items():
            log_str = self.Codes[style].value + log_str if value else log_str

        return log_str + self.Codes.RESET.value
