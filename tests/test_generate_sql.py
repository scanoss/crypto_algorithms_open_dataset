# SPDX-License-Identifier: MIT
import json
from pathlib import Path

from generate_sql import emit, insert_sql, update_sql, _quote


def test_quote_handles_basic_types():
    assert _quote(None) == "NULL"
    assert _quote("aes") == "'aes'"
    assert _quote("o'reilly") == "'o''reilly'"
    assert _quote(["a", "b"]) == "'[\"a\", \"b\"]'"
    assert _quote({"min": "128", "max": "256"}) == "'{\"max\": \"256\", \"min\": \"128\"}'"


def test_insert_sql_full_record():
    record = {
        "id": "aes",
        "name": "Advanced Encryption Standard",
        "oid": "2.16.840.1.101.3.4.1",
        "cryptoClass": "Symmetric-Key-Algorithm/Block-Cipher",
        "commonkeySize": "256",
        "specifiedkeySize": {"min": "128", "max": "256"},
        "reference": ["https://nist.gov/aes"],
    }
    sql = insert_sql(record)
    assert sql.startswith("INSERT INTO crypto_algorithms_metadata")
    assert "'aes'" in sql
    assert "'Advanced Encryption Standard'" in sql
    assert "'2.16.840.1.101.3.4.1'" in sql
    assert "common_key_size" in sql
    assert "specified_key_size" in sql
    assert sql.endswith(";")


def test_insert_sql_handles_missing_optional_fields():
    record = {"id": "min", "name": "Minimal"}
    sql = insert_sql(record)
    # missing fields should serialise as NULL
    assert sql.count("NULL") >= 5  # oid, crypto_class, common, specified, reference


def test_update_sql_does_not_set_id():
    record = {
        "id": "aes",
        "name": "AES new",
        "cryptoClass": "X/Y",
    }
    sql = update_sql(record)
    assert sql.startswith("UPDATE crypto_algorithms_metadata SET")
    set_clause = sql.split("WHERE")[0]
    # ensure 'id' is not in the SET clause as a standalone column
    assert " id =" not in set_clause and "SET id =" not in set_clause
    assert "WHERE id = 'aes'" in sql


def test_emit_writes_one_file_per_change_plus_combined(tmp_path: Path):
    diff_data = {
        "added": [{"id": "newalg", "record": {"id": "newalg", "name": "New"}}],
        "modified": [
            {"id": "aes",
             "before": {"id": "aes", "name": "old"},
             "after": {"id": "aes", "name": "new"}}
        ],
        "removed": [],
    }
    written = emit(diff_data, tmp_path / "sql", timestamp="20260101T000000Z")
    names = sorted(p.name for p in written)
    assert names == [
        "20260101T000000Z__all.sql",
        "20260101T000000Z__insert_newalg.sql",
        "20260101T000000Z__update_aes.sql",
    ]
    assert "INSERT" in (tmp_path / "sql" / "20260101T000000Z__insert_newalg.sql").read_text()
    assert "UPDATE" in (tmp_path / "sql" / "20260101T000000Z__update_aes.sql").read_text()
    combined = (tmp_path / "sql" / "20260101T000000Z__all.sql").read_text()
    assert "INSERT" in combined and "UPDATE" in combined


def test_emit_no_changes_writes_nothing(tmp_path: Path):
    written = emit({"added": [], "modified": [], "removed": []}, tmp_path / "sql",
                   timestamp="20260101T000000Z")
    assert written == []
    # output dir is created but empty
    assert (tmp_path / "sql").exists()
    assert list((tmp_path / "sql").iterdir()) == []
