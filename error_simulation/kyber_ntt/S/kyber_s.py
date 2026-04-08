import math
import random
import numpy as np
import ast
import random
import time
import os
import sys
import argparse
import threading
from lib_fault import *
##################################################################################
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



def barrett_multiplication_wordwise(a, b, n, l, w, f,  e0, e1, e2, e12, q_fault, r_fault, p, mode, injection, verbose):
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
    #print(f"mode: {mode[0]}")
    # Precompute mu = floor(2^k / n), where k is the bit-length of n multiplied by 2
    #k = n.bit_length() * 2
    k = l * 2
    x=0
    mu = (1 << k) // n  # Equivalent to 2^k // n
    if verbose: print(f"mu: {mu}, a:{a}, b:{b}")
    # Break `a` and `b` into chunks of `w` bits
    num_chunks = l // w
    #if a.bit_length() % w != 0:
    #    num_chunks += 1  # Add an extra chunk for remainder bits
    
    # Initialize result
    
    result = 0
    resultf = 0
    acc = 0
    #q_fault=0
    #r_fault=0
    l1=0
    l2=0
    l12=0
    #print(f"p: {p}")
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
            
            if p %2==1 and mode[0]=="c":
                 if(injection=="r"):
             	        c=flip_random_bits(c, k, f)
	                #c=flip_random_bits(c, ((i + j) * w)+2*w, f)
             	        print("random")
                 elif(injection=="b"):
                         c=flip_burst_bits(c, k, f)
            elif mode[0]=="x":
                 c=c
            elif mode[0]!="x" and mode[0]!="c":
                sys.exit(f"{mode[0]} is wrong fault mode, command should be -m pxx")
           
            
            #print(f"hamming_distance:{hamming_distance(c, cf)}")
            #if verbose: print(f"c:{c} and k:{k}")
            # Step 2: Compute q = floor(c * mu / 2^k) (Barrett pre-reduction)
            q = (c * mu) >> k
            
            #print(f"p in binary: {bin(p)[2:]}")
            if p%2==1 and mode[1]=="q":
                 if(injection=="r"):
             	        q=flip_random_bits(q, k, f)
             	        
                 elif(injection=="b"):
                         q=flip_burst_bits(q, k, f)
            elif mode[1]=="x":
                 q=q
            elif mode[1]!="x" and mode[1]!="q":
                #print(f"p for q: {p}")
                sys.exit(f"{mode[1]} is wrong fault mode, command should be -m xqx")
             
             
            if c < q*n or c >= (q+2)*n:
               q_fault=q_fault+1
            #else : 
            #   q_fault=0 

               
            if verbose: print(f"c_shitf:{q}")
            # Step 3: Compute r = c - q * n
            r = c- q * n
            
            
            if p %2==1 and mode[2]=="r":
                 if(injection=="r"):
             	        r=flip_random_bits(r, l, f)
                 elif(injection=="b"):
                         r=flip_burst_bits(r, l, f)
            elif mode[2]=="x":
                 r=r
            elif mode[2]!="x" and mode[2]!="r":
                #print(f"p for q: {p}")
                sys.exit(f"{mode[2]} is wrong fault mode, command should be -m xxxr")   
            
            #Invariant 2: arithmetic consistency
            if (c - r) % n != 0:
               r_fault = r_fault+1
            #else:
            #   r_fault = 0
		 
            #r=flip_random_bits(r, l, f)
            # Reduce r modulo n and accumulate the result
            if r >= n:
                result = result + r - n
                l1=1
            else:
                result = result + r  # Just add r if it's already less than n
                l1=0
            
            # Reduce the accumulated result modulo n
            if result >= n:
                result -= n
                l2=1
            else :
                l2=0           
                
                

            if l1==1 and l2==0:
             e1=e1+1
            
            if l2==1 and l1==0:
             e2=e2+1
             
            if l1 == 1 and l2==1:
               e12=e12+ 1  
               
            if l1 == 0 and l2==0:
               e0=e0+ 1  
            
            #if (q_fault | r_fault ) == 1:
            #   faults+= 1  
               
            if verbose: print(f"result:{result}")
            x=x+1
            #result=flip_random_bits(result, l, f)
    p=p>>1    
    return result, e0, e1, e2, e12, p, q_fault, r_fault

###########################################################################################

def rule_check(l, w, N):
    if(l%w!=0):
     print(f"Error: l={l} must be divisible by w={w}")
     sys.exit(1)  # Exit with a non-zero status code indicating an error.
    
    n=math.ceil(math.log2(N))
    #print(f"n={n} l={l}")
    if(l<=n):
     print(f"Error: l={l} must be grater than the number of binary bit required by N={N}")
     sys.exit(1)  # Exit with a non-zero status code indicating an error.


def l_binary(decimal, l):
 binary = bin(decimal)[2:]
 binary = binary.zfill(l) 
 #print(f"{l} bit Binary representation of {decimal} is {binary}")
 return binary

def generate_random_numbers(n, a, b):
    random_numbers = [random.randint(a, b) for _ in range(n)]
    return random_numbers




def modmult(a, b, M):
    return (a * b) % M

def modpow(alpha, n, M):
    if n == 0:
        return 1
    p = 1
    bn = bin(n)
    for b in bn[2:]:
        p = modmult(p, p, M)
        if b == '1':
            p = modmult(p, alpha, M)
    return p

def is_primitive(alpha, N, M):
    for i in range(1, N):
        if modpow(alpha, i, M) == 1:
            return False
    return modpow(alpha, N, M) == 1

def find_primitive(N, M):
    for alpha in range(2, M):
        if is_primitive(alpha, N, M):
            return alpha
    return 0

def findinv(alpha, M):
    for i in range(M):
        if modmult(alpha, i, M) == 1:
            return i

def bit_reverse(x, n):
    if type(x) == int:
        b = '{:0{width}b}'.format(x, width=n)
        return int(b[::-1], 2)
    else:
        x_out = np.zeros(len(x), dtype=int)
        for i in range(len(x)):
            x_out[i] = x[bit_reverse(i, n)]
        return x_out

def CT_Butterfly(i,j,n,x_out, A, twiddle_factor, M, length, f, l, w, array,  e0, e1, e2,e12, q_fault, r_fault, p, mode, injection, verbose):

    if length <= 1:
        x_out[0] = A[0]
        return x_out
    halflen = length >> 1
    #q_fault=0
    #r_fault=0
    for k in range(halflen):
        u = A[k]
        #v = modmult(A[k + halflen], twiddle_factor, M) # this line should be on for school book multiplication
        #if verbose: print (f"i:{i}, j:{j}, k:{k}, n:{n}, x_out{x_out}")
        if verbose: print (f"i:{i}, j:{j}, k:{k}")
        if verbose: print(f"twiddle_factorrr:{twiddle_factor}\t A[k + halflen]:{A[k + halflen]}")
        array[k+j*length]=array[k+j*length]+1
        array[k+halflen+j*length]=array[k+halflen+j*length]+1
        
        #p=p+1
        v, e0, e1, e2, e12, p, q_fault, r_fault = barrett_multiplication_wordwise(A[k + halflen], twiddle_factor, M, l, w, f,  e0, e1, e2, e12, q_fault, r_fault, p, mode, injection, verbose)
        x_out[k] = (u + v) % M
        x_out[k + halflen] = (u - v) % M
        #print(f"A:={x_out} \t A[k]:{x_out[k]}, A[k+halflen]:{x_out[k+halflen]}, i:{i}, j:{j}, k:{k+j*length}, k + halflen: {k + halflen+j*length}, w={twiddle_factor}, U={u}, V={v}, lenghth={length}")
    return array,  e0, e1, e2, e12, p, q_fault, r_fault

class fNTT:
    def __init__(self, N, M, alpha=None):
        self.N = N  # Degree of Polynomial 
        self.M = M
        self.Nlen = int(np.log2(N))
        #print(M)
        self.Ninv = findinv(self.N, self.M)
        if alpha is not None and not is_primitive(alpha, N, M):
            raise ValueError('Given alpha is not primitive')
        self.alpha = alpha or find_primitive(N, M)
        if self.alpha == 0:
            raise ValueError('No primitive root exists')
        if verbose: print(f"initial omega (nth root of unity): {self.alpha}")
        self.alpha_modpow_table = [modpow(self.alpha, i, M) for i in range(N+1)]
        self.bit_reverse_table = [bit_reverse(i, self.Nlen - 1) for i in range(N // 2)]
        if verbose: print(f"self.bit_reverse_table :{self.bit_reverse_table} self.Nlen:{self.Nlen}")
        if verbose:  print(f"twiddle factors :{self.alpha_modpow_table}")
    def forward(self, x_in, N, f, l, w,  e0, e1, e2, e12, q_fault, r_fault, p, mode, injection, verbose=False):
        #q_fault=0
        #r_fault=0       
        if len(x_in) != self.N:
            raise ValueError(f'Input should be sized {self.N}')
        x = np.copy(x_in)
        array=N*[0]
        for i in range(self.Nlen):
            n = 1 << i
            seqlen = self.N // n
            for j in range(n):
                twiddle_factor = self.alpha_modpow_table[self.bit_reverse_table[j] ]
                if verbose:print(f"ct omega forward: {twiddle_factor} j:{j}")
                
                array,  e0, e1, e2,e12, p, q_fault, r_fault=CT_Butterfly(i,j,n,x[seqlen * j: seqlen * (j + 1)], x[seqlen * j: seqlen * (j + 1)], twiddle_factor, self.M, seqlen, f, l, w, array,  e0, e1, e2,e12, q_fault, r_fault, p, mode, injection, verbose)
              
        #print(f"array: {array}")
        #print("--------------------")    
        return bit_reverse([i % self.M for i in x], self.Nlen),  e0, e1, e2,e12, p, q_fault, r_fault

    def inverse(self, x_in, N, f, l, w, e0, e1, e2, e12, q_fault, r_fault, p, mode, injection, verbose=False):
        #q_fault=0
        #r_fault=0 
        if len(x_in) != self.N:
            raise ValueError(f'Input should be sized {self.N}')
        x = np.copy(x_in)
        array=N*[0]
        for i in range(self.Nlen):
            n = 1 << i
            seqlen = self.N // n
            for j in range(n):
                twiddle_factor = self.alpha_modpow_table[(self.N - self.bit_reverse_table[j]) ]
                
                #twiddle_factor = self.alpha_modpow_table[self.N - self.bit_reverse_table[j]]
                array, e0, e1, e2, e12, p, q_fault, r_fault =CT_Butterfly(i,j,n,x[seqlen * j: seqlen * (j + 1)], x[seqlen * j: seqlen * (j + 1)], twiddle_factor, self.M, seqlen, f, l, w, array, e0, e1, e2,e12, q_fault, r_fault, p, mode, injection, verbose)
                  
        x = [modmult(i, self.Ninv, self.M) for i in x]
        return bit_reverse(x, self.Nlen),  e0, e1, e2,e12, p, q_fault, r_fault
def check_arrays(array1, array2):
    if len(array1) != len(array2):
        print(f"Wrong: Arrays have different lengths. {len(array1)} {len(array2)}")
        return False
    for i in range(len(array1)):
        if array1[i] != array2[i]:
            print(f"Wrong: Elements at index {i} are different ({array1[i]} != {array2[i]}).")
            return False
    print("Bingo !!  All elements match.")
    return True
if __name__ == "__main__":
    #N = 256  # Size of the input sequence, must be a power of 2, degree of polynomial 
    #M = 3329  # A prime number for modulus
    
    correct = 0
    faults = 0
    p_faults = 0
    e0 = 0
    e1 = 0
    e2 = 0
    e12 = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fault", type=int, default=1, required=False,
                        help="Number of Faulty bits (integer value)")
    parser.add_argument("-fl", "--faulty_loop", type=int, default=1024, required=False,
                        help="number of NTT loops affected by fault ")
    parser.add_argument("-i", "--injection", type=str, default="r", required=False,
                        help="fault injection type: random/burts")
    parser.add_argument("-m", "--mode", type=str,  default="xxr", required=False,
                        help="fault injected operations")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose mode")
    parser.add_argument("-c", "--chunk", type=int, required=False,
                        help="Number of partitions (integer value)")
    parser.add_argument("-l", "--length", type=int, default=12, required=False,
                        help="Number of partitions (integer value)")
    parser.add_argument("-w", "--wordsize", type=int, default=4, required=False,
                        help="Number of partitions (integer value)")
    parser.add_argument("-N", "--degree", type=int, default=256, required=False,
                        help="Number of partitions (integer value)")
    parser.add_argument("-M", "--mod", type=int, default=3329, required=False,
                        help="Number of partitions (integer value)")
    args = parser.parse_args()
    verbose = args.verbose
    f = args.fault
    injection = args.injection
    mode = args.mode
    fl = args.faulty_loop
    chunk = args.chunk
    l = args.length
    w = args.wordsize
    N = args.degree
    M = args.mod
    total_loop=int(np.log2(N))*(N//2)
    ntt = fNTT(N, M)
    #l = 12 #lenth of binary bits
    #w = 4  # how many binary bits will be processed
    seed="abcde"
    sample_size=int(math.log2(N))*N/2
    #A = generate_random_numbers(N, 0, M-1)
    sigma = os.urandom(32)  # Kyber seed
    k = 3                  # Kyber-512 → k=2, Kyber-768 → k=3, Kyber-1024 → k=4
    eta = 2                # depends on parameter set
    

    S = gen_s_vector(sigma, k, eta, N)
    S_hw = [x % M for x in S[0]]
    A=S_hw
    faults = 0
    p=0
    q_fault=0
    r_fault=0
    q_val=0
    p=flip_random_bits(p, total_loop , fl)
    ntt_A, e0, e1, e2, e12, p, q_fault, r_fault = ntt.forward(A, N, f, l, w,  e0, e1, e2, e12, q_fault, r_fault, p,  mode, injection, verbose=verbose)
    #print(f"p: {p}")
    #print(f"Forward NTT of A: {ntt_A}")
    if not (e0> e2 > e1> e12) : 
            p_faults=p_faults+1
     
    e0_val=100*e0/((l//w)*(l//w)*sample_size)
    e1_val=100*e1/((l//w)*(l//w)*sample_size)
    e2_val=100*e2/((l//w)*(l//w)*sample_size)
    e12_val=100*e12/((l//w)*(l//w)*sample_size)
    q_val=100*q_fault/((l//w)*(l//w)*sample_size)
    r_val=100*r_fault/((l//w)*(l//w)*sample_size)
    print(f"No loop : {e0_val}%")
    print(f"1st loop : {e1_val}%")
    print(f"2nd loop : {e2_val}%")
    print(f"Both loop : {e12_val}%")
    print(f"q_fault : {q_val}%")
    print(f"r_fault : {r_val}%")
    print(f"Efficiency of Probabilistic  : {p_faults}")
    print(f"You have entered faults in {fl} loops out of {total_loop}, fault insertion place: {mode}")
    e0 = 0
    e1 = 0
    e2 = 0
    e12 = 0
    q_fault=0
    r_fault=0
    inv_ntt_A,  e0, e1, e2,e12, p, q_fault, r_fault = ntt.inverse(ntt_A,N,f, l, w, e0, e1, e2,e12, q_fault, r_fault, p, mode, injection, verbose=verbose)
    #print(f"Inverse NTT A: {inv_ntt_A}")
    check_arrays(inv_ntt_A, A)
    print(f"RESULT {e0_val} {e1_val} {e2_val} {e12_val} {q_val}")
