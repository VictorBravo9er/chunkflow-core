"""Text chunking implementations."""
from __future__ import annotations

import re

from chunkflow.models import Chunk, Document


class SlidingWindowChunker:
    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 40) -> None:
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be strictly less than chunk_size")
        self.chunk_size: int = chunk_size
        self.chunk_step: int = chunk_size - chunk_overlap

    def chunk_document(self, doc: Document) -> list[Chunk]:
        text = doc.content
        if not text.strip():
            return []

        # Tokenize by whitespace
        words = text.split()
        if not words:
            return []

        chunks: list[Chunk] = []
        idx = 0
        chunk_num = 0

        while idx < len(words):
            window_words = words[idx : idx + self.chunk_size]
            chunk_text = " ".join(window_words)

            # Approximate char offsets
            start_offset = text.find(window_words[0]) if window_words else 0
            end_offset = start_offset + len(chunk_text)

            chunk = Chunk(
                chunk_id=f"{doc.doc_id}#chunk_{chunk_num}",
                doc_id=doc.doc_id,
                text=chunk_text,
                token_count=len(window_words),
                char_offset_start=start_offset,
                char_offset_end=end_offset,
                metadata=dict(doc.metadata),
            )
            chunks.append(chunk)
            chunk_num += 1

            idx += self.chunk_step
            if idx >= len(words):
                break

        return chunks


class SentenceBoundaryChunker:
    def __init__(self, max_words_per_chunk: int = 150) -> None:
        self.max_words_per_chunk: int = max_words_per_chunk

    def chunk_document(self, doc: Document) -> list[Chunk]:
        text = doc.content
        if not text.strip():
            return []

        # Split sentences roughly by . ! ? followed by space
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks: list[Chunk] = []

        current_words: list[str] = []
        current_sentences: list[str] = []
        chunk_num = 0

        for sentence in sentences:
            sentence_words = sentence.split()
            if len(current_words) + len(sentence_words) > self.max_words_per_chunk and current_words:
                chunk_text = " ".join(current_sentences)
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc.doc_id}#sentence_chunk_{chunk_num}",
                        doc_id=doc.doc_id,
                        text=chunk_text,
                        token_count=len(current_words),
                        char_offset_start=0,
                        char_offset_end=len(chunk_text),
                        metadata=dict(doc.metadata),
                    )
                )
                chunk_num += 1
                current_words = []
                current_sentences = []

            current_sentences.append(sentence)
            current_words.extend(sentence_words)

        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}#sentence_chunk_{chunk_num}",
                    doc_id=doc.doc_id,
                    text=chunk_text,
                    token_count=len(current_words),
                    char_offset_start=0,
                    char_offset_end=len(chunk_text),
                    metadata=dict(doc.metadata),
                )
            )

        return chunks
