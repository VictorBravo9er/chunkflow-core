"""End-to-end pipeline and retrieval unit tests."""
import unittest
from chunkflow.models import Document, SearchFilter
from chunkflow.pipeline import RetrievalPipeline


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = RetrievalPipeline()
        self.docs = [
            Document("doc1", "Compiler lexers break stream of characters into recognized tokens.", {"category": "compilers"}),
            Document("doc2", "Parsers build abstract syntax trees from linear token streams.", {"category": "compilers"}),
            Document("doc3", "Dense embeddings project natural language semantics onto vector spaces.", {"category": "nlp"}),
        ]
        self.pipeline.ingest_batch(self.docs)

    def test_pipeline_search_returns_ranked_results(self):
        results = self.pipeline.query("tokens and parsers", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].rank, 1)
        self.assertGreaterEqual(results[0].score, results[1].score)

    def test_metadata_filtering(self):
        results = self.pipeline.query(
            "transformers and models",
            top_k=5,
            filters=[SearchFilter(key="category", value="nlp")],
        )
        for r in results:
            self.assertEqual(r.chunk.metadata.get("category"), "nlp")


if __name__ == "__main__":
    unittest.main()
