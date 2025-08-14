import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, Viewer {st.session_state['first_name']}.")
st.write('')

if st.button('Click here to create and view comments!', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_johncomments.py')

if st.button("Click here to search for shows by streaming platform!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/16_johnstreaming.py')

if st.button("Click here to filter shows by genre and release date!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_johnshows.py')
  
if st.button("Click here to search for all shows!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_johnshowsearch.py')
