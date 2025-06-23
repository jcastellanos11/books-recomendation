# Librerías necesarias
import pandas as pd
import numpy as np


# Reemplaza valores nulos, menores a 10 o mayores a 100 con un valor aleatorio entre Q2 y Q3
def replace_null_with_random_iqr(age, q2, q3):
    if pd.isnull(age) or age < 10 or age > 100:
        return int(np.random.uniform(q2, q3))
    return age

# Función de limpieza general para los datasets de libros, valoraciones y usuarios
def cargar_y_limpiar_datos(df_libros, df_valoraciones, df_usuarios):
    # Crear copias para no modificar los originales
    libros = df_libros.copy()
    valoraciones = df_valoraciones.copy()
    usuarios = df_usuarios.copy()

    ##### LIMPIEZA DE LIBROS #####

    # Eliminar columnas innecesarias de URLs de imágenes
    libros.drop(columns=['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], errors='ignore', inplace=True)
    
    # Eliminar filas con valores faltantes en columnas clave
    libros.dropna(subset=['ISBN', 'Book-Title', 'Book-Author'], inplace=True)
    
    # Convertir el año de publicación a formato numérico, forzando errores a NaN
    libros['Year-Of-Publication'] = pd.to_numeric(libros['Year-Of-Publication'], errors='coerce')

    # Calcular la media de los años válidos (ignorando nulos)
    anio_promedio = libros['Year-Of-Publication'].mean(skipna=True)

    # Reemplazar valores nulos por el promedio redondeado
    libros['Year-Of-Publication'].fillna(round(anio_promedio), inplace=True)

    # Convertir a entero
    libros['Year-Of-Publication'] = libros['Year-Of-Publication'].astype(int)
    
    # Eliminar libros duplicados según el ISBN
    libros.drop_duplicates(subset='ISBN', inplace=True)

    ##### LIMPIEZA DE USUARIOS #####
    # Eliminar usuarios duplicados y sin identificador
    usuarios.drop_duplicates(subset='User-ID', inplace=True)
    usuarios.dropna(subset=['User-ID'], inplace=True)

    # Convertir edad a numérico y reemplazar nulos con un valor aleatorio entre Q2 y Q3
    usuarios['Age'] = pd.to_numeric(usuarios['Age'], errors='coerce')
    q2 = usuarios['Age'].dropna().quantile(0.50)
    q3 = usuarios['Age'].dropna().quantile(0.75)
    usuarios['Age'] = usuarios['Age'].apply(lambda age: replace_null_with_random_iqr(age, q2, q3))
    usuarios['Age'] = usuarios['Age'].astype(int)

    # Separar la columna 'Location' en tres nuevas columnas: 'City', 'State' y 'Country'
    location_split = usuarios["Location"].str.split(",", expand=True)
    usuarios["City"] = location_split[0].str.strip()
    usuarios["State"] = location_split[1].str.strip() if location_split.shape[1] > 1 else "unknown"
    usuarios["Country"] = location_split[2].str.strip() if location_split.shape[1] > 2 else "unknown"
    
    # Eliminar la columna original 'Location'
    usuarios.drop(columns=['Location'], errors='ignore', inplace=True)



    ##### LIMPIEZA DE VALORACIONES #####
    # Eliminar valoraciones con campos clave faltantes
    valoraciones.dropna(subset=['User-ID', 'ISBN', 'Book-Rating'], inplace=True)

    # Filtrar valoraciones fuera del rango válido (0 a 10)
    valoraciones = valoraciones[valoraciones['Book-Rating'].between(0, 10)]

    ## Eliminar registros que contengan libros inexistentes en el data set de libros ##

    # Asegurar que ISBN sea string y esté limpio en ambos datasets
    libros['ISBN'] = libros['ISBN'].astype(str).str.strip()
    valoraciones['ISBN'] = valoraciones['ISBN'].astype(str).str.strip()


    # Remover ceros a la izquierda solo si el ISBN es completamente numérico
    valoraciones['ISBN'] = valoraciones['ISBN'].apply(
        lambda x: str(int(x)) if x.isdigit() else x
    )

    # Filtrar valoraciones cuyo ISBN sí existe en libros
    valoraciones_iniciales = valoraciones.shape[0]
    valoraciones = valoraciones[valoraciones['ISBN'].isin(libros['ISBN'])]
    valoraciones_filtradas = valoraciones.shape[0]

    print(f"Se eliminaron {valoraciones_iniciales - valoraciones_filtradas} valoraciones con ISBN no presentes en libros.")


    ## Eliminar registros que contengan usuarios inexistentes en el data set de usuarios ##
    # Asegurar que User-ID tenga el mismo tipo de dato en ambos datasets (por seguridad)
    valoraciones['User-ID'] = valoraciones['User-ID'].astype(str).str.strip()
    usuarios['User-ID'] = usuarios['User-ID'].astype(str).str.strip()

    # Filtrar valoraciones cuyo User-ID exista en el dataset de usuarios
    valoraciones_antes = valoraciones.shape[0]
    valoraciones = valoraciones[valoraciones['User-ID'].isin(usuarios['User-ID'])]
    valoraciones_despues = valoraciones.shape[0]

    print(f"Se eliminaron {valoraciones_antes - valoraciones_despues} valoraciones con usuarios no presentes en el dataset de usuarios.")



    # Eliminar duplicados exactos
    valoraciones.drop_duplicates(inplace=True)

    # Devolver los tres datasets limpios
    return libros, valoraciones, usuarios

