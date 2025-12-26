import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")


@st.cache_data
def load_movies():
    r = requests.get(f"{API_URL}/movies", timeout=30)
    r.raise_for_status()
    return r.json()


@st.cache_data
def get_recommendations(movie):
    r = requests.get(
        f"{API_URL}/recommend/{movie}",
        timeout=30
    )
    r.raise_for_status()
    return r.json()


try:
    movies = load_movies()
except Exception as e:
    st.error("Backend API not running")
    st.exception(e)
    st.stop()


selected_movie = st.selectbox("Select a movie", movies)

if st.button("Recommend"):
    with st.spinner("Finding similar movies... 🍿"):
        response = get_recommendations(selected_movie)

    if "error" in response:
        st.warning(response["error"])
        st.stop()

    st.subheader("Recommended Movies")
    cols = st.columns(len(response["recommendations"]))

    for col, movie in zip(cols, response["recommendations"]):
        with col:
            if movie["poster"]:
                st.markdown(
                    f"""
                    <a href="{movie['tmdb_url']}" target="_blank">
                        <img src="{movie['poster']}"
                             style="width:100%; border-radius:10px;">
                    </a>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.caption("Poster unavailable")

            st.markdown(f"**{movie['title']}**")
