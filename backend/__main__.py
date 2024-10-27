import cmd
import sqlite3
import pandas as pd

from init import database, dummy_data
from selection import sample_calls

class Auditor(cmd.Cmd):
    intro = "Welcome to call audit controller, Type help or ? to list commands"
    prompt = "(audits) >> "

    db_path = r'./data/tables.db'
    app_database = r'../frontend/data/state.db'
    con = sqlite3.connect(db_path)

    def do_initialize(self, arg):
        "Build database and fill with dummy data"
        database.build_database(self.con)
        dummy_data.generate_agent_data(self.con)
        dummy_data.generate_call_data(self.con)

    def do_sample_calls(self, arg):
        "Fetches a sample of calls and writes to file"
        calls = sample_calls.pull_calls(self.con)
        sample = sample_calls.generate_sample(calls)
        # TODO abstract this into a function to clean up
        form_cols = [
            "QA_INTRODUCTION",
            "QA_OBJECTION",
            "QA_SCRIPT",
            "QA_VERIFICATION",
            "QA_TONE",
            "QA_DEADAIR",
            "QA_NOTES",
            "TL_INTRODUCTION",
            "TL_OBJECTION",
            "TL_SCRIPT",
            "TL_VERIFICATION",
            "TL_TONE",
            "TL_DEADAIR",
            "TL_NOTES",
            ]
        form = sample.reindex(
            columns = sample.columns.tolist() + form_cols
        )
        form.to_sql(
            name='audits',
            con=sqlite3.connect(self.app_database),
            if_exists='replace',
            index=False
        )

    def do_quit(self, arg):
        "Close databse connection and exit"
        self.con.close()
        return True

if __name__== "__main__":
    Auditor().cmdloop()
