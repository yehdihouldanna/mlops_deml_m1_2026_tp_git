import pandas as pd
from ruamel import yaml
from sklearn.linear_model import LinearRegression
import joblib
import mlflow

from ruamel.yaml import YAML

yaml_parser = YAML(typ='safe', pure=True)
with open("params.yaml", "r") as f:
    params = yaml_parser.load(f)["mlflow"]

# params = yaml.safe_load(open("params.yaml"))["mlflow"]
MLFLOW_TRACKING_URI  = params["MLFLOW_TRACKING_URI"]
EXPERIMENT_NAME = params["EXPERIMENT_NAME"]

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
    
    yaml_parser = YAML(typ='safe', pure=True)
    with open("params.yaml", "r") as f:
        params = yaml_parser.load(f)["evaluate"]

    model_path = params["model_path"]
    data_path = params["data_path"]
    
    # Load the trained model
    model = mlflow.sklearn.load_model(model_path)
    # model = joblib.load(model_path)
    
    # Evaluate the model
    evaluate_model(model, data_path)