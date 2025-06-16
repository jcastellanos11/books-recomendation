import pandas as pd
from .api_enricher import fetch_google_books_metadata  # Asegúrate de que esta función exista
from .preprocessing import clean_users_csv



if __name__ == '__main__':
    input_file = "./AIL_Library/books_data/users.csv"
    output_file = "./AIL_Library/books_data/clean_users.csv"

    file_valoraciones = "./AIL_Library/books_data/ratings.csv"

    clean_users_csv(input_file, output_file)
    print("Archivo CSV limpio creado:", output_file)


    # El archivo: books_enriched_full.csv debe ser generado
    # previamente por el script de enriquecimiento de libros.
    books_file = "./AIL_Library/books_data/books_enriched_full.csv"
    books = pd.read_csv(books_file, sep=";", encoding="latin1", on_bad_lines='skip')
    
    books = books.drop(columns=['Image-URL-S', 'Image-URL-M', 'Image-URL-L'])
    books.to_csv('books_enriched.csv', index=False)
    

    # 🧩 Preparación del dataset final para clustering con K-Means

    # Asegurarse de que la columna 'User-ID' tenga el mismo tipo de dato en ambos dataframes
    # df_usuarios ya tiene 'User-ID' como string debido a la lectura inicial.
    # df_valoraciones tiene 'User-ID' como int debido al dtype especificado en load_and_clean_data.
    # Convertimos 'User-ID' en df_usuarios a int para que coincida con df_valoraciones.

    df_usuarios = pd.read_csv(output_file, sep=";", encoding="latin1", on_bad_lines='skip')
    df_usuarios['User-ID'] = pd.to_numeric(df_usuarios['User-ID'], errors='coerce').fillna(-1).astype(int) # Usamos fillna(-1) para manejar posibles errores de conversión si los hubiera.

    df_valoraciones = pd.read_csv(file_valoraciones, sep=";", encoding="latin1", on_bad_lines='skip')
    

    # Fusionamos valoraciones con usuarios y libros para tener un dataset enriquecido
    valoraciones_usuarios = pd.merge(df_valoraciones, df_usuarios, on='User-ID', how='inner')
    valoraciones_usuarios['ISBN'] = valoraciones_usuarios['ISBN'].astype(str)
    books['ISBN'] = books['ISBN'].astype(str)

    dataset_final = pd.merge(valoraciones_usuarios, books, on='ISBN', how='inner')
    

    # Verificación de columnas tras el merge
    print("\nColumnas del dataset final:")
    print(dataset_final.columns.tolist())


    # Vista previa del dataset final
    print("\nDataset final para clustering:")
    print(dataset_final.head()) # Imprime el dataset final completo, no solo las features aún.