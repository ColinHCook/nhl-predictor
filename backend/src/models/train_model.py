from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np
import pickle

def train_model(data_path, model_path):
    # Load the preprocessed data
    data = pd.read_csv(data_path)
    X = data.drop(columns=['Date', 'Visitor Goals', 'Home Goals', 'Goal Difference'])
    y = data['Goal Difference'] > 0  # Example target variable: whether the visitor team won

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Feature scaling
    scaler = StandardScaler()
    
    # Initialize the model
    model = RandomForestClassifier(random_state=42)

    # Define the hyperparameter grid
    param_grid = {
        'model__n_estimators': [100, 200, 300],
        'model__max_depth': [10, 20, 30, None],
        'model__min_samples_split': [2, 5, 10],
        'model__min_samples_leaf': [1, 2, 4]
    }

    # Create a pipeline
    pipeline = Pipeline([
        ('scaler', scaler),
        ('model', model)
    ])

    # Perform grid search with cross-validation
    grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=StratifiedKFold(5), scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Get the best model from grid search
    best_model = grid_search.best_estimator_

    # Evaluate the model
    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    # Save the trained model
    with open(model_path, 'wb') as f:
        pickle.dump(best_model, f)

# Example usage
data_path = 'data/processed/cleaned_nhl_game_data.csv'
model_path = 'models/nhl_model.pkl'
train_model(data_path, model_path)
