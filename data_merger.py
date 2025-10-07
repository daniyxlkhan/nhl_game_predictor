import csv
import pandas as pd  

def merge_games_with_standings():
    games_df = pd.read_csv("nhl_games_data_small.csv")
    standings_df = pd.read_csv("nhl_standings_data_small.csv")

    merged_rows = []

if __name__ == "__main__":
    merge_games_with_standings()