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
        resp = requests.get(f"http://api:4000/sally/users/{user_id_watchlists}/watchlist")
        if resp.status_code == 200:
            watchlists = resp.json()
            st.write("**User Watchlists:**")
            for watchlist in watchlists:
                st.write(f"- {watchlist.get('name', 'Unnamed')} (ID: {watchlist.get('toWatchId', 'N/A')})")
        else:
            st.error(f"Failed to get watchlists: {resp.text}")
    except Exception as e:
        st.error(f"Error getting watchlists: {e}")

# Create Watchlist
st.subheader("Create New Watchlist")
user_id_create = st.number_input("User ID", min_value=1, key="user_create_watchlist")
watchlist_name = st.text_input("Watchlist Name", key="watchlist_name")
show_id = st.number_input("Show ID", min_value=1, key="show_id_create")  # Add Show ID input

if st.button("Create Watchlist"):
    if not watchlist_name or not show_id:  # Validate inputs
        st.error("Please enter both watchlist name and show ID")
    else:
        try:
            payload = {
                "name": watchlist_name,
                "showId": show_id  # Include showId in payload
            }
            resp = requests.post(f"http://api:4000/sally/users/{user_id_create}/watchlist", json=payload)
            if resp.status_code == 201:
                result = resp.json()
                st.success(f"Watchlist created successfully! ID: {result.get('toWatchId')}")
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
        resp = requests.put(f"http://api:4000/sally/user/{user_id_add_show}/watchlist/shows/{show_id_add}", json=payload)
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
        resp = requests.delete(f"http://api:4000/sally/user/{user_id_remove_show}/watchlist/shows/{show_id_remove}", json=payload)
        if resp.status_code == 201:
            st.success("Show removed from watchlist successfully!")
        else:
            st.error(f"Failed to remove show: {resp.text}")
    except Exception as e:
        st.error(f"Error removing show: {e}")



# ------------------------
# Display all Watchlists
# ------------------------

st.subheader("View All Watchlists")
try:
    resp = requests.get("http://api:4000/sally/watchlists")
    
    if resp.status_code == 200:
        watchlists_data = resp.json()
        
        if watchlists_data:
            st.success(f"Found {len(watchlists_data)} watchlist entries:")
            
            # Display watchlists in an organized way
            for i, watchlist in enumerate(watchlists_data, 1):
                with st.expander(f"{i}. {watchlist.get('name', 'Unnamed')} (User: {watchlist.get('userId', 'Unknown')})"):
                    st.write(f"**To Watch ID:** {watchlist.get('toWatchId', 'N/A')}")
                    st.write(f"**Name:** {watchlist.get('name', 'N/A')}")
                    st.write(f"**User ID:** {watchlist.get('userId', 'N/A')}")
                    st.write(f"**Show ID:** {watchlist.get('showId', 'N/A')}")
                    st.write(f"**Created At:** {watchlist.get('createdAt', 'N/A')}")
        else:
            st.info("No watchlists found.")
    else:
        st.error(f"Failed to load watchlists: {resp.text}")
except Exception as e:
    st.error(f"Error loading watchlists: {e}")


