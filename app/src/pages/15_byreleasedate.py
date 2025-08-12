import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Filtered by Release Date")
st.write('')

year = st.number_input("Enter a year", min_value=1900, max_value=2100, step=1, key="year_input")

if st.button("See Shows", use_container_width=True):
    try:
        resp = requests.get(f"http://api:4000/john/shows/release_date/{int(year)}")

        if resp.status_code == 200:
            shows = resp.json()
            if not shows:
                st.info("No shows found for that year.")
            else:
                st.success(f"Found {len(shows)} show(s) released in {year}")
                for s in shows:
                    st.write(f"**{s.get('title', 'Untitled')}**")
                    st.write(f"Rating: {s.get('rating', 'N/A')}")
                    st.write(f"Release Date: {s.get('releaseDate', 'Unknown')}")
                    st.write("---")
        elif resp.status_code == 404:
            st.warning("No shows found for that year.")
        else:
            st.error(f"Request failed: {resp.status_code}")

    except Exception as e:
        st.error(f"Error contacting API: {e}")