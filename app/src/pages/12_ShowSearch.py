import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Show Search")
st.write('')
st.write("Type in a keyword and I'll look for matching shows for you!")

keyword = st.text_input("Search by keyword", placeholder="e.g., crime, space, romance")

if st.button("Search Shows"):
    try:
        if keyword.strip() == "":
            st.warning("Please type something to search.")
        else:
            resp = requests.get(f"http://api:4000/john/shows/search", params={"keyword": keyword})
            if resp.status_code == 200:
                shows = resp.json()
                if shows:
                    for show in shows:
                        st.write(f"**{show.get('title', 'No Title')}**")
                        st.write(f"Rating: {show.get('rating', 'N/A')}")
                        st.write(f"Release Date: {show.get('releaseDate', 'Unknown')}")
                        st.write("---")
                else:
                    st.info("No shows found. Try another keyword.")
            else:
                st.error(f"Search failed: {resp.status_code} — {resp.text}")
    except Exception as e:
        st.error(f"Error searching shows: {e}")
