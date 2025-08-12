import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')


#starting with the same display as sallys to display shows
API_URL1 = "http://web-api:4000/alex/shows"
def fetch_shows():
    try:
        response = requests.get(API_URL1)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch shows. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return []

def main():
    st.title("Shows Filtered by Number of Seasons")

    shows = fetch_shows()
    if not shows:
        return

    # Extract max seasons from shows for slider max
    max_seasons = max(show.get("totalSeasons", 1) for show in shows)

    # Slider for max number of seasons
    max_selected = st.slider("Select max number of seasons to display:", 1, max_seasons, 3)

    # Filter shows
    filtered_shows = [show for show in shows if show.get("totalSeasons", 0) <= max_selected]

    st.write(f"Showing {len(filtered_shows)} shows with {max_selected} or fewer seasons:")

    for show in filtered_shows:
        title = show.get("title", "Untitled")
        total_seasons = show.get("totalSeasons", "N/A")
        rating = show.get("rating", "N/A")
        release_date = show.get("releaseDate", "Unknown")
        age_rating = show.get("ageRating", "N/A")
        streaming_platform = show.get("streamingPlatform", "Unknown")

        with st.expander(f"{title} (Total Seasons: {total_seasons})"):
            st.write(f"**Rating:** {rating}")
            st.write(f"**Release Date:** {release_date}")
            st.write(f"**Age Rating:** {age_rating}")
            st.write(f"**Streaming Platform:** {streaming_platform}")
            

if st.button('View the Simple API Demo', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_API_Test.py')

if st.button("View Classification Demo",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Classification.py')
  