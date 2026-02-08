# Kyber NTT in Key Gen without any fault injection

## Generation of A with Python random library
The design was simulated for **10,000** Kyber NTT Run. The total NTT Barrett iteration for 10,000 Kyber is **1,024x10,000**
Here how A is generated as 

```python
import random
def generate_random_numbers(n, a, b):
    random_numbers = [random.randint(a, b) for _ in range(n)]
    return random_numbers
```
Twiddle factors are taken as Kyber standard

|Kyber NTT (12, 4, 3329)|  # of loop |# of no reduction| # of 1st reduction| # of 2nd reduction | # of both reduction |
|-----------------------|------------|-----------------|-------------------|--------------------|---------------------|
|    min                |            |      74.446     |       0.282       |        22.721      |        0.000        |
|    max                |   1024     |      76.600     |       0.792       |        24.913      |        0.151        |
|    mean               |            |      75.655     |       0.519       |        23.788      |        0.036        |
|    sd                 |            |      0.282      |       0.071       |        0.278       |        0.019        |


| Kyber NTT (12, 6, 3329) | # of loop | # of no reduction | # of 1st reduction | # of 2nd reduction | # of both reduction |
|------------------------|-----------|-------------------|--------------------|--------------------|---------------------|
| min                    |           | 73.168945         | 1.513672           | 20.922852          | 0.024414            |
| max                    | 1024      | 76.757812         | 3.198242           | 24.536133          | 0.561523            |
| mean                   |           | 74.786416         | 2.253311           | 22.724836          | 0.235437            |
| sd                     |           | 0.419047          | 0.213354           | 0.417557           | 0.074523            |

## Generation of A with Kyber Specified XOF
The design was simulated for **10,000** Kyber NTT Run. The total NTT Barrett iteration for 10,000 Kyber is **1,024x10,000**
Here how A is generated as 

```python
def kyber_xof_12bit(seed: bytes, N: int, Q):
    """
    Generate N uniformly random coefficients in [0, 3328]
    using Kyber-style SHAKE128 XOF and 12-bit rejection sampling.
    
    Args:
        seed (bytes): input seed (typically rho || i || j)
        N (int): number of coefficients to generate
    
    Returns:
        list[int]: N coefficients modulo q
    """
    shake = shake_128(seed)
    coeffs = []

    buffer = bytearray()
    pos = 0

    while len(coeffs) < N:
        # Ensure enough bytes (3 bytes -> 2 x 12-bit values)
        if pos + 3 > len(buffer):
            buffer.extend(shake.digest(168))  # absorb more
            pos = 0

        # Extract two 12-bit values from 3 bytes
        b0 = buffer[pos]
        b1 = buffer[pos + 1]
        b2 = buffer[pos + 2]
        pos += 3

        d0 = b0 | ((b1 & 0x0F) << 8)
        d1 = (b1 >> 4) | (b2 << 4)

        if d0 < Q:
            coeffs.append(d0)
            if len(coeffs) == N:
                break
        if d1 < Q:
            coeffs.append(d1)

    return coeffs
```

| Kyber NTT (12, 4, 3329) | # of loop| No reduction (%) | 1st reduction (%) | 2nd reduction (%) | Both reductions (%) |
|------|------------------|-----------|-------------------|-------------------|---------------------|
| Min  | |74.6419 | 0.2062 | 22.7865 | 0.0000 |
| Max  | 1024|76.6493 | 0.8138 | 24.7938 | 0.1302 |
| Mean | |75.6566 | 0.5199 | 23.7874 | 0.0361 |
| sd  | |0.2812  | 0.0720 | 0.2776  | 0.0199 |

| Kyber NTT (12, 6, 3329) | # of loop | # of no reduction | # of 1st reduction | # of 2nd reduction | # of both reduction |
|------------------------|-----------|-------------------|--------------------|--------------------|---------------------|
| min  |           | 73.193359 | 1.562500 | 20.849609 | 0.024414 |
| max  | 1024      | 76.464844 | 3.125000 | 24.414062 | 0.537109 |
| mean |           | 74.775879 | 2.256665 | 22.732175 | 0.235281 |
| sd   |           | 0.425958  | 0.214496 | 0.419349  | 0.074882 |



| Kyber NTT (12, 12, 3329)  |  # of loop | No reduction (%) | 1st reduction (%) | 2nd reduction (%) | Both reductions (%) |
|------|--|------------------|-------------------|-------------------|---------------------|
| Min|  | 86.5234 | 6.7383 | 0.0000 | 0.0000 |
| Max|1024  | 93.2617 | 13.4766 | 0.0000 | 0.0000 |
| Mean| | 90.1225 | 9.8775 | 0.0000 | 0.0000 |
| Std|  | 0.8970  | 0.8970 | 0.0000 | 0.0000 |

# Kyber (l=12, w=4 )NTT in Key Gen with fault injection

|# faulty loop| faulty bit | place of fault| type of fault | No reduction (%) |1st reduction (%) |2nd reduction (%) | Both reductions (%) |
|--|--|--|--|--|--|--|--|
|x|0|x|X|74.64, 76.65, 75.66, 0.28|0.20, 0.81, 0.52, 0.07|22.79, 24.79, 23.79, 0.28|0.00, 0.13, 0.04, 0.02|
|1024|1|c|random|55.79, 58.55, 57.21, 0.35|2.35, 3.63, 2.98, 0.17|38.06, 41.01, 39.46, 0.35|0.13, 0.56, 0.33, 0.06|
|512|1|c|random|64.93, 67.87, 66.44, 0.36|1.26, 2.29, 1.75, 0.13|30.08, 33.08, 31.63, 0.37|0.04, 0.41, 0.18, 0.04|
|256|1|c|random|69.80, 72.50, 71.05, 0.34|0.72, 1.56, 1.14, 0.11|26.11, 28.96, 27.71, 0.35|0.01, 0.26, 0.11, 0.03|
|128|1|c|random|72.03, 74.59, 73.35, 0.31|0.43, 1.23, 0.83, 0.09|24.51, 27.05, 25.75, 0.32|0.00, 0.20, 0.07, 0.03|
|64|1|c|random|73.22, 75.59, 74.50, 0.30|0.36, 1.01, 0.67, 0.08|23.67, 26.03, 24.77, 0.30|0.00, 0.16, 0.05, 0.02|
|1024|2|c|random|48.97, 51.68, 50.29, 0.35|4.95, 7.06, 6.00, 0.25|41.64, 44.21, 42.94, 0.35|0.49, 1.09, 0.77, 0.09|
|512|2|c|random|61.57, 64.57, 62.97, 0.38|2.65, 4.01, 3.26, 0.18|31.90, 34.73, 33.37, 0.39|0.17, 0.65, 0.40, 0.07|
|256|2|c|random|68.08, 70.81, 69.32, 0.36|1.42, 2.38, 1.89, 0.14|27.06, 29.87, 28.58, 0.36|0.04, 0.40, 0.22, 0.05|
|128|2|c|random|71.28, 73.62, 72.49, 0.33| 0.85, 1.62, 1.20, 0.11|25.02, 27.39, 26.18, 0.33|0.02, 0.29, 0.13, 0.04|
|64|2|c|random|72.96, 75.17, 74.07, 0.31|0.53, 1.24, 0.86, 0.09|23.87, 26.09, 24.99, 0.31|0.00, 0.22, 0.08, 0.03|
