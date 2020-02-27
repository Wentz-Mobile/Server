import math
import random
import os

KEYSTRENGTH = 16
e = 65537

class Encryptor(object):
    def __init__(self, N):
        self.N = N

    def encrypt(self, message):
        return encrypt(message, e, self.N)


class Decryptor(object):
    def __init__(self):
        self.d, self.N, self.p, self.q = get_keys()

    def decrypt(self, messsage):
        return decrypt(messsage, self.d, self.N, self.p, self.q)

    def getN(self):
        return self.N

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
	    gcd, x, y = egcd(b % a, a)
	    return (gcd, y - (b//a) * x, x)


def is_prime(num, iterations):
    if num == 2:
        return True

    if num % 2 == 0 or num < 7:
        return False

    counter, exp = 0, num - 1
    while exp % 2 == 0:
        counter += 1
        exp //= 2
    for _ in range(iterations):
        base = random.randrange(2, num - 1)
        check = pow(base, exp, num)
        if check == 1 or check == num - 1:
            continue
        for _ in range(counter - 1):
            check = pow(check, 2, num)
            if check == num - 1:
                break
        else:
            return False
    return True


def get_prime(size):
    prime = int.from_bytes(os.urandom(size), byteorder="big")
    while not is_prime(prime, 300):
        prime = int.from_bytes(os.urandom(size), byteorder="big")
    return prime

def get_keys():
    d = -1
    while d <= 1:
        p = 1
        q = 1
        while math.log2(p) - math.log2(q) <= 0.1 or math.log2(p) - math.log2(q) >= 30:
            p = get_prime(KEYSTRENGTH)
            q = get_prime(KEYSTRENGTH)
        
        N = p * q
        phiN = (p - 1)*(q - 1)
        gcd, d, k = egcd(e, phiN)
        #print('phiN: ' + str(phiN))
        if N * 0.25 > d:
            d = 0
    return d, N, p, q

def encrypt(m, e, N):
    #print('---------------------------------------------------------------------------------------')
    #print('m: ' + str(m))
    m = int.from_bytes(m.encode(), byteorder="big")
    #print('m int: ' + str(m))
    mE = pow(m, e, N)
    #print('m (encrypted): ' + str(mE))
    return mE

def decrypt(m, d, N, p, q):
    dmp = d % (p -1)
    dmq = d % (q -1)
    iqmp = pow(q, -1, p)
    #print('---------------------------------------------------------------------------------------')
    m1 = pow(m, dmp, p)
    m2 = pow(m, dmq, q)
    s = (iqmp * (m1 - m2)) % p * q + m2
    #print('m (decrypted): ' + str(s))
    s = s.to_bytes(16, byteorder="big")
    s = s.decode('utf-8').lstrip('\0')
    #print('m: ' + s)
    return s

