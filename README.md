# NHL Game Predictor

<div align="center">
  <img src="nhl_logo.png" alt="NHL Logo" width="200"/>
</div>

Predicts NHL game winners using machine learning based on team statistics.

## What it does

- Collects historical NHL game data and team standings
- Trains a Random Forest model on past games
- Predicts winners for today's games with probability scores

## Setup

```bash
python -m venv nhl_game_predictor_env
source nhl_game_predictor_env/bin/activate
```

## Usage

### 1. Collect data (takes ~10 minutes)
```bash
python data_collector.py
```
This pulls games and standings from the NHL API for 2023-24 and 2024-25 seasons.
- **~1,300+ games** from October 2023 to January 2025
- **~30,000+ standings records** (32 teams tracked daily)

### 2. Prepare training data
```bash
python data_merger.py
```
Merges games with team standings to create the training dataset.

### 3. Train the model
```bash
python model_trainer.py
```
Trains the predictor and shows accuracy metrics. Saves the model to `nhl_model.pkl`.

### 4. Predict today's games
```bash
python live_predictor.py
```
Fetches today's schedule and predicts winners with probabilities.

## Files

- `data_collector.py` - Gets games and standings from NHL API
- `data_merger.py` - Combines games with team stats
- `model_trainer.py` - Trains the prediction model
- `live_predictor.py` - Makes predictions for live games
- `nhl_model.pkl` - Trained model (generated)
- `nhl_training_data.csv` - Training dataset (generated)

## How it works

The model is trained on over 1,300 NHL games with team statistics from before each game.

It uses these features to predict winners:
- Win/loss differential between teams
- Goals for/against differential
- Recent form (last 10 games)
- Goal differential advantage
- Home ice advantage

Typical accuracy is around 55-60% which is pretty good for sports prediction.
