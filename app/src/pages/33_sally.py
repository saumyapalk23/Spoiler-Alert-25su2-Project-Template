import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Sally API DEMO")

# API endpoint
API_URL = "http://web-api:4000/sally/shows/{int:showId}"

try:
    response = requests.get(API_URL)
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

    #             # Optional button for further action
    #             if st.button(f"View Details", key=f"view_{show_id}"):
    #                 st.session_state["selected_show_id"] = show_id
    #                 st.switch_page("pages/Show_Profile.py")

    else:
        st.error(f"Failed to fetch shows from API. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to API: {str(e)}")