#!/usr/bin/env python3
"""Benchmark the Aurekai semantic cache via LlamaIndex FunctionTool."""
import subprocess
from llama_index.core.tools import FunctionTool


def _aurekai_semantic_cache_bench(queries: int = 100) -> str:
    """Benchmark the Aurekai semantic cache"""
    out = subprocess.run(
        ["akai", "cache", "bench", "--queries", str(queries), "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


aurekai_semantic_cache_bench = FunctionTool.from_defaults(fn=_aurekai_semantic_cache_bench)


if __name__ == "__main__":
    print(aurekai_semantic_cache_bench.call(queries=100))
