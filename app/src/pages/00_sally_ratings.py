import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Sidebar navigation
SideBarLinks()

st.title("Reviews and Ratings")


# ------------------------
# Create Review
# ------------------------
st.subheader("Create Review")
col1, col2 = st.columns(2)
with col1:
    show_id_review = st.number_input("Initial Show ID", min_value=1, key="create_show_id")
    user_id_review = st.number_input("User ID", min_value=1, key="create_user_id")
with col2:
    review_rating = st.number_input("Rating", min_value=0.0, max_value=5.0, step=0.1, key="create_rating")
    writtenrev_id = st.number_input("Written Review ID", min_value=1, key="create_writtenrev_id")

review_content = st.text_area("Review Content", key="create_content")

if st.button("Create Review", key="btn_create_review"):
    try:
        payload = {
            "userId": user_id_review,
            "rating": review_rating,
            "content": review_content,
            "writtenrevId": writtenrev_id
        }
        resp = requests.post(f"http://api:4000/sally/shows/{show_id_review}/reviews", json=payload)
        if resp.status_code == 200:
            st.success("Review created successfully!")
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
    update_show_id = st.number_input("Show ID", min_value=1, key="upd_show_id")
    update_writtenrev_id = st.number_input("Written Review ID", min_value=1, key="upd_writtenrev_id")
with col2:
    update_user_id = st.number_input("User ID", min_value=1, key="upd_user_id")
    update_rating = st.number_input("Rating", min_value=0.0, max_value=5.0, step=0.1, key="upd_rating")

update_content = st.text_area("Review Content", key="upd_content")

if st.button("Update Review", key="btn_update_review"):
    try:
        payload = {
            "userId": update_user_id,
            "rating": update_rating,
            "content": update_content
        }
        resp = requests.put(f"http://api:4000/sally/shows/{update_show_id}/reviews/{update_writtenrev_id}", json=payload)
        if resp.status_code == 200:
            st.success("Review updated successfully!")
        else:
            st.error(f"Failed to update review: {resp.text}")
    except Exception as e:
        st.error(f"Error updating review: {e}")

st.divider()


# ------------------------
# Delete Review
# ------------------------
st.subheader("Delete Review")
col1, col2 = st.columns(2)
with col1:
    delete_show_id = st.number_input("Show ID", min_value=1, key="del_show_id")
with col2:
    delete_writtenrev_id = st.number_input("Written Review ID", min_value=1, key="del_writtenrev_id")

if st.button("Delete Review", key="btn_delete_review"):
    try:
        resp = requests.delete(f"http://api:4000/sally/shows/{delete_show_id}/reviews/{delete_writtenrev_id}")
        if resp.status_code == 200:
            st.success("Review deleted successfully!")
        else:
            st.error(f"Failed to delete review: {resp.text}")
    except Exception as e:
        st.error(f"Error deleting review: {e}")

# ------------------------
# Display all Reviews
# ------------------------

st.subheader("View All Reviews")
try:
    resp = requests.get("http://api:4000/sally/reviews")
    
    if resp.status_code == 200:
        reviews_data = resp.json()
        
        if reviews_data:
            st.success(f"Found {len(reviews_data)} review entries:")
            
            # Display reviews in an organized way
            for i, review in enumerate(reviews_data, 1):
                with st.expander(f"{i}. Review ID: {review.get('writtenrevId', 'Unknown')} (User: {review.get('userId', 'Unknown')})"):
                    st.write(f"**Written Review ID:** {review.get('writtenrevId', 'N/A')}")
                    st.write(f"**User ID:** {review.get('userId', 'N/A')}")
                    st.write(f"**Show ID:** {review.get('showId', 'N/A')}")
                    st.write(f"**Rating:** {review.get('rating', 'N/A')}")
                    st.write(f"**Content:** {review.get('content', 'N/A')}")
        else:
            st.info("No reviews found.")
    else:
        st.error(f"Failed to load reviews: {resp.text}")
except Exception as e:
    st.error(f"Error loading reviews: {e}")