import cmd
import sqlite3

from backend.init.database import build_database
from init import *

class Auditor(cmd.Cmd):
    intro = "Welcome to call audit controller, Type help or ? to list commands"
    prompt = "(audits) >> "

    db_path = r'../data/tables.db'
    con = sqlite3.connect(db_path)

    def do_initialize(self, arg):
        "Build database and fill with dummy data"
        database.build_database(self.con)
        database.generate_data(self.con)

    def do_quit(self, arg):
        "Close databse connection and exit"
        self.con.close()
        return True

if __name__== "__main__":
    Auditor().cmdloop()
