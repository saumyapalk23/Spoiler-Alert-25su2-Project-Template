import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    
    Welcome to Spoiler Alert! We are an app dedicated to letting you enjoy and review your favorite TV shows and onstage performances.
    
     From theatregoers and casual fans to performance artists and professionals in the field, this app offers a dedicated space 
     for users to rate, review, and discuss television, plays, and musicals: mediums that are often overlooked on mainstream 
     review platforms and relegated to non-dedicated forums such as Twitter or Reddit. 
     
    Stay tuned for more information and features to come!
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
