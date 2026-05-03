#!/usr/bin/env python3
"""Example: list all Aurekai LlamaIndex tools."""
import importlib, sys
sys.path.insert(0, ".")

tool_modules = [
    "scripts.doctor_deep",
    "scripts.manifest_verify",
    "scripts.release_gate",
]

for mod_name in tool_modules:
    mod = importlib.import_module(mod_name)
    print(f"Module: {mod_name}")
