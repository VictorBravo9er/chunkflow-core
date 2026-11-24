"""Command line interface for chunkflow retrieval."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import TextIO

from chunkflow.chunker import SlidingWindowChunker
from chunkflow.models import Document
from chunkflow.pipeline import RetrievalPipeline

SAMPLE_DOCS = [
    Document("doc1", "Python ast module enables compilers and code transformation tools.", {"topic": "compiler"}),
    Document("doc2", "Dense vector embeddings capture semantic meaning across vector space.", {"topic": "ai"}),
    Document("doc3", "Lisp S-expressions represent code directly as data structures.", {"topic": "compiler"}),
]


def load_documents_from_text_file(path: Path) -> list[Document]:
    """Read a plain text or markdown file as a single Document."""
    content = path.read_text(encoding="utf-8")
    return [Document(doc_id=path.name, content=content, metadata={"source": str(path)})]


def load_documents_from_jsonl(stream_or_file: TextIO | Path) -> list[Document]:
    """Load JSONL lines where each line contains at least content/text and optional doc_id and metadata."""
    lines: list[str]
    if isinstance(stream_or_file, Path):
        lines = stream_or_file.read_text(encoding="utf-8").splitlines()
    else:
        lines = stream_or_file.read().splitlines()

    docs: list[Document] = []
    for idx, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        content = data.get("content") or data.get("text")
        if not content:
            continue
        doc_id = str(data.get("id") or data.get("doc_id") or f"jsonl_doc_{idx}")
        metadata = data.get("metadata", {})
        if not isinstance(metadata, dict):
            metadata = {"meta": metadata}
        docs.append(Document(doc_id=doc_id, content=content, metadata=metadata))
    return docs


def load_documents_from_path(path_str: str) -> list[Document]:
    """Load documents from a file or recursively from a directory."""
    target = Path(path_str)
    if not target.exists():
        raise FileNotFoundError(f"Input path does not exist: {path_str}")

    if target.is_file():
        if target.suffix.lower() == ".jsonl":
            return load_documents_from_jsonl(target)
        return load_documents_from_text_file(target)

    docs: list[Document] = []
    # Recursively scan directory for readable text / markdown / jsonl files
    supported_extensions = {".txt", ".md", ".jsonl", ".py", ".rst", ".log"}
    for file_path in sorted(target.rglob("*")):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            if file_path.suffix.lower() == ".jsonl":
                docs.extend(load_documents_from_jsonl(file_path))
            else:
                docs.extend(load_documents_from_text_file(file_path))
    return docs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chunkflow",
        description="ChunkFlow vector retrieval CLI - ingest files/stdin and perform semantic search",
    )
    parser.add_argument(
        "--query",
        "-q",
        required=True,
        help="Semantic search query string",
    )
    parser.add_argument(
        "--input",
        "-i",
        action="append",
        dest="inputs",
        help="Path to a text file, markdown file, jsonl file, or directory. Can be passed multiple times. Use '-' for stdin.",
    )
    parser.add_argument(
        "--format",
        choices=["auto", "text", "jsonl"],
        default="auto",
        help="Input format (default: auto; stdin defaults to text unless --format jsonl is specified)",
    )
    parser.add_argument(
        "--output",
        "-o",
        choices=["text", "json", "jsonl"],
        default="text",
        help="Output format: 'text' (default), 'json', or 'jsonl'",
    )
    parser.add_argument(
        "--top-k",
        "-k",
        type=int,
        default=3,
        help="Number of results to return (default: 3)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=100,
        help="Word capacity per chunk for sliding window chunker (default: 100)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=20,
        help="Word overlap between adjacent chunks (default: 20)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    documents: list[Document] = []

    if args.inputs:
        for inp in args.inputs:
            if inp == "-":
                # Read from stdin
                if args.format == "jsonl":
                    documents.extend(load_documents_from_jsonl(sys.stdin))
                else:
                    content = sys.stdin.read()
                    if content.strip():
                        documents.append(Document(doc_id="stdin", content=content, metadata={"source": "stdin"}))
            else:
                documents.extend(load_documents_from_path(inp))
    else:
        # Default fallback to built-in sample documents
        documents = SAMPLE_DOCS

    if not documents:
        print("No documents loaded to query.", file=sys.stderr)
        return 1

    chunker = SlidingWindowChunker(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
    pipeline = RetrievalPipeline(chunker=chunker)
    pipeline.ingest_batch(documents)

    results = pipeline.query(args.query, top_k=args.top_k)

    if args.output == "json":
        items = [
            {
                "chunk_id": r.chunk.chunk_id,
                "score": r.score,
                "rank": r.rank,
                "text": r.chunk.text,
                "metadata": dict(r.chunk.metadata),
            }
            for r in results
        ]
        print(json.dumps(items, indent=2))
    elif args.output == "jsonl":
        for r in results:
            item = {
                "chunk_id": r.chunk.chunk_id,
                "score": r.score,
                "rank": r.rank,
                "text": r.chunk.text,
                "metadata": dict(r.chunk.metadata),
            }
            print(json.dumps(item))
    else:
        print(f"Top {len(results)} matches for query '{args.query}':\n")
        for r in results:
            print(f"[{r.rank}] Score: {r.score:.4f} | ID: {r.chunk.chunk_id}")
            print(f"    Text: {r.chunk.text}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
