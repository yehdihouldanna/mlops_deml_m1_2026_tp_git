import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import mlflow

MLFLOW_TRACKING_URI = "http://15.237.119.156:5000"
MLFLOW_TRACKING_URI = "http://localhost:5050"
EXPERIMENT_NAME = "Student_Experiment"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

def evaluate_model(model, data_path):
    # Load the preprocessed data
    df = pd.read_csv(data_path)
    
    # Split the data into features and target variable
    X = df.drop("GPA", axis=1)
    y = df["GPA"]

    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "linear_regression_model")
    
        # Evaluate the model
        score = model.score(X, y)
        print("R^2 Score:", score)
        rmse = ((y - model.predict(X)) ** 2).mean() ** 0.5
        print("RMSE:", rmse)
        mlflow.log_metric("R2_Score_eval", score)
        mlflow.log_metric("RMSE_eval", rmse)

    return score, rmse

if __name__ == "__main__":
    
    model_path = "models/linear_regression_model"
    data_path = "data/processed/data_processed.csv"
    
    # Load the trained model
    model = mlflow.sklearn.load_model(model_path)
    # model = joblib.load(model_path)
    
    # Evaluate the model
    evaluate_model(model, data_path)