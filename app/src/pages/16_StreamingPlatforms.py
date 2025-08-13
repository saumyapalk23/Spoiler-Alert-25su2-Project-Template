import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')
SideBarLinks()
st.title("Streaming Platforms")
st.write('')
PLATFORMS = {
    "Netflix": 1,
    "Hulu": 2,
    "Prime Video": 3,
    "Disney+": 4,
    "HBO Max": 5,
    "Apple TV+": 6,
    "Peacock": 7,
    "Paramount+": 8,
    "Fubo": 9,
    "BBC": 10,
    "Crunchyroll": 11,
    "Discovery+": 12,
    "ESPN": 13,
    "FandangoNow": 14,
    "YouTube": 15,
    "PlutoTV": 16,
}

platform = st.selectbox("Choose a platform", list(PLATFORMS.keys()))
platform_id = PLATFORMS[platform]

if st.button("Show catalog", use_container_width=True):
    try:
        url = f"http://api:4000/john/shows/streaming_platform/{int(platform_id)}"
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            shows = r.json()
            if not shows:
                st.info(f"No shows found on {platform}.")
            else:
                st.success(f"Found {len(shows)} show(s) on {platform}.")
                for s in shows:
                    st.write(f"**{s.get('title','Untitled')}**")
                    st.write(f"Rating: {s.get('rating','N/A')}")
                    st.write(f"Release Date: {s.get('releaseDate','Unknown')}")
                    st.write("---")
        elif r.status_code == 404:
            st.warning(f"No shows found on {platform}.")
        else:
            st.error(f"Request failed: {r.status_code}")
    except Exception as e:
        st.error(f"Error contacting API: {e}")