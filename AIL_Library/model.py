# Librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gdown

import kneed

from kneed import KneeLocator
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder


sns.set(style="whitegrid")# Librerías necesarias
import pandas as pd


from .limpieza import cargar_y_limpiar_datos





def train_model():

    # Cargar datasets originales
    libros_bruto = pd.read_csv('./AIL_Library/books_data/books_enriched_full.csv', sep=',', encoding='latin-1', on_bad_lines='skip', dtype=str)
    valoraciones_bruto = pd.read_csv('./AIL_Library/books_data/ratings.csv', sep=';', encoding='latin-1', on_bad_lines='skip')
    usuarios_bruto = pd.read_csv('./AIL_Library/books_data/users.csv', sep=';', encoding='latin-1', on_bad_lines='skip', dtype=str)

    # Aplicar limpieza
    df_libros, df_valoraciones, df_usuarios = cargar_y_limpiar_datos(libros_bruto, valoraciones_bruto, usuarios_bruto)

    
    # LIBROS: Pasar categorias a variables Numericas

    # Rellenar valores nulos con 'Unknown'
    df_libros['categories'] = df_libros['categories'].fillna('Unknown')

    # Aplicar codificación con LabelEncoder
    le = LabelEncoder()
    df_libros['categories_numericas'] = le.fit_transform(df_libros['categories'])

    # Ver diccionario de equivalencias (opcional)
    categorias_map = dict(zip(le.classes_, le.transform(le.classes_)))
    # print("\nDiccionario de categorías a números:")
    # print(categorias_map)

    # # Mostrar ejemplo de resultado
    # print("\nPrimeras filas con categorías numéricas:")
    # print(df_libros[['categories', 'categories_numericas']].head())


    # AUTORES: Pasar AUTORES a variables Numericas
    # Rellenar valores nulos con 'Unknown'
    df_libros['Book-Author'] = df_libros['Book-Author'].fillna('Unknown')

    # Aplicar codificación con LabelEncoder
    le = LabelEncoder()
    df_libros['author_numerico'] = le.fit_transform(df_libros['Book-Author'])

    # Ver diccionario de equivalencias (opcional)
    # author_map = dict(zip(le.classes_, le.transform(le.classes_)))
    # print("\nDiccionario de autores a números:")
    # print(author_map)

    # # Mostrar ejemplo de resultado
    # print("\nPrimeras filas con autores numéricas:")
    # print(df_libros[['Book-Author', 'author_numerico']].head())


    # Preparación del dataset final para clustering con K-Means

    # Asegurarse de que la columna 'User-ID' tenga el mismo tipo de dato en ambos dataframes
    # Convertimos 'User-ID' in df_valoraciones and df_usuarios to int
    df_usuarios['User-ID'] = pd.to_numeric(df_usuarios['User-ID'], errors='coerce').fillna(-1).astype(int)
    df_valoraciones['User-ID'] = pd.to_numeric(df_valoraciones['User-ID'], errors='coerce').fillna(-1).astype(int)


    # Fusionamos valoraciones con usuarios y libros para tener un dataset enriquecido
    valoraciones_usuarios = pd.merge(df_valoraciones, df_usuarios, on='User-ID', how='inner')
    dataset_final = pd.merge(valoraciones_usuarios, df_libros, on='ISBN', how='inner')


    # Columnas del dataset final:
    # ['User-ID', 'ISBN', 'Book-Rating', 'Age', 'City', 'State', 'Country', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'categories', 'language', 'categories_numericas', 'author_numerico']
    # Selección de características para clustering (Pendiente Definir)
    features = dataset_final[['User-ID', 'Age', 'author_numerico','Book-Rating', 'categories_numericas']]


    #Armamos base
    # Paso 1: rating promedio por usuario
    df_rating_prom = features.groupby("User-ID")["Book-Rating"].mean().reset_index()
    df_rating_prom.columns = ["User-ID", "rating_promedio_usuario"]

    # Paso 2: número de libros leídos
    df_num_libros = features.groupby("User-ID")["Book-Rating"].count().reset_index()
    df_num_libros.columns = ["User-ID", "libros_leídos"]

    # Paso 3 Autor mas frecuente
    df_autor_dominante = features.groupby("User-ID")["author_numerico"].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]).reset_index()
    df_autor_dominante.columns = ["User-ID", "author_dominante"]

    # Paso 4: categoría más frecuente leída
    df_categoria_dominante = features.groupby("User-ID")["categories_numericas"].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]).reset_index()
    df_categoria_dominante.columns = ["User-ID", "categoria_dominante"]

    # Paso 5: edad (tomar la primera si está duplicada por libro)
    df_age = features.groupby("User-ID")["Age"].first().reset_index()

    # Unir todo
    df_perfil_usuarios = df_age.merge(df_rating_prom, on="User-ID") \
                            .merge(df_num_libros, on="User-ID") \
                            .merge(df_autor_dominante, on="User-ID") \
                            .merge(df_categoria_dominante, on="User-ID")

    from sklearn.preprocessing import StandardScaler

    # Variables a usar en el clustering
    X = df_perfil_usuarios[["Age",
                            "rating_promedio_usuario",
                            "libros_leídos",
                            "author_dominante",
                            "categoria_dominante"]]

    # Escalado Z-score
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)


    # Elegimos un número de clusters = 4
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    # Asignar los resultados del clustering al DataFrame df_perfil_usuarios
    df_perfil_usuarios['cluster'] = clusters

    # Promedios por grupo para interpretar
    df_perfil_usuarios.groupby("cluster").mean(numeric_only=True)

    
    # KMEANS ANINADO
    # Crear una nueva columna para guardar microclusters
    df_perfil_usuarios["microcluster"] = -1  # valor temporal

    # Número de microclusters que quieres por macrocluster (puede variar si lo deseas ajustar)
    n_micro = 3

    # Aplicar KMeans dentro de cada macrogrupo
    for macro_id in df_perfil_usuarios["cluster"].unique():
        # Subconjunto del macrogrupo
        subset = df_perfil_usuarios[df_perfil_usuarios["cluster"] == macro_id].copy()
        idx = subset.index

        # Aplicar KMeans al subconjunto
        kmeans_micro = KMeans(n_clusters=n_micro, random_state=42)
        micro_labels = kmeans_micro.fit_predict(subset.drop(columns=["cluster", "microcluster"]))

        # Guardar microcluster como combinación jerárquica
        df_perfil_usuarios.loc[idx, "microcluster"] = [f"{macro_id}_{m}" for m in micro_labels]

    save_model(df_perfil_usuarios, df_valoraciones)


    



def save_model(df_perfil_usuarios, df_valoraciones):
    print("Guardando modelo de microclusters...")
    df_perfil_usuarios.to_csv("perfil_usuarios.csv", index=False)
    df_valoraciones.to_csv("valoraciones.csv", index=False)
    pass


# return:  df_historial_microclusters, libros_populares
def load_model(df_valoraciones, libros_bruto, df_perfil_usuarios):
    import pandas as pd

    # Cargar ratings
    ratings = df_valoraciones
    # Filtrar solo ratings útiles (> 0)
    # ratings = ratings[ratings["Book-Rating"].astype(int) > 0]

    # Asegurar que ISBN sea string
    df_valoraciones['ISBN'] = df_valoraciones['ISBN'].astype(str)

    # Calcular promedio y número de valoraciones por libro
    libros_populares = df_valoraciones.groupby("ISBN").agg(
        promedio_valoracion=("Book-Rating", "mean"),
        cantidad_valoraciones=("Book-Rating", "count")
    ).reset_index()

    # Filtrar libros con un mínimo de valoraciones (ej. al menos 10)
    libros_populares = libros_populares[libros_populares["cantidad_valoraciones"] >= 10]

    # Ordenar por promedio y cantidad de valoraciones
    libros_populares = libros_populares.sort_values(
        by=["promedio_valoracion", "cantidad_valoraciones"],
        ascending=[False, False]
    )

    # Unir con metadata de libros
    libros_populares = libros_populares.merge(
        libros_bruto[["ISBN", "Book-Title", "Book-Author", "categories"]],
        on="ISBN",
        how="left"
    ).drop_duplicates()

    libros_populares.to_csv("libros_populares.csv", index=False)

    ratings['User-ID'] = ratings['User-ID'].astype(str)
    df_perfil_usuarios['User-ID'] = df_perfil_usuarios['User-ID'].astype(str)

    df_historial_microclusters = ratings.merge(
        df_perfil_usuarios[["User-ID", "cluster", "microcluster"]],
        on="User-ID",
        how="inner"  # ← importante para evitar NaN
    )

    return df_historial_microclusters, libros_populares




def recomendar_with_microclusters(user_id, historial_df, libros_bruto, libros_populares, top_n=10):
    user_id = str(user_id)
    historial_df["User-ID"] = historial_df["User-ID"].astype(str)

    # Si el usuario no existe, devolver top libros populares
    if user_id not in historial_df["User-ID"].values:
        return libros_populares.head(top_n).reset_index(drop=True)

    # Obtener macro y microcluster del usuario
    user_row = historial_df[historial_df["User-ID"] == user_id].iloc[0]
    macrocluster = user_row["cluster"]
    microcluster = user_row["microcluster"]

    # Libros que ya leyó
    libros_usuario = set(historial_df[historial_df["User-ID"] == user_id]["ISBN"])

    # Usuarios en el mismo microcluster (excluyendo al usuario actual)
    otros_micro = historial_df[(historial_df["microcluster"] == microcluster) & 
                               (historial_df["User-ID"] != user_id)]

    # Libros recomendables desde el microcluster
    libros_recomendables_micro = otros_micro[~otros_micro["ISBN"].isin(libros_usuario)]
    top_isbn_micro = libros_recomendables_micro["ISBN"].value_counts().head(top_n).index.tolist()

    # Si hay suficientes recomendaciones, usar esas
    if len(top_isbn_micro) >= top_n:
        top_isbn = top_isbn_micro
    else:
        # Si no hay suficientes, buscar en el macrocluster
        otros_macro = historial_df[(historial_df["cluster"] == macrocluster) &
                                   (historial_df["User-ID"] != user_id)]
        libros_recomendables_macro = otros_macro[~otros_macro["ISBN"].isin(libros_usuario)]
        top_isbn_macro = libros_recomendables_macro["ISBN"].value_counts().head(top_n).index.tolist()

        # Combinar sin duplicar
        top_isbn = list(dict.fromkeys(top_isbn_micro + top_isbn_macro))[:top_n]

    # Obtener info de libros
    libros_bruto["ISBN"] = libros_bruto["ISBN"].astype(str)
    top = libros_bruto[libros_bruto["ISBN"].isin(top_isbn)][["ISBN", "Book-Title", "Book-Author", "categories"]].drop_duplicates()

    return top.reset_index(drop=True)


def test_model(user, df_historial_microclusters, df_libros, libros_populares):
    res = recomendar_with_microclusters(user, df_historial_microclusters, df_libros, libros_populares)
    
    return res



# train_model()



# libros_bruto = pd.read_csv('./AIL_Library/books_data/books_enriched_full.csv', sep=',', encoding='latin-1', on_bad_lines='skip', dtype=str)
# df_valoraciones = pd.read_csv('valoraciones.csv', sep=',', encoding='latin-1', on_bad_lines='skip')
# df_perfil_usuarios = pd.read_csv('perfil_usuarios.csv', sep=',', encoding='latin-1', on_bad_lines='skip', dtype=str)

# load_model(df_valoraciones, libros_bruto, df_perfil_usuarios)