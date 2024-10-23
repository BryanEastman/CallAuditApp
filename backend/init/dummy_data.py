from posix import replace
import pandas as pd
import numpy as np
from itertools import cycle
import datetime as dt
import sqlite3

def generate_agent_data(con: sqlite3.Connection):
    agent_ids = list(range(0, 500))
    n_agents = len(agent_ids)

    agent_title_dict = {
        'associate dialer': .2
        , 'dialer': .5
        , 'senior dialer': .2
        , 'leader': .09
        , 'senior leader':.01
    }

    random_titles = np.random.choice(
        list(agent_title_dict.keys()),
        p=list(agent_title_dict.values()),
        size=n_agents
    )

    dialers = [i for i, x in enumerate(random_titles) if x in ('associate dialer', 'dialer','senior dialer')]
    leader_ids = [i for i, x in enumerate(random_titles) if x == 'leader']
    sr_leader_ids = [i for i, x in enumerate(random_titles) if x == 'senior leader']

    leader_hierarchy = dict(
        zip(leader_ids, cycle(sr_leader_ids))
    )

    dialer_hierarchy = dict(
        zip(dialers, cycle(leader_ids))
    )

    dialers_leaders_df = pd.DataFrame.from_dict(
        data=dialer_hierarchy,
        columns = ['AGENTLEADERID'],
        orient='index'
    )

    leaders_leaders_df = pd.DataFrame.from_dict(
        data=leader_hierarchy,
        columns = ['AGENTLEADERID'],
        orient='index'
    )

    hierarchy_df = pd.concat([dialers_leaders_df, leaders_leaders_df])

    agent_data = pd.DataFrame.from_dict(
        data = dict(enumerate(random_titles)),
        columns=['AGENTTITLE'], orient='index'
    )

    agent_data.reset_index(inplace=True, names='AGENTID')
    agents_df = pd.merge(
        agent_data, hierarchy_df,
        left_on='AGENTID', right_index=True,
        how='left'
    )
    agents_df.fillna(501, inplace=True)

    agents_df.to_sql(
        if_exists='replace',
        index=False,
        con=con,
        name='agent'
    )

def generate_call_data(con: sqlite3.Connection):
    call_ids = list(range(0, 100_000))
    n = len(call_ids)
    call_date_ranges = [dt.date(2024, 8, 1) - dt.timedelta(days = x) for x in range(21)]
    hours = list(range(9, 23))
    mins = secs = list(range(0,59))

    dialers = list(con.execute("SELECT agentid FROM agent WHERE agenttitle LIKE '%dialer'"))
    dialer_id_list = [x[0] for x in dialers]

    random_dialer = np.random.choice(
        dialer_id_list,
        size=n
    )
    random_date = np.random.choice(
        call_date_ranges,
        size=n
    )
    random_hour = np.random.choice(
        hours,
        size=n
    )
    random_min = np.random.choice(
        mins,
        size=n
    )
    random_sec = np.random.choice(
        secs,
        size=n
    )
    random_conversion = np.random.choice(
        [True, False],
        p=[.03,.97],
        size=n,
        replace=True
    )
    combined = list(
        zip(
            call_ids,
            random_dialer,
            random_date,
            random_hour,
            random_min,
            random_sec,
            random_conversion
        )
    )

    call_datalist = [
        (
            *x[:2],
            dt.datetime.combine(x[2], dt.time(*[t for t in x[-4:-1]])),
            x[-1]
        ) for x in combined
    ]

    calls_df = pd.DataFrame.from_records(
        call_datalist, columns=['CALLID','AGENTID','CALLSTARTDATETIME','CONVERTED']
    )

    calls_df.to_sql(
        name='call_data',
        con=con,
        if_exists='replace',
        index=False
    )
