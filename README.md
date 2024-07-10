<!--

SPDX-FileContributor: [Author Name(s)] <[Optional: Email Address(es)]>

SPDX-License-Identifier: CC0-1.0
-->

# Cryptographic Algorithms Open Dataset

This data set, which includes a list of cryptography algorithms with an open source implementation, was originally the output of SCANOSS mining efforts across its entire data base, which includes all relevant open source software published. Today, the intention is to turn this repository into a collaborative project to enrich and maintain this data set, not just for export control, the original target activity, but for other purposes as well, like quantum safe or compliance with a variety of regulations.

## Folder Structure
There are two main folders in this repo and several subfolders:
* [definitions_crypto_algorithms](definitions_crypto_algorithms)
    * [list_definitions_crypto_algorithms](definitions_crypto_algorithms/list_definitions_crypto_algorithms)
    * [spec_crypto_algorithms](definitions_crypto_algorithms/spec_crypto_algorithms)
* [utilities](utilities)
* [docs_crypto_algorithms](docs_crypto_algorithms)

### Definitions_crypto_algorithms

The [definitions_crypto_algorithms](definitions_crypto_algorithms) folder contains the current definitions list together the information to create new ones or enrich the existing ones

You can find the index of the cryptography algorithms and their corresponding algorithId in the [definition_index_crypto_algorithms.md](/definitions_crypto_algorithms/definitions_index_crypto_algorithms.md) fine. This is the best place to start.

#### list_definitions_crypto_algorithms

The [list_definitions_crypto_algorithms](definitions_crypto_algorithms folder contains a set of YAML files which define all the available cryptography algorithms to be used when searching for hints inside source files.

#### spec_crypto_algorithms

The [spec_crypto_algorithms](definitions_crypto_algorithms/spec_crypto_algorithms) contains the information to create new definitions, or to enrich the existing ones, as well as a description of the syntax followed on each definition. If you want to understand the syntaxt of each one of the definitions, this is the place to go.

### Utilities

The [utilities](utilities) folder contains some helper utility scripts written in Python to illustrate how these definitions can be leveraged.

The primary example is [crypto_detect.py](utilities/crypto_detect.py).
More details on how to use it can be found [here](utilities/README.md)

### docs_crypto_algorithms

The [docs_crypto_algorithms](docs_crypto_algorithms) folder contains documents that are relevant for maintainers, contributors and users, related to the project and its releases.

## Contributing New Cryptographic Data

If you find a missing/invalid keyword, please do the following:
- Fork the [repo](https://github.com/scanoss/crypto_algorithms_open_dataset)
- Update or Add the affected YAML files inside the [definitions](definitions) folder
- Create a Pull Request with the details of the update

The team will review these requests and accept them into repo for everyone to benefit from.

## License

This project is released under the Creative Commons Public Domain CC0-1.0 license. 
Full details can be found [here](LICENSE).
