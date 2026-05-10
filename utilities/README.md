<!--
SPDX-FileCopyrightText: 2024 2024 SCAN Open Source Solutions SL (scanoss.com)
SPDX-FileContributor: [Author Name(s)] <[Optional: Email Address(es)]>

SPDX-License-Identifier: MIT
-->

# Introduction
This folder contains utility/helper scripts to best leverage the cryptographic algorithms project.

## Analyse Folder for Crypto
The [crypto_detect.py](crypto_detect.py) is a Python script that loads the
[`keywords/`](../keywords) folder and the SPDX metadata from the
[`external/spdx-crypto/`](../external/spdx-crypto) submodule, and uses them
to scan the specified target folder for evidence of cryptography.

Make sure the submodule is initialised before running:

```bash
git submodule update --init --recursive
```

### Requirements
Python 3.7 or higher.

The dependencies can be found in the [requirements.txt](requirements.txt) file.

To install dependencies, run:
```bash
pip3 install -r requirements.txt
```

### Usage
To run the Crypto Detect, please call it from the CLI using:
```shell
python3 crypto_detect.py --help
```

From the [root](../.) of the project, simply run:
```shell
python3 utilities/crypto_detect.py <src-folder>
```

By default the script reads the keyword definitions from `./keywords/` and
the SPDX metadata from `./external/spdx-crypto/yaml/`. Use `-c <path>` to
point at a different repository root.

To run in quiet mode, simply add `--quiet`.
