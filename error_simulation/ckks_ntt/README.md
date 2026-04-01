
# CKKS NTT in A generation
## Generation of A with Python random library
The design was simulated for **10,000** falcon-512 NTT Run. The total NTT Barrett iteration for 10,000 CKKS is **12x2048x10,000**
Here how A is generated as 

```python
import secrets
def generate_a_ckks(N, q):
    
 a = [secrets.randbelow(q) for _ in range(N)]
    
 return a
```
Twiddle factors are taken as CKKS standard


## For W-=8 and l=32

|# faulty loop| faulty bit | place of fault| type of fault | No reduction (%) |1st reduction (%) |2nd reduction (%) | Both reductions (%) |
|--|--|--|--|--|--|--|--|
|24576|1|c|random|58.96, 59.36, 59.16, 0.05|0.64, 0.74, 0.69, 0.01|39.91, 40.27, 40.09, 0.05|0.04, 0.08, 0.06, 0.00|
|1024|1|c|random|68.15, 68.50, 68.33, 0.04|0.16, 0.21, 0.18, 0.01|31.31, 31.66, 31.48, 0.04|0.00, 0.01, 0.01, 0.00|
|256|1|c|random|68.47, 68.78, 68.63, 0.04|0.14, 0.19, 0.17, 0.01|31.05, 31.35, 31.20, 0.04|0.00, 0.01, 0.00, 0.00|

===== END =====
