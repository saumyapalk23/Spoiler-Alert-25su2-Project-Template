import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')
SideBarLinks()

st.title("Filtered by genre")
st.write('')

GENRES = {
    "Comedy|Drama": 1,
    "Action|Thriller": 2,
    "Drama|Thriller": 3,
    "Documentary": 4,
    "Comedy": 5,
    "Comedy|Drama|Romance": 6,
    "Drama|Romance": 7,
    "Horror": 8,
    "Adventure|Animation": 9,
    "Comedy|Horror": 10,
    "Drama|Mystery": 11,
    "Crime|Drama|Thriller": 12,
    "Drama|Mystery": 13,
    "Action|Drama|War": 14,
    "Comedy": 15,
    "Children|Comedy": 16,
    "Horror": 17,
    "Comedy|Drama": 18,
    "Comedy|Horror": 19,
    "Drama": 20,
    "Drama|Western": 21,
    "Comedy|Romance": 22,
    "Action|Drama": 23,
    "Sci-Fi|Thriller": 24,
    "Documentary": 25,
    "Comedy": 26,
    "Comedy": 27,
    "Drama|Thriller": 28,
    "Adventure|Animation|Horror|Sci-Fi|Thriller": 29,
    "Documentary": 30,
    "Action|Adventure|Drama|War": 31,
    "Documentary": 32,
    "Drama": 33,
    "Comedy|Fantasy": 34,
    "Comedy": 35,
    "Action|Horror": 36,
    "Documentary": 37,
    "Comedy|Drama": 38,
    "Crime|Drama|Romance": 39,
    "Adventure|Fantasy": 40,
}

genre_label = st.selectbox("Choose a genre", list(GENRES.keys()))
genre_id = GENRES[genre_label]

if st.button("See Shows", use_container_width=True):
    try:
        url = f"http://api:4000/john/shows/genre/{int(genre_id)}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            shows = r.json()
            if not shows:
                st.info(f"No shows found for {genre_label}.")
            else:
                st.success(f"Found {len(shows)} show(s) for {genre_label}.")
                for s in shows:
                    st.write(f"**{s.get('title','Untitled')}**")
                    st.write(f"Rating: {s.get('rating','N/A')}")
                    st.write(f"Release Date: {s.get('releaseDate','Unknown')}")
        elif r.status_code == 404:
            st.warning(f"No shows found for {genre_label}.")
        else:
            st.error(f"Request failed: {r.status_code}")
    except Exception as e:
        st.error(f"Error talking to the API: {e}")