#!/usr/bin/env python3
"""Export a verifiable proof bundle of the current pipeline state via LlamaIndex FunctionTool."""
import subprocess
from llama_index.core.tools import FunctionTool


def _aurekai_proof_bundle_export(output_path: str = "/tmp/aurekai-proof-bundle.tar.gz") -> str:
    """Export a verifiable proof bundle of the current pipeline state"""
    out = subprocess.run(
        ["akai", "proof", "export", "--output", output_path],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


aurekai_proof_bundle_export = FunctionTool.from_defaults(fn=_aurekai_proof_bundle_export)


if __name__ == "__main__":
    print(aurekai_proof_bundle_export.call(output_path="/tmp/aurekai-proof-bundle.tar.gz"))
