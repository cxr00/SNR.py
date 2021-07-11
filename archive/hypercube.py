from snr import *
import random


def random_seq():
    return Seq([random.randint(1, 5) for k in range(random.randint(2, 3))])


def generalized_inclusive_sig_identity(N, d):
    """
    An identity for computing the generalized inclusive signature function
    in a given dimension

    :param N: The dimension of the function
    :param d: The signature to be transformed
    :return: The identity S_N
    """
    assert N > 0
    out = Seq()

    binom = Seq([1, 1])**(N-1)

    for k in range(N):
        to_add = (-1)**k * (binom[k+1]*d + binom[k]) * (d*x)**k
        out += to_add

    return out


def alternate_generalized_inclusive_sig_identity(N, d):
    """
    The power triangular prism generalized inclusive signature function (GISF)

    :param N: The dimension of the power N-tangular prism
    :param d: The signature of the prism
    :return: The constructed GISF
    """
    assert N > 0
    out = Seq()

    binom = Seq([1, 1])**(N-1)

    for k in range(N):
        to_add = (-1)**k * (binom[k]*d + binom[k+1]) * x**k
        out += to_add

    return out


def hypercube_signature_function(hypercube, l=10, inclusive=False):
    """
    The signature function generalized to four dimensions.

    This process is trivially extended to higher dimensions
    using the pattern given below.
    :param hypercube: The hypercube which will have the signature function performed
    :param l: The length of the resultant signature function
    :param inclusive: Whether the signature function is inclusive or not
    """
    out = Seq()

    for n in range(l):
        _sum = 0
        for y in range(n + 1):
            for t in range(n + 1):
                for p in range(n + 1):
                    for j in range(n + 1):
                        if inclusive:
                            if y + t + p + j <= n:
                                _sum += hypercube[y][t][p][j]
                        else:
                            if y + t + p + j == n:
                                _sum += hypercube[y][t][p][j]
        out.append(_sum)

    return out


def one_beginning_hypercube(d: Seq, l=std_l//3):
    """
    A generalization of the power triangle to 4 dimensions.
    This is the canonical one-beginning object in 4 dimensions
    """
    hypercube = [Cube.blank(l) for n in range(l)]
    b_d = Block.power(d)

    for n in range(l):
        print(f"completed {n}")
        for y in range(l):
            hypercube[n][y] = d**(n+y) * b_d

    return hypercube


def cube_unit_test_1():
    cube = Cube.power_triangular_prism(Seq([1, 1]))
    print(cube.f())
    print(cube.i())
    print()

    cube = Cube.sen(Seq([1]))
    print(cube.f())
    print(cube.i())
    print()

    cube = Cube.power(Seq([1, 1]))
    print(cube.f())
    print(cube.i())
    print()

    cube = Cube.power_trapezoid(Seq([1, 1]))
    print(cube.f())
    print(cube.i())
    print()


def hypercube_unit_test_1():
    hypercube = one_beginning_hypercube(Seq([1, 1]), l=12)
    hc_f = hypercube_signature_function(hypercube, l=12, inclusive=False)
    print(hc_f)
    print(hc_f.i())
    print()


def hypercube_unit_test_2():
    l = 10

    d = Seq([1, 1, 1])
    alt = (3*d + 1) - (3*d**2 + 3*d)*x + (d**3 + 3*d**2)*x**2 - (d*x)**3
    alt_2 = generalized_inclusive_sig_identity(4, d)
    hypercube = one_beginning_hypercube(d, l=l)
    hc_f = hypercube_signature_function(hypercube, l=l, inclusive=True)
    print(hc_f)
    print(hc_f.i())
    print(alt)
    print(alt_2)


def tesseract_signature_function(tesseract, l=10, inclusive=False):
    """
    The signature function generalized to five dimensions.
    """
    out = Seq()

    for n in range(l):
        _sum = 0
        for y in range(n + 1):
            for t in range(n + 1):
                for p in range(n + 1):
                    for j in range(n + 1):
                        for k in range(n + 1):
                            if inclusive:
                                if y + t + p + j + k <= n:
                                    _sum += tesseract[y][t][p][j][k]
                            else:
                                if y + t + p + j + k == n:
                                    _sum += tesseract[y][t][p][j][k]
        out.append(_sum)

    return out


def one_beginning_tesseract(d: Seq, l=std_l // 3):
    """
    A generalization of the power triangle to 5 dimensions.
    This is the canonical one-beginning object in 5 dimensions
    """
    tesseract = [[Cube.blank(l) for n in range(l)] for k in range(l)]
    b_d = Block.power(d).truncate(l)

    for n in range(l):
        for y in range(l):
            print(f"completed {n}, {y}")
            for t in range(l):
                tesseract[n][y][t] = d ** (n + y + t) * b_d

    return tesseract


def six_dimensional_signature_function(sixdim, l=10, inclusive=False):
    """
    The signature function generalized to six dimensions.
    """
    out = Seq()

    for n in range(l):
        _sum = 0
        for y in range(n + 1):
            for t in range(n + 1):
                for p in range(n + 1):
                    for j in range(n + 1):
                        for k in range(n + 1):
                            for i in range(n + 1):
                                if inclusive:
                                    if y + t + p + j + k + i <= n:
                                        _sum += sixdim[y][t][p][j][k][i]
                                else:
                                    if y + t + p + j + k + i == n:
                                        _sum += sixdim[y][t][p][j][k][i]
        out.append(_sum)

    return out


def one_beginning_six_dimensional_figure():
    """
    This is REALLY slow. But the two generalized signature identities
    still (appear to) hold.
    """
    l = 10
    d = Seq([1, -1])

    sixdim = [[[Cube.blank(l) for k in range(l)] for y in range(l)] for n in range(l)]

    b_d = Block.power(d).truncate(l)

    for n in range(l):
        for y in range(l):
            for t in range(l):
                for k in range(l):
                    sixdim[n][y][t][k] = d ** (n + y + t + k) * b_d
            print(f"completed {n} {y}")

    f = six_dimensional_signature_function(sixdim, l, inclusive=False)
    print(f)
    print(f.i())
    print(Sig(d) + Sig(d) + Sig(d) + Sig(d) + Sig(d))
    print()

    f = six_dimensional_signature_function(sixdim, l, inclusive=True)
    print(f)
    print(f.i())
    print(generalized_inclusive_sig_identity(6, d))


def tesseract_unit_test():
    d = Seq([1, 1])
    t = one_beginning_tesseract(d, l=10)

    t_f = tesseract_signature_function(t, inclusive=False)
    print(t_f)
    print(t_f.i())
    print(Sig(d) + Sig(d) + Sig(d) + Sig(d))
    print()

    t_f = tesseract_signature_function(t, inclusive=True)
    print(t_f)
    print(t_f.i())

    alt = (4 * d + 1) - (6 * d + 4) * (d * x) + (4 * d + 6) * (d * x) ** 2 - (d + 4) * (d * x) ** 3 + (d * x) ** 4
    alt_2 = generalized_inclusive_sig_identity(5, d)
    print(alt)
    print(alt_2)


def hypercube_triangular_prism():
    l = 12
    # for b in range(10):
    d = Seq([1, 1])
    cube = Cube.power_triangular_prism(d, l)
    hypercube = [cube for k in range(l)]

    h_f = hypercube_signature_function(hypercube, l, inclusive=True)
    print(h_f)
    print(h_f.i())
    print(alternate_generalized_inclusive_sig_identity(4, d))
    print()

    h_f = hypercube_signature_function(hypercube, l, inclusive=False)
    print(h_f)
    print(h_f.i())
    print(Sig(d) + Sig(1) + Sig(1))
    print()

hypercube_triangular_prism()

def tesseract_triangular_prism():
    l=12
    for b in range(10):
        d = Seq(b)
        cube = Cube.power_triangular_prism(d, l)

        tesseract = [[cube for k in range(l)] for n in range(l)]

        t_f = tesseract_signature_function(tesseract, l, inclusive=True)
        print(t_f.i())
        print(alternate_generalized_inclusive_sig_identity(5, d))
        print()


def hypercube_power_trapezoid():
    """
    This is a form of power trapezoid hypercube. It has
    a particularly interesting closed form.
    """
    l = 20
    for b in range(10):
        d = random_seq()
        c_d = Cube.power_trapezoid(d)
        hypercube = [c_d for k in range(l)]
        h_f = hypercube_signature_function(hypercube, l, inclusive=True)

        print(b, "\t", h_f.i())
        alt = (d+3) - (3*d + 2)*x + (2*d - 2)*x**2 + (2*d + 3)*x**3 - (3*d + 1)*x**4 + d*x**5
        print("\t", alt)
        print()


def hypercube_alt_power_trapezoid():
    """
    This is another form of power trapezoid hypercube, but
    it does not appear to have a closed form identity.
    """
    def generate_trapezoid(d: Seq, g: Seq):
        b = Block.blank(std_l)
        b[0] = g
        for n in range(1, std_l):
            b[n] = b[n - 1] * d

        return b

    l = 20
    for b in range(10):
        hypercube = [Cube.blank(l) for k in range(l)]
        d = random_seq()

        for n in range(l):
            for y in range(l):
                g = Seq([1 for k in range(n + y + 1)])
                hypercube[n][y] = generate_trapezoid(d, g)

        hc_f = hypercube_signature_function(hypercube, l, inclusive=True)
        print(b, "\t", hc_f)
        print(b, "\t", hc_f.i())




def inclusive_sig_identity_block():
    """
    An interesting block constructed using the generalized inclusive
    signature function (GISF)
    """
    d = Seq([1, 1])
    b = Block([generalized_inclusive_sig_identity(N, d) for N in range(1, 30)])
    print(b)
    print(b.f())
    print(b.f().i())


def inclusive_sig_identity_block_2():
    """
    An interesting block using the alternate GISF
    """
    d = Seq([1])

    b = Block([alternate_generalized_inclusive_sig_identity(N, d) for N in range(1, 30)])
    print(b)
    print(b.f())
    print(b.i())


def sen_inclusive_signature_function():
    l = 20
    for b in range(10):
        d = Seq(b)
        s = Cube.sen(d, l)
        print(s.f(inclusive=True))
        print(s.i(inclusive=True))

        print(s.f(inclusive=False))
        print(s.i(inclusive=False))
        print()


def power_triangular_prism_inclusive():
    l = 20
    for b in range(10):
        d = Seq([random.randint(1, 5) for k in range(random.randint(2, 5))])
        c_d = Cube.power_triangular_prism(d, l)

        print(c_d.f(inclusive=True))
        print(c_d.i(inclusive=True))

        alt = (d + 2) - (2*d + 1)*x + d*x**2
        print(alt)
        print()


def power_trapezoid_inclusive():
    l = 20
    for b in range(10):
        d = Seq([random.randint(1, 5) for k in range(random.randint(2, 5))])
        c_d = Cube.power_trapezoid(d)

        print(d)
        print(c_d.i(inclusive=True))
        alt = (d+2) - (2*d + 2*x)*x + (2*d + 1)*x**3 - d*x**4
        print(alt)
        print()