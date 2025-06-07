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
        st.caption(post['snippet'])
        st.divider()
