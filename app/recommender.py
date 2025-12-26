import os
import pickle
import requests

BASE_POSTER_URL = "https://image.tmdb.org/t/p/w500"

# LOAD ONCE AT IMPORT TIME
with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)


def fetch_movie_details(movie_title):
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    if not TMDB_API_KEY:
        return {"poster": None, "tmdb_url": None}

    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie_title}

    try:
        response = requests.get(url, params=params, timeout=5).json()
    except:
        return {"poster": None, "tmdb_url": None}

    if response.get("results"):
        movie = response["results"][0]
        return {
            "poster": BASE_POSTER_URL + movie["poster_path"]
            if movie.get("poster_path")
            else None,
            "tmdb_url": f"https://www.themoviedb.org/movie/{movie['id']}",
        }

    return {"poster": None, "tmdb_url": None}


def recommend(movie, top_n=5):
    if movie not in movies["title"].values:
        return []

    index = movies[movies["title"] == movie].index[0]
    distances = similarity[index]

    recommended = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1 : top_n + 1]

    results = []
    for i in recommended:
        title = movies.iloc[i[0]].title
        details = fetch_movie_details(title)

        results.append(
            {
                "title": title,
                "poster": details["poster"],
                "tmdb_url": details["tmdb_url"],
            }
        )

    return results
