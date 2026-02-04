# Barrett Reduction Pipeline for Modular Arithmetic

## Overview

This repository contains a **pipelined hardware implementation of Barrett Reduction** for efficient modular arithmetic on FPGAs. Barrett reduction is commonly used in **modular multiplication and exponentiation**, and is a core arithmetic primitive in **lattice-based Post-Quantum Cryptography (PQC)** schemes such as Kyber and Dilithium.

The design focuses on **high throughput**, **deterministic latency**, and **hardware efficiency**, making it suitable for cryptographic accelerators and fault-analysis studies.

---

## Key Features

- Fully **pipelined Barrett reduction architecture**
- Parameterizable modulus and operand bit-width
- Suitable for **NTT, modular multiplication, and modular exponentiation**
- Synthesizable RTL design
- Optimized for **Xilinx Artix-7 FPGA**
- Clean stage-wise pipeline structure for timing closure

---

## Barrett Reduction Algorithm

For an integer `x` and modulus `n`, Barrett reduction computes:

