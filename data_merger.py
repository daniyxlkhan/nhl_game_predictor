import csv
import pandas as pd  

def merge_games_with_standings():
    games_df = pd.read_csv("nhl_games_data_small.csv")
    standings_df = pd.read_csv("nhl_standings_data_small.csv")

    games_df.columns = games_df.columns.str.strip()
    standings_df.columns = standings_df.columns.str.strip()

    merged_rows = []

    for _, game in games_df.iterrows():
        # Find away team's stats for this game date
        away_stats = standings_df[
            (standings_df['date'] == game['date']) & 
            (standings_df['teamName'] == game['away_team'])
        ]
        
        # Find home team's stats for this game date  
        home_stats = standings_df[
            (standings_df['date'] == game['date']) & 
            (standings_df['teamName'] == game['home_team'])
        ]
        
        if not away_stats.empty and not home_stats.empty:
            # Combine game + both teams' stats into one row
            merged_row = {
                'date': game['date'],
                'away_team': game['away_team'],
                'home_team': game['home_team'],
                'away_wins': away_stats.iloc[0]['wins'], # get wins from the first row of dataframe 
                'away_losses': away_stats.iloc[0]['losses'],
                'away_goals_for': away_stats.iloc[0]['goalFor'],
                'away_goals_against': away_stats.iloc[0]['goalAgainst'],
                'away_l10_wins': away_stats.iloc[0]['l10Wins'],         
                'away_l10_losses': away_stats.iloc[0]['l10Losses'],      
                'away_l10_ties': away_stats.iloc[0]['l10Ties'],          
                'home_wins': home_stats.iloc[0]['wins'], 
                'home_losses': home_stats.iloc[0]['losses'],
                'home_goals_for': home_stats.iloc[0]['goalFor'],
                'home_goals_against': home_stats.iloc[0]['goalAgainst'],
                'home_l10_wins': home_stats.iloc[0]['l10Wins'],         
                'home_l10_losses': home_stats.iloc[0]['l10Losses'],      
                'home_l10_ties': home_stats.iloc[0]['l10Ties'], 
                'winner': game['winner'],
                'final_score': game['final_score'],
                'total_goals': game['total_goals']
            }
            merged_rows.append(merged_row)
    
    merged_df = pd.DataFrame(merged_rows)
    merged_df.to_csv("nhl_training_data.csv", index=False)

if __name__ == "__main__":
    merge_games_with_standings()