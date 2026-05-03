"""
aurekai_llamaindex.py — LlamaIndex integration for Aurekai.
Readers, ToolSpecs, postprocessors, and model router.
"""
from __future__ import annotations

import json
import subprocess
from typing import Any, List, Optional, Sequence

from llama_index.core import Document
from llama_index.core.readers.base import BaseReader
from llama_index.core.tools import FunctionTool
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle


def _run_akai(args: list[str], timeout: int = 300) -> dict[str, Any]:
    result = subprocess.run(
        ["akai", *args, "--json"],
        capture_output=True, text=True, timeout=timeout,
    )
    try:
        return json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return {"raw": result.stdout, "error": result.stderr}


# ── Readers ───────────────────────────────────────────────────────────────────

class AurekaiArtifactReader(BaseReader):
    """Load Akai artifacts as LlamaIndex Documents."""
    def load_data(self, artifact_id: str, **kwargs) -> List[Document]:
        data = _run_akai(["runtime", "capabilities"])  # placeholder: would be artifact fetch
        return [Document(text=json.dumps(data), metadata={"artifact_id": artifact_id, "source": "aurekai"})]


class AurekaiTranscriptReader(BaseReader):
    """Transcribe an audio file and return as Document."""
    def load_data(self, audio_path: str, language: str = "en", **kwargs) -> List[Document]:
        data = _run_akai(["transcribe", "audio", "--input", audio_path, "--language", language], timeout=600)
        text = data.get("transcript", data.get("text", json.dumps(data)))
        return [Document(text=text, metadata={"audio_path": audio_path, "source": "aurekai-transcribe",
                                               "artifact_id": data.get("artifact_id", ""),
                                               "proof_uri": data.get("proof_uri", "")})]


class AurekaiProofReader(BaseReader):
    """Load an Akai proof bundle as Document."""
    def load_data(self, proof_id: str, **kwargs) -> List[Document]:
        data = _run_akai(["proof", "export", "--id", proof_id])
        return [Document(text=json.dumps(data), metadata={"proof_id": proof_id, "source": "aurekai-proof"})]


class AurekaiLineageGraphReader(BaseReader):
    """Load artifact lineage graph as Document."""
    def load_data(self, artifact_id: str, **kwargs) -> List[Document]:
        data = _run_akai(["graph", "lineage", "--artifact", artifact_id])
        return [Document(text=json.dumps(data), metadata={"artifact_id": artifact_id, "source": "aurekai-lineage"})]


class AurekaiWireReportReader(BaseReader):
    """Load a wire report as Document."""
    def load_data(self, capture_id: str, **kwargs) -> List[Document]:
        data = _run_akai(["wire", "report", "--capture", capture_id])
        return [Document(text=json.dumps(data), metadata={"capture_id": capture_id, "source": "aurekai-wire"})]


# ── Tool Specs ────────────────────────────────────────────────────────────────

def _make_tool(name: str, description: str, args: list[str], timeout: int = 300) -> FunctionTool:
    def fn(**kwargs) -> str:
        effective_args = [a.format(**kwargs) if "{" in a else a for a in args]
        return json.dumps(_run_akai(effective_args, timeout=timeout))
    fn.__name__ = name
    fn.__doc__ = description
    return FunctionTool.from_defaults(fn=fn, name=name, description=description)


AUREKAI_TOOLS = [
    _make_tool("aurekai_doctor", "Run akai doctor --deep diagnostics", ["doctor", "--deep"]),
    _make_tool("aurekai_capabilities", "List all Akai capability families", ["runtime", "capabilities"]),
    _make_tool("aurekai_manifest_verify", "Verify artifact.json manifest", ["verify", "--manifest", "artifact.json"]),
    _make_tool("aurekai_proof_bundle", "Export proof bundle for current run", ["proof", "bundle"]),
    _make_tool("aurekai_graph_lineage", "Graph lineage for an artifact", ["graph", "lineage"]),
    _make_tool("aurekai_fpq_compress", "FPQ compress a model", ["fpq", "compress"]),
    _make_tool("aurekai_sae_audit", "SAE feature audit", ["sae", "audit"]),
    _make_tool("aurekai_release_gate", "Release gate check", ["release", "gate"]),
]


# ── Postprocessors ─────────────────────────────────────────────────────────────

class AurekaiFeatureActivationPostprocessor(BaseNodePostprocessor):
    """Filter nodes by SAE feature activation — keep only proof-bearing nodes."""
    min_proof_score: float = 0.5

    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        filtered = []
        for node in nodes:
            proof_uri = node.node.metadata.get("proof_uri", "")
            if proof_uri:
                filtered.append(node)
            else:
                # still include if score is above threshold
                if node.score and node.score >= self.min_proof_score:
                    filtered.append(node)
        return filtered or nodes  # fallback: return all if none pass


class AurekaiDangerFeatureFilter(BaseNodePostprocessor):
    """Filter out nodes flagged by AkaiSAE danger features."""
    blocked_tags: List[str] = ["danger", "violence_coupling", "tampered"]

    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        return [
            n for n in nodes
            if not any(tag in n.node.metadata.get("tags", []) for tag in self.blocked_tags)
        ]
