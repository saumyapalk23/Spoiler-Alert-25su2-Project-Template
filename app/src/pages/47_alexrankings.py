import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title(f"Welcome Analyst {st.session_state['first_name']}.")

#-----------------------------------------------------------------------
API_URL5 = "http://web-api:4000/alex/shows/{id}"
if st.button("Top 5 Shows - Average Star Ranking",key="avg_rating"):
    try:
        response = requests.get(API_URL5)
        if response.status_code == 200:
            shows = response.json()
            for show in shows:
                showName = show.get("title", "N/A")
                rating = show.get("average_rating", "Unknown")

                with st.expander(f"**Show:** {showName}"):
                     st.write(f"**Average Rating:** {rating}")
        else:
            st.error(f"Failed to fetch shows from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# ----------------------------------------------------------------------------
API_URL6 = "http://web-api:4000/alex/shows/{id}/watches/num-watches"
if st.button("Viewings - All Shows",key="num_watches"):
    try:
        response = requests.get(API_URL6)
        if response.status_code == 200:
            shows = response.json()
            for show in shows:
                showName = show.get("title", "N/A")
                viewings = show.get("num_watches", "Unknown")
                
                with st.expander(f"**Show:** {showName}"):
                     st.write(f"**Viewings:** {viewings}")
        else:
            st.error(f"Failed to fetch shows from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
