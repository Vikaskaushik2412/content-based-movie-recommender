import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv("tmdb_movies.csv")

# Keep required columns
movies = movies[['movie_id', 'title', 'cast', 'crew']].fillna('')

# Use title for searching
movies['search_title'] = movies['title'].astype(str)

# Fill missing values
movies = movies.fillna("")

# Create tags
movies['tags'] = (
    movies['cast'].astype(str) + ' ' +
    movies['crew'].astype(str)
)

# Convert text into vectors
vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(movies['tags'])

# Similarity matrix
similarity = cosine_similarity(vectors)


def recommend(movie_name):

    # Clean input and titles before matching
    movie_name = movie_name.strip().lower()

    matches = movies[
        movies['search_title'].astype(str).str.strip().str.lower() == movie_name
    ]

    # Fallback: partial match search
    if matches.empty:
        matches = movies[
            movies['search_title'].astype(str).str.lower().str.contains(movie_name, na=False)
        ]

    if matches.empty:
        print("Movie not found.")
        return

    movie_index = matches.index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    print("\nRecommended Movies:\n")

    for movie in movie_list:
        movie_data = movies.iloc[movie[0]]

        print(movie_data.title)


if __name__ == "__main__":

    print("🎬 Movie Recommendation System")
    print("-" * 35)

    movie_name = input(
        "Enter movie name: "
    )

    recommend(movie_name)