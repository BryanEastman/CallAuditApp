import sqlite3
import pandas as pd
import datetime as dt

def pull_calls(con: sqlite3.Connection):

    query = """
        SELECT *
        FROM call_data
        WHERE callstartdatetime BETWEEN
    """

    calls = pd.read_sql(
        sql=query,
        con=con,
        params=[]
    )
