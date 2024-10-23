import sqlite3
import os
import datetime as dt

def build_database(con: sqlite3.Connection):
    definition_filepath = r'./init/tables.sql'
    with open(definition_filepath) as f:
        sql = f.read()

    print("building database")
    print(sql)

    try:
       con.executescript(sql)
       con.commit()
       print("committed to database")
    except Exception as e:
       print(e)

    return True
