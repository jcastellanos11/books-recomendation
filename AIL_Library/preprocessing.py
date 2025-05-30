# AIL_Library/preprocessing.py
import pandas as pd
import numpy as np

def load_json_data(filepath):
    return pd.read_json(filepath)

def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna("unknown")
    return df
