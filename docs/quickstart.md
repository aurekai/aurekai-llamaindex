# Quickstart — aurekai-llamaindex

Aurekai LlamaIndex integration: wire Aurekai's `akai` CLI operations into LlamaIndex tools.

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`
- `akai` CLI on `PATH` (see [aurekai/aurekai](https://github.com/aurekai/aurekai))

## Run a script

```bash
python3 scripts/doctor_deep.py
python3 scripts/manifest_verify.py
python3 scripts/model_memory_pack.py
python3 scripts/sae_audit.py
python3 scripts/semantic_cache_bench.py
python3 scripts/proof_bundle_export.py
python3 scripts/release_gate.py
```

## Validate

```bash
bash tests/validate-schemas.sh
bash tests/validate-scripts.sh
```
