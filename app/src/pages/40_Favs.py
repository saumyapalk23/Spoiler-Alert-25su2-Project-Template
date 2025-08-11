import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar navigation
SideBarLinks()

st.title("Amanda API Demo")

if st.button("Show Top 5 Most Reviewed Shows"):
    try:
        resp = requests.get('http://api:4000/admin/shows/most-reviewed')
        
        st.write(f"Status Code: {resp.status_code}")
        shows = resp.json()  # This is where the error happens
        for show in shows:
            st.write(f"{show['title']} (ID: {show['showId']}), Reviews: {show['num_reviews']}")
    except Exception as e:
        st.error(f"Failed to load shows: {e}")


if st.button("Show Top 3 Most Recent Articles"):
    try:
        resp = requests.get(f"http://api:4000/admin/articles/most-recent")
        resp.raise_for_status()
        articles = resp.json()
        for article in articles:
            st.write(f"**{article['title']}** - {article.get('content', '')[:100]}...")
    except Exception as e:
        st.error(f"Failed to load articles: {e}")

if st.button("Show Article Genres"):
    try:
        resp = requests.get(f"http://api:4000/admin/articles/genres")
        resp.raise_for_status()
        genres = resp.json()
        for g in genres:
            # Adjust key name depending on backend response
            genre_name = g.get('genre') or g.get('name') or str(g)
            st.write(f"- {genre_name}")
    except Exception as e:
        st.error(f"Failed to load genres: {e}")

st.subheader("Add a Favorite")
user_id_add = st.text_input("User ID (add favorite)", key="user_add")
fav_id_add = st.text_input("Favorite ID", key="fav_add")
show_id_add = st.text_input("Show ID", key="show_add")
actor_id_add = st.text_input("Actor ID", key="actor_add")
if st.button("Add Favorite"):
    try:
        payload = {
            "favoriteID": fav_id_add,
            "showId": show_id_add,
            "actorId": actor_id_add,
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
actor_id_del = st.text_input("Actor ID", key="actor_del")
if st.button("Remove Favorite"):
    try:
        payload = {
            "favoriteID": fav_id_del,
            "showId": show_id_del,
            "actorId": actor_id_del,
        }
        resp = requests.delete(f"http://api:4000/admin/users/{user_id_del}/favorites/", json=payload)
        if resp.status_code == 200:
            st.success("Favorite removed successfully!")
        else:
            st.error(f"Failed to remove favorite: {resp.text}")
    except Exception as e:
        st.error(f"Error removing favorite: {e}")

if st.button("Show Most Popular Reviews"):
    try:
        resp = requests.get(f"http://api:4000/admin/reviews/most-popular")
        resp.raise_for_status()
        reviews = resp.json()
        st.subheader("Most Popular Reviews")
        for r in reviews:
            st.write(f"{r['title']} (Review ID: {r['reviewId']}), Comments: {r['num_comments']}")
    except Exception as e:
        st.error(f"Failed to load popular reviews: {e}")

st.subheader("Submit Feedback")
user_id_fb = st.text_input("User ID (feedback)", key="user_fb")
fb_title = st.text_input("Feedback Title", key="fb_title")
fb_content = st.text_area("Feedback Content", key="fb_content")

if st.button("Submit Feedback"):
    try:
        payload = {
            "title": fb_title,
            "content": fb_content,
        }
        resp = requests.post(f"http://api:4000/admin/users/{user_id_fb}/feedback/", json=payload)
        if resp.status_code == 200:
            st.success("Feedback submitted successfully!")
        else:
            st.error(f"Failed to submit feedback: {resp.text}")
    except Exception as e:
        st.error(f"Error submitting feedback: {e}")
