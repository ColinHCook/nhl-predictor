import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle

def evaluate_model(data_path, model_path):
    # Load the processed data
    df = pd.read_csv(data_path)

    # Prepare data for evaluation
    features = ['Visitor_Goals_Avg', 'Visitor_Allowed_Avg', 'Home_Goals_Avg', 'Home_Allowed_Avg', 'Goal Difference']
    target = (df['Visitor Goals'] > df['Home Goals']).astype(int)

    X = df[features]
    y = target

    # Load the model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Make predictions on the data
    y_pred = model.predict(X)

    # Evaluate the model
    accuracy = accuracy_score(y, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

    confusion = confusion_matrix(y, y_pred)
    print('Confusion Matrix:')
    print(confusion)

    report = classification_report(y, y_pred)
    print('Classification Report:')
    print(report)

if __name__ == "__main__":
    data_path = 'C:/Users/colin/Desktop/nhl-predictor/data/processed/cleaned_nhl_game_data.csv'
    model_path = 'C:/Users/colin/Desktop/nhl-predictor/models/nhl_model.pkl'
    evaluate_model(data_path, model_path)
