import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px


def get_lap_times():
    df = pd.read_csv("../times_2022.csv")
    lap_times = pd.DataFrame(columns=['time'])
    
    for col in df.columns:
        if col == 'time':
            continue
        df_col = df.loc[:,['time',col]]
        df_col = df_col.drop_duplicates(subset=col)
        df_col.loc[:,col] = df_col.loc[:,'time'].diff()
        lap_times = pd.merge(lap_times, df_col, how='outer', on='time')

    lap_times['time'] = pd.to_datetime(lap_times['time'], unit='s')
    return lap_times

def get_time_diff():
    lap_times = get_lap_times()

    lap_times['lap_diff'] = lap_times['Apolloon'] - lap_times['VTK']
    lap_times['total_diff'] = lap_times['lap_diff'].cumsum()
    print(lap_times.head())

    return lap_times

def plot_lap_times():
    lap_times = get_lap_times()
    lap_times['40 lap MA VTK'] = lap_times['VTK'].dropna().rolling(40, min_periods=1).mean() 
    lap_times['40 lap MA Apolloon'] = lap_times['Apolloon'].dropna().rolling(40, min_periods=1).mean() 
    fig = px.line(lap_times, x='time', y=['VTK','Apolloon', '40 lap MA VTK','40 lap MA Apolloon'], labels={"value": "Lap time (s)", "variable": "Team"})
    return fig

def plot_time_diff():
    time_diff = get_time_diff()
    fig = px.line(time_diff, x='time', y='total_diff')
    fig.show()

def generate_layout():
    fig = plot_lap_times()
    html.Div(children=[
            html.H1(children="Ruben's enge analytics"),
            dcc.Graph(
                figure = fig
                )
            ])


if __name__ == '__main__':
    app = Dash(__name__)
    app.layout = generate_layout
    app.run_server(host='0.0.0.0')

