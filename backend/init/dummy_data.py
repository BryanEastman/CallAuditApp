import pandas as pd
import numpy as np
from itertools import cycle
import datetime as dt

def generate_agent_data():
    agent_ids = list(range(1, 501))
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

    # issue stemming from agent_data df, maybe unordered dict is causing issue?
    agent_data = pd.DataFrame(
        {
            'AGENTID': [*agent_ids],
            'AGENTTITLE': [*random_titles]
        },
    )
    print(agent_data[agent_data.AGENTID.isin(dialers)])
    # agents_df = pd.merge(
    #     agent_data, hierarchy_df,
    #     left_on='AGENTID', right_index=True,
    #     how='left'
    # )




def generate_call_data():
    call_ids = list(range(1, 100_001))
    call_date_ranges = [dt.date(2024, 8, 1) - dt.timedelta(days = x) for x in range(21)]

    return

if __name__ == "__main__":
    generate_agent_data()
