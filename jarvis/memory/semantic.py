from jarvis.utils.logger import JarvisLogger


class SemanticMemory:
    """Vector-ready semantic memory layer.

    Currently uses keyword-based search via SQLite.
    Architecture prepared for ChromaDB/Qdrant integration.
    """

    def __init__(self):
        self.logger = JarvisLogger.get_logger("memory.semantic")

    def embed(self, text: str) -> list[float]:
        self.logger.warning("Embedding not implemented - using keyword fallback")
        return []

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        self.logger.debug(f"Semantic search for: {query[:50]}...")
        return []

    def store_embedding(self, text: str, metadata: dict | None = None):
        self.logger.debug("Embedding storage not implemented")
        pass
