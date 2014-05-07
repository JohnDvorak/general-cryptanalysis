#! usr/bin/python3
import math
import random
from fractions import gcd
# Python automatically and invisibly uses its large number
# implementation at runtime when neccesary. 

LARGE_NUM = 618240007109027021
P_MINUS_1 = 250387201

def pollard_p_minus_one_algorithm(n, bound):
    b = 2
    j = 1

    while j < bound+1:
        j += 1
        # Python's fast moduluar exponentiation
        b = pow(b,j,n)
        
    d = gcd(b-1, n)

    if 1 < d and d < n:
        return d
    else:
        return 'failure'

def is_prime(num):
    for i in range(2, int(num ** .5) + 1):
        if num % i == 0:
            return False
    return True

def miller_rabin(n):
    m = n - 1
    k = 0
    while (m % 2 == 0):
        k += 1
        m = m / 2

    assert(n-1 == 2**k * m)

    a = random.randrange(1,n)
    b = square_and_multiply(a,m,n)

    if b % n == 1:
        return 'prime'
    
    for i in range(k):
        if b % n == n-1:
            return 'prime'
        else:
            b = b ** 2 % n

    return 'composite'

def square_and_multiply(base, exponent, modulus):
    layout = []
    # 
    while exponent != 0:
        layout += [exponent%2]
        exponent /= 2

    layout.reverse()
    total = 1
    for multiple in layout:
        if multiple:
            total = (total ** 2 * base) % modulus
        else:
            total = pow(total,2,modulus)
    return total

# print(pollard_p_minus_one_algorithm(LARGE_NUM,30))

factor_1 = 250387201
factor_2 = 2469135821

#print(pollard_p_minus_one_algorithm(LARGE_NUM,25))

print(miller_rabin(21))


worst_rate = 0

for i in range(201000,199999,-1):
    primes = 0

    # Test ~1000 times
    for j in range(1000):
        if miller_rabin(i) == 'prime':
            primes += 1
    
    # If it's actually prime, doesn't matter
    if primes == 1000:
        continue
    # Needs float divison for percentage
    error_rate = primes / 1000.

    print(i,error_rate)
    if error_rate > worst_rate:
        worst_rate = error_rate
        worst_num = i

print('FINISHED!')
print(worst_num,worst_rate)

for j in range(100000):
    if miller_rabin(200431) == 'prime':
        primes += 1

error_rate_200431 = primes / 100000.
print(error_rate_200431)
