from snr import *
import random


def hankel_sig_conv():
    """
    Perform signature convolution on a Hankel matrix.

    H_d * g produces A143212 when d = g = {1, 1}
    """

    def hankel_matrix(s=Seq([1, 1]), l=std_l):
        """
        Construct a Hankel matrix from a given sequence
        """
        s_f = s.f(std_l*2)
        b = Block.blank(l)
        for n in range(l):
            for k in range(l):
                b[n][k] = s_f[n+k]

        return b

    d = Seq([1, 1])
    g = Seq([1, 1])
    h = hankel_matrix(s=d)
    h_f = h.f(g=g)
    print(h)

    print(h_f)
    print(h_f.i())


def d_g_sig_subtraction_test_1():
    """
    Tests an alternate identity for signature subtraction of
    the two-digit signature g = {1, -1}
    """
    g = Sig([1, -1])
    for i in range(10):
        d = Sig([random.randint(1, 3) for k in range(random.randint(2, 6))])
        print(d, "::", d-g)
        print((d-g).f())
        f_g = Seq([1, d[0] - 1, d[1] + d[0]*d[0] - (d[0] - 1)])
        for n in range(3, std_l):
            _sum = 0
            for k in range(1, n+1):
                _sum += f_g[n-k] * d[k-1]
            f_g.append(_sum)
        print(f_g)
        print(f_g == g.f())
        print()


def d_g_sig_subtraction_test_2():
    """
    Tests an alternate identity for signature subtraction
    of an arbitrary two-digit signature
    """
    p = Sig([random.randint(1, 6) for k in range(2)])
    print("p ::", p)
    print()

    for i in range(10):
        d = Sig([random.randint(1, 6) for k in range(random.randint(2, 6))])
        g = d-p
        print(d, "::", g)
        print(g.f())

        f_g = Seq([
            1,
            d[0] - p[0],
            d[1] - p[1] + d[0]*(d[0] - p[0])
        ])

        for n in range(len(p) + 1, std_l):
            _sum = 0
            for k in range(1, n+1):
                _sum += f_g[n-k] * d[k-1]
            f_g.append(_sum)
        print(f_g)
        print(f_g == g.f())
        print()


def d_g_sig_subtraction_test_3():
    """
    Tests an alternate identity for signature subtraction
    of an arbitrary signature of any length
    """
    for i in range(10):
        p = Sig([random.randint(1, 10) for k in range(random.randint(2, 15))])
        print("p ::", p)

        d = Sig([random.randint(1, 10) for k in range(random.randint(2, 15))])
        g = d - p
        g_f = g.f()
        print(d, "::", g)
        print(g_f)

        f_g = Seq([1])
        for n in range(1, std_l):
            _sum = d[n-1] - p[n-1]
            for k in range(1, n):
                _sum += d[k-1] * f_g[n-k]
            f_g.append(_sum)

        print(f_g)
        print(g.f() == f_g)
        print()


def sequence_builder(t=1):
    """
    A curious sequence with an interesting identity at t=1
    """

    f_d = Seq()
    for n in range(10):
        f_d += (n+1) * (x + 1)**(t+1) * x**((t+2)*n) * (-1)**n

    return f_d


def sequence_builder_2(t=1):
    """
    An altered version of sequence_builder which does not
    multiply by (-1)**n
    """

    f_d = Seq()
    for n in range(10):
        f_d += (n+1) * (x + 1)**(t+1) * x**((t+2)*n)

    return f_d


def memoization_of_signature_addition_test():
    """
    Tests the memoized formulas for computing signature addition
    of two arbitrary sequences.

    The memoization is only more efficient if you have already
    computed either F_a or F_b; otherwise it is faster to compute
    signature addition a + b followed by F_{a + b}
    """
    a = Sig([random.randint(1, 6) for k in range(random.randint(2, 5))])
    b = Sig([random.randint(1, 6) for k in range(random.randint(2, 5))])

    print((a + b).f())

    f_a = a.f()
    f_ab_alt = Seq(1)
    for n in range(1, std_l):
        _sum = f_a[n]
        for k in range(1, n+1):
            _sum += f_ab_alt[n-k]*b[k-1]
        f_ab_alt.append(_sum)

    print(f_ab_alt)

    f_b = b.f()
    f_ab_alt = Seq(1)
    for n in range(1, std_l):
        _sum = f_b[n]
        for k in range(1, n+1):
            _sum += f_ab_alt[n-k]*a[k-1]
        f_ab_alt.append(_sum)

    print(f_ab_alt)

