"""In-memory vector index with metadata filtering."""
from __future__ import annotations

from typing import Any

import numpy as np

from chunkflow.embedder import cosine_similarity
from chunkflow.models import Chunk, QueryResult, SearchFilter


class VectorIndex:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self._doc_map: dict[str, list[Chunk]] = {}

    def add_chunk(self, chunk: Chunk) -> None:
        if chunk.embedding is None:
            raise ValueError(f"Chunk '{chunk.chunk_id}' has no embedding vector.")
        self.chunks.append(chunk)
        if chunk.doc_id not in self._doc_map:
            self._doc_map[chunk.doc_id] = []
        self._doc_map[chunk.doc_id].append(chunk)

    def add_chunks(self, chunks: list[Chunk]) -> None:
        for chunk in chunks:
            self.add_chunk(chunk)

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 5,
        filters: list[SearchFilter] | None = None,
    ) -> list[QueryResult]:
        candidates = self.chunks

        # Apply metadata filters
        if filters:
            for flt in filters:
                candidates = [
                    c for c in candidates if c.metadata.get(flt.key) == flt.value
                ]

        scored: list[tuple[float, Chunk]] = []
        for chunk in candidates:
            if chunk.embedding is None:
                continue
            sim = cosine_similarity(query_vector, chunk.embedding)
            scored.append((sim, chunk))

        # Sort descending by score
        scored.sort(key=lambda x: x[0], reverse=True)

        results: list[QueryResult] = []
        for rank, (score, chunk) in enumerate(scored[:top_k], start=1):
            results.append(QueryResult(chunk=chunk, score=score, rank=rank))

        return results

    def get_by_document(self, doc_id: str) -> list[Chunk]:
        return list(self._doc_map.get(doc_id, []))

    def count(self) -> int:
        return len(self.chunks)
