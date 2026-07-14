from agent.vectorstore import VectorStoreHandler
from langchain_core.tools import tool


@tool
def get_context(query: str):
    """
    Based on the given query, this one helps provide context to answer the query based on previous discussions

    Inputs:
        query (:str): The user's query
    """
    store = VectorStoreHandler("./kb")
    results = store.query(query)
    return results
