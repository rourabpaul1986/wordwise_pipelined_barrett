
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


===== END =====
