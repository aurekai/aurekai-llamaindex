# Scripts — aurekai-llamaindex

| Script | Description |
|---|---|
| `scripts/doctor_deep.py` | Run Aurekai doctor --deep and return structured diagnostics |
| `scripts/manifest_verify.py` | Verify an Aurekai manifest against the deploy schema |
| `scripts/model_memory_pack.py` | Pack model memory artifacts for the given tag |
| `scripts/sae_audit.py` | Run a Sparse Autoencoder (SAE) audit on the given model |
| `scripts/semantic_cache_bench.py` | Benchmark the Aurekai semantic cache |
| `scripts/proof_bundle_export.py` | Export a verifiable proof bundle of the current pipeline state |
| `scripts/release_gate.py` | Run the release gate check for the given version |

Each script exposes a callable importable as a LlamaIndex tool.
