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

| Kyber NTT (12, 4, 3329) | # of loop| No reduction (%) | 1st reduction (%) | 2nd reduction (%) | Both reductions (%) |
|------|------------------|-----------|-------------------|-------------------|---------------------|
| Min  | |74.6419 | 0.2062 | 22.7865 | 0.0000 |
| Max  | 1024|76.6493 | 0.8138 | 24.7938 | 0.1302 |
| Mean | |75.6566 | 0.5199 | 23.7874 | 0.0361 |
| sd  | |0.2812  | 0.0720 | 0.2776  | 0.0199 |

