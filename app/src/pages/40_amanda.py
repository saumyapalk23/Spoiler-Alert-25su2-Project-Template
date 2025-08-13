import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar navigation
SideBarLinks()

st.title(f"Welcome Analyst {st.session_state['first_name']}.")

st.subheader("Add a Favorite")
user_id_add = st.text_input("User ID (add favorite)", key="user_add")
fav_id_add = st.text_input("Favorite ID", key="fav_add")
show_id_add = st.text_input("Show ID", key="show_add")
if st.button("Add Favorite"):
    try:
        payload = {
            "favoriteID": fav_id_add,
            "showId": show_id_add,
        }
        resp = requests.post(f"http://api:4000/admin/users/{user_id_add}/favorites/", json=payload)
        if resp.status_code == 200:
            st.success("Favorite added successfully!")
        else:
            st.error(f"Failed to add favorite: {resp.text}")
    except Exception as e:
        st.error(f"Error adding favorite: {e}")

st.subheader("Remove a Favorite")
user_id_del = st.text_input("User ID (remove favorite)", key="user_del")
fav_id_del = st.text_input("Favorite ID", key="fav_del")
show_id_del = st.text_input("Show ID", key="show_del")
if st.button("Remove Favorite"):
    try:
        payload = {
            "favoriteID": fav_id_del,
            "showId": show_id_del,
        }
        resp = requests.delete(f"http://api:4000/admin/users/{user_id_del}/favorites/", json=payload)
        if resp.status_code == 200:
            st.success("Favorite removed successfully!")
        else:
            st.error(f"Failed to remove favorite: {resp.text}")
    except Exception as e:
        st.error(f"Error removing favorite: {e}")


# -----------------------------------------------------------------------------
st.markdown("---")  # Add a separator line

st.subheader("View Favorites")

if st.button("View Favorites"):
    try:
        resp = requests.get(f"http://api:4000/admin/users/favorites/")
        if resp.status_code == 200:
            favorites_data = resp.json()
            
            if favorites_data and len(favorites_data) > 0:
                st.success(f"Found {len(favorites_data)} favorites total")
                
                # Display favorites in a nice format
                for i, favorite in enumerate(favorites_data, 1):
                    with st.expander(f"Favorite #{i}"):
                        st.write(f"**User ID:** {favorite.get('userID', 'N/A')}")
                        st.write(f"**Favorite ID:** {favorite.get('favoriteID', 'N/A')}")
                        st.write(f"**Show ID:** {favorite.get('showId', 'N/A')}")
                        # Add any other fields that might be in the response
                        for key, value in favorite.items():
                            if key not in ['userID', 'favoriteID', 'showId']:
                                st.write(f"**{key.title()}:** {value}")
            else:
                st.info("No favorites found in the database")
        else:
            st.error(f"Failed to retrieve favorites: {resp.text}")
    except Exception as e:
        st.error(f"Error retrieving favorites: {e}")

