# SPDX-License-Identifier: MIT
"""Shared pytest fixtures: build a minimal SPDX/keywords pair on disk."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


@pytest.fixture
def fake_repo(tmp_path: Path) -> dict:
    """A small synthetic dataset:

    SPDX has: aes, sha2, mlkem
    Keywords has:
      - aes (linked, normal)
      - sha2 (linked, normal)
      - MLKEM (case-collision against SPDX 'mlkem')
      - chacha20 (keyword-only, no SPDX counterpart)
      - bad (body algorithmId mismatch with filename)

    SPDX-only id (no keyword file) implicit: 'sha2'... actually sha2 has a
    keyword file. So SPDX-only is the single id 'lonely_spdx'.
    """
    spdx_dir = tmp_path / "external" / "spdx-crypto" / "yaml"
    kw_dir = tmp_path / "keywords"

    _write(spdx_dir / "aes.yaml", (
        "id: aes\nname: Advanced Encryption Standard\n"
        "cryptoClass: Symmetric-Key-Algorithm/Block-Cipher\n"
        "commonkeySize: '256'\n"
    ))
    _write(spdx_dir / "sha2.yaml", (
        "id: sha2\nname: SHA-2\n"
        "cryptoClass: Cryptographic-Hash-Function/Hash-Function\n"
    ))
    _write(spdx_dir / "mlkem.yaml", (
        "id: mlkem\nname: ML-KEM\n"
        "cryptoClass: Asymmetric-Key-Algorithm/Post-Quantum-Cryptography\n"
    ))
    _write(spdx_dir / "lonely_spdx.yaml", (
        "id: lonely_spdx\nname: Lonely\ncryptoClass: x/y\n"
    ))

    _write(kw_dir / "aes.yaml", (
        "algorithmId: aes\nkeywords:\n  - aes.h\n  - AES_set_encrypt_key\n"
    ))
    _write(kw_dir / "sha2.yaml", (
        "algorithmId: sha2\nkeywords:\n  - sha256.h\n  - SHA256_Init\n"
    ))
    _write(kw_dir / "MLKEM.yaml", (
        "algorithmId: MLKEM\nkeywords:\n  - mlkem_keygen\n"
    ))
    _write(kw_dir / "chacha20.yaml", (
        "algorithmId: chacha20\nkeywords:\n  - chacha20_init\n"
    ))
    _write(kw_dir / "bad.yaml", (
        "algorithmId: not_bad\nkeywords:\n  - x\n"
    ))

    return {"root": tmp_path, "spdx": spdx_dir, "keywords": kw_dir}
