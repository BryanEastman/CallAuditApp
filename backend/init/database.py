import sqlite3
import os
import datetime as dt

def build_database(connection: sqlite3.Connection):
    definition_file = './tables.sql'

    try:
       connection.executescript(definition_file)
    except Exception as e:
       print(e)

    return True
