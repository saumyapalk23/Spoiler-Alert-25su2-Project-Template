import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.title("Watchlists")


# Get User Watchlists
st.subheader("View User Watchlists")
user_id_watchlists = st.number_input("User ID", min_value=1, key="user_watchlists")
if st.button("Get Watchlists"):
    try:
        resp = requests.get(f"http://api:4000/sally/users/{user_id_watchlists}/watchlists")
        if resp.status_code == 200:
            watchlists = resp.json()
            st.write("**User Watchlists:**")
            for watchlist in watchlists:
                st.write(f"- {watchlist.get('name', 'Unnamed')} (ID: {watchlist.get('watchlistId', 'N/A')})")
        else:
            st.error(f"Failed to get watchlists: {resp.text}")
    except Exception as e:
        st.error(f"Error getting watchlists: {e}")

# Create Watchlist
st.subheader("Create New Watchlist")
user_id_create = st.number_input("User ID", min_value=1, key="user_create_watchlist")
watchlist_name = st.text_input("Watchlist Name", key="watchlist_name")
if st.button("Create Watchlist"):
    try:
        payload = {"name": watchlist_name}
        resp = requests.post(f"http://api:4000/sally/users/{user_id_create}/watchlists", json=payload)
        if resp.status_code == 201:
            st.success("Watchlist created successfully!")
        else:
            st.error(f"Failed to create watchlist: {resp.text}")
    except Exception as e:
        st.error(f"Error creating watchlist: {e}")

# Add Show to Watchlist
st.subheader("Add Show to Watchlist")
col1, col2 = st.columns(2)
with col1:
    user_id_add_show = st.number_input("User ID", min_value=1, key="user_add_show")
    show_id_add = st.number_input("Show ID", min_value=1, key="show_add_watchlist")
with col2:
    watchlist_id_add = st.number_input("Watchlist ID", min_value=1, key="watchlist_add")

if st.button("Add Show to Watchlist"):
    try:
        payload = {"toWatchId": watchlist_id_add}
        resp = requests.put(f"http://api:4000/sally/user/{user_id_add_show}/watchlists/shows/{show_id_add}", json=payload)
        if resp.status_code == 201:
            st.success("Show added to watchlist successfully!")
        else:
            st.error(f"Failed to add show: {resp.text}")
    except Exception as e:
        st.error(f"Error adding show: {e}")

# Remove Show from Watchlist
st.subheader("Remove Show from Watchlist")
col1, col2 = st.columns(2)
with col1:
    user_id_remove_show = st.number_input("User ID", min_value=1, key="user_remove_show")
    show_id_remove = st.number_input("Show ID", min_value=1, key="show_remove_watchlist")
with col2:
    watchlist_id_remove = st.number_input("Watchlist ID", min_value=1, key="watchlist_remove")

if st.button("Remove Show from Watchlist"):
    try:
        payload = {"toWatchId": watchlist_id_remove}
        resp = requests.delete(f"http://api:4000/sally/user/{user_id_remove_show}/watchlists/shows/{show_id_remove}", json=payload)
        if resp.status_code == 201:
            st.success("Show removed from watchlist successfully!")
        else:
            st.error(f"Failed to remove show: {resp.text}")
    except Exception as e:
        st.error(f"Error removing show: {e}")


