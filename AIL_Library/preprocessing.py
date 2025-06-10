# AIL_Library/preprocessing.py
import pandas as pd
import numpy as np



def load_json_data(filepath):
    return pd.read_json(filepath)

def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna("unknown")
    return df


def clean_users_csv(input_filepath, output_filepath):
    # Cargar el archivo CSV con la codificación adecuada
    df = pd.read_csv(input_filepath, sep=";", encoding="latin1")  # Cambia "latin1" si es necesario

    # Dividir la columna "Location" en "City", "State", y "Country"
    location_split = df["Location"].str.split(",", expand=True)
    df["City"] = location_split[0].str.strip()
    df["State"] = location_split[1].str.strip() if location_split.shape[1] > 1 else "unknown"
    df["Country"] = location_split[2].str.strip() if location_split.shape[1] > 2 else "unknown"

    # Eliminar la columna original "Location"
    df = df.drop(columns=["Location"])

    # Manejar valores nulos en la columna "Age"
    q1 = df['Age'].dropna().quantile(0.25)  # Primer cuartil (Q1)
    q3 = df['Age'].dropna().quantile(0.75)  # Tercer cuartil (Q3)
    df['Age'] = df['Age'].apply(lambda age: replace_null_with_random_iqr(age, q1, q3))
    df['Age'] = df['Age'].astype(int)  # Convertir a entero
    # Guardar el nuevo archivo CSV limpio
    df.to_csv(output_filepath, index=False, sep=";", encoding="utf-8")

def replace_null_with_random_iqr(age, q1, q3):
    if pd.isnull(age):  # Si el valor es NULL
        return int(np.random.uniform(q1, q3))  # Generar un número aleatorio entre Q1 y Q3
    return age  # Si no es NULL, devolver el valor original

