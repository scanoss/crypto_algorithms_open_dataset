<!--
SPDX-FileContributor: SCANOSS
SPDX-License-Identifier: CC0-1.0
-->

# Cryptographic Algorithms Open Dataset

This repository defines a set of source-code **keywords** that can be used to
detect cryptographic algorithm usage. Algorithm **metadata** (canonical name,
OID, cryptographic class, key sizes, references) is sourced from the
[SPDX cryptographic-algorithm-list](https://github.com/spdx/cryptographic-algorithm-list)
and joined with our keyword set by the algorithm `id`.

The two repositories are intentionally split:

| Source | What it owns |
| ------ | ------------ |
| `spdx/cryptographic-algorithm-list` | Algorithm metadata (single source of truth). |
| this repo | Keyword definitions used to detect each algorithm in source code. |

## Folder structure

```
keywords/<algorithmId>.yaml       # one file per algorithm; only id + keywords[]
spec/                             # YAML format spec and template
external/spdx-crypto/             # Git submodule pinned to a commit of the SPDX list
scripts/                          # build_linked_dataset.py, validate_consistency.py
dist/                             # generated artifacts (committed, kept current by CI)
utilities/crypto_detect.py        # example consumer of this dataset
docs_crypto_algorithms/           # project docs
```

### Generated artifacts in `dist/`

These files are produced by `scripts/build_linked_dataset.py` and kept current
by the GitHub workflows. **Do not edit them manually.**

* `crypto_algorithms_keywords.json` — `{id: [keywords...]}` for every
  algorithm in `keywords/`.
* `crypto_algorithms_linked.json` — `{id: {spdx: <metadata>, keywords: [...]}}`
  for every id that exists in **both** `keywords/` and SPDX. IDs that only
  exist in this repo (no SPDX counterpart yet) are intentionally absent here;
  see `dist/inconsistency_report.json`.
* `spdx_snapshot.json` — copy of the SPDX records keyed by id, used by the
  SPDX-change detector as a diff baseline.

## Cloning and updating the SPDX submodule

```sh
git clone --recurse-submodules https://github.com/scanoss/crypto_algorithms_open_dataset.git
# or, on an existing clone
git submodule update --init --recursive
```

To pull a newer SPDX state locally (workflows do this automatically):

```sh
git submodule update --remote external/spdx-crypto
```

## Adding or updating a keyword set

1. Find the SPDX `id` for the algorithm in
   [`external/spdx-crypto/yaml/`](external/spdx-crypto/yaml). The filename
   without `.yaml` is the id.
2. Create or edit `keywords/<id>.yaml`:

   ```yaml
   # SPDX-License-Identifier: CC0-1.0
   algorithmId: <id>
   keywords:
     - <keyword 1>
     - <keyword 2>
   ```

3. Open a PR. The build/validate workflow runs and refreshes `dist/` artifacts.

If the algorithm is not yet in SPDX, file the keyword YAML under the SCANOSS
id you choose — `scripts/validate_consistency.py` will list it as
keywords-only and the linked JSON will skip it until SPDX gains the entry.

## Algorithm consistency rules

* **`id` casing**: when SPDX has the same id with different casing, the SPDX
  id wins. Rename the keyword YAML accordingly.
* **Other inconsistencies** (missing in SPDX, mismatched names): reported by
  the validator only; nothing is generated for them in `dist/crypto_algorithms_linked.json`.

## Utilities

`utilities/crypto_detect.py` is a small Python tool that loads keywords from
`keywords/` and metadata from the SPDX submodule, and scans a folder for
matches. See [`utilities/README.md`](utilities/README.md).

## Contributing

Fork → branch → PR. The team will review and merge.

## License

Released under the Creative Commons Public Domain CC0-1.0 license. Full
details in [`LICENSES/`](LICENSES).
