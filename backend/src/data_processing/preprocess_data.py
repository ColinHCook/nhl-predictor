import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle

def preprocess_data(input_file, output_file, encoder_path, scaler_path):
    df = pd.read_csv(input_file)
    
    # Create new columns
    df['Goal Difference'] = df['Visitor Goals'] - df['Home Goals']

    # Calculate rolling averages
    df['Visitor_Goals_Avg'] = df.groupby('Visitor Team')['Visitor Goals'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    df['Visitor_Allowed_Avg'] = df.groupby('Visitor Team')['Home Goals'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    df['Home_Goals_Avg'] = df.groupby('Home Team')['Home Goals'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    df['Home_Allowed_Avg'] = df.groupby('Home Team')['Visitor Goals'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

    # One-hot encode categorical features
    encoder = OneHotEncoder()
    encoded_teams = encoder.fit_transform(df[['Visitor Team', 'Home Team']])
    encoded_df = pd.DataFrame(encoded_teams.toarray(), columns=encoder.get_feature_names_out(['Visitor Team', 'Home Team']))
    df = df.join(encoded_df)

    # Drop original categorical columns
    df = df.drop(columns=['Visitor Team', 'Home Team'])

    # Standardize numerical features, excluding rolling averages
    scaler = StandardScaler()
    numerical_features = ['Visitor Goals', 'Home Goals', 'Goal Difference']
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    # Save encoder and scaler
    with open(encoder_path, 'wb') as f:
        pickle.dump(encoder, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

    df.to_csv(output_file, index=False)

# Example usage
input_file = 'data/raw/nhl_game_data.csv'
output_file = 'data/processed/cleaned_nhl_game_data.csv'
encoder_path = 'models/encoder.pkl'
scaler_path = 'models/scaler.pkl'
preprocess_data(input_file, output_file, encoder_path, scaler_path)
