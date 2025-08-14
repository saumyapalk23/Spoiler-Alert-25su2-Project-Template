import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title(f"Welcome, Analyst {st.session_state['first_name']}.")

# ----------------------------------------------------------------------------
API_URL3 = "http://web-api:4000/alex/shows/{id}/reviews/most-recent"
if st.button("Most Recent Reviews",key="most_recent"):
    try:
        response = requests.get(API_URL3)
        if response.status_code == 200:
            reviews = response.json()
            for review in reviews:
                showId = review.get("showId", "N/A")
                showName = review.get("title", "Unknown")
                user = review.get("userName", "Untitled")
                rating = review.get("rating", "N/A")
                content = review.get("content", "Unknown")

                with st.expander(f"{user}"):
                    st.write(f" **Show:** {showName}")
                    st.write(f"**Rating:** {rating}")
                    st.write(f"**Review:** {content}")

        else:
            st.error(f"Failed to fetch shows from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# ----------------------------------------------------------------------------
API_URL4 = "http://web-api:4000/alex/reviews/time-reviewed"
if st.button("All Reviews - Created At",key="time_made"):
    try:
        response = requests.get(API_URL4)
        if response.status_code == 200:
            reviews = response.json()
            for review in reviews:
                revId = review.get("writtenrevId", "Untitled")
                time = review.get("createdAt", "N/A")
                content = review.get("content", "N/A")

                with st.expander(f"Review Id: {revId}"):
                    st.write(f"**Created At:** {time}")
                    st.write(f"**Review:** {content}")

        else:
            st.error(f"Failed to fetch shows from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

