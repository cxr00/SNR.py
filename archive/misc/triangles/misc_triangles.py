from snr import *


def binomial(n, k):
    def factorial(n):
        if n == 0:
            return 1
        else:
            out = 1
            for i in range(2, n):
                out *= i
            return out

    return factorial(n) / (factorial(k) * factorial(n - k))
    # return (Seq([1, 1])**n)[k]


def losanitch_triangle():

    b = Block.blank()

    b[0][0] = 1

    for n in range(1, std_l):
        for k in range(n+1):
            if not n % 2 and k % 2:
                b[n][k] = b[n-1][k-1] + b[n-1][k] - binomial(n//2 - 1, (k-1)//2)
            else:
                b[n][k] = b[n-1][k-1] + b[n-1][k]

    print(b)

    b_f = b.f()
    b_fi = b_f.i()

    print(b_f)
    print(b_fi)


def euler_number_triangle():

    b = Block.blank()

    for n in range(std_l):
        for k in range(n+1):
            if k == 0 or k == n:
                b[n][k] = 1
            else:
                b[n][k] = (k+1) * b[n-1][k] + (n + 1 - k) * b[n-1][k-1]

    print(b)

    b_f = b.f()
    b_fi = b_f.i()

    print(b_f)
    print(b_fi)


def bernoulli_triangle():
    b = Block.blank()

    for n in range(std_l):
        _d = Seq([1, 1]) ** n
        b[n] = (_d * Seq([1]).f(l=std_l))[:n+1]

    print(b)

    b_f = b.f()
    b_fi = b_f.i()

    print(b_f)
    print(b_fi)

