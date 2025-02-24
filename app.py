# Import libraries and modules
import json
import streamlit as st
from get_articles import main
from CONSTANTS import SOURCES, TECHCRUNCH_TOPICS, PERSONAS
from summarizer import summarize_news

# Set the title with an emoji for a modern look
st.title("📰 AI-powered News Aggregator")
st.subheader("Summarized news tailored for targeted personas")

# Sidebar UI enhancements
st.sidebar.title("🔍 Filter News")
st.sidebar.markdown("---")  # Add a separator for better UI

# Select news source
source = st.sidebar.selectbox("🗞️ Select a News Source", options=SOURCES)

# Select topic and persona
category = st.sidebar.selectbox("📌 Select a topic", options=TECHCRUNCH_TOPICS.keys())
persona = st.sidebar.selectbox("🎭 Select a persona", options=PERSONAS)

# Add some spacing
st.sidebar.markdown("###")

# Submit button with better spacing
submit_button = st.sidebar.button("🚀 Fetch News", type="primary")


# Function to display summarized news
# @st.cache_resource(show_spinner=False)
def display_summarized_news(links, summaries):
    for link, news_object in zip(links, summaries):
        with st.expander(f"**{news_object['title']}**"):
            st.markdown(f"📄 *{news_object['summary']}*")
            st.link_button("🔗 Read Full Article", link)


# Handle submit button click
if submit_button:
    if category is not None and persona is not None:
        with st.spinner("Aggregating and summarizing news..."):
            try:
                links, articles = main(category, persona)
                response = summarize_news(articles, persona)
                summaries = json.loads(response.content)

                # Display summaries in a structured format
                if summaries:
                    st.success("✅ News loaded successfully!")
                    display_summarized_news(links, summaries)
                else:
                    st.warning("⚠️ No news found for this selection.")

            except Exception as e:
                st.error(f"❌ Error fetching news: {str(e)}")
    else:
        st.warning("⚠️ Please select a topic and persona.")
