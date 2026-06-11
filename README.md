# 🎬 Movie Recommendation Engine

A Content-Based Movie Recommendation System built using Machine Learning and Streamlit.

## 🚀 Features

- Movie recommendations based on cast and crew similarity
- TF-IDF Vectorization
- Cosine Similarity algorithm
- TMDB API integration
- Movie posters
- Ratings and movie overview
- Save favorite movies
- Responsive Streamlit interface
- Quick movie search

## 🛠️ Tech Stack

- Python
- Pandas
- Scikit-Learn
- Streamlit
- TMDB API
- Requests

## 📊 Machine Learning Approach

The recommendation engine uses:

1. Data preprocessing
2. Feature engineering using cast and crew information
3. TF-IDF Vectorization
4. Cosine Similarity to calculate movie relationships
5. Content-based filtering for recommendations

## 📁 Project Structure

text movie-recommendation-engine/ │ ├── app.py ├── main.py ├── tmdb_movies.csv ├── requirements.txt └── README.md 

## ⚙️ Installation

Clone the repository:

bash git clone https://github.com/your-username/movie-recommendation-engine.git cd movie-recommendation-engine 

Install dependencies:

bash pip install -r requirements.txt 

Run the application:

bash streamlit run app.py 

## 🔑 Environment Variables

Create Streamlit secrets and add:

toml TMDB_API_KEY="YOUR_API_KEY" 

## 🎯 How It Works

- Select a movie from the dropdown.
- Click Get Recommendations.
- The model finds movies with similar cast and crew patterns.
- View additional movie details using TMDB API integration.
- Save movies to your favorites list.

## 📸 Screenshots

Add screenshots of your application here.

## 👨‍💻 Author

Vikas Kaushik

BCA Student | Aspiring Data Scientist | Machine Learning Enthusiast

## 📜 License

This project is created for learning and portfolio purpose
