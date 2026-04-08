

# Kyber NTT in Key Gen without any fault injection

## Generation of S with Python random library
The design was simulated for **10,000** Kyber NTT Run. The total NTT Barrett iteration for 10,000 Kyber is **1,024x10,000**
Here how s is generated as 

```python
from hashlib import shake_128
import hashlib

def cbd_eta(buf, eta, N):
    coeffs = []
    pos = 0
    for _ in range(N):
        a = sum((buf[pos + j] & 1) for j in range(eta))
        b = sum((buf[pos + eta + j] & 1) for j in range(eta))
        coeffs.append(a - b)
        pos += 2 * eta
    return coeffs
def gen_s_vector(sigma, k, eta, N):
    s = []
    for i in range(k):
        shake = hashlib.shake_256(sigma + bytes([i]))
        buf = shake.digest(2 * eta * N)
        s.append(cbd_eta(buf, eta, N))
    return s
```

|# faulty loop| faulty bit | place of fault| type of fault | No reduction (%) |1st reduction (%) |2nd reduction (%) | Both reductions (%) |
|--|--|--|--|--|--|--|--|
