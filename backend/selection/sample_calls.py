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
        , sample_window AS (
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
                AND callendreason IN ('Converted','ClientHangup')
        )

        SELECT *
        FROM sample_window
        WHERE agentid NOT IN ( --prefilter to min sample
            SELECT DISTINCT agentid
            FROM sample_window
            GROUP BY callendreason, agentid
            HAVING COUNT(*) < 2
        )

    """

    calls = pd.read_sql(
        sql=query,
        con=con
    )

    return calls

def generate_sample(calls_df: pd.DataFrame) -> pd.DataFrame:
    param_grouping = calls_df.groupby(['CALLENDREASON','AGENTID'])
    sampled = param_grouping.sample(n=2)

    return sampled.sort_values('AGENTID')

if __name__=="__main__":
    con = sqlite3.connect(r'/home/beastman/Projects/Portfolio/CallAuditApp/backend/data/test/test_tables.db')
    calls = pull_calls(con)
