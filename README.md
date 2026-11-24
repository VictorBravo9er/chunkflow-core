# chunkflow-core

A high-performance text chunking, dense vector embedding, and semantic retrieval pipeline engine in Python.

Designed for AI/LLM retrieval workflows (RAG), featuring sliding-window chunkers, dense vector embeddings with cosine distance calculation, metadata filtering, in-memory vector indices, and retrieval pipelines.

Detailed architectural diagrams and subsystem contracts are documented in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 1. Installation & Environment Setup

`chunkflow-core` requires Python 3.10+ and NumPy.

```bash
# Clone and enter the repository
cd chunkflow-core

# Install dependencies (e.g. using pip or uv)
pip install -e .
```

To run with the local Python runtime directly:
```bash
PYTHONPATH=src python3.14 -m unittest discover tests
```

---

## 2. Quickstart Tutorial

### Basic Ingestion & Retrieval Pipeline

```python
from chunkflow.models import Document, SearchFilter
from chunkflow.pipeline import RetrievalPipeline
from chunkflow.chunker import SlidingWindowChunker
from chunkflow.embedder import DeterministicEmbedder
from chunkflow.index import VectorIndex

# 1. Initialize pipeline components
pipeline = RetrievalPipeline(
    chunker=SlidingWindowChunker(chunk_size=50, chunk_overlap=10),
    embedder=DeterministicEmbedder(dimension=64),
    index=VectorIndex()
)

# 2. Prepare documents with metadata
docs = [
    Document(
        doc_id="doc_compiler",
        content="Abstract syntax trees and bytecode compilation optimize runtime execution.",
        metadata={"category": "engineering", "topic": "compilers"}
    ),
    Document(
        doc_id="doc_rag",
        content="Retrieval augmented generation retrieves relevant chunks from a vector database.",
        metadata={"category": "ai", "topic": "rag"}
    )
]

# 3. Ingest documents into index
pipeline.ingest_batch(docs)

# 4. Perform semantic search
results = pipeline.query("vector search and retrieval", top_k=2)

for r in results:
    print(f"Rank {r.rank} (Score: {r.score:.4f}) - Doc: {r.chunk.doc_id}")
    print(f"Text: {r.chunk.text}\n")
```

---

## 3. Metadata Filtering

You can restrict queries using `SearchFilter`:

```python
from chunkflow.models import SearchFilter

filters = [SearchFilter(key="category", value="ai")]

results = pipeline.query(
    query_text="vector database",
    top_k=5,
    filters=filters
)

for r in results:
    assert r.chunk.metadata["category"] == "ai"
```

---

## 4. Chunking Strategies

### Sliding Window Chunker

Ideal for fixed-token context windows with continuous boundary overlap:

```python
from chunkflow.chunker import SlidingWindowChunker
from chunkflow.models import Document

chunker = SlidingWindowChunker(chunk_size=100, chunk_overlap=20)
doc = Document("doc1", "long text passage goes here ...")
chunks = chunker.chunk_document(doc)

for c in chunks:
    print(f"{c.chunk_id}: {c.token_count} words ({c.char_offset_start}..{c.char_offset_end})")
```

### Sentence Boundary Chunker

Ideal for preserving natural linguistic context:

```python
from chunkflow.chunker import SentenceBoundaryChunker
from chunkflow.models import Document

chunker = SentenceBoundaryChunker(max_words_per_chunk=120)
doc = Document("doc2", "First sentence. Second sentence! Third sentence?")
chunks = chunker.chunk_document(doc)
```

---

## 5. Using the CLI

`chunkflow-core` provides a command-line interface for querying custom documents or sample documents:

```bash
# Query sample documents (default fallback)
chunkflow --query "compilers and syntax" --top-k 2

# Query single or multiple files or directories
chunkflow -q "retrieval augmented generation" -i README.md -i docs/

# Pipe content from standard input (text)
cat doc.txt | chunkflow -q "vector search" -i -

# Pipe JSONL stream from standard input
cat stream.jsonl | chunkflow -q "semantic similarity" -i - --format jsonl
```

Command-line flags:
- `--query`, `-q` *(required)*: Query string to embed and search.
- `--input`, `-i` *(optional, repeatable)*: Path to file(s), directory, or `-` for stdin.
- `--format` *(optional, default: `auto`)*: Format for input (`auto`, `text`, `jsonl`).
- `--top-k`, `-k` *(optional, default: 3)*: Maximum number of ranked results to return.
- `--chunk-size` *(optional, default: 100)*: Sliding window chunk size in words.
- `--chunk-overlap` *(optional, default: 20)*: Word overlap between adjacent chunks.

---

## 6. Architecture & Subsystems

```text
chunkflow-core/
├── src/
│   └── chunkflow/
│       ├── __init__.py      # Package entry points
│       ├── models.py        # Document, Chunk, SearchFilter, QueryResult
│       ├── chunker.py       # Sliding-window & sentence chunkers
│       ├── embedder.py      # Vector embedder with cosine math
│       ├── index.py         # In-memory vector index with metadata filters
│       ├── pipeline.py      # End-to-end RAG orchestrator
│       └── cli.py           # Command-line interface
└── tests/
    ├── test_chunker.py      # Chunking overlap & sentence boundary tests
    ├── test_embedder.py     # Vector normalization and cosine distance
    └── test_pipeline.py     # End-to-end ingest and semantic search
```

For comprehensive architecture specs, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 7. Running Tests

```bash
PYTHONPATH=src python3.14 -m unittest discover tests
```
