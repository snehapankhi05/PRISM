from backend.app.services.rag.base import RetrievalResult, Retriever


class ChromaRetriever(Retriever):
    def __init__(
        self,
        vector_store,
        embedding_provider,
        collection_name: str = "prism_documents_v1",
    ):
        self.collection = vector_store.get_or_create_collection(
            collection_name
        )
        self.embedding_provider = embedding_provider

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        source_id: str | None = None,
    ) -> list[RetrievalResult]:

        query_embedding = self.embedding_provider.embed_query(query)

        where = {"source_id": source_id} if source_id else None

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        return [
           RetrievalResult(
            chunk_id=metadata.get("source_reference", ""),
            content=document,
            source_reference=metadata.get("source_reference", ""),
            score=distance,
            metadata=metadata,
        )
            for document, metadata, distance in zip(
                documents,
                metadatas,
                distances,
            )
        ]