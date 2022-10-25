import requests
import pandas as pd
from time import sleep, time

YEAR = 2022

class Scraper:
    def __init__(self):
        self.last_updated = int(time())

        self.df = pd.DataFrame()
        self.update_df()

    def start(self):
        print("Scraper started")
        while True:
            sleep(1)
            self.update_df()

    def save_df(self):
        timestamp = int(time())
        self.df.to_csv(f"times_{YEAR}.csv")
        self.df.to_csv(f"backup/times_{YEAR}_{timestamp}.csv")
        print(f"Saved df to csv on {timestamp}")

    def fetch_data(self):
        # response = requests.get(f"http://data.24urenloop.be/scores-{YEAR}.json")
        try:
            response = requests.get(f"http://127.0.0.1:8000/scores-{YEAR}.json")
        except:
            print("Failed to connect")
            return {'time': int(time())}

        if response.text:
            return response.json()
        else:
            return {'time': int(time())}

    def update_df(self):
        data = self.fetch_data()

        if data is None or'teams' not in data:
            return

        if data['time'] >= self.last_updated:
            self.last_updated = data['time']
            new_row = {team['name']:team['laps'] for team in data['teams']}
            new_row["time"] = data['time']
            new_df = pd.DataFrame.from_records([new_row], index='time')
            self.df = pd.concat([self.df, new_df])

        if data['time'] % 60 == 0:
            self.save_df()

if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()


