# AIL_Library/preprocessing.py
import pandas as pd
import numpy as np


def clean_users_csv(filepath, output_filepath=None):
    df = pd.read_csv(filepath, sep=';' ,encoding='latin1')
    df = df.drop_duplicates(subset=["User-ID"])
    df = df[df["User-ID"].notnull()]
    df = df.fillna("unknown")
    
    # Separar la columna Location en City, State, Country
    location_split = df["Location"].str.split(",", n=2, expand=True)
    df["City"] = location_split[0].str.strip()
    df["State"] = location_split[1].str.strip()
    df["Country"] = location_split[2].str.strip()

    # Eliminar la columna original Location
    df = df.drop(columns=["Location"])
    
    # Opcional: guardar el resultado en un nuevo CSV
    if output_filepath:
        df.to_csv(output_filepath, index=False, sep=';')
    
    return df