# Barrett Modular Multiplication

## Overview

This repository contains a **pipelined hardware implementation of Barrett Modular Multiplication** for efficient modular arithmetic on FPGAs. Barrett Modular Multiplication is commonly used in **modular multiplication and exponentiation**, and is a core arithmetic primitive in **lattice-based Post-Quantum Cryptography (PQC)** schemes such as Kyber and Dilithium.

The design focuses on **high throughput**, **deterministic latency**, and **hardware efficiency**, making it suitable for cryptographic accelerators and fault-analysis studies.

---

## Key Features

- Fully **pipelined Barrett Modular Multiplication architecture**
- Parameterizable modulus and operand bit-width
- Suitable for **NTT, modular multiplication, and modular exponentiation**
- Synthesizable RTL design
- Optimized for **Xilinx Artix-7 FPGA**
- Clean stage-wise pipeline structure for timing closure

---

## Barrett Modular Multiplication Algorithm

For an integer `a` and `b` and modulus `n`, Barrett reduction computes:


where:
- `μ = ⌊2^k / n⌋`
- `k` is chosen based on operand size

This avoids expensive division and enables efficient hardware implementation.

---

## Pipeline Architecture

The design is organized into multiple pipeline stages:

1. Partial multiplication
2. Shift and truncation
3. Intermediate subtraction
4. Final correction stage

Each stage is fully registered to maximize clock frequency.

---

## Resource Utilization

The design was synthesized using **Xilinx Vivado** targeting an **Artix-7 FPGA**.


|Application |      l,w,q     | LUTs | FF | Slice | DSP | Power (mw) | CC | CP(ns)| 
|------------|----------------|------|----|-------|-----|------------| ---|-------|
|            | 12, 4, 3329    | 100  | 47 |   31  |  2  |  99       | 9  |  9.84 |
|  Kyber     | 12, 6, 3329    | 109  | 47 |   41  |  2  |  99       | 4  |  9.02 |
|            | 12, 12, 3329   | 31  | 13 |   17  |  5  |  100      | 4  |  6.99 |
|  Dilithium | 24, 4, 8380417 | 273  | 108|   97  |  4  |  116       | 36 | 12.85 |
|            | 24, 6, 8380417 | 290  |174 |  108  |  4  |  119       | 16 | 12.7  |
|            | 24, 8, 8380417 | 308  |108 |  99   |  4  |  119       | 9  | 12.68 |
|            | 24, 12, 8380417| 201  |154 |  85   |  5  |  120       | 4  | 12.62 |

> **Note:** Replace `XXX` with post-synthesis values from Vivado.

| Parameter | LUTs | Slices |
|----------|------|--------|
| Barrett Pipeline (Baseline) | XXX | XXX |
| With Fault Detection | XXX | XXX |
| With Full Pipelining | XXX | XXX |

> **Note:** Replace `XXX` with post-synthesis values from Vivado.

---

## Performance Summary

| Metric | Value |
|------|------|
| Clock Frequency | XXX MHz |
| Latency | XXX cycles |
| Throughput | 1 result / cycle (after pipeline fill) |

---

## Directory Structure

