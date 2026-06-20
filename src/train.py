
import mlflow
# Train a simple model (e.g., Logistic Regression)
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
import os
import pandas as pd

MLFLOW_TRACKING_URI = "http://15.237.119.156:5000"
MLFLOW_TRACKING_URI = "http://localhost:5050"
EXPERIMENT_NAME = "Student_Experiment"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

def train_model(data_path, model_output_path):

    # Load the preprocessed data
    df = pd.read_csv(data_path)
    
    # Split the data into features and target variable
    X = df.drop("GPA", axis=1)
    y = df["GPA"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    with mlflow.start_run():

        model = LinearRegression()
        model.fit(X_train, y_train)

        score = model.score(X_test, y_test)
        print("Test R^2 Score:", score)
        rmse = ((y_test - model.predict(X_test)) ** 2).mean() ** 0.5
        print("Test RMSE:", rmse)
        mlflow.log_metric("R2_Score", score)
        mlflow.log_metric("RMSE", rmse)
        mlflow.sklearn.log_model(model, "linear_regression_model")
        
        # Path to save the model
        os.makedirs(os.path.dirname(model_output_path), exist_ok=True)

        # Save the model on the mlflow server registry
        mlflow.sklearn.save_model(model, model_output_path)

if __name__ == "__main__":
    data_path = "data/processed/data_processed.csv"
    model_output_path = "models/linear_regression_model"
    
    train_model(data_path, model_output_path)