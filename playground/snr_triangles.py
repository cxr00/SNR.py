"""
This code is for demonstrating the identities given in 4.5
Honestly I'm impressed that I managed to find these

The code for each function is basically as follows:
1 Construct a particular triangle starting from Block.blank
2 (If applicable) Get aerated diagonal sum based on aeration coefficient a
3 Compare to manually constructed sequence s

The triangles given are of interest because of their elegant expression
in terms of their signatures.
"""
from snr import *


def K_d(d, a):
    b = Block.blank(std_l)
    f_d = d.f(std_l)
    for n in range(std_l):
        for y in range(n+1):
            b[n][y] = f_d[y]
    print(b.f(a))

    s = Sig(1) + Sig((x**a) * d.aerate(a+1))
    print(s.f())
    return b


def Q_d(d, a):
    b = Block.blank(std_l)
    f_d = d.f(std_l)
    for n in range(std_l):
        for y in range(n+1):
            b[n][y] = f_d[n-y]
    print(b.f(a))

    s = Sig(d) + Sig(x**a)
    print(s.f())
    return b


def G_d(d, a):
    b = Block.blank(std_l)
    f_d = d.f(std_l)
    for n in range(std_l):
        for y in range(n+1):
            b[n][y] = (f_d**(y+1))[n-y]
    print(b.f(a))

    s = d + x**a
    print(s.f())
    return b


def B_d(d, a):
    b = Block.blank(std_l)
    f_d = d.f(std_l)
    for n in range(std_l):
        for y in range(n+1):
            b[n][y] = (f_d**(n-y+1))[y]
    print(b.f(a))

    s = Seq([1]) + (x**a)*d.aerate(a+1)
    print(s.f())
    return b


def P_d(d, a):
    b = Block.blank(std_l)
    for n in range(std_l):
        for y in range(n+1):
            b[n][y] = (d**y)[n-y]
    print(b.f(a))

    s = d * x**a
    print(s.f())
    return b


def P_prime_d(d, a=1):
    b = Block.blank(std_l)
    for n in range(std_l):
        for y in range(n+1):
            b[n][y] = (d**(y+1))[n-y]
    print(b.f(a))

    s = d*(x**a)
    print(d*s.f())
    return b


def J_d(d, a):
    b = Block.blank(std_l)
    for n in range(std_l):
        for y in range(n+1):
            b[n][y] = (d**(n-y))[y]
    print(b.f(a))

    s = d.aerate(a+1)
    print(s.f())
    return b


# When d = Seq([1, 1]) then J_prime_d(n) = A000930(n+1)
def J_prime_d(d, a):
    b = Block.blank(std_l)
    for n in range(std_l):
        for y in range(n+1):
            b[n][y] = (d**(n-y+1))[y]
    print(b.f(a))

    s = d.aerate(a+1)
    print(s * s.f())
    return b


d = Seq([1, 2, 4])
J_prime_d(d, 1)
