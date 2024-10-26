import unittest
import sqlite3
from init import dummy_data, database
from selection import sample_calls
import pandas as pd
import calendar
import datetime as dt
import os

class TestDatabase(unittest.TestCase):

    test_db_path = rf'../data/test/test_tables.db'
    con = sqlite3.connect(test_db_path)
    cur = con.cursor()

    if len(con.execute("SELECT * FROM call_data LIMIT 1").fetchone()) < 1:
        database.build_database(con)
        date_gen = dummy_data.create_datedim(con)
        agent_gen = dummy_data.generate_agent_data(con)
        call_gen = dummy_data.generate_call_data(con)

    def test_callend_converted_only_true(self):
        calls = pd.from_sql(con=self.con, sql="SELECT * FROM call_data LIMIT 1000")
        self.assertTrue(
            calls[
                (calls['CONVERTED'] == True) & (calls['CALLENDREASON'] != 'Converted')
                ].shape[0] == 0
        )

    def test_calendar(self):
        cal = dummy_data.create_datedim(self.con)

    def test_pull(self):
        pull = sample_calls.pull_calls(self.con)
        print(pull)
