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

st.title(f"Welcome, Analyst {st.session_state['first_name']}.")


# ----------------------------------------------------------------------------
API_URL2 = "http://web-api:4000/alex/users"
if st.button("Active User Count", key="active"):
    try:
        response = requests.get(API_URL2)
        if response.status_code == 200:
            users = response.json()
            for user in users:
                st.write(f" There are {user['num_users']} active users.")
        else:
            st.error(f"Failed to fetch shows from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# ----------------------------------------------------------------------------

if st.button('Click here to check recent review statistics!', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/46_alexreviews.py')

if st.button("Click here to check recent top show rankings and viewings!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/47_alexrankings.py')

if st.button("Click here to filter shows by season count!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/48_alexfiltershow.py')
  