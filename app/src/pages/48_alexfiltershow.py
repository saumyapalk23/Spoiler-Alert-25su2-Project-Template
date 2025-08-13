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


# Fetch data from the API
try:
    shows = requests.get('http://api:4000/alex/shows').json()
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching shows: {e}")
    shows = []

# Get the slider value
selected_szn = st.slider("Choose season:", 0, 20, (0, 20))

# Filter shows based on the slider value
filtered_shows = []
for show in shows:
    try:
        # Safely convert the season value to an integer
        season_value = int(show.get('season', 0))
        if selected_szn[0] <= season_value <= selected_szn[1]:
            filtered_shows.append(show)
    except (ValueError, TypeError):
        # This block catches errors where 'season' isn't a number
        # It's a good practice to log or handle this, but for now, we just continue.
        continue

# Display the results
if filtered_shows:
    st.write('Here are the shows you requested!')
    st.dataframe(filtered_shows)
else:
    st.write('No shows found that meet your criteria.')
