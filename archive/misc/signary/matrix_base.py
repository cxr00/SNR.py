from snr import *


def counting_test_1(d, l=10):
    """
    The original matrix base interpretation using a power triangle.
    This function computes the n-th powers of numbers in this base
    For example, d={1,1} produces the Bell numbers.
    """
    base = Block.power(d, l=l)

    out = [1]

    for n in range(1, l):
        g = 0
        for k in range(n):
            g += out[k] * base[n-1][k]
        out.append(g)

    return Seq(out)


def counting_test_2(d, l=10):
    """
    Matrix base interpretation when M(n, k) = F_d(n-k). This is
    identical to using F_d as a base.
    """
    base = Block.blank(l)
    d_f = d.f(l=l)

    for n in range(l):
        for k in range(n+1):
            base[n][k] = d_f[n-k]

    print(base)

    out = [1]

    for n in range(1, l):
        g = 0
        for k in range(n):
            g += out[k] * base[n-1][k]
        out.append(g)

    return Seq(out)

