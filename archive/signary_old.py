from snr import Seq

# get_10_x -> reduce_by_one -> generate_uncarry -> get_base_10_value
# This class relies on the 'uncarry' method, when counting was a lot
# more difficult. signary_old.py has the advanced system that can handle
# arbitrary bases which are IOBNS
class Signary:

    _DIV = ""

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

    # Begin with the number 10_d^x
    @staticmethod
    def get_10_x(d, x):
        out = [0 for k in range(x)]
        out.append(1)
        return Signary(d, Seq(out))

    @staticmethod
    def generate_uncarry(d, x):
        out = [0 for k in range(x+1)]
        out[x] = -1
        for k in range(0, x):
            out[k] = d[x-1-k]
        return Seq(out)

    @staticmethod
    def reduce_by_one(s):
        if s.n[0] > 0:
            s.n[0] -= 1
            return s
        for x in range(1, len(s.n)):
            if s.n[x] > 0:
                s.n += Signary.generate_uncarry(d, x)
                return Signary.reduce_by_one(s).trim()
            else:
                continue
        return s

    @staticmethod
    def get_base_10_value(s):
        d_f = s.d.f(l=len(s.n) + 1)
        out = 0
        for k in range(len(s.n)):
            out += s.n[k] * d_f[k]
        return out


d = Seq([1, 1, 2])
s = Signary.get_10_x(d, 5)

d_f = d.f(l=len(s.n))

for x in range(d_f[len(d_f)-1]):
    s = Signary.reduce_by_one(s)
    print(s, Signary.get_base_10_value(s))
