import requests
from bs4 import BeautifulSoup, SoupStrainer
from CONSTANTS import TECHCRUNCH_TOPICS
import streamlit as st

@st.cache_resource(show_spinner=False)
def fetch_article_links(category: str) -> list[str]:
    """
    Fetches article links for a given category from TechCrunch.

    Args:
        category (str): The category to fetch articles for.

    Returns:
        list[str]: A list of article links.
    """
    category_url = TECHCRUNCH_TOPICS.get(category)
    if category_url is None:
        raise ValueError(f"Invalid category: {category}")

    try:
        response = requests.get(f"https://techcrunch.com/{category_url}")
        response.raise_for_status()
        content = response.text

        # Parse the HTML content to find article links
        soup = BeautifulSoup(
            content,
            "html.parser",
            parse_only=SoupStrainer(attrs={"class": "loop-card__title-link"}),
        )
        return [anchor["href"] for anchor in soup.find_all("a", href=True)]
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

@st.cache_resource(show_spinner=False)
def fetch_article_content(link: str) -> str:
    """
    Fetches the content of an article given its link.

    Args:
        link (str): The URL of the article.

    Returns:
        str: The content of the article.
    """
    try:
        response = requests.get(link)
        response.raise_for_status()
        content = response.text

        # Parse the HTML content to find the article text
        soup = BeautifulSoup(
            content,
            "html.parser",
            parse_only=SoupStrainer(attrs={"id": "speakable-summary"}),
        )
        if soup is None:
            raise ValueError(f"Failed to parse the HTML content of {link}.")
        
        text = soup.get_text(strip=False)
        if text is None or not isinstance(text, str):
            raise ValueError(f"Failed to extract the text content of {link}.")
        
        return text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return ""

@st.cache_resource(show_spinner=False)
def main(category: str, persona: str) -> tuple[list[str], list[str]]:
    """
    Main function to fetch article links and their content for a given category.

    Args:
        category (str): The category to fetch articles for.
        persona (str): The persona for which the articles are being fetched.

    Returns:
        tuple[list[str], list[str]]: A tuple containing a list of article links and their content.
    """
    links = fetch_article_links(category)
    article_content = [fetch_article_content(link) for link in links[:10]]
    return links, article_content