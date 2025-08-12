import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar navigation
SideBarLinks()

st.title("Sally API Demo")

# Update Show Rating
st.subheader("Update Show Rating")
show_id_rating = st.number_input("Show ID", min_value=1, key="show_rating")
new_rating = st.number_input("New Rating", min_value=0.0, max_value=5.0, step=0.1, key="rating")
if st.button("Update Show Rating"):
    try:
        payload = {"rating": new_rating}
        resp = requests.put(f"http://api:4000/sally/shows/{show_id_rating}", json=payload)
        if resp.status_code == 200:
            st.success("Show rating updated successfully!")
        else:
            st.error(f"Failed to update rating: {resp.text}")
    except Exception as e:
        st.error(f"Error updating rating: {e}")

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

# Create Review
st.subheader("Create Review")
col1, col2 = st.columns(2)
with col1:
    show_id_review = st.number_input("Show ID", min_value=1, key="show_review")
    user_id_review = st.number_input("User ID", min_value=1, key="user_review")
with col2:
    review_rating = st.number_input("Rating", min_value=0.0, max_value=5.0, step=0.1, key="review_rating")

review_content = st.text_area("Review Content", key="review_content")

if st.button("Create Review"):
    try:
        payload = {
            "userId": user_id_review,
            "rating": review_rating,
            "content": review_content
        }
        resp = requests.post(f"http://api:4000/sally/shows/{show_id_review}/reviews", json=payload)
        if resp.status_code == 201:
            result = resp.json()
            st.success(f"Review created successfully! Review ID: {result.get('reviewId')}")
        else:
            st.error(f"Failed to create review: {resp.text}")
    except Exception as e:
        st.error(f"Error creating review: {e}")

# Update Review
st.subheader("Update Review")
col1, col2 = st.columns(2)
with col1:
    review_id_update = st.number_input("Review ID", min_value=1, key="review_id_update")
    user_id_update = st.number_input("User ID", min_value=1, key="user_update")
with col2:
    update_rating = st.number_input("New Rating", min_value=0.0, max_value=5.0, step=0.1, key="update_rating")

update_content = st.text_area("New Review Content", key="update_content")

if st.button("Update Review"):
    try:
        payload = {
            "userId": user_id_update,
            "rating": update_rating,
            "content": update_content
        }
        resp = requests.put(f"http://api:4000/sally/reviews/{review_id_update}", json=payload)
        if resp.status_code == 200:
            st.success("Review updated successfully!")
        else:
            st.error(f"Failed to update review: {resp.text}")
    except Exception as e:
        st.error(f"Error updating review: {e}")

# Delete Review
st.subheader("Delete Review")
col1, col2 = st.columns(2)
with col1:
    review_id_delete = st.number_input("Review ID", min_value=1, key="review_id_delete")
with col2:
    user_id_delete = st.number_input("User ID", min_value=1, key="user_delete")

if st.button("Delete Review"):
    try:
        payload = {"userId": user_id_delete}
        resp = requests.delete(f"http://api:4000/sally/reviews/{review_id_delete}", json=payload)
        if resp.status_code == 200:
            st.success("Review deleted successfully!")
        else:
            st.error(f"Failed to delete review: {resp.text}")
    except Exception as e:
        st.error(f"Error deleting review: {e}")

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