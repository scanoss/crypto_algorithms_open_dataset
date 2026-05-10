#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Detect changes between current SPDX state and dist/spdx_snapshot.json.

Compares the live submodule (or any directory passed via --spdx-dir) against
a previously written snapshot (default dist/spdx_snapshot.json) and emits a
JSON diff to stdout (or --out).

Output schema:
{
  "added":    [{"id": "<id>", "record": <spdx record>}],
  "modified": [{"id": "<id>", "before": <record>, "after": <record>}],
  "removed":  [{"id": "<id>", "record": <record>}]
}

Removals are reported but the consumers (SQL generator, workflow) currently
ignore them; SPDX entries are not normally removed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_io import REPO_ROOT, load_spdx  # noqa: E402

DEFAULT_SNAPSHOT = REPO_ROOT / "dist" / "spdx_snapshot.json"


def diff(current: dict, snapshot: dict) -> dict:
    cur_ids = set(current)
    snap_ids = set(snapshot)
    added = [{"id": i, "record": current[i]} for i in sorted(cur_ids - snap_ids)]
    removed = [{"id": i, "record": snapshot[i]} for i in sorted(snap_ids - cur_ids)]
    modified = []
    for i in sorted(cur_ids & snap_ids):
        if current[i] != snapshot[i]:
            modified.append({"id": i, "before": snapshot[i], "after": current[i]})
    return {"added": added, "modified": modified, "removed": removed}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--spdx-dir", type=Path, default=None,
                   help="path to SPDX yaml folder (default: external/spdx-crypto/yaml)")
    p.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT,
                   help=f"path to baseline snapshot (default: {DEFAULT_SNAPSHOT.relative_to(REPO_ROOT)})")
    p.add_argument("--out", type=Path, default=None,
                   help="write diff JSON to this path (default: stdout)")
    args = p.parse_args(argv)

    if not args.snapshot.exists():
        print(f"snapshot not found: {args.snapshot}", file=sys.stderr)
        return 2

    current = load_spdx(args.spdx_dir) if args.spdx_dir else load_spdx()
    snapshot = json.loads(args.snapshot.read_text())

    result = diff(current, snapshot)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    else:
        sys.stdout.write(payload)

    # exit code: 0 if no changes, 1 if any changes detected (so workflow can branch on it)
    has_changes = bool(result["added"] or result["modified"] or result["removed"])
    return 1 if has_changes else 0


if __name__ == "__main__":
    sys.exit(main())
