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


    def test_logger_prog_bar_1(self):
        """Assign an iterable to the logger's ProgressBar object BEFORE the for loop"""
        items = self.logger.progress_bar(list(range(0, 15)), 'Testing pre-loop setup..')
        for item in items:
            # Do stuff...
            sleep(0.1)


    def test_logger_prog_bar_2(self):
        """Assign an iterable to the logger's ProgressBar object IN the for loop statement"""
        items = list(range(0, 15))
        for item in self.logger.progress_bar(items, 'Testing in-loop setup...'):
            # Do stuff...
            sleep(0.1)


    def test_logger_prog_bar_3(self):
        """Yield the logger's ProgressBar object and assign an iterable. Loop over the ProgressBar iterable."""
        items = list(range(0, 15))
        with self.logger.progress_bar.watch(items, 'Testing context manager logger.pb watch iterable...') as pb_items:
            for item in pb_items:
                # Do stuff...
                sleep(0.1)


    def test_cm_prog_bar(self):
        """Create a ProgressBar with a set length & manually update inside a loop"""
        items = list(range(0, 15))
        with ProgressBar.custom(len(items), title='Testing context manager new progress bar, manual update...', draw_mode='pacman') as pb:
            for item in items:
                # Do stuff...
                sleep(0.1)
                # Update Progress Bar
                pb.update()


    def test_enumerate_prog_bar(self):
        """Testing that the enumerate functionality remains intact."""
        items = list(range(0, 15))
        with self.logger.progress_bar.watch(items, 'Testing progress bar with enumerate...') as pb_items:
            for i, item in enumerate(pb_items):
                # Do stuff...
                sleep(0.1)
