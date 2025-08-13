import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Comments")

# Create Comment
st.subheader("Create New Comment")
col1, col2 = st.columns(2)
with col1:
    user_id_comment = st.number_input("User ID", min_value=1, key="user_comment")
with col2:
    pass

comment_content = st.text_area("Comment Content", key="comment_content")

review_id_comment = st.number_input("Review ID", min_value=1, key="review_comment")

if st.button("Create Comment"):
    try:
        payload = {
            "userID": user_id_comment,
            "content": comment_content
        }
        
        url = f"http://api:4000/john/reviews/{int(review_id_comment)}/comments"
        response = requests.post(url, json=payload)
        
        if response.status_code == 201:
            result = response.json()
            st.success(f"Comment created successfully! Comment ID: {result.get('writtencomID')}")
        else:
            st.error(f"Failed to create comment: {response.text}")
    except Exception as e:
        st.error(f"Error creating comment: {e}")
# Update Comment
st.subheader("Update Comment")
col1, col2 = st.columns(2)
with col1:
    review_id_update = st.number_input("Review ID", min_value=1, key="review_id_update")
    user_id_update   = st.number_input("User ID",   min_value=1, key="user_update")
with col2:
    comment_id_update = st.number_input("Comment ID", min_value=1, key="comment_id_update")

update_content = st.text_area("New Comment Content", key="update_comment_content")

if st.button("Update Comment"):
    try:
        if not str(update_content).strip():
            st.error("Content cannot be empty.")
        else:
            url = (
                f"http://api:4000/john/reviews/"
                f"{int(review_id_update)}/comments/{int(comment_id_update)}"
            )

            payload = {
                "userID": int(user_id_update),
                "content": str(update_content).strip()
            }

            response = requests.put(url, json=payload, timeout=10)

            if response.status_code == 200:
                st.success("Comment updated successfully!")
            elif response.status_code == 404:
                st.error("Comment not found for this review or you don't own it.")
            else:
                st.error(f"Failed to update comment: {response.text}")
    except Exception as e:
        st.error(f"Error updating comment: {e}")

# Delete comment 
st.subheader("Delete Comment")
col1, col2 = st.columns(2)
with col1:
    review_id_delete_comment = st.number_input("Review ID", min_value=1, key="review_id_delete_comment")
    user_id_delete_comment = st.number_input("User ID",   min_value=1, key="user_delete_comment")
with col2:
    comment_id_delete = st.number_input("Comment ID", min_value=1, key="comment_id_delete")

if st.button("Delete Comment"):
    try:
        payload = {
            "userID": int(user_id_delete_comment)
        }
        url = (
            f"http://api:4000/john/reviews/"
            f"{int(review_id_delete_comment)}/comments/{int(comment_id_delete)}"
        )
        response = requests.delete(url, json=payload, timeout=10)

        if response.status_code == 200:
            st.success("Comment deleted successfully!")
        elif response.status_code == 404:
            st.error("Comment not found or you're not authorized to delete it.")
        else:
            st.error(f"Failed to delete comment: {response.text}")
    except Exception as e:
        st.error(f"Error deleting comment: {e}")

# display comment activity 
st.subheader("Comment Activity")

user_id = st.session_state.get("user_id")
user_id = user_id or st.number_input("User ID", min_value=1, value=1, step=1)

try:
    url = f"http://api:4000/john/users/{int(user_id)}/comments/activity"
    r = requests.get(url)

    if r.status_code != 200:
        st.error(f"API error {r.status_code}")
    else:
        events = r.json() or []
        if not events:
            st.info("No comment activity yet.")
        else:
            for ev in events:
                action = (ev.get("action") or "").lower()
                if action not in ("created", "updated"):
                    continue
                header = f"{action.upper()} comment #{ev.get('commentId','?')} review #{ev.get('reviewId','?')}"
                with st.expander(header):
                    st.write(f"By user {ev.get('userId','?')} at {ev.get('activityAt','?')}")
                    st.write("Content:")
                    st.code(ev.get("content",""))
except Exception as e:
    st.error(f"Failed to load: {e}")