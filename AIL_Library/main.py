import sys
import pandas as pd
from .api_enricher import fetch_google_books_metadata  # Asegúrate de que esta función exista
from .preprocessing import clean_users_csv
from .model import test_model



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python -m AIL_Library.main <user>")
        sys.exit(1)
    user = sys.argv[1]
    # ...carga tus DataFrames aquí...


    df_historial_microclusters = pd.read_csv('perfil_usuarios.csv', sep=',', encoding='latin-1', on_bad_lines='warn', dtype=str)
    df_libros = pd.read_csv('./AIL_Library/books_data/books_enriched_full.csv', sep=';', encoding='latin-1', on_bad_lines='warn')
    libros_populares = pd.read_csv('./AIL_Library/books_data/users.csv', sep=';', encoding='latin-1', on_bad_lines='warn', dtype=str)

    res = test_model(user, df_historial_microclusters, df_libros, libros_populares)