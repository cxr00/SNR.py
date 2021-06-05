from snr import *

std_l = 50


def catalan_convolution(j):
    def generate_cantor_numbers(l):
        out = Seq(1)
        for n in range(l):
            out = out.f()
        return out

    out = []
    c = generate_cantor_numbers(std_l)

    for n in range(len(c)):
        out.append(j**(n+1) * c[n])

    return Seq(out)


def triangle_construction():
    """
    A construction from Zeddar which produces interesting signatures

    When m = 1 and j = 1, the aerated Catalan numbers are produced

    It also appears that when j is some integer > 1, the aerated generalized Catalan numbers C(j, n) are produced

    When using the aerated signature function, another identity emerges as will be discussed in future writings
    """
    j = 1
    a = 1

    # Start with a block full of zeroes
    p = Block.blank(l=std_l)

    # Initial value
    p[0][0] = 1

    # Fill values of the triangle
    for n in range(1, std_l):
        for k in range(std_l):
            if n == k:
                p[n][k] = 1
            elif n > k:
                p[n][k] = p[n-1][k-1] + (j * p[n-1][k+1])
            elif n < k:
                p[n][k] = 0

    print(p)

    p_f = p.f(a=a)
    p_i = p_f.i()
    print(p_f)  # Signature function of the block
    print(p_i)  # Inverse signature function of the block
    print()

    # s = p_f[::2]
    #
    # print(s)
    # print(s.i())

    print(x * catalan_convolution(j).aerate(2) + x ** a)


def catalan_triangle():
    """
    Performs the signature function on the Catalan triangle

    Regardless of the aeration coefficient, the Catalan numbers are
    present in the signature through a neat identity
    """
    a = 2
    b = Block.blank(std_l)

    b[0][0] = 1

    for n in range(1, std_l):
        for k in range(std_l):
            if k == 0:
                b[n][k] = 1
            elif k == 1:
                b[n][k] = n
            elif 1 < k < n + 1:
                b[n][k] = b[n][k-1] + b[n-1][k]

    print(b)
    print(b.f(a=a))
    print(b.i(a=a))

    print(1 + x ** a * catalan_convolution(1).aerate(a + 1))

