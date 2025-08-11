import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Alex API DEMO")

# API endpoint
API_URL1 = "http://web-api:4000/alex/shows"
if st.button("Show Top 5 Most Reviewed Shows", key="most_reviewed"):
    try:
        response = requests.get(API_URL1)
        if response.status_code == 200:
            shows = response.json()
            for show in shows:
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

# ----------------------------------------------------------------------------
API_URL5 = "http://web-api:4000/alex/shows/{id}"
if st.button("Average Star Ranking",key="avg_rating"):
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
if st.button("Viewings",key="num_watches"):
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
