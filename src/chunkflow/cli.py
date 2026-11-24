"""Command line interface for chunkflow retrieval."""
from __future__ import annotations

import argparse
import sys
from chunkflow.models import Document
from chunkflow.pipeline import RetrievalPipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ChunkFlow vector retrieval CLI")
    parser.add_argument("--query", "-q", required=True, help="Semantic search query string")
    parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of results to return")
    args = parser.parse_args(argv)

    pipeline = RetrievalPipeline()
    sample_docs = [
        Document("doc1", "Python ast module enables compilers and code transformation tools.", {"topic": "compiler"}),
        Document("doc2", "Dense vector embeddings capture semantic meaning across vector space.", {"topic": "ai"}),
        Document("doc3", "Lisp S-expressions represent code directly as data structures.", {"topic": "compiler"}),
    ]
    pipeline.ingest_batch(sample_docs)

    results = pipeline.query(args.query, top_k=args.top_k)
    print(f"Top {len(results)} matches for query '{args.query}':\n")
    for r in results:
        print(f"[{r.rank}] Score: {r.score:.4f} | ID: {r.chunk.chunk_id}")
        print(f"    Text: {r.chunk.text}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
