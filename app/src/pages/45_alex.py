import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title(f"Welcome Analyst {st.session_state['first_name']}.")

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
            
# ----------------------------------------------------------------------------
API_URL2 = "http://web-api:4000/alex/users"
if st.button("Active User Count", key="active"):
    try:
        response = requests.get(API_URL2)
        if response.status_code == 200:
            users = response.json()
            for user in users:
                st.write(f" There are {user['num_users']} active users.")
        else:
            st.error(f"Failed to fetch shows from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
