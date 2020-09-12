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
