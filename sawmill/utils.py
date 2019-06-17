from contextlib import contextmanager
from enum import Enum
from timeit import default_timer as timer
import sys


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


class ProgressBar:
    def __init__(
        self,
        total: int = None,
        iteration: int = None,
        prefix: str = 'Progress',
        suffix: str = 'Complete',
        decimals: int = 2,
        length: int = 80,
        draw_mode: str = ''):
        """ """
        self.total = total
        self.iteration = iteration
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length

        self.start = None
        self.end = None
        self.__iterable = None

        self.draw_interval = 0.25
        self.draw_time = 0
        self.draw_count = 0

        self.prefix_colour = Colour.ORANGE.value
        self.number_colour = Colour.PURPLE.value
        self.suffix_colour = Colour.GREEN.value
        self.bar_colour = Colour.GREEN.value
        self.done_fill='█'
        self.active_fill='█'
        self.bar_ends = '|'
        self.bar_back = ['-' for _ in range(self.length)]

        if draw_mode == 'pacman':
            self.done_fill=' '
            self.active_fill = self.colour_string('ᗣ', Colour.RED.value)
            self.active_fill += self.colour_string(' ᗣ', Colour.LIGHT_BLUE.value)
            self.active_fill += self.colour_string(' ᗣ', Colour.ORANGE.value)
            self.active_fill += self.colour_string(' ᗣ', Colour.PINK.value)
            self.active_fill += self.colour_string(' ᗧ', Colour.YELLOW.value)
            self.bar_ends = self.colour_string('||', Colour.BLUE.value)
            for i, v in enumerate(self.bar_back):
                self.bar_back[i] = '•' if i in [x*6 for x in range(1,20)] else '·'
            self.bar_colour = Colour.YELLOW.value


    def __call__(self, iterable, title=''):
        """Use a ProgressBar to iterate through an iterable."""
        if title:
            print(self.colour_string(title, Colour.WHITE.value))
        self.reset()
        self.total = len(iterable)
        self.__iterable = iter(iterable)
        return self


    def __iter__(self):
        return self


    def __next__(self):
        try:
            value = next(self.__iterable)
            if not self.start:
                self.start = timer()
            self.update()
            return value

        except StopIteration:
            if not self.end:
                self.end = timer()
            sys.stdout.write('\n')
            sys.stdout.flush()
            print(self.colour_string(f'{self.total} items processed in %.2fs' % (self.end-self.start), Colour.PINK.value))
            raise


    @contextmanager
    def watch(self, iterable, title=''):
        """A context manager that yields an already existing ProgressBar as an interable wrapper"""
        print()
        if title:
            print(self.colour_string(title, Colour.WHITE.value))

        yield self(iterable)
        self.reset()
        print()


    def draw(self):
        self.draw_count += 1
        self.draw_time = timer()

        full_value = 100 * (self.iteration / float(self.total))
        display_value = f'%.{str(self.decimals)}f' % full_value

        filled_length = int(self.length * self.iteration // self.total)
        filled_bar = self.done_fill * filled_length
        empty_bar = ''.join(self.bar_back[filled_length: self.length])
        bar = filled_bar + self.active_fill + self.colour_string(empty_bar, self.bar_colour)

        out_string = self.colour_string(f'\r{self.prefix} ', self.prefix_colour)
        out_string += self.bar_ends
        out_string += self.colour_string(f'{bar}', self.bar_colour)
        out_string += self.bar_ends
        out_string += self.colour_string(f' {display_value}% ', self.number_colour)
        out_string += self.colour_string(f'{self.suffix}', self.suffix_colour)

        sys.stdout.write(out_string)
        sys.stdout.flush()


    def colour_string(self, input_str, colour):
        return '\033[38;5;%dm' % colour + input_str + '\033[0m'


    def update(self):
        self.iteration += 1
        if (timer() - self.draw_time) > self.draw_interval or self.iteration == self.total:
            self.draw()


    def reset(self):
        self.iteration = 0
        self.total = None
        self.start = None
        self.end = None


    @classmethod
    @contextmanager
    def custom(cls, total, iteration=0, title='', prefix='Progress', suffix='Complete', decimals=2, length=80, draw_mode=''):
        """A context manager that yields a new ProgressBar object - gives user control of contructor args"""
        if title:
            print(cls.colour_string(cls, title, Colour.WHITE.value))

        start = timer()
        yield cls(total, iteration, prefix, suffix, decimals, length, draw_mode)
        end = timer()

        sys.stdout.write('\n')
        sys.stdout.flush()
        print(cls.colour_string(cls, f'{total} items processed in %.2fs' % (end-start), Colour.PINK.value))
