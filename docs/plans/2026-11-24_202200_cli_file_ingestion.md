# 2026-11-24 CLI File & Ingestion Support Plan

> Status: 🟢 COMPLETED
> Related Subsystem: `src/chunkflow/cli.py`, `pyproject.toml`

## Objectives
- [x] Add file, directory, and stdin / JSONL ingestion support to `chunkflow.cli`
- [x] Provide CLI arguments: `--input` / `-i` (files/directories or standard input), `--format` (text/jsonl), `--query` / `-q`, `--top-k` / `-k`, `--chunk-size`, `--chunk-overlap`
- [x] Add console script entrypoint `chunkflow` in `pyproject.toml`
- [x] Add unit and end-to-end integration tests for CLI (`tests/test_cli.py`)
- [x] Verify test suite passes and update documentation / `README.md`
