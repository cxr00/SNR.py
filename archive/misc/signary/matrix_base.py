from snr import *


# The original, uses a power triangle as the base
# This function computes the "powers" of numbers in this base
# For example, d=[1,1] produces the Bell numbers
def counting_test_1(d, l=10):
    base = Block.power(d, l=l)

    out = [1]

    for n in range(l):
        g = 0
        for e in range(n+1):
            g += out[e] * base[n][e]
        out.append(g)

    return Seq(out)


def counting_test_2(d, l=10):
    base = Block.blank(l)
    d_f = d.f(l=l)

    for n in range(l):
        for k in range(n+1):
            base[n][k] = d_f[n-k]

    print(base)

    out = [1]

    for n in range(l):
        g = 0
        for e in range(n+1):
            g += out[e] * base[n][e]
        out.append(g)

    return Seq(out)


d = Seq([1])

s = counting_test_2(d)

print(s)
print(s.i())
