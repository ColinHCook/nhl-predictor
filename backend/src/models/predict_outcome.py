import pandas as pd
import pickle

def predict_outcome(visitor_team, home_team, visitor_goals_avg, visitor_allowed_avg, home_goals_avg, home_allowed_avg, model_path):
    # Load the model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'Visitor_Goals_Avg': [visitor_goals_avg],
        'Visitor_Allowed_Avg': [visitor_allowed_avg],
        'Home_Goals_Avg': [home_goals_avg],
        'Home_Allowed_Avg': [home_allowed_avg],
        'Goal Difference': [visitor_goals_avg - home_goals_avg]
    })

    # Make a prediction
    prediction = model.predict(input_data)
    return 'Visitor Wins' if prediction[0] == 1 else 'Home Wins'

# Example usage
if __name__ == "__main__":
    model_path = 'C:/Users/colin/Desktop/nhl-predictor/models/nhl_model.pkl'
    result = predict_outcome('TeamA', 'TeamB', 2.5, 2.7, 3.1, 2.8, model_path)
    print(result)
