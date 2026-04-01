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


|Application | application, l,w,q | LUTs | FF | Slice | DSP | Power (mw) | CC | CP(ns)| CLK(MHz) |
|------------|--------------------|------|----|-------|-----|------------| ---|-------|-----|
|BMM         | Kyber, 12, 4,3329  | 100  | 47 |   38  |  2  |  106       | 10  |  9.46 | 100 |
|BMM +SRM    | Kyber, 12, 4,3329  | 163  | 156|   83  |  2  |  107       | 10  |  9.33 | 100 |
|BMM  | Kyber, 12, 6, 3329 | 113  | 47 |   43  |  2  |  108       | 5  |  9.32  |100  |
|BMM   | Kyber, 12, 12, 3329| 31   | 26 |   13  |  5  |  106       | 2  |  11.67 |83|
|BMM   | CKKS, 32, 8, 1811939329 | 234  | 84 |  74   |  3  |  130   | 17  |  8.78 |100|
|BMM   | CKKS, 32, 16, 1811939329 | 184  | 44 |  76  |  4  |  131  | 5  |  8.71 |100|
|BMM   | CKKS, 32, 32, 1811939329 | 163  | 66 |  52  |  6  |  131  | 2  |  8.36 |100|

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

