import cmd
import sqlite3

from init import database, dummy_data
from selection import sample_calls

class Auditor(cmd.Cmd):
    intro = "Welcome to call audit controller, Type help or ? to list commands"
    prompt = "(audits) >> "

    db_path = r'../data/tables.db'
    con = sqlite3.connect(db_path)

    def do_initialize(self, arg):
        "Build database and fill with dummy data"
        database.build_database(self.con)
        dummy_data.generate_agent_data(self.con)
        dummy_data.generate_call_data(self.con)

    def do_sample_calls(self, arg):
        "Fetches a sample of calls and writes to file"
        sample_calls.pull_calls(self.con)

    def do_quit(self, arg):
        "Close databse connection and exit"
        self.con.close()
        return True

if __name__== "__main__":
    Auditor().cmdloop()
