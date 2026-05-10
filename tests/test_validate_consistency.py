# SPDX-License-Identifier: MIT
from validate_consistency import build_report


def test_report_summary(fake_repo):
    r = build_report(keywords_dir=fake_repo["keywords"], spdx_dir=fake_repo["spdx"])
    s = r["summary"]
    assert s["keyword_count"] == 5
    assert s["spdx_count"] == 4
    # aes + sha2 are linked. MLKEM is a case collision (not counted as linked).
    assert s["linked"] == 2
    assert s["case_collisions"] == 1
    assert s["body_id_mismatches"] == 1
    assert s["keywords_without_spdx"] == 2  # chacha20, bad
    assert s["spdx_without_keywords"] == 1  # lonely_spdx


def test_case_collision_payload(fake_repo):
    r = build_report(keywords_dir=fake_repo["keywords"], spdx_dir=fake_repo["spdx"])
    assert r["case_collisions"] == [{"keyword_id": "MLKEM", "spdx_id": "mlkem"}]


def test_body_id_mismatch_payload(fake_repo):
    r = build_report(keywords_dir=fake_repo["keywords"], spdx_dir=fake_repo["spdx"])
    assert len(r["body_id_mismatches"]) == 1
    m = r["body_id_mismatches"][0]
    assert m["file_id"] == "bad"
    assert m["algorithmId_in_body"] == "not_bad"


def test_only_side_lists(fake_repo):
    r = build_report(keywords_dir=fake_repo["keywords"], spdx_dir=fake_repo["spdx"])
    # MLKEM is excluded from keyword-only because its case-folded match is
    # already accounted for by the case-collision report.
    assert r["keywords_without_spdx"] == ["bad", "chacha20"]
    assert r["spdx_without_keywords"] == ["lonely_spdx"]
