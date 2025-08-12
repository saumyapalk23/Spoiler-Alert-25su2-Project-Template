import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Filters")
st.write('')

if st.button("View shows filtered by genre",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_bygenre.py')

if st.button("View shows filtered by release date",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/15_byreleasedate.py')
  