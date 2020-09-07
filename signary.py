from snr import Seq
import random


def is_increasing(f_d):
    for k in range(len(f_d)):
        if f_d[k] < f_d[k-1]:
            return False
    return True


class Signary:

    _DIV = "."

    def __init__(self, d, n):
        self.d = d
        self.n = n

    def __str__(self):
        out = self.n.val[::-1]
        return Signary._DIV.join([str(k) for k in out])

    def trim(self):
        out = self.n
        for x in range(len(out) - 1, -1 , -1):
            if out[x] == 0:
                out.val.pop(x)
            else:
                self.n = out
                return self
        self.n = out
        return self

    def get_base_10(self):
        f_d = self.d.f(l=len(self.n))
        out = 0
        for k in range(len(self.n)):
            out += f_d[k] * self.n[k]
        return out

    @staticmethod
    def create_numeration(d, N):
        """
        This algorithm fails when f_d is not monotonic increasing

        :param d: the signature of the numeration
        :param N: the base-10 value to give the numeration
        :return: The number N in signary form
        """
        f_d = d.f(l=25) # Using large length to avoid better code
        if not is_increasing(f_d):
            raise ValueError("Sequence " + str(f_d) + " is not increasing")
        p = 0
        for k in range(25):
            if N > f_d[k]:
                p += 1
            else:
                break
        out = [0 for k in range(p)]
        for k in range(p, -1, -1):
            while N >= f_d[k]:
                N -= f_d[k]
                out[k] += 1
        return Signary(d, Seq(out))


d = Seq([9, 6])
N = random.randint(0, random.randint(0, 100000))
S = Signary.create_numeration(d, N)

print(d.f(len(S.n)))
print(N)
print(S)
print(S.get_base_10())
