"""Embedder and similarity math unit tests."""
import unittest
import numpy as np
from chunkflow.embedder import DeterministicEmbedder, cosine_similarity, euclidean_distance


class TestEmbedder(unittest.TestCase):
    def setUp(self):
        self.embedder = DeterministicEmbedder(dimension=32)

    def test_embedding_normalization(self):
        vec = self.embedder.embed_text("test sentence")
        self.assertEqual(vec.shape, (32,))
        norm = np.linalg.norm(vec)
        self.assertAlmostEqual(float(norm), 1.0, places=5)

    def test_reproducibility(self):
        v1 = self.embedder.embed_text("identical text")
        v2 = self.embedder.embed_text("identical text")
        np.testing.assert_array_almost_equal(v1, v2)

    def test_cosine_similarity_identical(self):
        v1 = self.embedder.embed_text("some content")
        sim = cosine_similarity(v1, v1)
        self.assertAlmostEqual(sim, 1.0, places=5)

    def test_euclidean_distance(self):
        v1 = self.embedder.embed_text("sentence A")
        v2 = self.embedder.embed_text("sentence B")
        dist = euclidean_distance(v1, v2)
        self.assertGreater(dist, 0.0)


if __name__ == "__main__":
    unittest.main()
