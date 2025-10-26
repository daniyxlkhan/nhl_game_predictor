from datetime import datetime
import json
import requests

def get_team_stats(team_abbrev):
    """Fetch current season stats for a team from NHL API"""
    try:
        url = f"https://api-web.nhle.com/v1/standings/now"
        response = requests.get(url)
        data = response.json()

        team_stats = None
        for team in data['standings']:
            if team['teamAbbrev']['default'] == team_abbrev:
                team_stats = team
                break
        
        if not team_stats:
            print(f"Team {team_abbrev} not found in standings")
            return None
         
        stats = {
            'wins': team_stats['wins'],
            'losses': team_stats['losses'],
            'goals_for': team_stats['goalFor'],
            'goals_against': team_stats['goalAgainst'],
            'l10_wins': team_stats['l10Wins'],
            'l10_losses': team_stats['l10Losses'],
        }
        
        return stats
    except Exception as e:
        print(f"Error fetching games: {e}")
        return []


def get_todays_games():
    """Fetch today's NHL schedule"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"https://api-web.nhle.com/v1/schedule/{today}"
        response = requests.get(url)

        if response.code.status == 200:
            # with open('test.json', 'w') as f:
            #     json.dump(response.json(), f, indent=2)
            data = response.json()
        else:
            print(f"Error for {today}: {response.status_code}")
            return None

        games = []

        if 'gameWeek' in data:
            for day in data['gameWeek']:
                if day['date'] == today:
                    for game in day['games']:
                        games.append({
                            'home_team': game['homeTeam']['abbrev'],
                            'away_team': game['awayTeam']['abbrev'],
                            'home_team_name': game['homeTeam']['placeName']['default'],
                            'away_team_name': game['awayTeam']['placeName']['default'],
                            'game_time': game['startTimeUTC']
                        })
        return games
    except Exception as e:
        print(f"Error fetching games: {e}")
        return []
    

get_team_stats("TOR")