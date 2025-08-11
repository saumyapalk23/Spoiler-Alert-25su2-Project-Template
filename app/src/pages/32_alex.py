import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Alex API DEMO")

# API endpoint
API_URL1 = "http://web-api:4000/alex/shows"

if st.button("Show Top 5 Most Reviewed Shows", key=0):
    try:
        response = requests.get(API_URL1)
        if response.status_code == 200:
            shows = response.json()
            # Display each show in an expander
            for show in shows:
                # Defensive key access in case DB returns tuples/dicts differently
                show_id = show.get("showId", "N/A")
                title = show.get("title", "Untitled")
                season = show.get("season", "N/A")
                rating = show.get("rating", "N/A")
                release_date = show.get("releaseDate", "Unknown")
                age_rating = show.get("ageRating", "N/A")
                streaming_platform = show.get("streamingPlatform", "Unknown")

                with st.expander(f"{title} (Season {season})"):
                    st.write(f"**Show ID:** {show_id}")
                    st.write(f"**Rating:** {rating}")
                    st.write(f"**Release Date:** {release_date}")
                    st.write(f"**Age Rating:** {age_rating}")
                    st.write(f"**Streaming Platform:** {streaming_platform}")
        else:
            st.error(f"Failed to fetch shows from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# ----------------------------------------------------------------------------
API_URL2 = "http://web-api:4000/alex/users"
if st.button("Active User Count",type='primary',
             use_container_width=True):
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

# ----------------------------------------------------------------------------
