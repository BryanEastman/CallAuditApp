import pandas as pd
import sqlite3

def get_audits(app_con: sqlite3.Connection, db_con: sqlite3.Connection):
    auds = pd.read_sql(
        "SELECT * FROM audits"
        , con=app_con
    )
    auds.to_sql(
        name='audits'
        , if_exists='replace'
        , index=False
        , con=db_con
    )

def get_corrections(app_con: sqlite3.Connection, db_con: sqlite3.Connection):
    # TODO: add when corrections form complete
    return

def write_dashboard(db_con: sqlite3.Connection, dash_filepath: str):
    dash_view = pd.read_sql(
        "SELECT * FROM dashboard"
        , con=db_con
    )
    with open(dash_filepath, 'w') as f:
        file = f.read()

    dash_view.to_csv(
        path_or_buf=file
        , index=False
    )
    return
