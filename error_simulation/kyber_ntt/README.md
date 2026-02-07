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
|1024|1|c|random|55.79, 58.55, 57.21, 0.35|2.35, 3.63, 2.98, 0.17|38.06, 41.01, 39.46, 0.35|0.13, 0.56, 0.33, 0.06|
|512|1|c|random|64.93, 67.87, 66.44, 0.36|1.26, 2.29, 1.75, 0.13|30.08, 33.08, 31.63, 0.37|0.04, 0.41, 0.18, 0.04|
|512|1|c|random|||||
