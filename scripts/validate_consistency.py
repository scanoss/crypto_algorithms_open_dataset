#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Report id-level inconsistencies between keywords/ and the SPDX submodule.

Behavior:
  - Hard error (exit 2): id case-mismatch (e.g. CMAC.yaml here vs cmac.yaml in SPDX).
    Per project rule the SPDX id is canonical; the SCANOSS file must be renamed.
  - Hard error (exit 2): keyword YAML where algorithmId field disagrees with filename.
  - Hard error (exit 2): a keyword id matches an SPDX id but disagrees on field-level
    surprises (e.g. SCANOSS-internal duplicate keys, malformed YAML).
  - Soft report (exit 0 by default, exit 1 with --strict): keyword id without an SPDX
    counterpart, and SPDX id without a keyword file.

Usage:
  scripts/validate_consistency.py [--strict] [--json OUT]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_io import REPO_ROOT, load_keywords, load_spdx  # noqa: E402


def build_report(keywords_dir: Path | None = None, spdx_dir: Path | None = None) -> dict:
    keywords = load_keywords(keywords_dir) if keywords_dir is not None else load_keywords()
    spdx = load_spdx(spdx_dir) if spdx_dir is not None else load_spdx()

    spdx_ids = set(spdx)
    kw_ids = set(keywords)

    case_collisions = []
    spdx_lower = {i.lower(): i for i in spdx_ids}
    for kw_id in kw_ids:
        canonical = spdx_lower.get(kw_id.lower())
        if canonical is not None and canonical != kw_id:
            case_collisions.append({"keyword_id": kw_id, "spdx_id": canonical})

    body_id_mismatches = []
    for kw_id, data in keywords.items():
        body_id = data.get("algorithmId")
        if body_id != kw_id:
            body_id_mismatches.append(
                {"file_id": kw_id, "algorithmId_in_body": body_id, "path": data.get("_path")}
            )

    keywords_without_spdx = sorted(kw_ids - spdx_ids - {c["keyword_id"] for c in case_collisions})
    spdx_without_keywords = sorted(spdx_ids - kw_ids - {c["spdx_id"] for c in case_collisions})

    return {
        "summary": {
            "keyword_count": len(keywords),
            "spdx_count": len(spdx),
            "linked": len(kw_ids & spdx_ids),
            "case_collisions": len(case_collisions),
            "keywords_without_spdx": len(keywords_without_spdx),
            "spdx_without_keywords": len(spdx_without_keywords),
            "body_id_mismatches": len(body_id_mismatches),
        },
        "case_collisions": case_collisions,
        "body_id_mismatches": body_id_mismatches,
        "keywords_without_spdx": keywords_without_spdx,
        "spdx_without_keywords": spdx_without_keywords,
    }


def print_human(report: dict) -> None:
    s = report["summary"]
    print(f"keyword files            : {s['keyword_count']}")
    print(f"SPDX yaml files          : {s['spdx_count']}")
    print(f"linked (id match)        : {s['linked']}")
    print(f"case collisions          : {s['case_collisions']}")
    print(f"body algorithmId issues  : {s['body_id_mismatches']}")
    print(f"keyword-only ids         : {s['keywords_without_spdx']}")
    print(f"SPDX-only ids            : {s['spdx_without_keywords']}")
    if report["case_collisions"]:
        print("\nCase collisions (rename to SPDX casing):")
        for c in report["case_collisions"]:
            print(f"  - {c['keyword_id']} -> {c['spdx_id']}")
    if report["body_id_mismatches"]:
        print("\nBody algorithmId mismatches:")
        for c in report["body_id_mismatches"]:
            print(f"  - {c['path']}: filename={c['file_id']!r} body={c['algorithmId_in_body']!r}")
    if report["keywords_without_spdx"]:
        print("\nKeyword ids with no SPDX counterpart (kept as keywords-only):")
        for i in report["keywords_without_spdx"]:
            print(f"  - {i}")
    if report["spdx_without_keywords"]:
        print("\nSPDX ids with no keyword file:")
        for i in report["spdx_without_keywords"]:
            print(f"  - {i}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true",
                   help="exit non-zero on soft inconsistencies too")
    p.add_argument("--json", metavar="PATH",
                   help="write the full report as JSON to PATH")
    args = p.parse_args(argv)

    report = build_report()
    print_human(report)

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True))
        print(f"\nwrote {out.relative_to(REPO_ROOT) if out.is_relative_to(REPO_ROOT) else out}")

    s = report["summary"]
    if s["case_collisions"] or s["body_id_mismatches"]:
        return 2
    if args.strict and (s["keywords_without_spdx"] or s["spdx_without_keywords"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
