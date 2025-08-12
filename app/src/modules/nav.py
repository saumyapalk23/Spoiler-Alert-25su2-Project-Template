# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Filmmaker Role ------------------------
def SallyHome():
    st.sidebar.page_link(
        "pages/33_sally.py", label="Sally's Homepage", icon="👤"
    )

def ReviewsAndRatings():
    st.sidebar.page_link(
        "pages/00_sally_ratings.py", label="Reviews and Ratings", icon="👤"
    )

def Watchlists():
    st.sidebar.page_link(
        "pages/01_sally_watchlists.py", label="Watchlists", icon="🏦"
    )

def Follows():
    st.sidebar.page_link("pages/02_sally_follows.py", label="Follows", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ShowSearch():
    st.sidebar.page_link("pages/12_ShowSearch.py", label="Search for shows", icon="🔎")


def Comments():
    st.sidebar.page_link(
        "pages/11_Comments.py", label="Comments", icon="💬"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")


def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )
def Favorites():
    st.sidebar.page_link(
        "pages/40_amanda.py", label="Favs", icon="❤️"
    )

def Rankings():
    st.sidebar.page_link(
        "pages/46_alexreviews.py", label="Reviews", icon="💌"
    )
def Reviews():
    st.sidebar.page_link(
        "pages/47_alexrankings.py", label="Rankings", icon="⭐"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "filmmaker":
            SallyHome()
            ReviewsAndRatings()
            Watchlists()
            Follows()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "viewer":
            Comments()
            ShowSearch()
            ClassificationNav()
            NgoDirectoryNav()
            AddNgoNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "analyst":
            Rankings()
            Reviews()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")