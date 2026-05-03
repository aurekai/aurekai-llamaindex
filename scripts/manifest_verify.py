#!/usr/bin/env python3
"""Verify an Aurekai manifest against the deploy schema via LlamaIndex FunctionTool."""
import subprocess
from llama_index.core.tools import FunctionTool


def _aurekai_manifest_verify(manifest_path: str = "artifact.json") -> str:
    """Verify an Aurekai manifest against the deploy schema"""
    out = subprocess.run(
        ["akai", "verify", "--manifest", manifest_path, "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


aurekai_manifest_verify = FunctionTool.from_defaults(fn=_aurekai_manifest_verify)


if __name__ == "__main__":
    print(aurekai_manifest_verify.call(manifest_path="artifact.json"))
