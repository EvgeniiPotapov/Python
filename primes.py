from random import randint
from math import sqrt


def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x


def jacobi(a, n):
    if a < 0:
        return int(jacobi(-a,n)) * int((-1)**((n-1)/2))
    if a % 2 == 0:
        return int(jacobi(a/2,n)) * int((-1)**((n*n-1)/8))
    if a == 1:
        return 1
    if a < n:
        return int(jacobi(n, a)) * int((-1)**(((a-1)*(n-1))/4))
    return jacobi(a % n, n)


def is_prime(n):
    if n % 2 == 0:
        return False
    k = 11
    for i in range(k):
        a = randint(1, n-1)
        if gcd(a,n) > 1:
            return False
        if (a**((n-1)//2)) % n != jacobi(a,n)%n:
            return False
    return True


def run_prime_siblings():
    file = open("primes5000.txt", "w")
    sign = True
    p = 5
    count = 0

    while sign:
        p2 = 2*p + 1
        if (not is_prime(p)) or (not is_prime(p2)):
            p += 2
            continue
        a = round(p - 2*sqrt(p))
        b = round(p + 2*sqrt(p))
        a2 = round(p2 - 2*sqrt(p))
        b2 = round(p2 + 2*sqrt(p))
        for q in range(a+2, b):
            if not is_prime(q):
                continue
            q2 = 2*q + 1
            if not is_prime(q2):
                continue
            if q2 < b2 and q2 > a2 and p != q:
                stri = "p = " + str(p) + " p2 = "+str(p2)+" q = "+str(q)+" q2 = "+str(q2) + "\n"
                file.write(stri)
                count += 1
                print(count)
                if count == 5000:
                    sign = False
        p += 2
    file.close()


def print_primes(quant):
    file = open("real_primes.txt", "w")
    done = 0
    p = 3
    while done < quant:
        if is_prime(p):
            st = str(p) + "\n"
            file.write(st)
            done += 1
            if done % 5000 == 0:
                print(done)
        p += 2

    file.close()


print(jacobi(3, 5))
