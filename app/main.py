from fastapi import FastAPI
from app.recommender import recommend
import pickle

app = FastAPI(title="Movie Recommendation API")

movies = pickle.load(open("movies.pkl", "rb"))

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/movies")
def get_movies():
    return movies['title'].tolist()

@app.get("/recommend/{movie_name}")
def get_recommendations(movie_name: str):
    recommendations = recommend(movie_name)
    if not recommendations:
        return {"error": "Movie not found"}
    return {"recommendations": recommendations}
