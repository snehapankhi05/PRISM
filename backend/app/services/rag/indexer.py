from backend.app.services.ingestion.document import NormalizedDocument

from backend.app.services.rag.base import EmbeddingProvider
from backend.app.services.rag.chroma import ChromaVectorStore


class RAGIndexer:
    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: ChromaVectorStore,
        collection_name: str = "prism_documents_v1",
    ):
        self.embedding_provider = embedding_provider
        self.collection = vector_store.get_or_create_collection(
            collection_name
        )

    def index(self, document: NormalizedDocument) -> None:
        if not document.sections:
            return

        contents = [
            section.content
            for section in document.sections
        ]

        embeddings = self.embedding_provider.embed(contents)

        ids = [
            section.section_id
            for section in document.sections
        ]

        metadatas = [
            {
                "source_reference": section.source_reference,
                "source_type": document.source_type,
                "title": document.title or "",
            }
            for section in document.sections
        ]

        self.collection.upsert(
            ids=ids,
            documents=contents,
            embeddings=embeddings,
            metadatas=metadatas,
        )