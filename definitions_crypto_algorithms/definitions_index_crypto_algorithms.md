<!--

SPDX-FileContributor: [Author Name(s)] <[Optional: Email Address(es)]>

SPDX-License-Identifier: CC0-1.0
-->

# Defined algorithms by

This is the index of the cryptography algorithms definitions including the algorithmId ordered by category.

* Date: 2025-04-07
* listVersion:

Algorithm information can be found on: 
 
 ```
    definitions_crypro_algorithms/algorithms/<category>/<algorithmId>
 ```
Keywords definition for each algorithm can be found on:
 
 ```
    definitions_crypro_algorithms/definitions/<category>/<algorithmId>
 ```

## Asymmetric Encryption

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| blum-goldwasser | Blum-Goldwasser Probabilistic Public-key Encryption | 320 |
| dhe | Diffie-Hellman Ephemeral | 128 |
| dhe | Diffie-Hellman Ephemeral | 128 |
| dhies | Diffie-Hellman Integrated Encryption Scheme | 128 |
| dsa | Digital Signature Algorithm | 128 |
| ecc | Elliptic Curve Cryptography | 128 |
| ecdh | Elliptic Curve Diffie-Hellman | 128 |
| ecdsa | Elliptic Curve Digital Signature Algorithm | 128 |
| ecmqv | Elliptic Curve Menezes-Qu-Vanstone | 128 |
| ed25519 | Edwards-curve Digital Signature Algorithm |  |
| elgamal | ElGamal | 128 |
| luc | LUC Public Key Cryptosystem | 64 |
| mqv | Menezes-Qu-Vanstone | 512 |
| naccachestern | Naccache-Stern Encryption Algorithm | 1024-2048 |
| rabin | Rabin | 128 |
| rsa | RSA Cryptosystem | 128 |
| rsa-oaep | RSA with Optimal Asymmetric Encryption Padding | 128 |
| xtr | XTR Public Key System | 64 |

## Authentication

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| eccpwd | Elliptic Curve Password Authenticated Key Exchange | 128-256 |
| kerberos | Kerberos Authentication Protocol | 56-256 |
| psk | Pre-Shared Key Authentication | 128-256 |

## Block Cipher Modes

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| cbc | Cipher Block Chaining |  |
| ccm | Counter with CBC-MAC |  |
| cfb | Cipher Feedback |  |
| ctr | Counter Cipher |  |
| ecb | Electronic Codebook |  |
| gcm | Galois/Counter Mode |  |
| ofb | Output Feedback |  |
| xts | XEX-Based Codebook mode |  |

## Certificate Formats

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| ASN1 | Abstract Syntax Notation One | 256 |
| pgp | Pretty Good Privacy | 128 |
| pkcs12 | PKCS #12: Personal Information Exchange Syntax | 128 |
| pkcs7 | PKCS #7: Cryptographic Message Syntax | 128 |

## Cryptographic Primitive

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| xoodyak | Xoodyak Cryptographic Primitive | 128-256 |

## Data Clustering

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| dcc | Dynamic Contrastive Clustering | 64 |

## Digital Signature Algorithm

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| dss | Digital Signature Standard | 1024-3072 |
| dstu4145 | DSTU 4145 Digital Signature Algorithm | 163-431 |
| ecnr | Elliptic Curve Nyberg-Rueppel Signature Algorithm | 160-521 |
| ed448 | Edwards-Curve Digital Signature Algorithm 448 | 224 |
| eddsa | Edwards-Curve Digital Signature Algorithm | 128-224 |
| iso9796 | ISO 9796 Digital Signature | 1024-3072 |
| rsassapss | RSA Signature Scheme with Appendix - Probabilistic Signature Scheme | 1024-4096 |

## Generic curves

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| gecc | Generic elliptic curve | - |

## Hash Function

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| harakav2 | Haraka v2 Hash Function | 256-512 |
| kangarootwelve | KangarooTwelve Hash Function | 128 |
| kupyna | Kupyna Hash Function | 256-512 |
| marsupilamifourteen | Marsupilami-14 Hash Function | 256 |
| parallelhash | Parallel Hash Function | 128-256 |
| sm3 | SM3 Cryptographic Hash Algorithm | 256 |
| tuplehash | TupleHash Function | 128-256 |

## Hash Functions

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| blake2 | BLAKE2 | 256/512 |
| blake3 | BLAKE3 | 256/512 |
| haval | HAVAL Hash Function | 128 |
| keccak | Keecak | 256 |
| md160 | RIPEMD-160 Hash Function | 64 |
| md2 | MD2 Message-Digest Algorithm | 256 |
| md4 | MD4 Message-Digest Algorithm | 128 |
| md5 | MD5 Message-Digest Algorithm | 128 |
| md6 | MD6 Message-Digest Algorithm | 512 |
| mdc2 | MDC-2 | 128 |
| ripemd | RIPEMD Family of Hash Functions | 128 |
| sha1 | Secure Hash Algorithm 1 | 160 |
| sha2 | Secure Hash Algorithm 2 | 224-512 |
| sha3 | Secure Hash Algorithm 3 | 224-512 |
| shs | Secure Hash Standard | 128 |
| skein | Skein Hash Function | 256 |
| ssha | Salted SHA | 128 |
| tiger | Tiger Hash Function | 256 |
| whirpool | Whirlpool Hash Function | 128 |

## Key Agreement

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| ansix942 | ANSI X9.42 Key Agreement | 1024-3072 |
| x25519 | X25519 Key Exchange | 128 |
| x448 | X448 Key Exchange | 224 |
| xdh | Extended Diffie-Hellman | 128-224 |

## Key Derivation Functions

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| ansix963 | ANSI X9.63 Key Derivation Functions | 128-512 |
| bcrypt | Bcrypt Password Hashing Function | 320 |
| concatenationkdf | Concatenation Key Derivation Functions | 128-512 |
| hkdf | HMAC-based Key Derivation Functions | 128-512 |
| kdf1 | Key Derivation Functions 1 | 128-512 |
| kdf2 | Key Derivation Functions 2 | 128-512 |
| kdfcounter | Counter Mode Key Derivation Functions | 128-512 |
| kdfdoublepipeline | Double Pipeline Iteration Key Derivation Functions | 128-512 |
| kdffeedback | Feedback Mode Key Derivation Functions | 128-512 |
| kdfsession | Session Key Derivation Functions | 128-512 |
| mgf1 | Mask Generation Function 1 | 128-512 |
| pbe | Password-Based Encryption | 128 |
| pbes1 | Password-Based Encryption Scheme 1 | 128 |
| pbes2 | Password-Based Encryption Scheme 2 | 256 |
| pbkdf1 | Password-Based Key Derivation Function 1 | 128 |
| pbkdf2 | Password-Based Key Derivation Function 2 | 128 |
| scrypt | Scrypt Key Derivation Functions | 128-256 |

## Key Encapsulation

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| rsakem | RSA Key Encapsulation Mechanism | 1024-4096 |

## Key Wrapping

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| rfc3211wrap | RFC 3211 Password-based Key Wrapping | 128-256 |

## Message Authentication Codes

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| CMAC | Cipher-based Message Authentication Codes | 128 |
| argon2 | Cipher-based Message Authentication Codes | - |
| cms | Count-Min Sketch | 64 |
| kmac | Keccak Message Authentication Codes | 128-256 |
| siphash | SipHash Pseudorandom Function | 64-128 |

## Password Hashing

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| mscash | Microsoft Cache Hash (MSCASH) | 256 |
| mscash2 | Microsoft Cache Hash v2 (MSCASH2) | 128 |

## Polynomial Functions

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| adler32 | Adler-32 Checksum Algorithm | 32 |
| crc16 | Cyclic Redundancy Check 16-bit | 16 |
| crc32 | Cyclic Redundancy Check 32-bit | 32 |
| fasthash | FastHash | 256 |
| fletcher | Fletcher | 64 |
| fnv1 | Fowler–Noll–Vo | 1024 |

## Post-Quantum Cryptography

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| bike | Bit Flipping Key Encapsulation | 128-256 |
| crystals-kyber | Crystals-Kyber | - |
| dilithium | CRYSTALS-Dilithium Signature Algorithm | 128-256 |
| falcon | Fast-Fourier Lattice-based Compact Signatures | 128-256 |
| frodokem | FrodoKEM Post-Quantum Key Encapsulation | 128-256 |
| gemss | Great Multivariate Signature Scheme | 128-256 |
| gmss | Generalized Merkle Signature Scheme | 128-256 |
| hqc | Hamming Quasi-Cyclic | 128-256 |
| hss | Hierarchical Signature Scheme | 128-256 |
| lms | Leighton-Micali Signature Scheme | 128-256 |
| mceliece | McEliece | 64 |
| mldsa | Multilevel Digital Signature Algorithm | 128-256 |
| mlkem | Module Lattice Key Encapsulation Mechanism | 128-256 |
| ntruencrypt | NTRUEncrypt | 128 |
| picnic | Picnic Signature Algorithm | 128-256 |
| qtesla | Quantum-resistant Tesla Signature Scheme | 128-256 |
| rainbow | Rainbow | - |
| sike | Supersingular Isogeny Key Encapsulation | - |
| sphincs+ | SPHINCS+ | - |
| sphincsplus | SPHINCS+ Signature Algorithm | 128-256 |
| xmss | eXtended Merkle Signature Scheme | 128-256 |
| xmssmt | XMSS Multi-Tree Signature Scheme | 128-256 |

## Random Number Generation

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| ansix931 | ANSI X9.31 Random Number Generator | 128-256 |
| csprng | Cryptographically Secure Pseudo-Random Number Generator | - |
| drbg | Deterministic Random Bit Generator | - |
| fortuna | Fortuna | 64 |
| isaac | ISAAC Stream Cipher | 256 |
| yarrow | Yarrow Pseudorandom Number Generator | 160 |

## Secure Protocols

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| fcrypt |  | 128 |
| feal | Fast Data Encipherment Algorithm | 64 |
| gea0-x | GSM Encryption Algorithm | 64-128 |
| nimbus | Nimbus | 256 |
| seal | Software-optimized Encryption Algorithm | 128 |
| srp | Secure Remote Password | 128 |
| tcrypt | TCrypt Disk Encryption | 128 |

## Stream Cipher

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| hc | HC Stream Cipher | 128-256 |

## Symmetric Encryption

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| 3des | Triple Data Encryption Standard | 128 |
| 3way | 3 Way | 128 |
| aes | Advanced Encryption Standard | 128-256 |
| aria | ARIA Block Cipher | 128-256 |
| bearlion | BearLion | 128 |
| blowfish | Blowfish Block Cipher | 320 |
| camellia | Camellia | 256 |
| cast | CAST Block Cipher Family | 320 |
| chacha20 | ChaCha | 256 |
| cmea | Cellular Message Encryption Algorithm | 64 |
| cobra | Cobra Stream Cipher | 128 |
| des | Data Encryption Standard | 168 |
| desede | Triple Data Encryption Standard (DESede) | 168 |
| f8 | F8 Mode of Operation | 128 |
| gost | GOST Block Cipher | 64 |
| grain | Grain | 128 |
| hc128 | HC-128 | 128 |
| hc256 | HC-256 | 256 |
| hmac | Hash-based Message Authentication Codes | - |
| hmac | Hash-based Message Authentication Codes | - |
| ice | Indispensable Cryptographic Engine | 128 |
| idea | International Data Encryption Algorithm | 64 |
| juniper | Juniper |  |
| kalyna | Kalyna Block Cipher | 128-512 |
| kazumi | Kasumi | 128 |
| khazad | Khazad | 128 |
| lea | Lightweight Encryption Algorithm | 128-256 |
| loki91 | LOKI-91 Block Cipher | 64 |
| lucifer | Lucifer Block Cipher | 128 |
| misty1 | MISTY1 Block Cipher | 32 |
| multi2 | Multi2 | 128 |
| noekeon | Noekeon Block Cipher | 128 |
| panama | PANAMA | 128 |
| quad | Quad | 128 |
| rabbit | Rabbit | 128 |
| rc2 | RC2 Block Cipher | 128 |
| rc4 | RC4 Stream Cipher | 2048 |
| rc4-hmac | RC4 with HMAC | 2048 |
| rc5 | RC5 Block Cipher | 128 |
| rc6 | RC6 Block Cipher | 128 |
| rijndael | Rijndael | 256 |
| safer | Secure And Fast Encryption Routine | 128 |
| salsa10 | Salsa10 Stream Cipher | 64 |
| salsa20 | Salsa20 | 256 |
| salsa20 | Salsa20 Stream Cipher | 128 |
| sapphire | Sapphire Stream Cipher | 256 |
| seed | SEED Block Cipher | 256 |
| serpent | Serpent Block Cipher | 128 |
| shacal | SHACAL Block Cipher | 128 |
| shark | SHARK Block Cipher | 64 |
| skipjack | SKIPJACK Block Cipher | 32 |
| sms4 | SMS4 Block Cipher | 128 |
| snerfu | SNERFU Hash Function | 256 |
| snow | SNOW Stream Cipher | 128 |
| sober | SOBER Stream Cipher | 128 |
| sosemanuk | Sosemanuk Stream Cipher | 128 |
| tdes | Triple Data Encryption Standard | 128 |
| tea | Tiny Encryption Algorithm | 128 |
| threefish | Threefish Block Cipher | 1024 |
| tnepres | Serpent Block Cipher (reversed) | 256 |
| twofish | Twofish Block Cipher | 64 |
| vmpc | Variably Modified Permutation Composition |  |
| wake | Word Auto Key Encryption | 64 |
| xtea | eXtended Tiny Encryption Algorithm | 128 |
| zipcrypt | ZipCrypto | 64 |
| zuc | ZUC Stream Cipher | 128 |

## Zero-Knowledge Proof

| Algorithm ID | Algorithm | Strength |
|-------------|-----------|----------|
| zk-snarks | Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge | - |
| zk-starks | Zero-Knowledge Scalable Transparent Arguments of Knowledge | - |

