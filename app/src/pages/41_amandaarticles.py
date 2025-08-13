import streamlit as st
import requests
from modules.nav import SideBarLinks


# Initialize sidebar navigation
SideBarLinks()
st.title(f"Welcome Admin {st.session_state['first_name']}.")


if st.button("Show Most Popular Reviews"):
    try:
        resp = requests.get(f"http://api:4000/admin/reviews/most-popular")
        reviews = resp.json()
        st.subheader("Most Popular Reviews")
        for r in reviews:
            st.write(f"**Show: {r['title']}**, Review ID: {r['writtenrevId']}, Content: {r['content']}, Comments: {r['num_comments']}")
    except Exception as e:
        st.error(f"Failed to load popular reviews: {e}")


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
        articles = resp.json()
        for article in articles:
            st.write(f"**{article['title']}** - {article.get('content', '')[:100]}...")
    except Exception as e:
        st.error(f"Failed to load articles: {e}")


if st.button("Show Article Genres for 3 Most Recent Articles"):
    try:
        resp = requests.get("http://api:4000/admin/articles/most-recent/genres")
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
