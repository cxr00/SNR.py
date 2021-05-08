from snr import *


# Computes the first l digits of the unique signature convolution inverse of a given signature from the right and left
# The existence of unique multiplicative inverse for all a not equal to 0 is a condition of the near-field axioms


def first_nonzero(g):
    # Get the position of the first non-zero digit of g
    for e in range(1, len(g)):
        if g[e] != 0:
            return e
    return -1


def get_inverse_on_right(d, l=std_l):

    inverse = Seq(1 / d[0])
    x_pow_prev = 0
    d_pow = d

    while len(inverse) < l:
        product = (d * Sig(inverse))[:l]
        print("product:", product)
        x_pow = first_nonzero(product)
        if x_pow > x_pow_prev:
            for n in range(x_pow - x_pow_prev):
                d_pow *= d
            x_pow_prev = x_pow

        inverse -= ((x**x_pow) * product[x_pow]) / d_pow[0] # Uses d**x_pow, which is very slow
        print("inverse:", inverse)
        print()


def get_inverse_on_left(d, l=std_l):
    # This is the fast one, see below comment
    inverse = Seq(1 / d[0])
    x_pow_prev = 0
    d_pow = d

    while len(inverse) < l:
        product = (Sig(inverse) * d)[:l]
        print("product:", product)
        x_pow = first_nonzero(product)

        inverse -= ((x**x_pow) * product[x_pow]) / d[0] # Divide with d, not with d**x_pow
        print("inverse:", inverse)


get_inverse_on_left(Sig([2, 1]), l=30)
