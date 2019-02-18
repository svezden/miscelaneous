## Routine to compute the prime factors of a number
## It has been modified to compute the prime factors of a list running up to 2^M, by steps of 4 units

M = 10
n = 4

def prime_factors(n):
    i = 2
    factors, b = [],{}
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    for item in factors:
        b[item] = b.get(item, 0) + 1
    return b

while n <= 2**M:
    if prime_factors(n).get(2)%2==0:
        print(n,prime_factors(n))
    n+=4
