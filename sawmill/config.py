from decouple import config
from enum import Enum
import logging
import os

from .utils import Colour, MsgFormat


class Conf:
    """
    Sawmill config file.
    Allows the user to set options which will determine how logs are displayed
    """
    # ---------------------------------------------------
    # Developer Mode
    # ---------------------------------------------------
    #   True: console & file output active.
    #   False: sysout is active.
    DEVELOPER_MODE = config('SAWMILL_DEVELOPER_LOGS', default=False, cast=bool)
    PB_DRAW_MODE = config('SAWMILL_PB_MODE', default='', cast=str)


    # ---------------------------------------------------
    # Default logging level of each output type
    # ---------------------------------------------------
    DEFAULT_FILE_LEVEL = logging.DEBUG
    DEFAULT_SYSOUT_LEVEL = logging.INFO
    DEFAULT_CONSOLE_LEVEL = logging.DEBUG

    # ---------------------------------------------------
    # File output settings
    # ---------------------------------------------------
    output_dir = 'sawmill/log_files/'
    file_name = 'timber.log'
    
    
    if DEVELOPER_MODE:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    FILE = {
        'MSG_FMT': MsgFormat.SYSOUT,
        'DATE_FMT': '%d/%m/%Y %I:%M:%S%p',
        'OUTPUT_DIR': output_dir + file_name,
        'MAX_BYTES': 200000,
        'BACKUPS': 3,
    }

    # ---------------------------------------------------
    # Sysout settings
    # ---------------------------------------------------
    SYSOUT = {
        'MSG_FMT': MsgFormat.SYSOUT,
        'DATE_FMT': '%d/%m/%Y %I:%M:%S%p',
    }

    # ---------------------------------------------------
    # Console output settings
    # ---------------------------------------------------
    DEBUG = {
        'fmt': MsgFormat.BOXED_S,
        'primary_colour': Colour.BLUE,
        'secondary_colour': Colour.DARK_RED,
        'tertiary_colour': Colour.LIGHT_BLUE,
    }
    INFO = {
        'fmt': MsgFormat.LINE,
        'primary_colour': Colour.DARK_YELLOW,
        'secondary_colour': Colour.GREEN,
        'tertiary_colour': Colour.WHITE,
    }
    WARNING = {
        'fmt': MsgFormat.SIMPLE,
        'primary_colour': Colour.YELLOW,
        'secondary_colour': Colour.DARK_YELLOW,
        'tertiary_colour': Colour.ORANGE,
    }
    ERROR = {
        'fmt': MsgFormat.BOXED_L,
        'primary_colour': Colour.RED,
        'secondary_colour': Colour.LIGHT_RED,
        'tertiary_colour': Colour.RED,
    }
    CRITICAL = {
        'fmt': MsgFormat.BOXED_L,
        'primary_colour': Colour.PINK,
        'secondary_colour': Colour.PINK,
        'tertiary_colour': Colour.PURPLE,
    }
