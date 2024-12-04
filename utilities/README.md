<!--
SPDX-FileCopyrightText: 2024 2024 SCAN Open Source Solutions SL (scanoss.com)
SPDX-FileContributor: [Author Name(s)] <[Optional: Email Address(es)]>

SPDX-License-Identifier: MIT
-->

# Introduction
This folder contains utility/helper scripts to best leverage the cryptographic algorithms project.

## Analyse Folder for Crypto
The [crypto_detect.py](crypto_detect.py) is a Python script that loads the [definitions](../definitions) folder
into memory and uses it to scan ghe specified target folder for evidence of cryptography.

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

To process the current `.` folder in its entirety, please use the following command:
```shell
python3 crypto_detect.py -c <your-custom-definitions\> .
```

From the [root](../.) of the project, simply run:
```shell
python3 crypto_detect.py <src-folder>
```

The [definitions](../definitions_crypto_algorithms) are loaded by default, and the `<src-folder>` is whatever you want to analyse.

To run in quiet mode, simply add `--quiet`.
