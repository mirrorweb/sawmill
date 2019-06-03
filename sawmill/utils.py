from enum import Enum


class MsgFormat(Enum):
    """Structure of the log that will be output. To add a new format just add an Enum option and change your config."""
    SIMPLE = (
        '%(levelname)6s\t%(message)s'
    )
    LINE = (
        '%(levelname)6s\t[%(name)s] %(funcName)s %(message)s'
    )
    BOXED_L = (
        '\t.------------------------------------------------------------------------------------------------------\n'
        '%(levelname)6s%(message)s\n'
        '\t|______________________________________________________________________________________________________\n'
        '\t| [%(name)s] %(funcName)s\n'
        '\t| "%(pathname)s", line %(lineno)s\n'
        '\t\'------------------------------------------------------------------------------------------------------'
    )
    BOXED_M = (
        '\t.------------------------------------------------------------------------------------------------------\n'
        '%(levelname)6s%(message)s\n'
        '\t| "%(pathname)s", line %(lineno)s\n'
        '\t\'------------------------------------------------------------------------------------------------------'
    )
    BOXED_S = (
        '\t.------------------------------------------------------------------------------------------------------\n'
        '%(levelname)6s%(message)s\n'
        '\t\'------------------------------------------------------------------------------------------------------'
    )
    SYSOUT = (
        '%(asctime)s - %(levelname)8s - [%(name)s] - %(message)s (%(filename)s: %(lineno)d)'
    )

class Colour(Enum):
        """256 colour values"""
        RED = 160
        LIGHT_RED = 9
        DARK_RED = 124

        BLUE = 39
        LIGHT_BLUE = 45
        DARK_BLUE = 25

        GREEN = 106
        LIGHT_GREEN = 46
        DARK_GREEN = 22

        YELLOW = 184
        LIGHT_YELLOW = 228
        DARK_YELLOW = 178

        ORANGE = 208
        LIGHT_ORANGE = 214
        DARK_ORANGE = 166

        PURPLE = 135
        LIGHT_PURPLE = 177
        DARK_PURPLE = 55

        PINK = 211
        LIGHT_PINK = 218
        DARK_PINK = 204

        WHITE = 255
        GREY = 243
        LIGHT_GREY = 250
        DARK_GREY = 237
        BLACK = 232

def show_logger_tree():
    """prints all loggers in a tree hierarchy structure"""
    # create a list of all loggers, with root at [0]
    output = ['-------------------------------']
    output.append(f'   + root [{logging.getLevelName(logging.getLogger().level)}]')

    for name, logger in sorted(logging.Logger.manager.loggerDict.items()):
        if isinstance(logger, logging.PlaceHolder):
            continue

        indent = '   '*(name.count('.')+1) if name != 'root' else ''
        prop = '+ ' if logger.propagate else '  '
        handlers = ': ' + str(logger.handlers) if len(logger.handlers) > 0 else ''
        level = logging.getLevelName(logger.level)
        eff_level = logging.getLevelName(logger.getEffectiveLevel())
        level_str = f' [{level}]' if level == eff_level else f' [{level} -> {eff_level}]'

        output.append(indent + prop + name + level_str + handlers)

    output.append('-------------------------------')
    print('\n'.join(output))
