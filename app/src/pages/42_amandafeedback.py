import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar navigation
SideBarLinks()
st.title(f"Welcome Admin {st.session_state['first_name']}.")
st.subheader("Submit Feedback")
userId = st.text_input("UserId (This must be an integer.)", key="userId")
content = st.text_area("Feedback Content", key="content")

if st.button("Submit Feedback"):
    try:
        data = {
            "content": content,
            "userId": userId,
        }
        resp = requests.post(f"http://api:4000/admin/users/{userId}/feedback/", json=data)
        if resp.status_code == 200:
            st.success("Feedback submitted successfully!")
        else:
            st.error(f"Failed to submit feedback: {resp.text}")
    except Exception as e:
        st.error(f"Error submitting feedback: {e}")

st.subheader("View All Feedback")
try:
    # Adjust this endpoint based on your API structure
    resp = requests.get("http://api:4000/admin/users/feedback")
    
    if resp.status_code == 200:
        feedback_data = resp.json()
        
        if feedback_data:
            st.success(f"Found {len(feedback_data)} feedback entries:")
            
            # Display feedback in an organized way
            for i, feedback in enumerate(feedback_data, 1):
                with st.expander(f"{i}. (User: {feedback.get('userId', 'Unknown')})"):
                    st.write(f"**User ID:** {feedback.get('userId', 'N/A')}")
                    st.write(f"**Content:** {feedback.get('content', 'N/A')}")
                    if 'createdAt' in feedback:
                        st.write(f"**Created:** {feedback['createdAt']}")
                    if 'id' in feedback:
                        st.write(f"**ID:** {feedback['id']}")
        else:
            st.info("No feedback found.")
    else:
        st.error(f"Failed to load feedback: {resp.text}")
except Exception as e:
    st.error(f"Error loading feedback: {e}")