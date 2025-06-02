import os

from AIL_Library import preprocessing
# AIL_Library/main.py
# from AIL_Library import preprocessing, clustering, recommender

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    users_path = os.path.join(BASE_DIR, 'books_data', 'users.csv')
    clean_path = os.path.join(BASE_DIR, 'books_data', 'users.clean.csv')

    books_path = os.path.join(BASE_DIR, 'books_data', 'books.csv')
    clean_books_path = os.path.join(BASE_DIR, 'books_data', 'books.clean.csv')

    print("AIL Library main module is running.")


    preprocessing.clean_users_csv(users_path,clean_path)

    print("Data loaded and cleaned successfully.")


    preprocessing.clean_books_csv(books_path, clean_books_path)
    print("Books data cleaned successfully.")