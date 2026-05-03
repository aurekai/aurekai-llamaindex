#!/usr/bin/env python3
"""Pack model memory artifacts for the given tag via LlamaIndex FunctionTool."""
import subprocess
from llama_index.core.tools import FunctionTool


def _aurekai_model_memory_pack(tag: str = "latest") -> str:
    """Pack model memory artifacts for the given tag"""
    out = subprocess.run(
        ["akai", "pack", "--tag", tag, "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


aurekai_model_memory_pack = FunctionTool.from_defaults(fn=_aurekai_model_memory_pack)


if __name__ == "__main__":
    print(aurekai_model_memory_pack.call(tag="latest"))
