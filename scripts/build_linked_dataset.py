#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the generated dataset artifacts in dist/.

Outputs (all JSON, sorted keys, indent=2):
  dist/crypto_algorithms_linked.json   - {id: {spdx: {...}, keywords: [...]}} for ids
                                          present in both SPDX and keywords/.
  dist/crypto_algorithms_keywords.json - {id: [keywords...]} for every keyword file.
  dist/spdx_snapshot.json              - {id: <full spdx record>} for every SPDX yaml.
                                          Used as the diff baseline by the SPDX-change
                                          detector.

This script is the sole writer of dist/. All workflows call it after their
specific mutation step (keyword change / submodule bump).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_io import REPO_ROOT, load_keywords, load_spdx  # noqa: E402

DIST_DIR = REPO_ROOT / "dist"


def _strip_keyword_internal(record: dict) -> list:
    return list(record.get("keywords") or [])


def build_keywords_index(keywords: dict[str, dict]) -> dict[str, list]:
    return {kid: _strip_keyword_internal(r) for kid, r in sorted(keywords.items())}


def build_linked(keywords: dict[str, dict], spdx: dict[str, dict]) -> dict[str, dict]:
    linked: dict[str, dict] = {}
    for kid in sorted(set(keywords) & set(spdx)):
        linked[kid] = {
            "spdx": spdx[kid],
            "keywords": _strip_keyword_internal(keywords[kid]),
        }
    return linked


def build_spdx_snapshot(spdx: dict[str, dict]) -> dict[str, dict]:
    return {sid: spdx[sid] for sid in sorted(spdx)}


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(DIST_DIR), help="output directory (default: dist/)")
    args = p.parse_args(argv)

    out = Path(args.out)
    keywords = load_keywords()
    spdx = load_spdx()

    write_json(out / "crypto_algorithms_keywords.json", build_keywords_index(keywords))
    write_json(out / "crypto_algorithms_linked.json", build_linked(keywords, spdx))
    write_json(out / "spdx_snapshot.json", build_spdx_snapshot(spdx))

    print(f"keywords : {len(keywords)}")
    print(f"spdx     : {len(spdx)}")
    print(f"linked   : {len(set(keywords) & set(spdx))}")
    print(f"wrote artifacts under {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
