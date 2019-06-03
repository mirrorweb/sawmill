from typing import List
import unittest
import logging

from sawmill.logger import Sawmill

__all__: List = ['SawmillTests']

class SawmillTests(unittest.TestCase):
    def setUp(self):
        self.logger = Sawmill.new_logger(__name__)

    def test_one(self):
        self.assertTrue(isinstance(self.logger, logging.Logger))

