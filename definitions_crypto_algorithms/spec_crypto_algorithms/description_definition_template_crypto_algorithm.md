# Cryptographic algorithm definition in YAML

This document describes every one of the sections and fields included in the cryptographic algorithm definition template

## Structure

The template is structured in two:
* Version f the definition listVersion
* Cryptographic algorithm definition, including the key information.

This second part is structured in 3 sections
* <section1> characterize the cryptographic algorithm
* <section2> provides unique references to the implementations of the algorithm, based on SWHID and PURL
* <section3> provides additional information and references

## Identifiers and attributes

### listVersion

* Description: release version of the cryptographic algorithm definition list
* Values: MM.mm where MM an mm represent integers
    * MM: major version
    * mm: minor version

### section 1: cryptography algorithm definition

#### algorithmId

* Description: univocal identifier for every cryptographic algorithm. This project provides an identifier per algorithm.
* Values: check the identifiers_algorithmId.yaml file, which includes the list of approved cryptography identifiers.

#### securityStrength

* Description: security strength provided by an algorithm with a particular key length is a measure of the difficulty of subverting the cryptographic protection that is provided by the algorithm and key
* Values: bbbb, where bbbb is an integer, provided in bits

#### securityLifetime

* Description: the estimated time period during which data protected by a specific cryptographic algorithm (and key size) remains secure
* Values: YYYY, where YYYY is the year.

#### algorithmName

* Description: name provided by the author of the algorithm, widely accepted or the corresponding standardization body and its acronym
* Values: <Acronym>-<Name> where:
    * <Acronym> correspond to the commonly used acronym for the cryptographic algorithm
    * <Name> corresponds full name of the cryptopgraphic algorithm

### section 2: algorithm implementations

#### name

* Description: name of the software package that implements the cryptographic algorithm (library)
* Values: short name of the software package

#### version

* Description: version of the software package that implements the cryptographic algorithm (library)
* Values: <MM.mm.x> where MM, mm and x are integers corresponding to:
    * MM: major version
    * mm: mior version
    * x: patchset

Values format might vary depending on the software package

#### swhid

* Description: SoftWare Hash IDentifier is an intrinsic, unique and persistent identifier assigned to software artifacts, enabling their precise and unambiguous identification and tracking across various platforms and repositories.
* Values: check the [Syntax](https://www.swhid.org/specification/v1.1/4.Syntax/), [Core Identifiers](https://www.swhid.org/specification/v1.1/5.Core_identifiers/) and [Qualified Identifiers](https://www.swhid.org/specification/v1.1/6.Qualified_identifiers/) sections of the [SWHID specification](https://www.swhid.org/specification/v1.1/) to better understand the allowed values.

#### purl

* Description: Package URL (PURL) is a format for uniquely identifying software packages, serving as an extrinsic identifier that enables interoperability across package managers and repositories by providing a consistent means of referencing software artifacts.
* Values: check PURL [specification](https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst) to better understand the allowed values.


#### description

* Description: additional information related to the corresponding the implementation of the algorithm
* Values: text string

### section 3: references and keywords

#### crossRef

* Description: links to relevant information related to the cryptographic algorithm that is useful in the declaration
* Values: URL

#### keywords

* Description: these keywords can be used to identify a certain algorithm. Any one match will indicate the cryptographic implementations found. It's important not to repeat keywords between definitions.
* Values: list of unique strings (with or without spaces).
