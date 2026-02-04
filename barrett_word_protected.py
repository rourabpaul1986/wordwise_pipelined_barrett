import random
import argparse

##########convert Binary################        
    
'''def l_binary(decimal, l):
    """Return binary representation of a number with l bits."""
    binary = bin(decimal)[2:]
    return binary.zfill(l) '''  
def l_binary(decimal, l):
    """
    Return l-bit two's complement binary representation
    (works for positive and negative numbers)
    """
    return format(decimal & ((1 << l) - 1), f'0{l}b')

def flip_random_bits(decimal, l, n):
    """
    Flip n random bits in a length-l binary representation of 'decimal'
    and return the resulting integer.
    """
    bits = list(l_binary(decimal, l))
    # choose n unique bit positions
    positions = random.sample(range(l), n)

    # flip bits
    for pos in positions:
        bits[pos] = '1' if bits[pos] == '0' else '0'
   
    # convert binary string → decimal
    faulty_decimal = int(''.join(bits), 2)

    return faulty_decimal

def generate_n_bit_random_number(n):
    """
    Generate an n-bit random number.

    Args:
    n (int): Number of bits.

    Returns:
    int: A random n-bit number.
    """
    if n <= 0:
        raise ValueError("Number of bits must be a positive integer.")
    
    # Generate a random number in the range [2^(n-1), 2^n - 1]
    lower_bound = 1 << (n - 1)  # Equivalent to 2^(n-1)
    upper_bound = (1 << n) - 1  # Equivalent to 2^n - 1
    
    return random.randint(lower_bound, upper_bound)

#print(f"{n}-bit random number: {random_number}")
def barrett_multiplication_wordwise(a, b, n, l, w, faults, e0, e1, e2, e12, verbose):
    """
    Perform modular multiplication using Barrett Reduction in a wordwise manner.

    Args:
    a (int): First operand (e.g., 16 bits)
    b (int): Second operand (e.g., 16 bits)
    n (int): Modulus
    w (int): Number of bits to process at a time (e.g., 4 bits)

    Returns:
    int: Result of (a * b) % n
    """
    # Precompute mu = floor(2^k / n), where k is the bit-length of n multiplied by 2
    #k = n.bit_length() * 2
    k = l * 2
    mu = (1 << k) // n  # Equivalent to 2^k // n
    if verbose: print(f"mu: {mu}, a:{a}, b:{b}")
    # Break `a` and `b` into chunks of `w` bits
    num_chunks = l // w
    #if a.bit_length() % w != 0:
    #    num_chunks += 1  # Add an extra chunk for remainder bits

    # Initialize result
    result = 0
    acc = 0
    q_fault=0
    r_fault=0
    l1=0
    l2=0
    l12=0
    # Iterate through chunks of `a`
    for i in range(num_chunks):
        aw = (a >> (i * w)) & ((1 << w) - 1)
        #print(f"aw: {aw}, {i}")
        # Iterate through chunks of `b`
        for j in range(num_chunks):
            
            bw = (b >> (j * w)) & ((1 << w) - 1)
            if verbose: print(f"-----------i:{i}, j:{j}--aw: {aw}--bw: {bw}-----------")
            # Step 1: Compute the product for the current chunks
            c = aw * bw
            if verbose: print(f"c:{c}")
            # Align the result by shifting according to the chunk positions
            c <<= (i + j) * w  #c_shift
            cf=flip_random_bits(c, 2*(l//w)+((i + j) * w), 1)
            #print(f"c:{c}, cf: {cf}")
            if verbose: print(f"c:{c} and k:{k}")
            # Step 2: Compute q = floor(c * mu / 2^k) (Barrett pre-reduction)
            q = (c * mu) >> k
            #print(f"c:{c},  q: {q}")
            if cf < q*n or cf >= (q+2)*n:
               q_fault=1
            else : 
               q_fault=0  

               
            if verbose: print(f"c_shitf:{q}")
            # Step 3: Compute r = c - q * n
            r = c - q * n
            
            #Invariant 2: arithmetic consistency
            if (cf - r) % n != 0:
               r_fault = 1
            else:
               r_fault = 0
		 
		 
            # Reduce r modulo n and accumulate the result
            if r >= n:
                result = result + r - n
                l1=1
            else:
                result = result + r  # Just add r if it's already less than n
                l1=0
            if verbose: print(f"T:{r}")
            # Reduce the accumulated result modulo n
            if result >= n:
                result -= n
                l2=1
            else :
                l2=0           
                
                
            if (q_fault | r_fault ) == 1:
               faults+= 1  
               
            if l1==1 and l2==0:
             e1=e1+1
            
            if l2==1 and l1==0:
             e2=e2+1
             
            if l1 == 1 and l2==1:
               e12=e12+ 1  
               
            if l1 == 0 and l2==0:
               e0=e0+ 1  
            
            if verbose: print(f"result:{result}")

    return result, faults, e0, e1, e2, e12

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()
#args.verbose == True
# Example usage
#a = 5792  # 16-bit operand
#b = 1229  # 16-bit operand
l=16
w=8
#n = 72639  # Modulus
#n = 3329  # Modulus
n = generate_n_bit_random_number(l)
#n = 37907  # Modulus

samples = 10

correct = 0
faults = 0
e0 = 0
e1 = 0
e2 = 0
e12 = 0
for i in range(samples):
        a = generate_n_bit_random_number(l)
        b = generate_n_bit_random_number(l)

        res, faults, e0, e1, e2, e12 = barrett_multiplication_wordwise(a, b, n, l, w, faults, e0, e1, e2,e12, args.verbose)
        ref = (a * b) % n

        if res == ref:
            correct += 1
        #if fault:
        #    faults += 1

print(f"Logically Corrected wordiwse barret  results : {correct}/{samples}")
print(f"Accuracy        : {100*correct/samples:.2f}%")
print(f"Faults detected : {100*faults/((l//w)*(l//w)*samples)}%")
print(f"No loop : {100*e0/((l//w)*(l//w)*samples)}%")
print(f"1st loop : {100*e1/((l//w)*(l//w)*samples)}%")
print(f"2nd loop : {100*e2/((l//w)*(l//w)*samples)}%")
print(f"Both loop : {100*e12/((l//w)*(l//w)*samples)}%")
#print(f"Total loop : {e0+e1+e2+e12}")
