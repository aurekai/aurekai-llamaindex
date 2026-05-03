#!/usr/bin/env python3
"""Run the release gate check for the given version via LlamaIndex FunctionTool."""
import subprocess
from llama_index.core.tools import FunctionTool


def _aurekai_release_gate(version: str = "0.8.0-alpha.4") -> str:
    """Run the release gate check for the given version"""
    out = subprocess.run(
        ["akai", "release", "gate", "--version", version, "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


aurekai_release_gate = FunctionTool.from_defaults(fn=_aurekai_release_gate)


if __name__ == "__main__":
    print(aurekai_release_gate.call(version="0.8.0-alpha.4"))
