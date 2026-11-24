"""Unit and functional tests for ChunkFlow CLI."""
from __future__ import annotations

import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from chunkflow.cli import (
    build_parser,
    load_documents_from_jsonl,
    load_documents_from_path,
    load_documents_from_text_file,
    main,
)


class TestCli(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_load_documents_from_text_file(self) -> None:
        sample_file = self.temp_path / "sample.txt"
        sample_file.write_text("Hello world text content for testing.", encoding="utf-8")
        docs = load_documents_from_text_file(sample_file)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].doc_id, "sample.txt")
        self.assertEqual(docs[0].content, "Hello world text content for testing.")
        self.assertEqual(docs[0].metadata.get("source"), str(sample_file))

    def test_load_documents_from_jsonl(self) -> None:
        jsonl_content = (
            '{"id": "doc_1", "text": "First chunkflow line", "metadata": {"tag": "a"}}\n'
            '{"doc_id": "doc_2", "content": "Second chunkflow line", "metadata": {"tag": "b"}}\n'
            '{"text": "Third line with auto id"}\n'
        )
        stream = io.StringIO(jsonl_content)
        docs = load_documents_from_jsonl(stream)
        self.assertEqual(len(docs), 3)
        self.assertEqual(docs[0].doc_id, "doc_1")
        self.assertEqual(docs[0].content, "First chunkflow line")
        self.assertEqual(docs[0].metadata["tag"], "a")

        self.assertEqual(docs[1].doc_id, "doc_2")
        self.assertEqual(docs[1].content, "Second chunkflow line")

        self.assertEqual(docs[2].doc_id, "jsonl_doc_3")
        self.assertEqual(docs[2].content, "Third line with auto id")

    def test_load_documents_from_path_directory(self) -> None:
        sub_dir = self.temp_path / "sub"
        sub_dir.mkdir()
        (sub_dir / "doc1.txt").write_text("Sub document one", encoding="utf-8")
        (sub_dir / "doc2.md").write_text("# Markdown Title\nSub document two", encoding="utf-8")
        (sub_dir / "data.jsonl").write_text('{"id": "j1", "content": "JSONL content"}\n', encoding="utf-8")
        (sub_dir / "ignored.bin").write_text("binary", encoding="utf-8")

        docs = load_documents_from_path(str(self.temp_path))
        self.assertEqual(len(docs), 3)
        doc_ids = {d.doc_id for d in docs}
        self.assertIn("doc1.txt", doc_ids)
        self.assertIn("doc2.md", doc_ids)
        self.assertIn("j1", doc_ids)

    def test_main_default_sample_docs(self) -> None:
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            code = main(["--query", "compilers", "-k", "2"])
            self.assertEqual(code, 0)
            output = fake_out.getvalue()
            self.assertIn("Top 2 matches for query 'compilers':", output)
            self.assertIn("[1] Score:", output)

    def test_main_with_file_input(self) -> None:
        test_file = self.temp_path / "compilers.txt"
        test_file.write_text("Compilers convert source code to bytecode or machine instructions.", encoding="utf-8")

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            code = main(["-q", "bytecode compilation", "-i", str(test_file)])
            self.assertEqual(code, 0)
            output = fake_out.getvalue()
            self.assertIn("compilers.txt#chunk_0", output)
            self.assertIn("Compilers convert source code", output)

    def test_main_with_stdin_text(self) -> None:
        stdin_content = "Linear algebra and matrix decompositions form the backbone of vector algorithms."
        with patch("sys.stdin", new=io.StringIO(stdin_content)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                code = main(["-q", "linear algebra", "-i", "-"])
                self.assertEqual(code, 0)
                output = fake_out.getvalue()
                self.assertIn("stdin#chunk_0", output)
                self.assertIn("Linear algebra and matrix", output)

    def test_main_with_stdin_jsonl(self) -> None:
        stdin_jsonl = '{"id": "doc_algebra", "text": "Linear algebra and vector spaces."}\n'
        with patch("sys.stdin", new=io.StringIO(stdin_jsonl)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                code = main(["-q", "vector spaces", "-i", "-", "--format", "jsonl"])
                self.assertEqual(code, 0)
                output = fake_out.getvalue()
                self.assertIn("doc_algebra#chunk_0", output)


if __name__ == "__main__":
    unittest.main()
