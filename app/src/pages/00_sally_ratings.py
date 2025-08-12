import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Sidebar navigation
SideBarLinks()

st.title("Reviews and Ratings")

# ------------------------
# Update Review Rating
# ------------------------
st.subheader("Update Review Rating")
col1, col2 = st.columns(2)
with col1:
    show_id_rating = st.number_input("Show ID", min_value=1, key="update_show_id")
    review_id_rating = st.number_input("Review ID", min_value=1, key="update_review_id")
with col2:
    new_rating = st.number_input("New Rating", min_value=0.0, max_value=5.0, step=0.1, key="update_new_rating")

if st.button("Update Review Rating", key="btn_update_rating"):
    try:
        payload = {"rating": new_rating}
        resp = requests.put(f"http://api:4000/sally/shows/{show_id_rating}/reviews/{review_id_rating}", json=payload)
        if resp.status_code == 200:
            st.success("Review rating updated successfully!")
        else:
            st.error(f"Failed to update review rating: {resp.text}")
    except Exception as e:
        st.error(f"Error updating review rating: {e}")

# ------------------------
# Create Review
# ------------------------
st.subheader("Create Review")
col1, col2 = st.columns(2)
with col1:
    show_id_review = st.number_input("Show ID", min_value=1, key="create_show_id")
    user_id_review = st.number_input("User ID", min_value=1, key="create_user_id")
with col2:
    review_rating = st.number_input("Rating", min_value=0.0, max_value=5.0, step=0.1, key="create_rating")

review_content = st.text_area("Review Content", key="create_content")

if st.button("Create Review", key="btn_create_review"):
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

# ------------------------
# Update Review
# ------------------------
st.subheader("Update Review")
col1, col2 = st.columns(2)
with col1:
    review_id_update = st.number_input("Review ID", min_value=1, key="update_review_review_id")
    user_id_update = st.number_input("User ID", min_value=1, key="update_review_user_id")
with col2:
    update_rating = st.number_input("New Rating", min_value=0.0, max_value=5.0, step=0.1, key="update_review_rating")

update_content = st.text_area("New Review Content", key="update_review_content")

if st.button("Update Review", key="btn_update_review"):
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

# ------------------------
# Delete Review
# ------------------------
st.subheader("Delete Review")
col1, col2 = st.columns(2)
with col1:
    review_id_delete = st.number_input("Review ID", min_value=1, key="delete_review_id")
with col2:
    user_id_delete = st.number_input("User ID", min_value=1, key="delete_user_id")

if st.button("Delete Review", key="btn_delete_review"):
    try:
        payload = {"userId": user_id_delete}
        resp = requests.delete(f"http://api:4000/sally/reviews/{review_id_delete}", json=payload)
        if resp.status_code == 200:
            st.success("Review deleted successfully!")
        else:
            st.error(f"Failed to delete review: {resp.text}")
    except Exception as e:
        st.error(f"Error deleting review: {e}")
