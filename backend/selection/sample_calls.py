import sqlite3
import pandas as pd
import datetime as dt

def pull_calls(con: sqlite3.Connection) -> pd.DataFrame:

    query = """
        WITH date_window AS (
            SELECT date, weekday
            FROM datedim
            WHERE weekday IN ('Sunday','Wednesday')
                AND YEARWEEK < strftime('%Y%W', 'now')
            ORDER BY date DESC
            LIMIT 2
        )

        SELECT *
        FROM call_data
        WHERE callstartdate BETWEEN (
            SELECT date
            FROM date_window
            WHERE weekday = 'Wednesday'
        ) AND (
            SELECT date
            FROM date_window
            WHERE weekday = 'Sunday'
        )
    """

    calls = pd.read_sql(
        sql=query,
        con=con
    )

    return calls

def sample_calls(calls_df: pd.DataFrame):
    return
