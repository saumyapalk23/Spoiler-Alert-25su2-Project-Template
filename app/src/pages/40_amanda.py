import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar navigation
SideBarLinks()

st.title("Amanda API Demo")

if st.button("Show Top 5 Most Reviewed Shows"):
    try:
        resp = requests.get('http://api:4000/admin/shows/most-reviewed')
        
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

if st.button("Show Article Genres for 3 Most Recent Articles"):
    try:
        resp = requests.get("http://api:4000/admin/articles/most-recent/genres")
        resp.raise_for_status()
        data = resp.json()
        genres = data.get('genres', [])
        
        if genres:
            st.write("**Genres of 3 Most Recent Articles:**")
            current_article = None
            
            for g in genres:
                article_id = g['articleID']
                article_title = g['title'] 
                created_at = g['createdAt']
                genre_title = g['genre_title']
                
                # Group by article
                if current_article != article_id:
                    if current_article is not None:
                        st.write("---")
                    st.write(f"**Article: {article_title}** (ID: {article_id})")
                    st.write(f"Created: {created_at}")
                    st.write("Genres:")
                    current_article = article_id
                
                st.write(f"  - {genre_title}")
        else:
            st.info("No recent articles with genres found")
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
if st.button("Remove Favorite"):
    try:
        payload = {
            "favoriteID": fav_id_del,
            "showId": show_id_del,
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
        reviews = resp.json()
        st.subheader("Most Popular Reviews")
        for r in reviews:
            st.write(f"{r['title']} (Review ID: {r['reviewId']}), Comments: {r['num_comments']}")
    except Exception as e:
        st.error(f"Failed to load popular reviews: {e}")
# -----------------------------------------------------------------------------
st.subheader("Submit Feedback")
userId = st.text_input("UserId (This must be an integer.)", key="userId")
title = st.text_input("Feedback Title", key="title")
content = st.text_area("Feedback Content", key="content")

if st.button("Submit Feedback"):
    try:
        data = {
            "title": title,
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
