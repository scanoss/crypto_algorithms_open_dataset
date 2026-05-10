# SPDX-License-Identifier: MIT
import json
from pathlib import Path

from build_linked_dataset import (
    build_keywords_index,
    build_linked,
    build_spdx_snapshot,
    write_json,
)
from data_io import load_keywords, load_spdx


def test_keywords_index(fake_repo):
    keywords = load_keywords(fake_repo["keywords"])
    idx = build_keywords_index(keywords)
    assert set(idx) == {"aes", "sha2", "MLKEM", "chacha20", "bad"}
    assert idx["aes"] == ["aes.h", "AES_set_encrypt_key"]
    assert idx["bad"] == ["x"]


def test_linked_only_strict_id_match(fake_repo):
    keywords = load_keywords(fake_repo["keywords"])
    spdx = load_spdx(fake_repo["spdx"])
    linked = build_linked(keywords, spdx)
    # aes + sha2 only. MLKEM (case-collision) is intentionally excluded;
    # chacha20 has no SPDX counterpart; bad is keyword-only.
    assert set(linked) == {"aes", "sha2"}
    assert linked["aes"]["spdx"]["id"] == "aes"
    assert linked["aes"]["keywords"] == ["aes.h", "AES_set_encrypt_key"]


def test_spdx_snapshot_round_trip(fake_repo):
    spdx = load_spdx(fake_repo["spdx"])
    snap = build_spdx_snapshot(spdx)
    assert set(snap) == {"aes", "sha2", "mlkem", "lonely_spdx"}
    assert snap["mlkem"]["name"] == "ML-KEM"


def test_write_json_roundtrip(tmp_path: Path, fake_repo):
    keywords = load_keywords(fake_repo["keywords"])
    spdx = load_spdx(fake_repo["spdx"])
    out = tmp_path / "out" / "linked.json"
    write_json(out, build_linked(keywords, spdx))
    data = json.loads(out.read_text())
    assert data["aes"]["spdx"]["name"] == "Advanced Encryption Standard"
