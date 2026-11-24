"""Chunker unit tests."""
import unittest
from chunkflow.models import Document
from chunkflow.chunker import SlidingWindowChunker, SentenceBoundaryChunker


class TestChunkers(unittest.TestCase):
    def test_sliding_window_chunker(self):
        words = [f"word{i}" for i in range(100)]
        content = " ".join(words)
        doc = Document(doc_id="test_doc", content=content, metadata={"source": "unit_test"})

        chunker = SlidingWindowChunker(chunk_size=40, chunk_overlap=10)
        chunks = chunker.chunk_document(doc)

        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0].token_count, 40)
        self.assertEqual(chunks[0].metadata["source"], "unit_test")
        self.assertTrue(chunks[0].chunk_id.startswith("test_doc#chunk_0"))

    def test_empty_document(self):
        doc = Document(doc_id="empty", content="   ")
        chunker = SlidingWindowChunker()
        chunks = chunker.chunk_document(doc)
        self.assertEqual(len(chunks), 0)

    def test_sentence_boundary_chunker(self):
        content = "This is sentence one. This is sentence two! And this is sentence three?"
        doc = Document(doc_id="sentence_doc", content=content)
        chunker = SentenceBoundaryChunker(max_words_per_chunk=10)
        chunks = chunker.chunk_document(doc)
        self.assertGreaterEqual(len(chunks), 1)


if __name__ == "__main__":
    unittest.main()
