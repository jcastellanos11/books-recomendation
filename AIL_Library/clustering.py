from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class NestedKMeans:
    def __init__(self, n_clusters_outer=3, n_clusters_inner=2):
        self.n_clusters_outer = n_clusters_outer
        self.n_clusters_inner = n_clusters_inner
        self.models = {}

    def fit(self, X):
        self.outer_model = KMeans(n_clusters=self.n_clusters_outer).fit(X)
        self.outer_labels = self.outer_model.labels_
        for i in range(self.n_clusters_outer):
            inner_X = X[self.outer_labels == i]
            self.models[i] = KMeans(n_clusters=self.n_clusters_inner).fit(inner_X)

    def predict_outer(self, X):
        return self.outer_model.predict(X)
