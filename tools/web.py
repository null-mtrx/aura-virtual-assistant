from langchain_core.tools import tool

import webbrowser
import wikipedia


@tool
def open_webpage(web_page_url: str) -> None:
    """Given a webpage url, it opens the site on the browser"""
    webbrowser.open_new_tab(web_page_url)


@tool
def open_wiki_page(wiki_title: str) -> str:
    """Given a topic on wikipedia, returns its summary"""
    return wikipedia.summary(wiki_title)
