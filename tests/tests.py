from time import sleep
from typing import List
import unittest
import logging

from sawmill.logger import Sawmill
from sawmill.utils import ProgressBar

__all__: List = ['SawmillTests']

class SawmillTests(unittest.TestCase):
    def setUp(self):
        self.logger = Sawmill.new_logger(__name__)

    def test_one(self):
        self.logger.debug("test output")
        self.assertTrue(isinstance(self.logger, logging.Logger))

    def test_logger_prog_bar(self):
        items = self.logger.progress_bar(list(range(0, 43)), 'Testing progress bar iterable...')
        for item in items:
            # Do stuff...
            sleep(0.1)

        items = list(range(0, 43))
        for item in self.logger.progress_bar(items, 'Testing progress bar iterable again...'):
            # Do stuff...
            sleep(0.1)


    def test_cm_prog_bar(self):
        items = list(range(0, 43))
        
        with ProgressBar.load(len(items), msg='Testing CM progress bar...', draw_mode='') as pb:
            for item in items:
                # Do stuff...
                sleep(0.1)
                # Update Progress Bar
                pb.update()

        with ProgressBar.load(len(items), msg='Testing CM pacman progress bar...', draw_mode='pacman') as pb:
            for item in items:
                # Do stuff...
                sleep(0.1)
                # Update Progress Bar
                pb.update()

