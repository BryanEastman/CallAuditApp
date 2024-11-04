import cmd
import sqlite3
import pandas as pd

from init import database, dummy_data
from selection import sample_calls
from audits import retrieve

class Auditor(cmd.Cmd):
    intro = "Welcome to call audit controller, Type help or ? to list commands"
    prompt = "(audits) >> "

    db_path = r'./data/tables.db'
    app_database = r'../frontend/data/state.db'
    con = sqlite3.connect(db_path)
    app_con = sqlite3.connect(app_database)
    dash_source = r'../dashboard'

    def do_initialize(self, arg):
        "Build database and fill with dummy data"
        database.build_database(self.con)
        dummy_data.generate_agent_data(self.con)
        dummy_data.generate_call_data(self.con)

    def do_sample_calls(self, arg):
        "Fetches a sample of calls and writes to file"
        calls = sample_calls.pull_calls(self.con)
        sample = sample_calls.generate_sample(calls)
        aud_assigned = sample_calls.assign_auditor(sample, ['A1','A2'])
        sample_calls.format_audits(self.app_con, aud_assigned)


    def do_audits(self, arg):
        retrieve.get_audits(self.app_con, self.con)
        # TODO: corrections pipe
        retrieve.write_dashboard(self.con, self.dash_source)

    def do_quit(self, arg):
        "Close databse connection and exit"
        self.con.close()
        self.app_con.close()
        return True

if __name__== "__main__":
    Auditor().cmdloop()
