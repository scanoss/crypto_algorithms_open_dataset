# SPDX-License-Identifier: MIT
"""Shared loaders for SPDX metadata and SCANOSS keyword YAML files."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KEYWORDS_DIR = REPO_ROOT / "keywords"
SPDX_YAML_DIR = REPO_ROOT / "external" / "spdx-crypto" / "yaml"


def _yaml_files(directory: Path) -> Iterator[Path]:
    for entry in sorted(directory.iterdir()):
        if entry.is_file() and entry.suffix == ".yaml":
            yield entry


def load_keywords(directory: Path = KEYWORDS_DIR) -> dict[str, dict]:
    """Return {algorithmId: {algorithmId, keywords[], _path}} keyed by filename stem."""
    out: dict[str, dict] = {}
    for path in _yaml_files(directory):
        stem = path.stem
        with path.open() as fh:
            data = yaml.safe_load(fh) or {}
        try:
            data["_path"] = str(path.relative_to(REPO_ROOT))
        except ValueError:
            data["_path"] = str(path)
        out[stem] = data
    return out


def load_spdx(directory: Path = SPDX_YAML_DIR) -> dict[str, dict]:
    """Return {id: spdx_record} keyed by filename stem."""
    if not directory.exists():
        raise FileNotFoundError(
            f"SPDX submodule not initialized at {directory}. "
            "Run: git submodule update --init --recursive"
        )
    out: dict[str, dict] = {}
    for path in _yaml_files(directory):
        with path.open() as fh:
            data = yaml.safe_load(fh) or {}
        out[path.stem] = data
    return out
