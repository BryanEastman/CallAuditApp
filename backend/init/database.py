import sqlite3
import os
import pandas as pd
import datetime as dt
import numpy as np

def build_database(connection: sqlite3.Connection):
    definition_file = './tables.sql'

    try:
       connection.executescript(definition_file)
    except Exception as e:
       print(e)

    return True

def generate_data():
    agent_ids = list(range(1, 501))
    n_agents = len(agent_ids)

    call_ids = list(range(1, 100_001))
    call_date_ranges = [dt.date(2024, 8, 1) - dt.timedelta(days = x) for x in range(21)]

    agent_title_list = {
        'associate dialer': .2
        , 'dialer': .5
        , 'senior dialer': .2
        , 'leader': .09
        , 'senior leader':.01
    }

    random_titles = np.random.choice(
        list(agent_title_list.keys()),
        p=list(agent_title_list.values()),
        size=500
    )

    leader_ids = [i for i, x in enumerate(random_titles) if x == 'leader']
    sr_leader_ids = [i for i, x in enumerate(random_titles) if x == 'senior leader']

    # TODO: assign leaders and sr leaders in hierarchy

    agent_data = pd.DataFrame(
        {
            'AGENTID': [*agent_ids],
            'AGENTTITLE': [*random_titles]
        },
    )

    print(agent_data)
    print(leader_ids)

    # call parameters: 3% of calls are transfers, 7% are attempts
if __name__ == "__main__":
    generate_data()
