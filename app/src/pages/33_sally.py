import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, Filmmaker {st.session_state['first_name']}.")
st.write('')


            

if st.button('Click here to create and update reviews!', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/00_sally_ratings.py')

if st.button("Click here to create and modify your watchlists!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_sally_watchlists.py')

if st.button("Click here to follow others and see some favorites!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_sally_follows.py')
  