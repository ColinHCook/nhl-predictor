from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the model
with open('models/nhl_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the encoders and scalers used during training
with open('models/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Load the preprocessed data to use as reference for stats
preprocessed_data = pd.read_csv('data/processed/cleaned_nhl_game_data.csv')

def fetch_team_stats(visitor_team, home_team):
    # Fetch the latest stats for the teams from the preprocessed data
    visitor_stats = preprocessed_data[preprocessed_data[f'Visitor Team_{visitor_team}'] == 1].iloc[-1]
    home_stats = preprocessed_data[preprocessed_data[f'Home Team_{home_team}'] == 1].iloc[-1]
    
    return {
        "visitor_goals_avg": visitor_stats['Visitor_Goals_Avg'],
        "visitor_allowed_avg": visitor_stats['Visitor_Allowed_Avg'],
        "home_goals_avg": home_stats['Home_Goals_Avg'],
        "home_allowed_avg": home_stats['Home_Allowed_Avg']
    }

def preprocess_input(visitor_team, home_team):
    # Fetch the stats for the teams
    stats = fetch_team_stats(visitor_team, home_team)

    # Create a dataframe for the input
    input_data = pd.DataFrame([[
        visitor_team, home_team, stats['visitor_goals_avg'], stats['visitor_allowed_avg'], stats['home_goals_avg'], stats['home_allowed_avg']
    ]], columns=['Visitor Team', 'Home Team', 'Visitor_Goals_Avg', 'Visitor_Allowed_Avg', 'Home_Goals_Avg', 'Home_Allowed_Avg'])

    # One-hot encode the teams
    encoded_teams = encoder.transform(input_data[['Visitor Team', 'Home Team']])
    encoded_df = pd.DataFrame(encoded_teams.toarray(), columns=encoder.get_feature_names_out(['Visitor Team', 'Home Team']))

    # Add the other statistics to the encoded dataframe
    stats_df = input_data[['Visitor_Goals_Avg', 'Visitor_Allowed_Avg', 'Home_Goals_Avg', 'Home_Allowed_Avg']]
    processed_input = pd.concat([encoded_df, stats_df], axis=1)
    
    # Ensure all required features are present
    required_features = model.feature_names_in_
    for col in required_features:
        if col not in processed_input.columns:
            processed_input[col] = 0
    
    # Return the processed input
    return processed_input[required_features]

def generate_statistical_explanation(features, prediction):
    explanation = []
    if 'Visitor_Goals_Avg' in features and 'Home_Goals_Avg' in features:
        visitor_goals_avg = features['Visitor_Goals_Avg'][0]
        home_goals_avg = features['Home_Goals_Avg'][0]
      

        if visitor_goals_avg > home_goals_avg:
            explanation.append(f"Visitor team has a higher average goals scored, {visitor_goals_avg}, compared to the home team, {home_goals_avg}.")
        else:
            explanation.append(f"Home team has a higher average goals scored, {home_goals_avg}, compared to the visitor team, {visitor_goals_avg}.")

    if 'Visitor_Allowed_Avg' in features and 'Home_Allowed_Avg' in features:
        visitor_allowed_avg = features['Visitor_Allowed_Avg'][0]
        home_allowed_avg = features['Home_Allowed_Avg'][0]
        if visitor_allowed_avg < home_allowed_avg:
            explanation.append(f"Visitor team has a lower average goals allowed, {visitor_allowed_avg}, compared to the home team, {home_allowed_avg}.")
        else:
            explanation.append(f"Home team has a lower average goals allowed, {home_allowed_avg}, compared to the visitor team, {visitor_allowed_avg}.")

    explanation.append(f"Based on these statistics, the model predicts that the {'visitor' if prediction else 'home'} team will win.")
    return " ".join(explanation)

@app.route('/predict', methods=['POST'])
def predict():
    content = request.json
    visitor_team = content['visitor_team']
    home_team = content['home_team']

    # Preprocess the input data
    features = preprocess_input(visitor_team, home_team)

    # Make prediction
    prediction = model.predict(features)[0]

    # Generate statistical explanation
    explanation = generate_statistical_explanation(features, prediction)

    # Handle the response data
    visitor_stats = {
        "visitor_goals_avg": float(features['Visitor_Goals_Avg'][0]) if 'Visitor_Goals_Avg' in features else None,
        "visitor_allowed_avg": float(features['Visitor_Allowed_Avg'][0]) if 'Visitor_Allowed_Avg' in features else None
    }
    home_stats = {
        "home_goals_avg": float(features['Home_Goals_Avg'][0]) if 'Home_Goals_Avg' in features else None,
        "home_allowed_avg": float(features['Home_Allowed_Avg'][0]) if 'Home_Allowed_Avg' in features else None
    }
    goal_difference = None  # Goal difference is not used in this prediction context

    return jsonify({
        'prediction': "Visitor Wins" if prediction else "Home Wins",
        'visitor_stats': visitor_stats,
        'home_stats': home_stats,
        'goal_difference': goal_difference,
        'explanation': explanation
    })

if __name__ == '__main__':
    app.run(debug=True)
