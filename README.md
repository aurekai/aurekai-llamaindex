<p align="center">
  <img src="https://raw.githubusercontent.com/aurekai/aurekai/main/assets/aurekai-logo.svg" alt="Aurekai" width="520" />
</p>

# `aurekai-llamaindex` · v0.8.0-alpha.5

Official LlamaIndex integration for Aurekai — 5 Readers, 8 FunctionTools, 2 postprocessors.

## Readers

| Reader | Description |
|---|---|
| `AurekaiArtifactReader` | Load Akai artifacts as Documents |
| `AurekaiTranscriptReader` | Transcribe audio → Document (with proof_uri metadata) |
| `AurekaiProofReader` | Load proof bundle as Document |
| `AurekaiLineageGraphReader` | Load artifact lineage graph as Document |
| `AurekaiWireReportReader` | Load wire report as Document |

## Tools

8 `FunctionTool` instances: `aurekai_doctor`, `aurekai_capabilities`, `aurekai_manifest_verify`, `aurekai_proof_bundle`, `aurekai_graph_lineage`, `aurekai_fpq_compress`, `aurekai_sae_audit`, `aurekai_release_gate`

## Postprocessors

| Postprocessor | Description |
|---|---|
| `AurekaiFeatureActivationPostprocessor` | Keep only proof-bearing nodes; fallback to score threshold |
| `AurekaiDangerFeatureFilter` | Filter out nodes tagged with SAE danger features |

## Quick Start

```python
from aurekai_llamaindex import AurekaiTranscriptReader, AUREKAI_TOOLS
from llama_index.core.agent import ReActAgent

reader = AurekaiTranscriptReader()
docs = reader.load_data("audio.wav", language="en")

agent = ReActAgent.from_tools(AUREKAI_TOOLS, verbose=True)
response = agent.chat("Run doctor deep and return the proof URI")
```


Aurekai integration surface for Llamaindex.

Status: active
Type: agent

## Core Template Set

- doctor-deep
- manifest-verify
- model-memory-pack
- sae-audit
- semantic-cache-bench
- proof-bundle-export
- release-gate

## Canonical References

- Platform: https://github.com/aurekai/aurekai
- Native runtime: https://github.com/aurekai/native-runtime
- Integration registry: https://github.com/aurekai/aurekai/blob/main/registry/integrations.json
- Ecosystem map: https://github.com/aurekai/aurekai/blob/main/ECOSYSTEM_NAMES.md
