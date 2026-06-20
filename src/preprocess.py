import pandas as pd
import os
import yaml

def read_data(path):
    df = pd.read_csv(path)
    return df

def preprocess_data(df):
    # Handle missing values
    df = df.fillna(df.mean())
    
    # Encode categorical variables
    df = pd.get_dummies(df, drop_first=True)
    
    return df

def save_data(df, output_path):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":

    params = yaml.safe_load(open("params.yaml"))["preprocess"]
    path = params["input"]
    output_path = params["output"]

    df = read_data(path)
    df_processed = preprocess_data(df)
    save_data(df_processed, output_path)