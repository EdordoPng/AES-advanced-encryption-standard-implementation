# AES Implementation

A complete implementation of the **Advanced Encryption Standard (AES)** developed as a university project for the **Advanced Topics in Cybersecurity** course.

## Project Description

This project provides a **Python implementation** of the AES (Advanced Encryption Standard) encryption algorithm based on the **FIPS 197** specification. The implementation includes all core operations of the algorithm, with a strong focus on both the theoretical and practical aspects of the finite field **GF(2^8)**, which AES relies on.

## Implemented Features

### **Finite Field Operations**

- **Addition and multiplication in GF(2^8)**
- **Implementation of the xTimes function**
- **Inversion in the finite field**

### **AES Transformations**

- **SubBytes** (non-linear substitution)
- **ShiftRows** (row permutation)
- **MixColumns** (linear column transformation)
- **AddRoundKey** (XOR with the round key)

### **Full Encryption Flow**

- **Key Expansion** (key schedule)
- **Complete implementation of AES rounds**

### **Advanced Functionalities**

- **Dynamic S-Box generation**
- **Optimization through combination of SubBytes and ShiftRows**
- **Analysis of masking effects on input data**

## Specific Features

### **S-Box Generation**

The project includes a function to dynamically generate the **S-Box** used in the SubBytes transformation, demonstrating the composition of **finite field inversion** and **affine transformation**.

### **Optimizations**

The implementation provides different versions of the encryption function:

- **Standard implementation**: `AES_encr`
- **Optimized version combining SubBytes and ShiftRows**: `AES_encr_combined_sb_and_sr`
- **Version for masking analysis**: `AES_encr_state_xor_m`

## Linearity Analysis of Transformations

The project includes a detailed analysis of how AES transformations behave under XOR operations, showing which transformations are **linear** (AddRoundKey, ShiftRows, MixColumns) and which are **non-linear** (SubBytes).

## Usage

```python
# State and key definition
AES_state = [
    [0x32, 0x88, 0x31, 0xe0],
    [0x43, 0x5a, 0x31, 0x37],
    [0xf6, 0x30, 0x98, 0x07],
    [0xa8, 0x8d, 0xa2, 0x34],
]

key = [
    [0x2b, 0x28, 0xab, 0x09],
    [0x7e, 0xae, 0xf7, 0xcf],
    [0x15, 0xd2, 0x15, 0x4f],
    [0x16, 0xa6, 0x88, 0x3c],
]

# Standard AES encryption
encrypted_state = AES_encr(AES_state, key)

# Generate the S-Box
sbox = gen_s_box()

# Optimized encryption (SubBytes + ShiftRows)
encrypted_state_optimized = AES_encr_combined_sb_and_sr(AES_state, key)

# Masking analysis
result_with_masking = AES_encr_state_xor_m(AES_state, key)
```

## Theoretical Aspects
The project explores various theoretical topics related to AES:

### Bit and Byte Ordering
Analysis of bit organization within bytes and the use of Big Endian encoding.

### Finite Field Arithmetic
Implementation of operations in GF(2^8) with details on the polynomial interpretation of bytes.

### Linearity Properties
Mathematical study of AES transformations, highlighting which are linear and which are not.

### Side-Channel Attack Resistance
Considerations on alternative AES state organizations to improve resistance against side-channel

# Official AESpaper link : https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf
