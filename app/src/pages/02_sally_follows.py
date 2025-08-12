import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.title("Follows")

# Follow User
st.subheader("Follow User")
col1, col2 = st.columns(2)
with col1:
    user_to_follow = st.number_input("User ID to Follow", min_value=1, key="user_to_follow")
with col2:
    follower_id = st.number_input("Follower ID", min_value=1, key="follower_id")

if st.button("Follow User"):
    try:
        payload = {"followerId": follower_id}
        resp = requests.post(f"http://api:4000/sally/users/{user_to_follow}/follows", json=payload)
        if resp.status_code == 201:
            st.success("User followed successfully!")
        else:
            st.error(f"Failed to follow user: {resp.text}")
    except Exception as e:
        st.error(f"Error following user: {e}")

# Unfollow User
st.subheader("Unfollow User")
col1, col2 = st.columns(2)
with col1:
    user_to_unfollow = st.number_input("User ID to Unfollow", min_value=1, key="user_to_unfollow")
with col2:
    unfollower_id = st.number_input("Unfollower ID", min_value=1, key="unfollower_id")

if st.button("Unfollow User"):
    try:
        payload = {"followerId": unfollower_id}
        resp = requests.delete(f"http://api:4000/sally/users/{user_to_unfollow}/follow", json=payload)
        if resp.status_code == 200:
            st.success("User unfollowed successfully!")
        else:
            st.error(f"Failed to unfollow user: {resp.text}")
    except Exception as e:
        st.error(f"Error unfollowing user: {e}")



# Get Favorite Shows by Users
st.subheader("Get Favorite Shows by Users")
age_filter = st.number_input("Age Filter (optional, leave 0 for all ages)", min_value=0, max_value=120, key="age_filter")

if st.button("Get Favorite Shows"):
    try:
        # Build URL with optional age parameter
        url = "http://api:4000/sally/shows/favorites/users"
        params = {}
        if age_filter > 0:
            params['age'] = age_filter
        
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            favorites = data.get('favorites', [])
            
            if favorites:
                st.write("**Favorite Shows:**")
                for show in favorites:
                    favorite_count = show.get('favorite_count', 0)
                    rating = show.get('rating', 'N/A')
                    st.write(f"**{show.get('title', 'Unknown')}** (ID: {show.get('showID', 'N/A')})")
                    st.write(f"  - Rating: {rating} | Favorited by: {favorite_count} users")
                    st.write(f"  - Platform: {show.get('streamingPlatform', 'N/A')} | Age Rating: {show.get('ageRating', 'N/A')}")
                    st.write(f"  - Season: {show.get('season', 'N/A')} | Release: {show.get('releaseDate', 'N/A')}")
                    st.write("---")
            else:
                if age_filter > 0:
                    st.info(f"No favorite shows found for users aged {age_filter}")
                else:
                    st.info("No favorite shows found")
        else:
            st.error(f"Failed to get favorite shows: {resp.text}")
    except Exception as e:
        st.error(f"Error getting favorite shows: {e}")
