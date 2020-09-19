from snr import *
import random


# An interesting new identity for aerated signature convolution
# Shown in SNR 3.4
def aeration_sum(d, g, a):
    out = Seq([0])
    for k in range(len(g)):
        out += (d**(k+1)).aerate(a) * x**k * g[k]
    return out


def test_aeration_summation():
    d = Seq([random.randint(1, 3) for k in range(random.randint(2, 5))])
    g = Seq([random.randint(1, 3) for k in range(random.randint(2, 5))])
    a = random.randint(1, 4)

    b_d = Block.power(d, taper=True)

    b_d_f = b_d.f(a=a, g=g)

    print(b_d_f.i())
    print(aeration_sum(d, g, a))

    print(aeration_sum(d, g, a) == b_d_f.i())


def matrix_convolution_associativity_test():
    # Select three sequences to be matrix-convolved
    d1 = Seq([2, 1])
    d2 = Seq([1, 1])
    d3 = Seq([1, 1])
    g = Seq([1])
    a = 2

    # Taper matrices for fullest mulitplication
    b_d1 = Block.power(d1, taper=True)
    b_d2 = Block.power(d2, taper=True)
    b_d3 = Block.power(d3, taper=True)

    # Test associativity
    b_d123 = (b_d1 * b_d2) * b_d3
    print(b_d123)
    b_d231 = b_d1 * (b_d2 * b_d3)
    print(b_d231)

    b_d123_f = b_d123.f(a=a, g=g)
    b_d231_f = b_d231.f(a=a, g=g)

    print(b_d123_f)
    print(b_d231_f)


def aerated_convolution_of_product():
    d = Seq([random.randint(1, 4) for k in range(random.randint(1, 5))])
    g = Seq([random.randint(1, 4) for k in range(random.randint(1, 5))])
    a = random.randint(1, 3)

    b_d = Block.power(d, taper=True)
    b_g = Block.power(g, taper=True)
    print(b_d)
    print(b_g)

    # The closed-est form I can find
    out = []
    for n in range(std_l):
        _sum = 0
        # This is really just performing a row of matrix multiplication
        for k in range(len(b_d[1])):
            _sum += b_d[1][k] * b_g[k][n]
        out.append(_sum)

    out = Seq(out).aerate(a)
    print(out)
    print((b_d * b_g).i(a=a))


def aeration_identity_1():
    d = Seq([1, 1])
    a = 2

    print(d.f().aerate(a))
    print((d.aerate(a) * x**(a-1)).f())


def matrix_construction_test():
    d = Seq([1, 1, 1])
    b = Block.blank(std_l)

    b[0][0] = 1
    for n in range(1, std_l):
        for y in range(n+1):
            _sum = 0
            for k in range(n-y):
                _sum += d[k]
            b[n][y] = _sum

    print(b)

    d_sum = (d * Seq([1]).f())[:std_l]

    # Needed to verify the first equation of 4.3
    for n in range(1, std_l):
        for y in range(n):
            fact = b[n][y] == d_sum[n-y-1]
            if not fact:
                print("doesn't work", b[n][y], d_sum[n-y-1])
                break


def matrix_construction_test_2():
    d = (Seq([1, 1]) * Seq([1]).f())[:std_l]
    b = Block.blank(std_l)
    b[0][0] = 1

    for n in range(1, std_l):
        for y in range(n):
            b[n][y] = d[n-y-1]

    print(b)

    b_p = b**std_l

    print(b_p)


def simple_identity_test():
    a = Seq([1, 1, 1])
    b = Seq([1])
    c = Seq([0, 1])

    print(Sig(a) + Sig(b-c))
    print(a + Seq(Sig(a)+Sig(b)) - Seq(Sig(a)+Sig(c)))


def left_distributive_identity_test():
    a = Sig([1, 1, 1])
    b = Sig([1, 1])
    c = Sig([1, 1])

    print(a * (b + c))
    print((a * b) + (a * c))


def memoization_test():
    a = Seq([1, 1])
    b = Seq([1, 1, 1])
    a_f = a.f()
    b_f = b.f()

    out = Seq([a_f[0]])

    for n in range(1, std_l):
        _sum = a_f[n]
        for k in range(1, n+1):
            _sum += out[n-k] * b[k-1]
        out.append(_sum)

    print(a_f * b_f)
    print(out)


memoization_test()