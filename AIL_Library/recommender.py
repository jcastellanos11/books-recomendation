import random

class RecommendationEngine:
    def __init__(self, cluster_data, user_history):
        self.cluster_data = cluster_data
        self.user_history = user_history

    def get_recommendations(self, user_id, cluster_id, num=5):
        books_seen = set(self.user_history.get(user_id, []))
        users_in_cluster = [u for u, cid in self.cluster_data.items() if cid == cluster_id and u != user_id]
        book_pool = set()
        for uid in users_in_cluster:
            book_pool.update(self.user_history.get(uid, []))
        recommendations = list(book_pool - books_seen)
        return random.sample(recommendations, min(num, len(recommendations)))
