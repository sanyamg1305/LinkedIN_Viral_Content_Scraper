import streamlit as st
from scraper import fetch_linkedin_posts

st.set_page_config(page_title="LinkedIn Viral Content Scraper", layout="wide")
st.title("LinkedIn Viral Content Scraper")

# Input for topics
topics_input = st.text_area(
    "Enter topics (one per line):",
    "B2B Lead generation\nCold outreach\nLinkedIn newsletters",
    height=100
)

if st.button("Fetch Posts"):
    topics = [topic.strip() for topic in topics_input.split('\n') if topic.strip()]
    
    with st.spinner("Fetching posts..."):
        posts = fetch_linkedin_posts(topics)
        
        if posts:
            st.success(f"Found {len(posts)} unique posts!")
            
            for post in posts:
                with st.container():
                    st.markdown("---")
                    st.markdown(f"### {post['title']}")
                    st.markdown(f"**Topic:** {post['topic']}")
                    st.markdown(f"**Link:** {post['link']}")
                    st.markdown(f"**Snippet:** {post['snippet']}")
                    if post['post_id']:
                        st.markdown(f"**Post ID:** {post['post_id']}")
        else:
            st.error("No posts found. Please try different topics.")