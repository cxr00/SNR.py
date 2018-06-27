from snr import Seq


def sig_match_conv(a: Seq, b: Seq, index: int):
    out = True
    l = len(b)
    for x in range(l):
        print(a[index+l-x], " ", b[x])
        out = a[index+l-x] >= b[x]
    return out


class Sen(Seq):

    def __init__(self, val=None, sig=None):
        super(Sen, self).__init__(val)
        if sig is None:
            self.sig = Seq([1])
        else:
            self.sig = Seq(sig)

    def resolve(self, sig=None):
        out = Seq(self.val)
        sig = sig if sig else self.sig
        l = len(self.val)
        for x in range(l):
            print(f"#{x}")
            print(sig_match_conv(out, sig, x))
            print()


d = Seq([0, 0, 1, 1, 1, 0, 1])

t = Sen(val=d)

t.resolve()
