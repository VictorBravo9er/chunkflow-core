"""End-to-end ingestion and semantic retrieval pipeline."""
from __future__ import annotations

from typing import List, Optional
from chunkflow.models import Document, Chunk, QueryResult, SearchFilter
from chunkflow.chunker import SlidingWindowChunker
from chunkflow.embedder import DeterministicEmbedder
from chunkflow.index import VectorIndex


class RetrievalPipeline:
    def __init__(
        self,
        chunker: Optional[SlidingWindowChunker] = None,
        embedder: Optional[DeterministicEmbedder] = None,
        index: Optional[VectorIndex] = None,
    ) -> None:
        self.chunker = chunker or SlidingWindowChunker(chunk_size=100, chunk_overlap=20)
        self.embedder = embedder or DeterministicEmbedder(dimension=64)
        self.index = index or VectorIndex()

    def ingest_document(self, doc: Document) -> List[Chunk]:
        chunks = self.chunker.chunk_document(doc)
        for c in chunks:
            c.embedding = self.embedder.embed_text(c.text)
        self.index.add_chunks(chunks)
        return chunks

    def ingest_batch(self, documents: List[Document]) -> int:
        total = 0
        for doc in documents:
            chunks = self.ingest_document(doc)
            total += len(chunks)
        return total

    def query(
        self,
        query_text: str,
        top_k: int = 3,
        filters: Optional[List[SearchFilter]] = None,
    ) -> List[QueryResult]:
        query_vec = self.embedder.embed_text(query_text)
        return self.index.search(query_vec, top_k=top_k, filters=filters)
