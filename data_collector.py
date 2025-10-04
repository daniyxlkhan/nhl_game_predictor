from datetime import datetime, timedelta
import time
import requests
import json
import csv

def collect_historical_games(start_date, end_date):
    """Collect games from a date range"""
    all_games = []
    
    # Convert string dates to datetime objects
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current_date <= end_date_obj:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"Collecting games for {date_str}...")
        
        # Get games for this date
        day_data = get_games_for_date(date_str)
        
        if day_data and 'gameWeek' in day_data:
            for week in day_data['gameWeek']:
                if 'games' in week:
                    for game in week['games']:
                        # Only collect completed games
                        if game.get('gameState') == 'OFF':
                            all_games.append(game)
        
        # Move to next date
        current_date += timedelta(days=1)
        
        # Be nice to the API (small delay)
        time.sleep(1)
    
    return all_games


def get_games_for_date(date_str):
    """Get all games for a specific date (format: YYYY-MM-DD)"""
    url = f"https://api-web.nhle.com/v1/schedule/{date_str}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open('api_response_games.json', 'w') as f:
                json.dump(response.json(), f, indent=2)
            return response.json()
        else:
            print(f"Error for {date_str}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception for {date_str}: {e}")
        return None


def get_standings_for_date(date_str):
    """Get all standings of each team for a specific date (format: YYYY-MM-DD)"""
    url = f"https://api-web.nhle.com/v1/standings/{date_str}";

    try:
        response = requests.get(url);
        if response.status_code == 200:
            with open('api_response_standings.json', 'w') as f:
                json.dump(response.json(), f, indent=2)
            return response.json()
        else:
            print(f"Error for {data_str}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception for {data_str}: {e}")
        return None

get_games_for_date("2024-03-15")
get_standings_for_date("2024-03-15")

def extract_game_data(games):
    """Extract clean data from games for machine learning"""
    clean_data = []
    
    for game in games:
        try:
            # Extract basic info
            date = game.get('startTimeUTC', '')[:10]  # Just date part
            away_team = game['awayTeam']['commonName']['default']
            home_team = game['homeTeam']['commonName']['default']
            away_score = game['awayTeam']['score']
            home_score = game['homeTeam']['score']
            # Extract more advanced info
            

            # Calculate our prediction targets
            total_goals = away_score + home_score
            winner = 'home' if home_score > away_score else 'away'
            final_score = f"{away_score}-{home_score}"
            
            # Create clean row
            game_row = {
                'date': date,
                'away_team': away_team,
                'home_team': home_team,
                'away_score': away_score,
                'home_score': home_score,
                'winner': winner,
                'final_score': final_score,
                'total_goals': total_goals
            }
            
            clean_data.append(game_row)
            
        except Exception as e:
            print(f"Error processing game: {e}")
            continue
    
    return clean_data

# # 2024 NHL Season
# print("Collecting games from 2024 NHL Season")
# games = collect_historical_games("2024-10-04", "2025-06-17")
# print(f"Found {len(games)} completed games")

# # Extract clean data
# print("\nExtracting clean data...")
# clean_games = extract_game_data(games)
# print(f"Successfully processed {len(clean_games)} games")

# # write all cleaned data onto a csv file
# with open('nhl_data.csv', mode='w') as csvfile:
#     fieldnames = clean_games[0].keys()
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for row in clean_games:
#         writer.writerow(row);

# Stats to keep track of from https://api-web.nhle.com/v1/standings/now

# BASIC
# teamCommonName
# losses
# wins
# ties
# gamesPlayed

# ADV
# goalsFor
# goalsAgainst 
# points
# pointsPctg

# l10Wins
# l10Ties
# l10Losses
# l10GoalsFor
# l10GoalAgainst