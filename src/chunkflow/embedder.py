"""Vector embeddings and distance calculations."""
from __future__ import annotations

import hashlib
import numpy as np
from typing import List


class DeterministicEmbedder:
    """Produces deterministic normalized dense embedding vectors from text.
    
    Uses SHA-256 seed hashing to produce realistic, reproducible unit vectors
    across fixed dimensions without requiring an external heavy LLM model download.
    """

    def __init__(self, dimension: int = 64) -> None:
        self.dimension = dimension

    def embed_text(self, text: str) -> np.ndarray:
        # Generate pseudo-random vector seeded by string hash
        cleaned = text.strip().lower()
        hasher = hashlib.sha256(cleaned.encode("utf-8"))
        seed = int.from_bytes(hasher.digest()[:8], "big") % (2**32)
        rng = np.random.default_rng(seed)

        vec = rng.standard_normal(self.dimension).astype(np.float32)
        norm = np.linalg.norm(vec)
        if norm > 1e-12:
            vec /= norm
        return vec

    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        return [self.embed_text(t) for t in texts]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    dot = float(np.dot(a, b))
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a < 1e-12 or norm_b < 1e-12:
        return 0.0
    return dot / (norm_a * norm_b)


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))
