import unittest
import sqlite3
from init import dummy_data, database
import pandas as pd
import calendar
import datetime as dt
import os

class TestDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.test_db_path = rf'../data/test/test_tables.db'
        self.con = sqlite3.connect(self.test_db_path)
        database.build_database(self.con)
        self.agent_gen = dummy_data.generate_agent_data(self.con)
        self.call_gen = dummy_data.generate_call_data(self.con)

        return super().setUp()

    def test_callend_converted_only_true(self):
        self.assertTrue(
            self.call_gen[
                (self.call_gen['CONVERTED'] == True) & (self.call_gen['CALLENDREASON'] != 'Converted')
                ].shape[0] == 0
        )

    def test_calendar(self):
        cal = dummy_data.create_datedim(self.con)

    def tearDown(self):
        self.con.close()
        os.remove(self.test_db_path)



class TestCallSample(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()
