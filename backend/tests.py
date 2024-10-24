import unittest
import sqlite3
from init import dummy_data
import pandas as pd

class TestDummyData(unittest.TestCase):

    def setUp(self) -> None:
        self.con = sqlite3.connect(r'../data/tables.db')
        self.agent_gen = dummy_data.generate_call_data(self.con)

        return super().setUp()

    def test_callend_converted_only_true(self):
        self.assertTrue(
            self.agent_gen[
                (self.agent_gen['CONVERTED'] == True) & (self.agent_gen['CALLENDREASON'] != 'Converted')
                ].shape[0] == 0
        )
