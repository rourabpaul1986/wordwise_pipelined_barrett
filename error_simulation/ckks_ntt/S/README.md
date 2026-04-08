
# CKKS NTT in S generation
## Generation of S with Python random library
The design was simulated for **10,000** falcon-512 NTT Run. The total NTT Barrett iteration for 10,000 CKKS is **12x2048x10,000**
Here how A is generated as 

```python
from hashlib import shake_128

import random

def generate_sparse_s(N, q,  h=64):
    s = [0] * N
    indices = random.sample(range(N), h)

    for i in indices[:h//2]:
        s[i] = 1
    for i in indices[h//2:]:
        s[i] = -1
    s_mod = [x % q for x in s]
    return s_mod

```
Twiddle factors are taken as CKKS standard


## For W-=8 and l=32

|# faulty loop| faulty bit | place of fault| type of fault | No reduction (%) |1st reduction (%) |2nd reduction (%) | Both reductions (%) |
|--|--|--|--|--|--|--|--|
|x|0|xxr|x|80.06, 83.81, 81.39, 0.46|0.07, 0.11, 0.09, 0.01|16.11, 19.85, 18.52, 0.46|0.00, 0.01, 0.00, 0.00|

