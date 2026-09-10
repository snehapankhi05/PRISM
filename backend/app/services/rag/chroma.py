import chromadb


class ChromaVectorStore:
    def __init__(self, path: str = "data/chroma"):
        self.client = chromadb.PersistentClient(path=path)

    def get_or_create_collection(self, name: str):
        return self.client.get_or_create_collection(name=name)