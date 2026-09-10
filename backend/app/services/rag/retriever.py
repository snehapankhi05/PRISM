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
        *,
        top_k: int = 5,
    ) -> list[RetrievalResult]:

        if not query.strip():
            return []

        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        query_embedding = self.embedding_provider.embed_query(query)

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = result.get("documents", [[]])[0]
        ids = result.get("ids", [[]])[0]
        distances = result.get("distances", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        return [
            RetrievalResult(
                chunk_id=chunk_id,
                content=content,
                source_reference=metadata.get(
                    "source_reference",
                    "",
                ),
                score=distance,
                metadata=metadata,
            )
            for chunk_id, content, distance, metadata in zip(
                ids,
                documents,
                distances,
                metadatas,
            )
        ]