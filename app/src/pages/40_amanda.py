import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

import streamlit as st
import pandas as pd
import requests

st.title(f"Welcome Analyst {st.session_state['first_name']}.")

# ----------------------------------------------------------------------------

if st.button('Click here to add/remove favorite actors!', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/43_amandafavs.py')

if st.button("Click here to check article and review statistics!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/41_amandaarticles.py')

if st.button("Click here to add and check user feedback!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/42_amandafeedback.py')
  