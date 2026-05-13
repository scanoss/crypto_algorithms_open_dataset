#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Emit SQL deltas for the crypto_algorithms_metadata table from a diff JSON.

Conservative target schema:
  CREATE TABLE crypto_algorithms_metadata (
    id                TEXT PRIMARY KEY,
    name              TEXT,
    oid               TEXT,
    crypto_class      TEXT,
    common_key_size   TEXT,
    specified_key_size TEXT,
    reference         TEXT
  );

Multi-valued fields (oid, commonkeySize, specifiedkeySize, reference) are
serialised to JSON text so a single column can hold scalars, lists, or
range objects without lossy flattening. The downstream consumer in
platform_deployment can refine the schema later.

Output: one SQL file per change under <out>/<timestamp>__<verb>_<id>.sql,
plus a single combined file <timestamp>__all.sql for convenience.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

TABLE = "crypto_algorithms_metadata"
COLUMNS = [
    ("id", "id"),
    ("name", "name"),
    ("oid", "oid"),
    ("cryptoClass", "crypto_class"),
    ("commonkeySize", "common_key_size"),
    ("specifiedkeySize", "specified_key_size"),
    ("reference", "reference"),
]


def _quote(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, (list, dict)):
        text = json.dumps(value, sort_keys=True)
    else:
        text = str(value)
    return "'" + text.replace("'", "''") + "'"


def insert_sql(record: dict) -> str:
    cols = ", ".join(db_col for _, db_col in COLUMNS)
    vals = ", ".join(_quote(record.get(spdx_field)) for spdx_field, _ in COLUMNS)
    return f"INSERT INTO {TABLE} ({cols}) VALUES ({vals});"


def update_sql(record: dict) -> str:
    set_clauses = [
        f"{db_col} = {_quote(record.get(spdx_field))}"
        for spdx_field, db_col in COLUMNS
        if spdx_field != "id"
    ]
    rid = _quote(record["id"])
    return f"UPDATE {TABLE} SET {', '.join(set_clauses)} WHERE id = {rid};"


def emit(diff_data: dict, out_dir: Path, timestamp: str | None = None) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = timestamp or dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    written: list[Path] = []
    combined: list[str] = []

    for entry in diff_data.get("added", []):
        sql = insert_sql(entry["record"])
        path = out_dir / f"{ts}__insert_{entry['id']}.sql"
        path.write_text(sql + "\n")
        written.append(path)
        combined.append(sql)

    for entry in diff_data.get("modified", []):
        sql = update_sql(entry["after"])
        path = out_dir / f"{ts}__update_{entry['id']}.sql"
        path.write_text(sql + "\n")
        written.append(path)
        combined.append(sql)

    if combined:
        combo = out_dir / f"{ts}__all.sql"
        combo.write_text("\n".join(combined) + "\n")
        written.append(combo)
    return written


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--diff", type=Path, required=True, help="diff JSON from detect_spdx_changes.py")
    p.add_argument("--out", type=Path, required=True, help="output sql/ directory")
    p.add_argument("--timestamp", type=str, default=None,
                   help="override timestamp (UTC ISO basic) - useful for tests/repro")
    args = p.parse_args(argv)

    data = json.loads(args.diff.read_text())
    written = emit(data, args.out, timestamp=args.timestamp)
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
