"""Domain models for chunkflow text processing and retrieval."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class Document:
    doc_id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    token_count: int
    char_offset_start: int
    char_offset_end: int
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: np.ndarray | None = None


@dataclass
class SearchFilter:
    key: str
    value: Any


@dataclass
class QueryResult:
    chunk: Chunk
    score: float
    rank: int
