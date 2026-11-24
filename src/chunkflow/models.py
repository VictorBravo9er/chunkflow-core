"""Domain models for chunkflow text processing and retrieval."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import numpy as np


@dataclass
class Document:
    doc_id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    token_count: int
    char_offset_start: int
    char_offset_end: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None


@dataclass
class SearchFilter:
    key: str
    value: Any


@dataclass
class QueryResult:
    chunk: Chunk
    score: float
    rank: int
