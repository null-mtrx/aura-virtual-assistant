import chromadb

from typing import Literal


class VectorStoreHandler:
    def __init__(self, store_location):
        self.store_location = store_location
        self.chroma = chromadb.PersistentClient(path=self.store_location)
        self.collection = self.chroma.get_or_create_collection(name="knowledge-base")

    def add_to_knowledge_base(self, data: dict):
        documents = [data[entry]["content"] for entry in data]
        ids = [data[entry]["id"] for entry in data]
        metadata = [metadata for metadata in list(data.values())]

        self.collection.add(documents=documents, metadatas=metadata, ids=ids)

    def query(self, query: str, count: int = 5):
        results = self.collection.query(query_texts=query, n_results=count)
        return results["documents"]
