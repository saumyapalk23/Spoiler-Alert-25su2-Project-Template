import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Streaming Platforms")
st.write('')

# Match these ids in mock data 
PLATFORMS = {
    "Netflix": 1,
    "Hulu": 2,
    "Prime Video": 3,
    "Disney+": 4,
    "Max (HBO)": 5,
    "Apple TV+": 6,
    "Peacock": 7,
    "Paramount+": 8,
}

platform = st.selectbox("Choose a platform", list(PLATFORMS.keys()))
platform_id = PLATFORMS[platform]

if st.button("Show catalog", use_container_width=True):
    try:
        response = requests.get(f"http://api:4000/john/shows/streaming_platform/{int(platform_id)}")
        if response.status_code == 200:
            shows = response.json()
            if not shows:
                st.info(f"No shows found on {platform}.")
            else:
                st.success(f"Found {len(shows)} show(s) on {platform}.")
                for s in shows:
                    st.write(f"**{s.get('title','Untitled')}**")
                    st.write(f"Rating: {s.get('rating','N/A')}")
                    st.write(f"Release Date: {s.get('releaseDate','Unknown')}")
        elif response.status_code == 404:
            st.warning(f"No shows found on {platform}.")
        else:
            st.error(f"Request failed: {response.status_code}")
    except Exception as e:
        st.error(f"Error contacting API: {e}")
