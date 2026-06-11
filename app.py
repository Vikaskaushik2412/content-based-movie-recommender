import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import os

# Page config
st.set_page_config(
    page_title="Kaushik's Movie Recommendation Engine",
    page_icon="🎬",
    layout="wide"
)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e1b4b,#312e81);
    background-size: 400% 400%;
    animation: gradientFlow 12s ease infinite;
}

@keyframes gradientFlow {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

h1 {
    text-align:center;
    font-size:2.8rem !important;
    font-weight:900;
    background:linear-gradient(90deg,#22d3ee,#a855f7,#ec4899);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

h3,p,label {
    color:white !important;
}

div[data-testid="stMetric"] {
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(15px);
    border:1px solid rgba(255,255,255,0.15);
    border-radius:24px;
    padding:18px;
    box-shadow:0 10px 30px rgba(0,0,0,.25);
}

.stAlert {
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(15px);
    color:white;
    border-radius:20px;
}

div.stButton > button {
    background:linear-gradient(90deg,#06b6d4,#8b5cf6,#ec4899);
    color:white;
    border:none;
    border-radius:16px;
    font-size:18px;
    font-weight:800;
    padding:14px;
    width:100%;
    transition:all .3s ease;
}

div.stButton > button:hover {
    transform:scale(1.05);
}

div[data-baseweb="select"] {
    background:rgba(255,255,255,.08);
    backdrop-filter:blur(12px);
    border-radius:18px;
}

.movie-card {
    background:rgba(255,255,255,.08);
    backdrop-filter:blur(16px);
    padding:20px;
    margin:18px 0;
    border-radius:24px;
    border:1px solid rgba(255,255,255,.15);
    box-shadow:0 10px 30px rgba(0,0,0,.25);
    transition:all .35s ease;
    animation:fadeUp .6s ease;
}

.movie-card:hover {
    transform:translateY(-10px) scale(1.02);
    border-color:#22d3ee;
}

@keyframes fadeUp {
    from {opacity:0; transform:translateY(25px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)
# Load dataset
@st.cache_data
def load_data():
    movies = pd.read_csv("tmdb_movies.csv")

    movies = movies[['movie_id', 'title', 'cast', 'crew']].fillna('')

    movies['tags'] = (
        movies['cast'].astype(str) + ' ' +
        movies['crew'].astype(str)
    )

    return movies


movies = load_data()

try:
    API_KEY = st.secrets["TMDB_API_KEY"]
except:
    API_KEY = "d3d50b4bdcd3cad65fafce221650ba18"

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = requests.get(url, timeout=3).json()

        poster = None
        if data.get("poster_path"):
            poster = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"

        return {
            "poster": poster,
            "rating": data.get("vote_average", "N/A"),
            "overview": data.get("overview", "No description available.")
        }
    except:
        return {
            "poster": None,
            "rating": "N/A",
            "overview": "No description available."
        }

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if 'show_details' not in st.session_state:
    st.session_state.show_details = {}

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

# Build vectors and similarity matrix
@st.cache_resource
def build_similarity(data):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(data['tags'])
    return cosine_similarity(vectors)

similarity = build_similarity(movies)


def recommend(movie_name):

    matches = movies[
        movies['title'].astype(str).str.strip().str.lower() ==
        movie_name.strip().lower()
    ]

    if matches.empty:
        return []

    movie_index = matches.index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for movie in movie_list:
        recommendations.append({
            "title": movies.iloc[movie[0]].title,
            "id": movies.iloc[movie[0]].movie_id,
            "score": round(float(movie[1]) * 100, 1)
        })
    return recommendations


# UI
st.title("🎬 Kaushik's Movie Recommender")
st.caption("Built by Vikas Kaushik")

st.markdown("""
### About this Project

This recommendation system suggests similar movies based on cast and crew information.
The similarity scores are calculated using TF-IDF Vectorization and Cosine Similarity.

**Tech Stack:** Python, Pandas, Scikit-Learn, Streamlit
""")

col1, col2 = st.columns(2)

with col1:
    st.metric("🎬 Movies Available", len(movies))

with col2:
    st.metric("Recommendation Type", "Content-Based")

search_term = st.text_input("🔍 Quick Search")

movie_options = movies['title'].values
if search_term:
    movie_options = [m for m in movie_options if search_term.lower() in str(m).lower()]

selected_movie = st.selectbox(
    "Select a Movie",
    movie_options
)

if st.button("Get Recommendations"):
    st.session_state.recommendations = recommend(selected_movie)
    st.session_state.selected_movie = selected_movie

if st.button("Clear Results"):
    st.session_state.recommendations = []
    st.session_state.show_details = {}

if st.session_state.recommendations:

    st.success(
        f"Recommendations based on: {st.session_state.selected_movie}"
    )

    recommendations = st.session_state.recommendations

    st.markdown("## Recommended Movies")
    cols = st.columns(3)

    for idx, movie in enumerate(recommendations):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='movie-card'>
                <h3>{movie['title']}</h3>
                <p>🎯 Match Score: {movie['score']}%</p>
                <p>Content-based recommendation using cast and crew similarity.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"ℹ️ View Details {movie['id']}"):
                st.session_state.show_details[movie['id']] = not st.session_state.show_details.get(movie['id'], False)

            if st.session_state.show_details.get(movie['id'], False):
                movie_details = fetch_movie_details(movie['id'])

                if movie_details['poster']:
                    st.image(movie_details['poster'], use_container_width=True)

                st.write(f"⭐ Rating: {movie_details['rating']}")
                st.write(movie_details['overview'])

            if st.button(f"❤️ Save {movie['id']}"):
                if movie['title'] not in st.session_state.favorites:
                    st.session_state.favorites.append(movie['title'])

st.markdown("---")
st.subheader("❤️ Saved Movies")

if st.session_state.favorites:
    for fav in st.session_state.favorites.copy():
        col1, col2 = st.columns([4,1])

        with col1:
            st.write("•", fav)

        with col2:
            if st.button(f"❌ Remove {fav}"):
                st.session_state.favorites.remove(fav)
                st.rerun()
else:
    st.caption("No saved movies yet.")

st.markdown("---")
st.caption("Built by Vikas Kaushik • Python • Scikit-Learn • Streamlit")