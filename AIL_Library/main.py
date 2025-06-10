import pandas as pd
from .api_enricher import fetch_google_books_metadata  # Asegúrate de que esta función exista
from .preprocessing import clean_users_csv


def get_metadata(row):
    meta = fetch_google_books_metadata(row['Book-Title'])
    # Asegúrate de que meta sea un dict con las claves esperadas
    categories = meta.get('categories', None)
    language = meta.get('language', None)
    return pd.Series([categories, language])

if __name__ == '__main__':
    input_file = "./AIL_Library/books_data/users.csv"
    output_file = "./AIL_Library/books_data/clean_users.csv"
    clean_users_csv(input_file, output_file)
    print("Archivo CSV limpio creado:", output_file)

    books_file = "./AIL_Library/books_data/books.csv"



    books_file = "./AIL_Library/books_data/books.csv"
    books = pd.read_csv(books_file, sep=";", encoding="latin1", on_bad_lines='skip')
    books[['categories', 'language']] = books.apply(get_metadata, axis=1)
    
    books = books.drop(columns=['Image-URL-S', 'Image-URL-M', 'Image-URL-L'])
    books.to_csv('books_enriched.csv', index=False)
    