<!--
SPDX-FileContributor: SCANOSS
SPDX-License-Identifier: CC0-1.0
-->

# Keyword YAML specification

Each algorithm is defined by a single YAML file under `keywords/` whose
filename equals its algorithm id and matches the `id` of the corresponding
entry in the SPDX [cryptographic-algorithm-list](https://github.com/spdx/cryptographic-algorithm-list)
repository.

## File location

```
keywords/<algorithmId>.yaml
```

The folder is flat: there is no per-category subfolder. The algorithm
category (`cryptoClass` / `cryptoSubClass`) lives in SPDX and is joined into
the generated dataset (`dist/crypto_algorithms_linked.json`).

## Fields

### algorithmId

* Description: SPDX algorithm id. Acts as the join key between this repo and
  SPDX. MUST equal the filename (without `.yaml`).
* Cardinality: [1]
* Values: string. Use the SPDX id verbatim, including its case.

### keywords

* Description: strings used to detect the algorithm in source code. A match
  on any one keyword indicates the algorithm is implemented or used.
* Cardinality: [1..*]
* Values: list of unique strings. Keywords MUST NOT be repeated across
  algorithms. Keywords may contain spaces or punctuation.

## Template

See [`keyword_template.yaml`](keyword_template.yaml).

## Algorithm not yet in SPDX

If an algorithm has no SPDX counterpart yet, the file still lives at
`keywords/<algorithmId>.yaml` using a SCANOSS-chosen id; the consistency
validator (`scripts/validate_consistency.py`) will report it as
keywords-only. Such entries appear in `crypto_algorithms_keywords.json`
but NOT in `crypto_algorithms_linked.json` (which only includes ids
present in SPDX).
