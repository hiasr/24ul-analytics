from fastapi import FastAPI
import pandas as pd
import random
import math
import time

app = FastAPI()
CACHE_DATA = {
        'time': int(time.time()),
        'teams': [{'name': 'Apolloon', 'laps': 0},
                    {'name': 'VTK', 'laps': 0}]
}

@app.get("/scores-2022.json")
async def get_scores():
    timestamp_now = int(time.time())
    timestamp_cache = CACHE_DATA['time']
    
    CACHE_DATA['teams'][0]['laps'] += (timestamp_now-timestamp_cache)/80*random.uniform(0.8,1.2)
    CACHE_DATA['teams'][1]['laps'] += (timestamp_now-timestamp_cache)/70*random.uniform(0.8,1.2)
    CACHE_DATA['time'] = timestamp_now

    return {'time': timestamp_now,
            'teams': [{'name': team['name'],'laps': math.floor(team['laps'])} for team in CACHE_DATA['teams']] 
        }


@app.get("/get-lap-times")
async def get_lap_times():
    df = pd.read_csv("../times_2022.csv")
    lap_times = dict()
    
    for col in df.columns:
        if col == 'time':
            continue
        df_col = df.loc[:,['time',col]]
        df_col = df_col.drop_duplicates(subset=col)
        df_col.loc[:,'time'] = df_col.loc[:,'time'].diff()
        lap_times[col] = list(df_col['time'])[1:]

    return lap_times
