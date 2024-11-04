from itertools import cycle
import sqlite3
import pandas as pd
import datetime as dt

def pull_calls(con: sqlite3.Connection) -> pd.DataFrame:
    query = """
        WITH date_window AS (
            SELECT date, weekday
            FROM datedim
            WHERE weekday IN ('Sunday','Wednesday')
                -- AND YEARWEEK < strftime('%Y%W', 'now')
                AND YEARWEEK = 202436
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

        SELECT s.*
            , a.AGENTLEADERID
        FROM sample_window s
            LEFT JOIN agent a ON a.agentid = s.agentid
        WHERE s.agentid NOT IN ( --prefilter to min sample
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

    return sampled

def assign_auditor(sample_df: pd.DataFrame, auditors: list) -> pd.DataFrame:
    iter_auds = cycle(auditors)
    samp_leaders_grouping = sample_df.groupby(['AGENTLEADERID', 'CALLENDREASON'])
    auditor_sample = samp_leaders_grouping.sample(n=5)
    aud_assignment = list(zip(auditor_sample.CALLID, iter_auds))
    aud_df = pd.DataFrame.from_records(
        aud_assignment,
        columns = ['CALLID','AUDITOR']
    )
    merged = pd.merge(
        sample_df,
        aud_df,
        how='left',
        on='CALLID'
    )

    return merged

def format_audits(aud_con: sqlite3.Connection, assignment_df: pd.DataFrame):
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
    form = assignment_df.reindex(
        columns = assignment_df.columns.tolist() + form_cols
    )
    form.to_sql(
        name='audits',
        con=aud_con,
        if_exists='replace',
        index=False
    )

if __name__=="__main__":
    con = sqlite3.connect(r'/home/beastman/Projects/Portfolio/CallAuditApp/backend/data/test/test_tables.db')
    calls = pull_calls(con)
    s1 = generate_sample(calls)
    a = assign_auditor(s1, ['a1','a2'])
