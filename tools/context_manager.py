from agent.vectorstore import VectorStoreHandler
from langchain_core.tools import tool

import json


@tool
def get_context(query: str):
    """
    Based on the given query, this one helps provide context to answer the query based on previous discussions

    Inputs:
        query (:str): The user's query
    """
    data = {}

    with open("config.json", "r") as file:
        data = file.read()

    vector_store_path = data["agent_dets"]["vector_store"]

    store = VectorStoreHandler(vector_store_path)
    results = store.query(query)
    return results
