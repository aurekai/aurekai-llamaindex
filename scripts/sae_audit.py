#!/usr/bin/env python3
"""Run a Sparse Autoencoder (SAE) audit on the given model via LlamaIndex FunctionTool."""
import subprocess
from llama_index.core.tools import FunctionTool


def _aurekai_sae_audit(model_id: str = "default") -> str:
    """Run a Sparse Autoencoder (SAE) audit on the given model"""
    out = subprocess.run(
        ["akai", "sae", "audit", "--model", model_id, "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


aurekai_sae_audit = FunctionTool.from_defaults(fn=_aurekai_sae_audit)


if __name__ == "__main__":
    print(aurekai_sae_audit.call(model_id="default"))
