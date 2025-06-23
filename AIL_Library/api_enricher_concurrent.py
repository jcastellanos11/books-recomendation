import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

CACHE_FILE = "books_metadata_cache.json"

# Cargar cache si existe
try:
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}

def fetch_google_books_metadata(title, isbn=None):
    key = isbn if isbn else title
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

# Ejemplo de procesamiento paralelo
def enrich_books_parallel(books):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for book in books:
            futures.append(executor.submit(fetch_google_books_metadata, book['title'], book.get('isbn')))
        for future in as_completed(futures):
            meta = future.result()
            # Procesar meta...

# Al final, guarda el cache
with open(CACHE_FILE, "w") as f:
    json.dump(cache, f)