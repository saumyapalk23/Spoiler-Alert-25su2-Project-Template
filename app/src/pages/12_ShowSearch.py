import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Keyword Show Search")
st.write('')

keyword = st.text_input("Search by keyword", placeholder="e.g., crime, detective, romance")

if st.button("Search Shows"):
    try:
        if not keyword.strip():
            st.warning("Please type something to search.")
        else:
            r = requests.get(
                "http://api:4000/john/shows/search",
                params={"keyword": keyword.strip()})
            if r.ok:
                shows = r.json()
                if not shows:
                    st.info("No shows found. Try another keyword.")
                else:
                    for s in shows:
                        st.write(f"**{s.get('title', 'No Title')}**")
                        st.write(f"Rating: {s.get('rating', 'N/A')}")
                        st.write(f"Release Date: {s.get('releaseDate', 'Unknown')}")
                        st.write(f"Season: {s.get('season', '—')}")
                        st.write(f"Age Rating: {s.get('ageRating', '—')}")
                        st.write(f"Platform: {s.get('streamingPlatform', '—')}")
            else:
                st.error(f"Search failed: {r.status_code}")
    except Exception as e:
        st.error(f"Error searching shows: {e}")