import streamlit as st
from scraper import fetch_linkedin_posts

st.set_page_config(page_title="LinkedIn Post Finder", layout="centered")

st.title("🔎 LinkedIn Viral Post Scraper")
topics_input = st.text_area("Enter topics (comma-separated)", "B2B Lead generation, Cold outreach, LinkedIn newsletters")

if st.button("Fetch Top Posts"):
    topics = [t.strip() for t in topics_input.split(",") if t.strip()]
    with st.spinner("Scraping..."):
        results = fetch_linkedin_posts(topics)

    st.success("Done! ✅")
    for post in results:
        st.subheader(f"🔹 {post['topic']}")
        st.markdown(f"[{post['title']}]({post['link']})")
        
        # Display engagement metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👍 Likes", f"{post['engagement']['likes']:,}")
        with col2:
            st.metric("💬 Comments", f"{post['engagement']['comments']:,}")
        with col3:
            st.metric("🔄 Shares", f"{post['engagement']['shares']:,}")
        
        st.caption(post['snippet'])
        st.divider()