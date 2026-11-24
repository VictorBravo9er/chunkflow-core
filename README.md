# chunkflow-core

A high-performance text chunking, vector embedding, and semantic similarity search pipeline engine in Python.

Designed for AI/LLM retrieval workflows (RAG), featuring sliding-window chunkers, dense vector embeddings with cosine distance calculation, metadata filtering, in-memory inverted & vector indices, and reranking pipelines.

## Key Subsystems

- `src/chunkflow/models.py`: Core domain data structures (`Document`, `Chunk`, `QueryResult`, `SearchFilter`).
- `src/chunkflow/chunker.py`: Sliding window, character-based, sentence-aware, and markdown-aware token chunkers with configurable overlap.
- `src/chunkflow/embedder.py`: Dense vector embedding generators (including deterministic normalized vector projection for testing and reproducible semantic search).
- `src/chunkflow/index.py`: Vector index supporting k-nearest-neighbors (k-NN) with cosine similarity, L2 distance, and metadata tag filtering.
- `src/chunkflow/pipeline.py`: End-to-end ingestion, chunking, indexing, and query retrieval pipeline.
- `src/chunkflow/cli.py`: Interactive CLI tool for indexing documents and querying the knowledge store.

## Architecture

```text
chunkflow-core/
├── src/
│   └── chunkflow/
│       ├── __init__.py      # Package entry points
│       ├── models.py        # Document, Chunk, QueryResult
│       ├── chunker.py       # Sliding-window & sentence chunkers
│       ├── embedder.py      # Vector embedder with cosine math
│       ├── index.py         # In-memory vector & inverted index
│       ├── pipeline.py      # End-to-end RAG orchestrator
│       └── cli.py           # Command-line interface
└── tests/
    ├── __init__.py
    ├── test_chunker.py      # Chunking overlap & sentence boundary tests
    ├── test_embedder.py     # Vector normalization and cosine distance
    └── test_pipeline.py     # End-to-end ingest and semantic search
```

## Running Tests

```bash
python3 -m unittest discover tests
```
