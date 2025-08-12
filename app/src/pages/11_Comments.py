import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Comments")

# Create Comment
st.subheader("Create New Comment")
col1, col2 = st.columns(2)
with col1:
    review_id_comment = st.number_input("Review ID", min_value=1, key="review_comment")
    user_id_comment = st.number_input("User ID", min_value=1, key="user_comment")
with col2:
    pass

comment_content = st.text_area("Comment Content", key="comment_content")

if st.button("Create Comment"):
    try:
        payload = {
            "userID": user_id_comment,
            "content": comment_content
        }
        resp = requests.post(
            f"http://api:4000/john/reviews/{review_id_comment}/comments",
            json=payload
        )
        if resp.status_code == 201:
            result = resp.json()
            st.success(f"Comment created successfully! Comment ID: {result.get('writtencomID')}")
        else:
            st.error(f"Failed to create comment: {resp.text}")
    except Exception as e:
        st.error(f"Error creating comment: {e}")

# Update Comment
st.subheader("Update Comment")
col1, col2 = st.columns(2)
with col1:
    review_id_update = st.number_input("Review ID", min_value=1, key="review_id_update")
    user_id_update   = st.number_input("User ID", min_value=1, key="user_update")
with col2:
    comment_id_update = st.number_input("Comment ID", min_value=1, key="comment_id_update")

update_content = st.text_area("New Comment Content", key="update_comment_content")
if st.button("Update Comment"):
    try:
        payload = {
            "writtencomID": int(comment_id_update), 
            "userID": int(user_id_update),           
            "content": update_content                
        }
        resp = requests.put(
            f"http://api:4000/john/reviews/{int(review_id_update)}/comments",
            json=payload
        )
        if resp.status_code == 200:
            st.success("Comment updated successfully!")
        elif resp.status_code == 404:
            st.error("Comment not found or you're not authorized to update it.")
        else:
            st.error(f"Failed to update comment: {resp.text}")
    except Exception as e:
        st.error(f"Error updating comment: {e}")

# Delete comment 
st.subheader("Delete Comment")
col1, col2 = st.columns(2)
with col1:
    review_id_delete_comment = st.number_input("Review ID", min_value=1, key="review_id_delete_comment")
with col2:
    user_id_delete_comment = st.number_input("User ID", min_value=1, key="user_delete_comment")

comment_id_delete = st.number_input("Comment ID", min_value=1, key="comment_id_delete")

if st.button("Delete Comment"):
    try:
        payload = {
            "userID": int(user_id_delete_comment),
            "writtencomID": int(comment_id_delete)
        }
        resp = requests.delete(
            f"http://api:4000/john/reviews/{int(review_id_delete_comment)}/comments",
            json=payload
        )
        if resp.status_code == 200:
            st.success("Comment deleted successfully!")
        elif resp.status_code == 404:
            st.error("Comment not found or you're not authorized to delete it.")
        else:
            st.error(f"Failed to delete comment: {resp.text}")
    except Exception as e:
        st.error(f"Error deleting comment: {e}")