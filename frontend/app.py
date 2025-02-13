import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Constants
API_URL = "http://localhost:8000"


def fetch_articles():
    """Fetch analyzed articles from API"""
    response = requests.get(f"{API_URL}/articles")
    return response.json()


def create_sentiment_chart(df):
    """Create sentiment analysis chart"""
    fig = px.scatter(
        df,
        x="published_at",
        y="sentiment_score",
        color="sentiment_label",
        hover_data=["title"],
        title="Sentiment Analysis Over Time",
    )
    return fig


def create_fake_news_chart(df):
    """Create fake news probability chart"""
    fig = px.histogram(
        df,
        x="fake_news_probability",
        title="Distribution of Fake News Probability",
        nbins=20,
    )
    return fig


def main():
    st.title("News Analyzer Dashboard")

    # Sidebar controls
    st.sidebar.header("Controls")
    if st.sidebar.button("Fetch New Articles"):
        query = st.sidebar.text_input("Search Query (optional)")
        days = st.sidebar.number_input(
            "Days to fetch", min_value=1, max_value=7, value=1
        )
        requests.post(f"{API_URL}/fetch-news", params={"query": query, "days": days})
        st.sidebar.success("Fetched new articles!")

    # Main content
    try:
        # Fetch and prepare data
        articles = fetch_articles()
        if not articles:
            st.warning("No articles found. Try fetching new articles.")
            return

        df = pd.DataFrame(articles)
        df["published_at"] = pd.to_datetime(df["published_at"])

        # Display charts
        st.header("Sentiment Analysis")
        st.plotly_chart(create_sentiment_chart(df))

        st.header("Fake News Detection")
        st.plotly_chart(create_fake_news_chart(df))

        # Display articles table
        st.header("Latest Articles")
        st.dataframe(
            df[
                [
                    "title",
                    "source",
                    "sentiment_label",
                    "fake_news_probability",
                    "published_at",
                ]
            ].sort_values("published_at", ascending=False)
        )

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")


if __name__ == "__main__":
    main()
