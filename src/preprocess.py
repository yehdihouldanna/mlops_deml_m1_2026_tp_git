import pandas as pd
import os
import yaml
import s3fs

aws_params = yaml.safe_load(open("params.yaml"))["aws"]
def read_data(path):
    storage_options={"key": aws_params['aws_access_key_id'], "secret": aws_params['aws_secret_access_key']}
    df = pd.read_csv(path,storage_options=storage_options)
    return df

def preprocess_data(df):
    # Handle missing values
    df = df.fillna(df.mean())
    
    # Encode categorical variables
    df = pd.get_dummies(df, drop_first=True)
    
    return df

def save_data(df, output_path):
    output_dir = os.path.dirname(output_path)
    storage_options={"key": aws_params['aws_access_key_id'], "secret": aws_params['aws_secret_access_key']}
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_path, index=False, storage_options=storage_options)

if __name__ == "__main__":

    path = "data/raw/data.csv"
    output_path = "data/processed/data_processed.csv"
    
    path = "data/raw/data.csv"
    output_path = "data/processed/data_processed.csv"
    
    df = read_data(path)
    df_processed = preprocess_data(df)
    save_data(df_processed, output_path)
