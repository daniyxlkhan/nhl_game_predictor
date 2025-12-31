from datetime import datetime
import json
import requests
import joblib
import pandas as pd

# load trained model and features
model = joblib.load('nhl_model.pkl')
features = joblib.load('model_features.pkl')

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

        if response.status_code == 200:
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

def prepare_game_features(home_stats, away_stats):
    """Prepare features for prediction based on team stats"""
    # Calculate the same engineered features used in training
    wins_diff = home_stats['wins'] - away_stats['wins']
    losses_diff = home_stats['losses'] - away_stats['losses']
    goals_for_diff = home_stats['goals_for'] - away_stats['goals_for']
    goals_against_diff = home_stats['goals_against'] - away_stats['goals_against']
    l10_wins_diff = home_stats['l10_wins'] - away_stats['l10_wins']
    l10_losses_diff = home_stats['l10_losses'] - away_stats['l10_losses']
    
    # Goal differential
    home_goal_diff = home_stats['goals_for'] - home_stats['goals_against']
    away_goal_diff = away_stats['goals_for'] - away_stats['goals_against']
    goal_diff_advantage = home_goal_diff - away_goal_diff
    
    home_advantage = 1
    
    feature_dict = {
        'wins_diff': wins_diff,
        'losses_diff': losses_diff,
        'goals_for_diff': goals_for_diff,
        'goals_against_diff': goals_against_diff,
        'l10_wins_diff': l10_wins_diff,
        'l10_losses_diff': l10_losses_diff,
        'goal_diff_advantage': goal_diff_advantage,
        'home_advantage': home_advantage
    }
    
    # Create DataFrame with proper column order matching trained model
    df = pd.DataFrame([feature_dict])
    df = df[features]  # Ensure columns match the trained model
    return df


def predict_game(home_team_abbrev, away_team_abbrev):
    """Predict the outcome of a game"""
    home_stats = get_team_stats(home_team_abbrev)
    away_stats = get_team_stats(away_team_abbrev)
    
    if not home_stats or not away_stats:
        return None
    
    game_features = prepare_game_features(home_stats, away_stats)
    prediction = model.predict(game_features)[0]
    probability = model.predict_proba(game_features)[0]
    
    return {
        'prediction': 'home' if prediction == 'home' else 'away',
        'home_win_probability': probability[1] if len(probability) > 1 else probability[0],
        'away_win_probability': probability[0] if len(probability) > 1 else 1 - probability[0]
    }


def main():
    """Main function to predict today's games"""
    print("Fetching today's NHL games...\n")
    games = get_todays_games()
    
    if not games:
        print("No games scheduled for today.")
        return
    
    print(f"Found {len(games)} game(s) today:\n")
    
    for game in games:
        print(f"\n{'='*60}")
        print(f"{game['away_team_name']} @ {game['home_team_name']}")
        print(f"Game Time: {game['game_time']}")
        print(f"{'='*60}")
        
        prediction = predict_game(game['home_team'], game['away_team'])
        
        if prediction:
            winner = game['home_team_name'] if prediction['prediction'] == 'home' else game['away_team_name']
            print(f"\nPredicted Winner: {winner}")
            print(f"Home Win Probability: {prediction['home_win_probability']:.1%}")
            print(f"Away Win Probability: {prediction['away_win_probability']:.1%}")
        else:
            print("\nCould not make prediction - team stats unavailable")


if __name__ == "__main__":
    main()