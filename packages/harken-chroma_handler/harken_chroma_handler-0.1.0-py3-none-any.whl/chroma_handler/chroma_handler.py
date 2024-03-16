import uuid
from typing import Literal

try:
    import chromadb
    from chromadb.utils import embedding_functions
    from chromadb import Collection, EmbeddingFunction, QueryResult, GetResult, Settings
except:
    import sys

    import pysqlite3

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
    import chromadb
    from chromadb.utils import embedding_functions
    from chromadb import Collection, EmbeddingFunction, QueryResult, GetResult, Settings


class ChromaIndex:
    def __init__(
            self,
            persist_directory: str | None = None,
            embedding_function: EmbeddingFunction | None = None,
            host: str | None = None,
            port: int | None = None,
            distance: str = "cosine"
    ) -> None:
        self.persist_directory = persist_directory
        self.host = host
        self.port = port
        self.distance = distance

        self.embedding_function = embedding_function
        if self.host and self.port:
            self.client = chromadb.HttpClient(host=self.host, port=self.port,
                                              settings=Settings(anonymized_telemetry=False))
        elif self.persist_directory:
            self.client = chromadb.PersistentClient(path=self.persist_directory,
                                                    settings=Settings(anonymized_telemetry=False))
        else:
            raise Exception("You must define (host,port) or directory for you Chroma DB")

    def create_collection(self, name: str, description: str = ""):
        self.client.heartbeat()
        id = self.client.create_collection(
            name=name,
            embedding_function=self.embedding_function,
            get_or_create=True,
            metadata={
                "name": name,
                "description": description,
                "hnsw:space": self.distance,
            },
        )
        self.persist()
        return id

    def delete_collection(self, name: str) -> None:
        self.client.heartbeat()
        self.client.delete_collection(name=name)
        self.persist()

    def get_collection(self, name: str) -> Collection:
        self.client.heartbeat()
        collection = self.client.get_collection(name=name, embedding_function=self.embedding_function)
        return collection

    def add(self, name: str, ids: list[str], texts: list[str], embeddings: list[list[float]] | None = None,
            metadata: list[dict] | None = None):
        collection = self.get_collection(name)
        collection.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadata)
        self.persist()
        return ids

    def get(self, name: str, ids: list[str], where_condition: dict | None = None,
            where_document_condition: dict | None = None, include: list[Literal] | None = None) -> GetResult:
        if include is None:
            include = ["documents", "distances"]
        collection = self.get_collection(name)
        results = collection.get(
            ids=ids,
            where=where_condition,
            where_document=where_document_condition,
            include=include,
        )
        return results

    def upsert(self, name: str, ids: list[str], texts: list[str], embeddings: list[list[float]] | None = None,
               metadata: list[dict] | None = None):
        collection = self.get_collection(name)
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadata,
            documents=texts,
        )

    def delete(self, name: str, ids: list[str], where_condition: dict | None = None):
        collection = self.get_collection(name)
        collection.delete(
            ids=ids,
            where=where_condition
        )

    def query(self, name: str, query_texts: list[str], where_condition: dict | None = None,
              where_document_condition: dict | None = None, include: list[Literal] | None = None,
              n_results: int = 10) -> QueryResult:
        if include is None:
            include = ["documents", "distances"]
        collection = self.get_collection(name)
        retrieved_documents = collection.query(query_texts=query_texts,
                                               n_results=n_results,
                                               where=where_condition,
                                               where_document=where_document_condition,
                                               include=include)
        return retrieved_documents

    def reset_db(self) -> None:
        self.client.reset()

    def persist(self):
        try:
            self.client.persist()
        except:
            pass
