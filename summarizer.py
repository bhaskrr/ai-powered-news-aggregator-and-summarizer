# import libraries and modules
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set the GROQ_API_KEY environment variable
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

@st.cache_resource(show_spinner=False)
def get_chain():
    """
    Initializes and returns a chain for summarizing news articles using ChatGroq.

    This function sets up a ChatGroq client with a specified model and defines a
    prompt template for summarizing articles for different personas. The output
    is structured in JSON format with the keys: title and summary.

    Returns:
        A chain object that can be used to summarize articles.
    """
    # Initialize the ChatGroq client with the specified model
    client = ChatGroq(model="llama-3.3-70b-versatile")

    # Define the prompt template for summarizing news articles
    prompt = ChatPromptTemplate.from_messages(
        messages=[
            (
                "system",
                "You are a news bot that summarizes news for different personas.\
                Summarize the given news articles individually for the {persona} persona.\
                Structure the output in a json format with the keys: title and summary. Output only the json.",
            ),
            (
                "user",
                "{articles}",
            ),
        ],
    )

    # Create a chain by combining the prompt template and the client
    chain = prompt | client
    return chain

@st.cache_resource(show_spinner=False)
def summarize_news(articles: list[str], persona: str) -> list[str]:
    """
    Summarize the given news articles for the specified persona.

    Args:
        articles (list[str]): List of news articles to summarize.
        persona (str): The persona for which to summarize the articles.

    Returns:
        list[str]: List of summaries for the given articles.
    """
    return get_chain().invoke({"articles": articles, "persona": persona})
