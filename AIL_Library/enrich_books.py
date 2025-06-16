import pandas as pd
import os
# from .api_enricher import fetch_google_books_metadata
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_FILE = "./AIL_Library/books_data/parte1.csv"
OUTPUT_FILE = "./AIL_Library/books_data/books_enriched.csv"
CACHE_FILE = "books_metadata_cache.json"

# Cargar cache si existe
try:
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}

def fetch_google_books_metadata(title, isbn=None):
    key = str(isbn) if isbn else str(title)
    if key in cache:
        return cache[key]
    # Construir la URL de búsqueda
    query = f"isbn:{isbn}" if isbn else f"intitle:{title}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        # Extraer info relevante
        if "items" in data:
            info = data["items"][0]["volumeInfo"]
            meta = {
                "categories": info.get("categories", []),
                "language": info.get("language", None)
            }
        else:
            meta = {"categories": [], "language": None}
    else:
        meta = {"categories": [], "language": None}
    cache[key] = meta
    # Guardar cache periódicamente
    if len(cache) % 100 == 0:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)
    return meta

def enrich_and_append():
    # Leer encabezado
    with open(INPUT_FILE, encoding="latin1") as fin:
        header = fin.readline().strip()
        columns = [col.strip().replace('"', '') for col in header.split(";")]
    
    # Revisar si ya existe el archivo de salida y cuántos libros tiene
    processed_isbns = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, encoding="utf-8") as fout:
            next(fout)  # saltar encabezado
            for line in fout:
                isbn = line.split(",")[0]
                processed_isbns.add(isbn)
    else:
        # Escribir encabezado en el archivo de salida
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
            fout.write(header + ",categories,language\n")
    
    # Procesar libros uno por uno
    for chunk in pd.read_csv(INPUT_FILE, sep=";", encoding="latin1", on_bad_lines='skip', chunksize=1):
        chunk.columns = [col.strip().replace('"', '') for col in chunk.columns]
        row = chunk.iloc[0]
        isbn = str(row['ISBN'])
        if isbn in processed_isbns:
            continue  # Ya procesado

        print(f"Enriqueciendo: {row['Book-Title']} (ISBN: {isbn})")
        meta = fetch_google_books_metadata(row['Book-Title'])
        categories = meta.get('categories', None)
        language = meta.get('language', None)

        # Preparar línea para escribir
        values = [str(row[col]) for col in columns]
        # Si categories es lista, conviértela a string
        if isinstance(categories, list):
            categories = str(categories)
        line = ",".join(values) + f",{categories},{language}\n"

        with open(OUTPUT_FILE, "a", encoding="utf-8") as fout:
            fout.write(line)

    # Al final, guarda el cache
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

if __name__ == "__main__":
    enrich_and_append()