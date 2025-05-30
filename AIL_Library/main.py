
# AIL_Library/main.py
from AIL_Library import preprocessing, clustering, recommender

def run_pipeline():
    data = preprocessing.load_json_data("../data/sample_users_books.json")
    clean_df = preprocessing.clean_data(data)
    # Simulación de extracción de features numéricos para clustering
    # Aquí se deben transformar descripciones y géneros
    # Placeholder para ejemplo:
    from sklearn.feature_extraction.text import TfidfVectorizer
    vec = TfidfVectorizer()
    X = vec.fit_transform(clean_df["books"].apply(lambda b: b[0]["description"] if b else ""))

    model = clustering.NestedKMeans()
    model.fit(X.toarray())
    print("Modelo entrenado")

if __name__ == '__main__':
    run_pipeline()