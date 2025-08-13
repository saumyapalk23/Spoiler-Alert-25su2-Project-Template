import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')
SideBarLinks()

st.title("Filtered by genre")
st.write('')

genre_id = st.number_input("Genre ID", min_value=1, step=1, key="genre_id_input")
if st.button("See Shows", use_container_width=True):
    try:
        response = requests.get(f"http://api:4000/john/shows/genre/{int(genre_id)}")

        if response.status_code == 200:
            shows = response.json()
            if not shows:
                st.info("No shows found for this genre.")
            else:
                st.success(f"Found {len(shows)} show(s).")
                for s in shows:
                    st.write(f"**{s.get('title','Untitled')}**")
                    st.write(f"Rating: {s.get('rating','N/A')}")
                    st.write(f"Release Date: {s.get('releaseDate','Unknown')}")

        elif response.status_code == 404:
            st.warning("No shows found for this genre.")
        else:
            st.error(f"Request failed: {response.status_code}")

    except Exception as e:
        st.error(f"Error talking to the API: {e}")

