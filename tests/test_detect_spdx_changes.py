# SPDX-License-Identifier: MIT
import json
from pathlib import Path

from detect_spdx_changes import diff
from data_io import load_spdx
from build_linked_dataset import build_spdx_snapshot, write_json


def test_diff_no_changes(fake_repo):
    spdx = load_spdx(fake_repo["spdx"])
    snap = build_spdx_snapshot(spdx)
    result = diff(spdx, snap)
    assert result == {"added": [], "modified": [], "removed": []}


def test_diff_added_modified_removed(tmp_path: Path, fake_repo):
    current = load_spdx(fake_repo["spdx"])
    snapshot = build_spdx_snapshot(current)

    # Mutate snapshot to simulate "before"
    # 1. Drop 'aes' from snapshot -> simulate addition in current
    # 2. Change 'sha2' name in snapshot -> simulate modification in current
    # 3. Add a fake 'gone' to snapshot only -> simulate removal in current
    snapshot.pop("aes")
    snapshot["sha2"] = dict(snapshot["sha2"], name="SHA-2 (old)")
    snapshot["gone"] = {"id": "gone", "name": "Gone"}

    result = diff(current, snapshot)
    assert [a["id"] for a in result["added"]] == ["aes"]
    assert result["added"][0]["record"]["name"] == "Advanced Encryption Standard"
    assert [m["id"] for m in result["modified"]] == ["sha2"]
    assert result["modified"][0]["before"]["name"] == "SHA-2 (old)"
    assert result["modified"][0]["after"]["name"] == "SHA-2"
    assert [r["id"] for r in result["removed"]] == ["gone"]


def test_cli_exit_codes(tmp_path: Path, fake_repo, monkeypatch, capsys):
    """CLI: exit 0 on no diff, 1 on changes."""
    from detect_spdx_changes import main as detect_main

    # Snapshot exactly equal -> exit 0
    snap_path = tmp_path / "snap.json"
    write_json(snap_path, build_spdx_snapshot(load_spdx(fake_repo["spdx"])))
    rc = detect_main(["--spdx-dir", str(fake_repo["spdx"]), "--snapshot", str(snap_path),
                      "--out", str(tmp_path / "diff.json")])
    assert rc == 0
    assert json.loads((tmp_path / "diff.json").read_text())["added"] == []

    # Mutate snapshot -> exit 1
    snap = json.loads(snap_path.read_text())
    snap.pop("aes")
    snap_path.write_text(json.dumps(snap))
    rc = detect_main(["--spdx-dir", str(fake_repo["spdx"]), "--snapshot", str(snap_path),
                      "--out", str(tmp_path / "diff.json")])
    assert rc == 1
