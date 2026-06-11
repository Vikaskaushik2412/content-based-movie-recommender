# 🎬 Setup & Installation Guide

## Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git
- TMDB API Key (free account at https://www.themoviedb.org/settings/api)

## Step-by-Step Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Vikaskaushik2412/content-based-movie-recommender.git
cd content-based-movie-recommender
```

### 2. Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your TMDB API key
# You can use: nano .env (Linux/Mac) or Notepad .env (Windows)
```

### For Streamlit Secrets (Alternative Method)
Create `.streamlit/secrets.toml`:
```bash
mkdir .streamlit
touch .streamlit/secrets.toml
```

Add to `.streamlit/secrets.toml`:
```toml
TMDB_API_KEY = "your_api_key_here"
```

### 5. Verify Installation
```bash
# Test imports
python -c "import pandas, streamlit, sklearn; print('All dependencies installed!')"
```

### 6. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### API Key Issues
- Verify your TMDB API key is correct
- Check that your `.env` file is in the project root
- Ensure `.env` is in `.gitignore` (never commit secrets!)

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Slow Initial Load
- First run may take time to download and process movie dataset
- Subsequent runs will be faster due to caching

## Virtual Environment Deactivation
```bash
deactivate
```

## Project Structure
```
content-based-movie-recommender/
├── app.py                  # Streamlit web interface
├── main.py                 # ML model & recommendation logic
├── tmdb_movies.csv         # Movie dataset
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore patterns
└── README.md              # Project documentation
```

## Next Steps
1. Explore the app interface
2. Try searching for your favorite movie
3. Check recommendations based on similar cast/crew
4. Customize the algorithm in main.py

For issues, please check the README.md or create a GitHub issue.
