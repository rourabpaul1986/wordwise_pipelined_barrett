#!/usr/bin/env python3

import subprocess
import numpy as np
import sys

# ============================================================
# Configuration
# ============================================================
PYTHON = "python3"

#KYBER_SCRIPT = "kyber_ntt.py"   # use absolute path if needed
KYBER_SCRIPT = "dilithium_ntt.py"   # use absolute path if needed
RUNS = 100                     # number of repetitions

# Optional default arguments passed to kyber_ntt.py
DEFAULT_ARGS = [
    "-f", "1"
]

# ============================================================
# Storage arrays
# ============================================================
no_loop = []
loop1 = []
loop2 = []
both_loop = []


# ============================================================
# Statistics helper
# ============================================================
def stats(name, arr):
    arr = np.asarray(arr, dtype=float)

    if arr.size == 0:
        print(f"\n{name}: NO DATA")
        return

    print(f"\n{name}")
    print(f"  Min  : {arr.min():.6f}")
    print(f"  Max  : {arr.max():.6f}")
    print(f"  Mean : {arr.mean():.6f}")
    print(f"  Std  : {arr.std():.6f}")


# ============================================================
# Main loop
# ============================================================
print(f"\nRunning {KYBER_SCRIPT} for {RUNS} runs\n")

for run in range(RUNS):
    print(f"Run {run + 1}/{RUNS}")

    cmd = [PYTHON, KYBER_SCRIPT] + DEFAULT_ARGS

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    # ---- print stderr if something went wrong ----
    if result.stderr.strip():
        print("STDERR:")
        print(result.stderr)

    found = False

    for line in result.stdout.splitlines():
        if line.startswith("RESULT"):
            try:
                _, e0, e1, e2, e12 = line.split()
                no_loop.append(float(e0))
                loop1.append(float(e1))
                loop2.append(float(e2))
                both_loop.append(float(e12))
                found = True
            except ValueError:
                print("Malformed RESULT line:", line)

    if not found:
        print("WARNING: RESULT line not found")
        print("STDOUT was:")
        print(result.stdout)


# ============================================================
# Final statistics
# ============================================================
print("\n================= STATISTICS =================")

stats("No loop", no_loop)
stats("1st loop", loop1)
stats("2nd loop", loop2)
stats("Both loop", both_loop)

print("\n==============================================")
