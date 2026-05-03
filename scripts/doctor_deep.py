#!/usr/bin/env python3
"""Run Aurekai doctor --deep and return structured diagnostics via LlamaIndex FunctionTool."""
import subprocess
from llama_index.core.tools import FunctionTool


def _aurekai_doctor_deep() -> str:
    """Run Aurekai doctor --deep and return structured diagnostics"""
    out = subprocess.run(
        ["akai", "doctor", "--deep", "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


aurekai_doctor_deep = FunctionTool.from_defaults(fn=_aurekai_doctor_deep)


if __name__ == "__main__":
    print(aurekai_doctor_deep.call())
