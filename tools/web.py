from langchain_core.tools import tool

import webbrowser
import wikipedia
import youtubesearchpython


@tool
def open_webpage(web_page_url: str) -> None:
    """Given a webpage url, it opens the site on the browser"""
    webbrowser.open_new_tab(web_page_url)


@tool
def open_wiki_page(wiki_title: str) -> str:
    """Given a topic on wikipedia, returns its summary"""
    return wikipedia.summary(wiki_title)


@tool
def open_youtube_video(title: str):
    """Based on the video title/search query, it returns the url of the first video"""
    query_search = youtubesearchpython.VideosSearch(title, limit=1)
    url = query_search.result()["result"]["link"]
    webbrowser.open(url)
