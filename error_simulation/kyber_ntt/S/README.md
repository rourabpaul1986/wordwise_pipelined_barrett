

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
|x|0|cxx|random|77.66, 80.41, 78.95, 0.38|0.14, 0.61, 0.36, 0.06|19.18, 21.91, 20.61, 0.39|0.00, 0.24, 0.08, 0.04|
|1024|1|cxx|random|56.11, 58.72, 57.34, 0.36|2.31, 3.57, 2.90, 0.17|38.24, 40.87, 39.44, 0.36|0.14, 0.60, 0.33, 0.06|
|512|1|cxx|random|65.49, 68.58, 67.00, 0.40|1.16, 2.22, 1.65, 0.13|29.61, 32.76, 31.17, 0.40|0.05, 0.37, 0.18, 0.04|
|128|1|cxx|random|73.81, 76.81, 75.29, 0.41|0.41, 1.09, 0.70, 0.08|22.41, 25.55, 23.92, 0.42|0.00, 0.26, 0.09, 0.03|
|64|1|cxx|random|75.42, 78.50, 76.95, 0.41|0.29, 0.82, 0.54, 0.07|20.93, 23.87, 22.43, 0.41|0.00, 0.25, 0.08, 0.04|
|1024|2|cxx|random|48.81, 51.43, 50.29, 0.35|5.10, 6.88, 5.95, 0.25|41.80, 44.39, 42.99, 0.35|0.47, 1.17, 0.77, 0.09|
|512|2|cxx|random|61.39, 64.89, 63.37, 0.41|2.47, 3.99, 3.20, 0.18|31.62, 34.67, 33.04, 0.42|0.17, 0.68, 0.40, 0.07|
|128|2|cxx|random|72.79, 75.97, 74.34, 0.42|0.73, 1.55, 1.10, 0.10|22.91, 26.12, 24.42, 0.42|0.02, 0.35, 0.15, 0.04|
|64|2|cxx|random|74.87, 78.09, 76.48, 0.42|0.47, 1.04, 0.74, 0.09|21.14, 24.28, 22.68, 0.42|0.00, 0.27, 0.11, 0.04|
|1024|3|cxx|random|45.66, 48.32, 46.97, 0.34|7.44, 9.60, 8.53, 0.29|41.95, 44.43, 43.28, 0.35|0.81, 1.63, 1.23, 0.11|
|512|3|cxx|random|60.12, 63.30, 61.69, 0.41|3.73, 5.28, 4.49, 0.21|31.52, 34.71, 33.18, 0.42|0.36, 0.97, 0.63, 0.08|
|128|3|cxx|random|72.41, 75.42, 73.91, 0.43|1.01, 1.89, 1.43, 0.12|22.91, 26.00, 24.46, 0.43|0.07, 0.42, 0.21, 0.05|
|64|3|cxx|random|74.91, 77.97, 76.26, 0.42|0.51, 1.28, 0.90, 0.10|21.08, 24.16, 22.70, 0.42|0.02, 0.33, 0.14, 0.04|
