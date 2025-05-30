import requests

def fetch_google_books_metadata(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json().get("items", [])
        if items:
            volume_info = items[0].get("volumeInfo", {})
            return {
                "categories": volume_info.get("categories", []),
                "language": volume_info.get("language", "")
            }
    return {}