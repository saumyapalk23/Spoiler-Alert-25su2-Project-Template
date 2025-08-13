import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Keyword Show Search")
st.write('')

keyword = st.text_input("Search by keyword", placeholder="e.g., crime, space, romance")

if st.button("Search Shows"):
    try:
        if keyword.strip() == "":
            st.warning("Please type something to search.")
        else:
            response = requests.get(f"http://api:4000/john/shows/search", params={"keyword": keyword})
            if response.status_code == 200:
                shows = response.json()
                if shows:
                    for show in shows:
                        st.write(f"**{show.get('title', 'No Title')}**")
                        st.write(f"Rating: {show.get('rating', 'N/A')}")
                        st.write(f"Release Date: {show.get('releaseDate', 'Unknown')}")
                        st.write("---")
                else:
                    st.info("No shows found. Try another keyword.")
            else:
                st.error(f"Search failed: {response.status_code}")
    except Exception as e:
        st.error(f"Error searching shows: {e}")
