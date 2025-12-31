import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_winner_predictor():
    # Read the data 
    df = pd.read_csv("nhl_training_data.csv")
    df.columns = df.columns.str.strip()

    print(f"Loaded {len(df)} games")

    df['wins_diff'] = df['home_wins'] - df['away_wins']
    df['losses_diff'] = df['home_losses'] - df['away_losses']
    df['goals_for_diff'] = df['home_goals_for'] - df['away_goals_for']
    df['goals_against_diff'] = df['home_goals_against'] - df['away_goals_against']
    df['l10_wins_diff'] = df['home_l10_wins'] - df['away_l10_wins']
    df['l10_losses_diff'] = df['home_l10_losses'] - df['away_l10_losses']
    # Goal differential
    df['home_goal_diff'] = df['home_goals_for'] - df['home_goals_against']
    df['away_goal_diff'] = df['away_goals_for'] - df['away_goals_against']
    df['goal_diff_advantage'] = df['home_goal_diff'] - df['away_goal_diff']

    df['home_advantage'] = 1

    features = [
        'wins_diff', 'losses_diff', 'goals_for_diff', 'goals_against_diff',
        'l10_wins_diff', 'l10_losses_diff', 'goal_diff_advantage', 'home_advantage'
    ]
    
    X = df[features]    # Input data for the model
    y = df['winner']    # 'home' or 'away' (Correct answers what we want the model to predict)

    # Split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print(f"Training on {len(X_train)} games, testing on {len(X_test)} games")

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nWinner Prediction Results:")
    print(f"Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    print(f"Baseline (always pick home): {(y_test == 'home').mean():.3f}")
    
    # Detailed results
    print(f"\nDetailed Results:")
    print(classification_report(y_test, y_pred))
    
    # Test on a few examples
    print(f"\nSample Predictions:")
    for i in range(15):
        actual = y_test.iloc[i]
        predicted = y_pred[i]
        confidence = max(model.predict_proba(X_test.iloc[i:i+1])[0]) # returns 2D array with 1 row so im using [0]
        status = "(CORRECT)" if actual == predicted else "(WRONG)"
        print(f"{status} Actual: {actual} | Predicted: {predicted} | Confidence: {confidence:.2f}")
    
    return model, features

if __name__ == "__main__":
    model, features = train_winner_predictor()

    # Save the model
    joblib.dump(model, 'nhl_model.pkl')
    joblib.dump(features, 'model_features.pkl')