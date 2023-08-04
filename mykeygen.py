__student_name__ = 'Klarissa Jutivannadevi'
__student_id__ = '32266014'

import sys
import random
import math


# k is calculated using log base 4 since the probability of d is not prime is 4^-k
def get_k(d):
    return int(math.log(d, 4)) + 1


# code based on lecture note week 6
def modular_exponentiation(base, power, mod):
    current = base % mod
    binary_rep = bin(power)[2:]
    if binary_rep[-1] == '1':
        result = current
        binary_rep = binary_rep[:-1]
    else:
        result = 1
    for i in binary_rep[::-1]:
        current = (current * current) % mod
        if i == "1":
            result = (result * current) % mod
    return result


def miller_rabin_primality(n, k):
    count = 0
    if n % 2 == 0:
        return False
    if n == 3 or n == 2:  # edge case since randint accept at least 4
        return n
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2
        while count < k:
            count += 1
            a = random.randint(2, n - 2)
            if modular_exponentiation(a, n-1, n) != 1:
                return False
            for j in range(s):
                mod_exp = modular_exponentiation(a, pow(2, j) * t, n)
                if (modular_exponentiation(a, pow(2, j+1) * t, n) == 1) and not (mod_exp == 1 or mod_exp == n - 1):
                    return False
    return n


def get_secret_prime(d):
    p, q = 0, 0
    x = d
    k = get_k(d)
    # loop on q as q is filled after p
    while q == 0:
        check = miller_rabin_primality(pow(2, x) - 1, k)
        if check:
            if p == 0:
                p = check
            else:
                q = check
        x += 1
    return p, q


def gcd(val1, val2):
    if val1 - val2 >= 0:
        a = val1
        b = val2
    else:
        a = val2
        b = val1
    while b != 0:
        leftover = a % b
        a = b
        b = leftover
    return a


def get_exponent(p, q):
    lambdas = ((p-1) * (q-1)) // gcd(p-1, q-1)
    while True:
        e = random.randint(3, lambdas - 1)
        if gcd(e, lambdas) == 1:
            return e


if __name__ == '__main__':
    d = int(sys.argv[1])
    p, q = get_secret_prime(d)

    sp_content = ['# p\n', str(p) + '\n', '# q\n', str(q) + '\n']
    f = open("secretprimes.txt", "w")
    f.writelines(sp_content)
    f.close()

    modulus = p * q
    exponent = get_exponent(p, q)
    pk_content = ['# modulus (n)\n', str(modulus) + '\n', '# exponent (e)\n', str(exponent) + '\n']
    g = open("publickeyinfo.txt", "w")
    g.writelines(pk_content)
    g.close()

