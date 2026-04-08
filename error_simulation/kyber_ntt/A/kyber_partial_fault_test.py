#!/usr/bin/env python3

import subprocess
import numpy as np
import sys
import time
from multiprocessing import Pool, cpu_count

# ============================================================
# Configuration
# ============================================================
PYTHON = "python3"
mode = "xxr"
injection = "b"
SCRIPT = "kyber.py"   # adjust path if needed

RUNS = 10000          # repetitions per (f, fl)
F_VALUES = range( 1, 4)         # f = 1..6
FL_VALUES = [ 64 ]

OUT_FILE_latex = f"{SCRIPT[0:-3]}_latex_{mode}_{injection}.txt"
OUT_FILE_git = f"{SCRIPT[0:-3]}_git_{mode}_{injection}.txt"
'''BASE_ARGS = [
    "-m", mode",
    "-i", injection,
    "-l", "16",
    "-w", "4",
    "-N", "512",
    "-M", "12289",
]'''

'''BASE_ARGS = [
    "-m", "xqx",
    "-i", "r",
    "-l", "32",
    "-w", "8",
    "-N", "4096",
    "-M", "1811939329",
]'''

BASE_ARGS = [
    "-m", mode,
    "-i", injection,
    "-l", "12",
    "-w", "4",
    "-N", "256",
    "-M", "3329",
]
# ============================================================
# Worker function
# ============================================================
def run_one(cmd):
    """
    Run one kyber_ntt.py execution and extract RESULT values.
    Returns tuple (e0, e1, e2, e12) or None.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        for line in result.stdout.splitlines():
            if line.startswith("RESULT"):
                _, e0, e1, e2, e12, q_fault = line.split()
                return float(e0), float(e1), float(e2), float(e12), float(q_fault)

    except Exception as e:
        return None

    return None


# ============================================================
# Statistics helper
# ============================================================
def compute_stats(arr):
    arr = np.asarray(arr, dtype=float)
    return arr.min(), arr.max(), arr.mean(), arr.std()


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":

    nproc = cpu_count()
    print(f"\nUsing {nproc} CPU cores")

    with open(OUT_FILE_latex, "w") as fout_latex, open(OUT_FILE_git, "w") as fout_git:
        fout_latex.write(f"===== {SCRIPT} NTT Statistics =====\n\n")
        fout_git.write(f"===== {SCRIPT} NTT Statistics =====\n\n")

        for f in F_VALUES:
            for fl in FL_VALUES:

                print(f"\nRunning f={f}, fl={fl}")

                # Storage
                no_loop = []
                loop1 = []
                loop2 = []
                both_loop = []
                qfault_list = []

                # Build command list
                cmds = []
                for _ in range(RUNS):
                    cmd = [
                        PYTHON,
                        SCRIPT,
                        "-f", str(f),
                        "-fl", str(fl),
                    ] + BASE_ARGS
                    cmds.append(cmd)

                total = len(cmds)
                start = time.time()

                # Run in parallel
                with Pool(processes=nproc) as pool:
                    for idx, res in enumerate(pool.imap_unordered(run_one, cmds), 1):

                        if res is not None:
                            e0, e1, e2, e12,  q_val = res
                            no_loop.append(e0)
                            loop1.append(e1)
                            loop2.append(e2)
                            both_loop.append(e12)
                            qfault_list.append(q_val)

                        # ---- progress every 100 runs ----
                        if idx % 100 == 0 or idx == total:
                            elapsed = time.time() - start
                            rate = idx / elapsed if elapsed > 0 else 0
                            eta = (total - idx) / rate if rate > 0 else 0
                            print(
                                f"  Progress: {idx}/{total} | ETA {eta:6.1f}s",
                                end="\r"
                            )

                print()  # newline after progress

                # ---- compute stats ----
                nmin, nmax, nmean, nstd = compute_stats(no_loop)
                l1min, l1max, l1mean, l1std = compute_stats(loop1)
                l2min, l2max, l2mean, l2std = compute_stats(loop2)
                bmin, bmax, bmean, bstd = compute_stats(both_loop)
                qmin, qmax, qmean, qstd = compute_stats(qfault_list)
                count0 = sum(1 for x in no_loop if x < 74.64 or x > 76.65)
                count1 = sum(1 for y in loop1 if y < 0.20 or y > 0.81)
                count2 = sum(1 for z in loop2 if z < 22.79 or z > 24.79)
                # ---- print ----
                print(f"  No loop   : {nmin:.2f}, {nmax:.2f}, {nmean:.2f}, {nstd:.2f}")
                print(f"  1st loop  : {l1min:.2f}, {l1max:.2f}, {l1mean:.2f}, {l1std:.2f}")
                print(f"  2nd loop  : {l2min:.2f}, {l2max:.2f}, {l2mean:.2f}, {l2std:.2f}")
                print(f"  Both loop : {bmin:.2f}, {bmax:.2f}, {bmean:.2f}, {bstd:.2f}")
                print(f"count:{count0}, {count1}, {count2}")
                # ---- write to file ----
                #mode = "c"          # or parse from BASE_ARGS if you want
                if(injection=="r"):
                 inj  = "random"
                elif(injection=="b"):
                 inj="burst"
                else:
                 inj="unknown"

                fout_git.write(
                  f"|{fl}|{f}|{mode}|{inj}|"
                  #f"{qmin:.2f}, {qmax:.2f}, {qmean:.2f}, {qstd:.2f}|"
                  f"{nmin:.2f}, {nmax:.2f}, {nmean:.2f}, {nstd:.2f}|"
                  f"{l1min:.2f}, {l1max:.2f}, {l1mean:.2f}, {l1std:.2f}|"
                  f"{l2min:.2f}, {l2max:.2f}, {l2mean:.2f}, {l2std:.2f}|"
                  f"{bmin:.2f}, {bmax:.2f}, {bmean:.2f}, {bstd:.2f}|\n"
                )

                fout_latex.write(
                  f"{fl}&{f}&"
                  #f"{qmin:.2f}--{qmax:.2f} &"
                  f"{nmin:.2f}--{nmax:.2f} &"
                  f"{l1min:.2f}--{l1max:.2f}&"
                  f"{l2min:.2f}--{l2max:.2f}&"
                  f"{bmin:.2f}, {bmax:.2f}\n"
                )

        fout_latex.write("\n===== END =====\n")
        fout_git.write("\n===== END =====\n")
    
    print(f"\nAll results saved to {OUT_FILE_latex}")
    print(f"\nAll results saved to {OUT_FILE_git}")
